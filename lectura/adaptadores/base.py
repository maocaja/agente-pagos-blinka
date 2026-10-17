import hashlib
import importlib.util
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Protocol

_CONTRATO = Path(__file__).resolve().parents[2] / "contrato"
_ESQUEMA = json.loads((_CONTRATO / "factura-canonica.schema.json").read_text(encoding="utf-8"))

# contrato/ no es un paquete; se carga su validador por ruta para no copiarlo.
_spec = importlib.util.spec_from_file_location("contrato_validar", _CONTRATO / "validar.py")
_validar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validar)


@dataclass(frozen=True)
class Documento:
    id: str
    contenido: bytes
    formato: str
    nombre: str = ""

    @property
    def hash(self):
        return hashlib.sha256(self.contenido).hexdigest()


@dataclass
class Resultado:
    factura: Optional[dict]
    motivo: Optional[str] = None
    detalle: list = field(default_factory=list)

    @property
    def escala(self):
        return self.factura is None


class Adaptador(Protocol):
    nombre: str

    def soporta(self, documento: Documento) -> bool: ...
    def a_canonica(self, documento: Documento) -> Resultado: ...


def escalar(motivo, detalle=()):
    return Resultado(None, motivo, list(detalle))


def validar_canonica(factura):
    """Errores contra el esquema del contrato; lista vacia si valida."""
    return _validar.validar(factura, _ESQUEMA)
