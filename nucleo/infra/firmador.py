import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from ..dominio.recibo import serializar


class FirmadorEd25519:
    def __init__(self, clave: Ed25519PrivateKey, clave_version: str):
        self._clave = clave
        self.clave_version = clave_version

    def firmar(self, datos: bytes) -> bytes:
        return self._clave.sign(datos)

    @property
    def clave_publica(self) -> Ed25519PublicKey:
        return self._clave.public_key()


def verificar_firma(recibo: dict, publica: Ed25519PublicKey) -> bool:
    try:
        publica.verify(base64.b64decode(recibo["firma"]), serializar(recibo))
        return True
    except (InvalidSignature, KeyError, ValueError):
        return False
