from .chat import AdaptadorChat
from .correo import AdaptadorCorreo
from .imagen import AdaptadorImagen
from .pdf import AdaptadorPdf
from .registro import Registro
from .lote_csv import AdaptadorCsvLote
from .texto import AdaptadorTexto
from .xml_ubl import AdaptadorXml


def registro_multicanal(lector_imagen=None, contexto=None):
    """Imagen va antes que PDF: un PDF sin capa de texto es un escaneado. XML y CSV piden el contexto del ciclo."""
    adaptadores = [AdaptadorImagen(lector_imagen), AdaptadorPdf(), AdaptadorCorreo(), AdaptadorChat(),
                   AdaptadorTexto()]
    if contexto is not None:
        adaptadores += [AdaptadorXml(contexto), AdaptadorCsvLote(contexto)]
    return Registro(adaptadores)
