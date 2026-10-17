import hashlib
from pathlib import Path

from lectura.adaptadores.base import Resultado, escalar, validar_contra

from .cliente import FallaCliente
from .verificaciones import citas_en_texto, moneda_valida, totales_cuadran

_PROMPT = Path(__file__).resolve().parents[1] / "prompts" / "extractor.v1.md"
# Una cita ausente o una moneda invalida no se reintentan aqui: escalan con su motivo.
_ESCALAN = {"cita_evidencia": "cita_no_encontrada", "moneda": "moneda_invalida"}


class Extractor:
    def __init__(self, cliente, contador, modelos, ruta_prompt=_PROMPT):
        self._cliente, self._contador, self._modelos = cliente, contador, modelos
        self._instruccion = Path(ruta_prompt).read_text(encoding="utf-8")
        self._prompt_hash = hashlib.sha256(self._instruccion.encode("utf-8")).hexdigest()
        self._prompt_version = Path(ruta_prompt).stem.rsplit(".", 1)[-1]

    def _llamar(self, clave, texto):
        modelo_id = self._modelos[clave]["id"]
        try:
            resp = self._cliente.leer(modelo_id, self._instruccion, texto)
        except FallaCliente as f:
            self._contador.registrar(clave, f.tokens_entrada, f.tokens_salida)
            raise
        costo = self._contador.registrar(clave, resp.tokens_entrada, resp.tokens_salida)
        return resp, costo

    def extraer(self, texto, clave_modelo="haiku"):
        """Lectura del texto: factura = {extraccion, verificaciones, meta} o escala con motivo."""
        if self._contador.agotado:
            return escalar("tope_de_gasto")
        try:
            resp, costo = self._llamar(clave_modelo, texto)
        except FallaCliente as f:
            return escalar(f.motivo)
        if self._contador.gastado > self._contador.tope:
            return escalar("tope_de_gasto")
        errores = validar_contra("extraccion.schema.json", resp.contenido)
        if errores:
            return escalar("json_invalido", errores)
        ver = {"cita_evidencia": citas_en_texto(resp.contenido, texto),
               "moneda": moneda_valida(resp.contenido), "suma_lineas": totales_cuadran(resp.contenido)}
        for campo, motivo in _ESCALAN.items():
            if ver[campo] == "falla":
                return escalar(motivo, [campo])
        meta = {"prompt_version": self._prompt_version, "prompt_hash": self._prompt_hash,
                "modelo": self._modelos[clave_modelo]["id"], "tokens_entrada": resp.tokens_entrada,
                "tokens_salida": resp.tokens_salida, "costo_microusd": str(costo)}
        return Resultado({"extraccion": resp.contenido, "verificaciones": ver, "meta": meta})
