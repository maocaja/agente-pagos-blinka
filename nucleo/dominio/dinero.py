import math
from fractions import Fraction

from .errores import FallaCerrada
from .mandato import Mandato, exponentes_moneda

_REDONDEO = {
    "al_alza": math.ceil,
    "a_la_baja": math.floor,
    "al_entero_mas_cercano": lambda x: math.floor(x + Fraction(1, 2)),
}


def a_base_menor(monto_menor: str, moneda: str, m: Mandato) -> int:
    """Convierte a unidades menores de la moneda base con el redondeo del mandato (al alza por defecto)."""
    exp = exponentes_moneda()
    base = m.p["moneda_base"]
    if moneda not in exp or base not in exp or m.p["redondeo"] not in _REDONDEO:
        raise FallaCerrada(f"moneda {moneda} o redondeo desconocido")
    if not str(monto_menor).isdigit():
        raise FallaCerrada("monto no es un entero en unidades menores")
    tasa_base = m.tasa(base)
    v = Fraction(int(monto_menor), 10 ** exp[moneda]) * tasa_base / m.tasa(moneda) * 10 ** exp[base]
    return int(_REDONDEO[m.p["redondeo"]](v))
