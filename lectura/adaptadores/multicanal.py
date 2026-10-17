from .chat import AdaptadorChat
from .correo import AdaptadorCorreo
from .imagen import AdaptadorImagen
from .pdf import AdaptadorPdf
from .registro import Registro
from .texto import AdaptadorTexto


def registro_multicanal(lector_imagen=None):
    """Imagen va antes que PDF: un PDF sin capa de texto es un escaneado."""
    return Registro([AdaptadorImagen(lector_imagen), AdaptadorPdf(), AdaptadorCorreo(), AdaptadorChat(),
                     AdaptadorTexto()])
