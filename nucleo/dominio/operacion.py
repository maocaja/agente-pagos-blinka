import logging

_LOG = logging.getLogger("nucleo.operacion")


def anotar(evento: str, **campos) -> None:
    """Registro de operacion; el formateador solo deja pasar identificadores de correlacion y estados."""
    _LOG.info(evento, extra={"campos": campos})
