import itertools
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from ..dominio.mandato import cargar_mandato, ruta_ejemplo
from ..dominio.notificaciones import Notificaciones, cargar_datos
from ..dominio.registro_maestro import RegistroMaestro
from ..dominio.servicio import ServicioDecision
from ..infra.despacho import Despachador
from ..infra.firmador import FirmadorEd25519
from ..infra.libro import LibroSqlite
from ..infra.notificadores import canales_desde_entorno
from ..infra.registro import configurar_registros
from .app import crear_app
from .sesiones import Sesiones

REGISTRO = Path(__file__).resolve().parents[2] / "datos" / "registro-maestro.json"


def fabrica_de_servicios(ahora=lambda: datetime.now(timezone.utc), canales=None, despachar=None):
    """canales y despachar se inyectan en pruebas; por defecto salen del entorno y de un hilo comun."""
    datos = cargar_datos()
    despachar = despachar or Despachador(datos["entrega"])
    canales = canales or canales_desde_entorno(os.environ)

    def construir(version: str) -> ServicioDecision:
        contador = itertools.count(1)
        reg = RegistroMaestro.desde_archivo(REGISTRO, LibroSqlite())
        avisos = Notificaciones(canales, datos, ahora, despachar, "defecto", os.environ.get("APP_BASE_URL", ""))
        return ServicioDecision(cargar_mandato(ruta_ejemplo(version)), reg, lambda p: f"{p}_{next(contador):04d}",
                                lambda: "n_" + uuid.uuid4().hex[:10], ahora,
                                FirmadorEd25519(Ed25519PrivateKey.generate(), "k1"), avisos=avisos)
    return construir


def construir():
    configurar_registros()
    ids = lambda p: f"{p}_{uuid.uuid4().hex[:8]}"
    return crear_app(Sesiones(fabrica_de_servicios(), ids))


app = construir()
