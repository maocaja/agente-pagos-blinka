import json
from pathlib import Path

from .base import Documento, Resultado, escalar

_EXTRACCIONES = Path(__file__).resolve().parents[1] / "extracciones"


def documento_desde_archivo(ruta):
    ruta = Path(ruta)
    return Documento(id=ruta.stem, contenido=ruta.read_bytes(), formato="texto", nombre=ruta.name)


class AdaptadorTexto:
    """Texto plano. Hasta que exista el extractor (T2), sirve la lectura congelada que coincide por hash."""

    nombre = "texto"

    def __init__(self, carpeta=_EXTRACCIONES):
        self._carpeta = Path(carpeta)

    def soporta(self, documento: Documento) -> bool:
        return documento.formato == "texto"

    def a_canonica(self, documento: Documento) -> Resultado:
        for ruta in sorted(self._carpeta.glob("*.json")):
            factura = json.loads(ruta.read_text(encoding="utf-8"))
            if factura.get("documento", {}).get("hash") == documento.hash:
                return Resultado(factura)
        return escalar("sin_lectura_congelada", [documento.hash])
