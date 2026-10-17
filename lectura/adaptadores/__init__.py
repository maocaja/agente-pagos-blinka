"""Registro de adaptadores de entrada: cada formato entrega la canonica validada o escala."""
from .base import Documento, Resultado, Adaptador, escalar, validar_canonica
from .registro import Registro, registro_por_defecto
from .texto import AdaptadorTexto, documento_desde_archivo

__all__ = [
    "Documento", "Resultado", "Adaptador", "escalar", "validar_canonica",
    "Registro", "registro_por_defecto", "AdaptadorTexto", "documento_desde_archivo",
]
