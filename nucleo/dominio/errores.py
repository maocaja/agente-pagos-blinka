class FallaCerrada(Exception):
    """Dato, regla o moneda que no se puede evaluar: el motor responde ESCALAR, nunca PAGAR."""


class ErrorAccion(Exception):
    """Accion humana rechazada: la API la traduce al error del contrato."""

    def __init__(self, status, codigo, mensaje, detalle=None):
        super().__init__(mensaje)
        self.status, self.codigo, self.mensaje, self.detalle = status, codigo, mensaje, detalle


class ErrorEntrega(Exception):
    """Un canal no pudo entregar el aviso; espera_s es la espera pedida por el canal (429)."""

    def __init__(self, motivo, espera_s=None):
        super().__init__(motivo)
        self.motivo, self.espera_s = motivo, espera_s
