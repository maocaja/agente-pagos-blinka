"""Infraestructura comun de pruebas deterministas: sin red, reloj y semilla fijos."""
import os
import random
import socket
from datetime import datetime, timezone

import pytest

SEMILLA = int(os.environ.get("VERIFY_SEED", "7"))
LOCALES = {"127.0.0.1", "::1", "localhost"}

try:
    from hypothesis import settings
    # derandomize y database=None: mismos casos en cada corrida, sin estado entre corridas
    settings.register_profile("verify", derandomize=True, database=None, max_examples=100, deadline=None)
    if os.environ.get("HYPOTHESIS_PROFILE") == "verify":
        settings.load_profile("verify")
except ImportError:
    pass


@pytest.fixture(autouse=True)
def _determinismo(monkeypatch):
    random.seed(SEMILLA)
    conectar_real = socket.socket.connect

    def conectar(self, direccion, *args, **kwargs):
        host = direccion[0] if isinstance(direccion, tuple) else direccion
        if host not in LOCALES:
            raise RuntimeError(f"Red bloqueada en verify: {host}")
        return conectar_real(self, direccion, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", conectar)


@pytest.fixture
def ahora():
    # El codigo recibe el reloj por inyeccion; las pruebas nunca leen la hora real
    return datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
