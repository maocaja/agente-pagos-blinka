from datetime import datetime
from typing import Callable, Protocol

Reloj = Callable[[], datetime]
GeneradorId = Callable[[str], str]
GeneradorNonce = Callable[[], str]


class Firmador(Protocol):
    clave_version: str

    def firmar(self, datos: bytes) -> bytes: ...

    def firma_valida(self, documento: dict) -> bool: ...


class Libro(Protocol):
    """Reservas de presupuesto y nonces; reservar es atomico con el nonce."""

    def reservar(self, recibo_id: str, nonce: str, proveedor_id: str, periodo: str, monto: int, tope: int) -> None: ...

    def liberar(self, recibo_id: str) -> bool: ...

    def acumulado(self, periodo: str, proveedor_id: str | None = None) -> int: ...

    def consumir_nonce(self, nonce: str, recibo_id: str) -> bool: ...


class Notificador(Protocol):
    """Canal de avisos. destino va enmascarado; espaciado_s es la pausa minima entre envios."""

    nombre: str
    destino: str
    simulado: bool
    espaciado_s: float

    def enviar(self, texto: str) -> None: ...
