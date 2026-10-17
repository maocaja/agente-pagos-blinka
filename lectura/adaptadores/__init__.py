"""Registro de adaptadores de entrada: cada formato entrega la canonica validada o escala."""
from .base import Documento, Resultado, Adaptador, escalar, validar_canonica
from .registro import Registro, registro_por_defecto
from .multicanal import registro_multicanal
from .texto import AdaptadorTexto, documento_desde_archivo

__all__ = [
    "Documento", "Resultado", "Adaptador", "escalar", "validar_canonica",
    "Registro", "registro_por_defecto", "registro_multicanal", "AdaptadorTexto", "documento_desde_archivo",
]
