import json
from datetime import date
from pathlib import Path


class RegistroMaestro:
    """Proveedores, cuentas y acuerdos; el historial de facturas sirve a R2a y R2b."""

    def __init__(self, proveedores: list, libro, ciclo_id: str = "", facturas_previas: list | None = None,
                 empresa: str = ""):
        self._prov = {p["id"]: p for p in proveedores}
        self.libro, self.ciclo_id, self.empresa = libro, ciclo_id, empresa
        self.facturas = list(facturas_previas or [])
        self.estados: dict = {}

    @classmethod
    def desde_archivo(cls, ruta: Path, libro) -> "RegistroMaestro":
        d = json.loads(Path(ruta).read_text(encoding="utf-8"))
        return cls(d["proveedores"], libro, d["presupuesto"]["periodo"], empresa=d.get("empresa", ""))

    def proveedores(self) -> list:
        return list(self._prov.values())

    def proveedor(self, pid):
        return self._prov.get(pid)

    def dias_de_alta(self, pid, hoy: date):
        p = self._prov.get(pid)
        return None if p is None else (hoy - date.fromisoformat(p["alta"])).days

    def registrar_factura(self, f: dict, estado: str) -> None:
        self.facturas.append(f)
        self.estados[f["id"]] = estado
