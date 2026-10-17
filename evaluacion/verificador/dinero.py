"""Conversion a la moneda base con el redondeo del mandato; exacta, en enteros."""
from fractions import Fraction
from math import ceil, floor

REDONDEOS = {"al_alza": ceil, "a_la_baja": floor}


def a_base_menor(monto_menor, moneda, mandato, monedas):
    """Monto en unidades menores de la moneda base, o None si falta tasa, exponente o redondeo."""
    p = mandato["parametros"]
    redondear = REDONDEOS.get(p.get("redondeo"))
    tasa = p["tasas_cambio"]["unidades_por_usd"].get(moneda)
    exp = monedas.get(moneda, {}).get("exponente")
    exp_base = monedas.get(p["moneda_base"], {}).get("exponente")
    if None in (redondear, tasa, exp, exp_base):
        return None
    return redondear(Fraction(int(monto_menor)) * 10 ** exp_base / (10 ** exp * Fraction(str(tasa))))
