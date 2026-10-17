from pathlib import Path

from lectura.seguridad.instrucciones import con_senal_local

from .base import Documento, Resultado
from .congelada import canonica_congelada

_EXTRACCIONES = Path(__file__).resolve().parents[1] / "extracciones"
_FORMATO_POR_EXTENSION = {".pdf": "pdf", ".eml": "eml", ".jpg": "imagen", ".jpeg": "imagen", ".png": "imagen",
                          ".xml": "xml", ".csv": "csv"}


def documento_desde_archivo(ruta):
    ruta = Path(ruta)
    datos = ruta.read_bytes()
    formato = _FORMATO_POR_EXTENSION.get(ruta.suffix.lower(), "texto")
    if formato == "texto" and datos.startswith(b"[WhatsApp"):
        formato = "chat"
    return Documento(id=ruta.stem, contenido=datos, formato=formato, nombre=ruta.name)


class AdaptadorTexto:
    """Texto plano. Hasta que exista el extractor (T2), sirve la lectura congelada que coincide por hash."""

    nombre = "texto"

    def __init__(self, carpeta=_EXTRACCIONES):
        self._carpeta = Path(carpeta)

    def soporta(self, documento: Documento) -> bool:
        return documento.formato == "texto"

    def a_canonica(self, documento: Documento) -> Resultado:
        resultado = canonica_congelada(documento, self._carpeta)
        if resultado.factura is not None:
            con_senal_local(resultado.factura, documento.contenido.decode("utf-8", errors="ignore"))
        return resultado
