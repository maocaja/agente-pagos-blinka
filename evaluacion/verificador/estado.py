"""Estado propio del verificador: se reconstruye repitiendo la secuencia de entradas."""
from dataclasses import dataclass, field


@dataclass
class Recibida:
    proveedor: str
    numero: str
    hash: str
    base_menor: int
    fecha: str
    tipo: str
    veredicto: str
    periodo: str


@dataclass
class Estado:
    recibidas: list = field(default_factory=list)

    def registrar(self, r):
        self.recibidas.append(r)

    def del_proveedor(self, proveedor):
        return [r for r in self.recibidas if proveedor and r.proveedor == proveedor]

    def reservado(self, periodo, proveedor=None):
        """Suma de lo que un PAGAR reservo en el periodo, de todos o de un proveedor."""
        return sum(r.base_menor for r in self.recibidas
                   if r.veredicto == "PAGAR" and r.periodo == periodo and (proveedor is None or r.proveedor == proveedor))
