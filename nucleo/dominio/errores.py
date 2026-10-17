class FallaCerrada(Exception):
    """Dato, regla o moneda que no se puede evaluar: el motor responde ESCALAR, nunca PAGAR."""


class ErrorAccion(Exception):
    """Accion humana rechazada: la API la traduce al error del contrato."""

    def __init__(self, status, codigo, mensaje, detalle=None):
        super().__init__(mensaje)
        self.status, self.codigo, self.mensaje, self.detalle = status, codigo, mensaje, detalle
