import itertools
import uuid
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from ..dominio.mandato import cargar_mandato, ruta_ejemplo
from ..dominio.registro_maestro import RegistroMaestro
from ..dominio.servicio import ServicioDecision
from ..infra.firmador import FirmadorEd25519
from ..infra.libro import LibroSqlite
from .app import crear_app
from .sesiones import Sesiones

REGISTRO = Path(__file__).resolve().parents[2] / "datos" / "registro-maestro.json"


def fabrica_de_servicios(ahora=lambda: datetime.now(timezone.utc)):
    def construir(version: str) -> ServicioDecision:
        contador = itertools.count(1)
        reg = RegistroMaestro.desde_archivo(REGISTRO, LibroSqlite())
        return ServicioDecision(cargar_mandato(ruta_ejemplo(version)), reg, lambda p: f"{p}_{next(contador):04d}",
                                lambda: "n_" + uuid.uuid4().hex[:10], ahora,
                                FirmadorEd25519(Ed25519PrivateKey.generate(), "k1"))
    return construir


def construir():
    ids = lambda p: f"{p}_{uuid.uuid4().hex[:8]}"
    return crear_app(Sesiones(fabrica_de_servicios(), ids))


app = construir()
