import hashlib
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

_CONTRATO = Path(__file__).resolve().parents[2] / "contrato"
_EXTRACCIONES = Path(__file__).resolve().parents[1] / "extracciones"
_REINTENTABLES = {408, 409, 429, 500, 502, 503, 504, 529}


@dataclass(frozen=True)
class Respuesta:
    contenido: dict
    tokens_entrada: int
    tokens_salida: int


class FallaCliente(Exception):
    """Falla del cliente con motivo; los tokens ya gastados se cuentan igual."""

    def __init__(self, motivo, tokens_entrada=0, tokens_salida=0):
        super().__init__(motivo)
        self.motivo = motivo
        self.tokens_entrada = tokens_entrada
        self.tokens_salida = tokens_salida


class ClienteModelo(Protocol):
    def leer(self, modelo_id: str, instruccion: str, texto: str) -> Respuesta: ...


def esquema_de_salida():
    esquema = json.loads((_CONTRATO / "extraccion.schema.json").read_text(encoding="utf-8"))
    return {k: v for k, v in esquema.items() if k not in ("$schema", "$id", "title", "description")}


class ClienteAnthropic:
    """Messages API por HTTP con salida estructurada; la clave solo sale del entorno."""

    def __init__(self, url, max_tokens, timeout_s, max_retries, entorno=os.environ):
        self._url, self._max_tokens = url, max_tokens
        self._timeout, self._max_retries, self._entorno = timeout_s, max_retries, entorno

    def _peticion(self, modelo_id, instruccion, texto):
        clave = self._entorno.get("ANTHROPIC_API_KEY")
        if not clave:
            raise FallaCliente("sin_clave")
        cuerpo = {
            "model": modelo_id, "max_tokens": self._max_tokens, "system": instruccion,
            "messages": [{"role": "user", "content": f"<documento>\n{texto}\n</documento>"}],
            "output_config": {"format": {"type": "json_schema", "schema": esquema_de_salida()}},
        }
        cabeceras = {"content-type": "application/json", "x-api-key": clave, "anthropic-version": "2023-06-01"}
        return urllib.request.Request(self._url, json.dumps(cuerpo).encode(), cabeceras, method="POST")

    def _enviar(self, peticion):
        for intento in range(self._max_retries + 1):
            try:
                with urllib.request.urlopen(peticion, timeout=self._timeout) as r:
                    return json.loads(r.read())
            except urllib.error.HTTPError as e:
                if e.code not in _REINTENTABLES or intento == self._max_retries:
                    raise FallaCliente("http_4xx" if e.code < 500 else "http_5xx")
            except (urllib.error.URLError, TimeoutError):
                if intento == self._max_retries:
                    raise FallaCliente("timeout")

    def leer(self, modelo_id, instruccion, texto):
        datos = self._enviar(self._peticion(modelo_id, instruccion, texto))
        uso = datos.get("usage", {})
        ti, to = int(uso.get("input_tokens", 0)), int(uso.get("output_tokens", 0))
        parada = datos.get("stop_reason")
        if parada in ("refusal", "max_tokens"):
            raise FallaCliente("refusal" if parada == "refusal" else "truncado", ti, to)
        try:
            bloques = [b["text"] for b in datos["content"] if b.get("type") == "text"]
            return Respuesta(json.loads(bloques[0]), ti, to)
        except (KeyError, IndexError, ValueError, TypeError):
            raise FallaCliente("json_invalido", ti, to)


def _imprimir(menor, exponente):
    n = int(menor)
    if exponente == 0:
        return str(n)
    return f"{n // 10 ** exponente}.{n % 10 ** exponente:0{exponente}d}"


class ClienteCongelado:
    """Sirve la lectura guardada cuyo hash coincide con el texto; sin red ni gasto."""

    def __init__(self, carpeta=_EXTRACCIONES):
        self._carpeta = Path(carpeta)

    def leer(self, modelo_id, instruccion, texto):
        hash_ = hashlib.sha256(texto.encode("utf-8")).hexdigest()
        for ruta in sorted(self._carpeta.glob("*.json")):
            f = json.loads(ruta.read_text(encoding="utf-8"))
            if f["documento"]["hash"] == hash_:
                return Respuesta(_a_extraccion(f), 0, 0)
        raise FallaCliente("sin_lectura_congelada")


def _a_extraccion(f):
    m = f["montos"]
    exp = json.loads((_CONTRATO / "monedas.json").read_text(encoding="utf-8"))["monedas"][m["moneda"]]["exponente"]
    impreso = lambda v: _imprimir(v, exp)
    sen = f.get("senales", {}).get("texto_dirigido_al_agente", {})
    return {
        "tipo_documento": f["documento"]["tipo_documento"],
        "proveedor": {"nombre": f["emisor"]["nombre"], "id_fiscal": f["emisor"].get("id_fiscal") or "",
                      "pais": f["emisor"].get("pais") or ""},
        "numero_factura": f["referencias"]["numero"],
        "fechas": {"emision": f["fechas"]["emision"], "vencimiento": f["fechas"].get("vencimiento") or ""},
        "moneda": m["moneda"], "monto_total": impreso(m["total_menor"]),
        "cuenta": {"pais": f["cuenta"]["pais"], "ultimos4": f["cuenta"]["ultimos4"]},
        "lineas": [{"descripcion": x["descripcion"], "total": impreso(x["total_menor"])} for x in m["lineas"]],
        "suma_lineas": impreso(m["suma_lineas_menor"]) if m["suma_lineas_menor"] else "",
        "referencia_acuerdo": f["referencias"].get("acuerdo_ref") or "",
        "evidencia": f["evidencia"], "confianza": f["confianza"],
        "texto_dirigido_al_agente": {"presente": sen.get("p", 0) >= 0.5, "cita": sen.get("origen", "")},
    }
