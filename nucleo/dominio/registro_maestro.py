import json
from datetime import date
from pathlib import Path


class RegistroMaestro:
    """Proveedores, cuentas y acuerdos; el historial de facturas sirve a R2a."""

    def __init__(self, proveedores: list, facturas_previas: list | None = None):
        self._prov = {p["id"]: p for p in proveedores}
        self.facturas = list(facturas_previas or [])

    @classmethod
    def desde_archivo(cls, ruta: Path) -> "RegistroMaestro":
        return cls(json.loads(Path(ruta).read_text(encoding="utf-8"))["proveedores"])

    def proveedor(self, pid):
        return self._prov.get(pid)

    def dias_de_alta(self, pid, hoy: date):
        p = self._prov.get(pid)
        return None if p is None else (hoy - date.fromisoformat(p["alta"])).days

    def registrar_factura(self, f: dict) -> None:
        self.facturas.append(f)
