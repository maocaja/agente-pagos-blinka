from datetime import datetime
from typing import Callable, Protocol

Reloj = Callable[[], datetime]
GeneradorId = Callable[[str], str]
GeneradorNonce = Callable[[], str]


class Firmador(Protocol):
    clave_version: str

    def firmar(self, datos: bytes) -> bytes: ...
