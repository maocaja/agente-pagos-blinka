"""Cliente de la API del nucleo con la app en proceso (TestClient); solo para la corrida de integracion."""
import hashlib
from pathlib import Path


def arrancar():
    from fastapi.testclient import TestClient
    from nucleo.api.principal import app
    return TestClient(app)


class Sesion:
    def __init__(self, cliente, rol="analista"):
        self.cliente = cliente
        self.id = cliente.post("/api/sesion").json()["sesion_id"]
        self.cabeceras = {"X-Sesion-Id": self.id, "X-Rol": rol}

    def mandato(self):
        return self.cliente.get("/api/mandato", headers=self.cabeceras).json()

    def enviar(self, factura):
        r = self.cliente.post("/api/facturas", json=factura, headers={**self.cabeceras, "Idempotency-Key": factura["id"]})
        return r.status_code, r.json()


def huella_codigo(carpeta):
    h = hashlib.sha256()
    for p in sorted(Path(carpeta).rglob("*.py")):
        h.update(p.relative_to(carpeta).as_posix().encode() + p.read_bytes())
    return "sha256:" + h.hexdigest()
