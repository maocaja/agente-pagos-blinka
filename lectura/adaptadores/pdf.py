import io

from pypdf import PdfReader
from pypdf.errors import PyPdfError

from .congelada import AdaptadorDeTexto, Ilegible


def leer_pdf(contenido):
    """(estado, texto) con estado ok, pdf_cifrado o sin_texto; incluye texto blanco o diminuto."""
    try:
        lector = PdfReader(io.BytesIO(contenido))
        if lector.is_encrypted:
            return "pdf_cifrado", ""
        texto = "\n".join((p.extract_text() or "") for p in lector.pages).strip()
    except (PyPdfError, ValueError, OSError):
        return "sin_texto", ""
    return ("ok", texto) if texto else ("sin_texto", "")


class AdaptadorPdf(AdaptadorDeTexto):
    nombre = "pdf"
    formato = "pdf"

    def texto(self, documento):
        estado, texto = leer_pdf(documento.contenido)
        if estado != "ok":
            raise Ilegible(estado)
        return texto
