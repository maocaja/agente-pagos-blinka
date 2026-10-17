import json
from pathlib import Path

from lectura.seguridad.instrucciones import con_senal_local

from .base import Documento, Resultado, escalar

CARPETA_MULTICANAL = Path(__file__).resolve().parents[1] / "extracciones_multicanal"


class Ilegible(Exception):
    """El documento no se puede leer en local; el motivo escala sin llamar a la API."""

    def __init__(self, motivo):
        super().__init__(motivo)
        self.motivo = motivo


def canonica_congelada(documento: Documento, carpeta) -> Resultado:
    for ruta in sorted(Path(carpeta).glob("*.json")):
        factura = json.loads(ruta.read_text(encoding="utf-8"))
        if factura.get("documento", {}).get("hash") == documento.hash:
            return Resultado(factura)
    return escalar("sin_lectura_congelada", [documento.hash])


class AdaptadorDeTexto:
    """Base de los formatos con texto local: si se lee, entrega la lectura congelada por hash."""

    nombre = ""
    formato = ""

    def __init__(self, carpeta=CARPETA_MULTICANAL):
        self._carpeta = carpeta

    def soporta(self, documento: Documento) -> bool:
        return documento.formato == self.formato

    def texto(self, documento: Documento) -> str:
        raise NotImplementedError

    def a_canonica(self, documento: Documento) -> Resultado:
        try:
            texto = self.texto(documento)
        except Ilegible as e:
            return escalar(e.motivo)
        resultado = canonica_congelada(documento, self._carpeta)
        if resultado.factura is not None:
            con_senal_local(resultado.factura, texto)
        return resultado
