from dataclasses import dataclass
from typing import Any, Protocol

from lectura.extractor.cliente import FallaCliente
from lectura.normalizador.normalizador import normalizar_clave, normalizar_monto

from .base import Documento, Resultado, escalar, validar_contra
from .canonica import desde_extraccion
from .congelada import CARPETA_MULTICANAL, canonica_congelada
from .pdf import leer_pdf

_TIPOS_MEDIA = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".pdf": "application/pdf"}


class ClienteArchivo(Protocol):
    def leer_archivo(self, modelo_id: str, instruccion: str, contenido: bytes, tipo_media: str): ...


def _criticos(ext):
    """Campos que deben coincidir entre las dos lecturas; un monto ambiguo cuenta como distinto."""
    try:
        monto = normalizar_monto(ext["monto_total"], ext["moneda"])
    except ValueError:
        monto = None
    return {"monto": monto, "moneda": ext["moneda"], "numero": normalizar_clave(ext["numero_factura"]),
            "cuenta": (ext["cuenta"]["pais"], ext["cuenta"]["ultimos4"])}


@dataclass
class LectorDoble:
    """Dos lecturas independientes del archivo (Haiku y Sonnet) con tope de gasto."""

    cliente: ClienteArchivo
    contador: Any
    modelos: dict
    instruccion: str
    contexto: dict

    def _leer(self, clave, documento, tipo_media):
        modelo = self.modelos[clave]["id"]
        try:
            resp = self.cliente.leer_archivo(modelo, self.instruccion, documento.contenido, tipo_media)
        except FallaCliente as f:
            self.contador.registrar(clave, f.tokens_entrada, f.tokens_salida)
            raise
        return resp, self.contador.registrar(clave, resp.tokens_entrada, resp.tokens_salida)

    def leer(self, documento: Documento, tipo_media) -> Resultado:
        lecturas = []
        for clave in ("haiku", "sonnet"):
            if self.contador.agotado:
                return escalar("tope_de_gasto")
            try:
                lecturas.append(self._leer(clave, documento, tipo_media))
            except FallaCliente as f:
                return escalar(f.motivo)
        (a, costo_a), (b, costo_b) = lecturas
        for resp in (a, b):
            errores = validar_contra("extraccion.schema.json", resp.contenido)
            if errores:
                return escalar("json_invalido", errores)
        ca, cb = _criticos(a.contenido), _criticos(b.contenido)
        difieren = [campo for campo in ca if ca[campo] != cb[campo]]
        if difieren or ca["monto"] is None:
            return escalar("lectura_doble_difiere", difieren or ["monto"])
        lectura = {"metodo": "modelo", "modelo": f"{self.modelos['haiku']['id']}+{self.modelos['sonnet']['id']}",
                   "reintentos": 0, "tokens_entrada": a.tokens_entrada + b.tokens_entrada,
                   "tokens_salida": a.tokens_salida + b.tokens_salida, "desde_cache": False,
                   "motivo_falla": None, "costo_microusd": str(costo_a + costo_b)}
        return Resultado(desde_extraccion(a.contenido, documento, self.contexto, lectura))


class AdaptadorImagen:
    """Foto y PDF escaneado. Sin lector, sirve la lectura congelada; la salida siempre es de origen imagen."""

    nombre = "imagen"

    def __init__(self, lector=None, carpeta=CARPETA_MULTICANAL):
        self._lector, self._carpeta = lector, carpeta

    def soporta(self, documento: Documento) -> bool:
        if documento.formato == "imagen":
            return True
        return documento.formato == "pdf" and leer_pdf(documento.contenido)[0] == "sin_texto"

    def a_canonica(self, documento: Documento) -> Resultado:
        if self._lector is None:
            return canonica_congelada(documento, self._carpeta)
        sufijo = ".pdf" if documento.formato == "pdf" else "." + documento.nombre.rsplit(".", 1)[-1].lower()
        tipo = _TIPOS_MEDIA.get(sufijo)
        return self._lector.leer(documento, tipo) if tipo else escalar("tipo_no_soportado", [sufijo])
