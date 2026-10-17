import itertools
import json
import uuid
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from ..dominio.mandato import cargar_mandato, ruta_ejemplo
from ..dominio.registro_maestro import RegistroMaestro
from ..dominio.servicio import ServicioDecision
from ..infra.firmador import FirmadorEd25519
from .app import crear_app
from pathlib import Path

DATOS = Path(__file__).resolve().parents[1] / "datos_prueba"


def construir(version_mandato: str = "v2"):
    contador = itertools.count(1)
    ids = lambda p: f"{p}_{next(contador):04d}"
    ruta = ruta_ejemplo(version_mandato)
    m = cargar_mandato(ruta)
    srv = ServicioDecision(m, RegistroMaestro.desde_archivo(DATOS / "registro_maestro.json"), ids,
                           lambda: "n_" + uuid.uuid4().hex[:10], lambda: datetime.now(timezone.utc),
                           FirmadorEd25519(Ed25519PrivateKey.generate(), "k1"))
    return crear_app(srv, json.loads(ruta.read_text(encoding="utf-8")))


app = construir()
