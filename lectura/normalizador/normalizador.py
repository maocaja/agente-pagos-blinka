import json
import re
import unicodedata
from decimal import Decimal
from pathlib import Path

_MONEDAS = json.loads(
    (Path(__file__).resolve().parents[2] / "contrato" / "monedas.json").read_text(encoding="utf-8")
)["monedas"]

# Separador de miles y de decimales por convencion; es y pt coinciden.
_FORMATOS = {"es": (".", ","), "pt": (".", ","), "en": (",", ".")}


class NumeroAmbiguo(ValueError):
    """El texto admite dos lecturas; no se adivina."""


class MonedaDesconocida(ValueError):
    pass


def _limpiar(texto):
    # Un solo tramo numerico; "9?0" o "1 200" no se compactan porque eso seria adivinar.
    t = texto.replace("\u00a0", " ")
    if "-" in t or "?" in t:
        raise ValueError("monto negativo o ilegible")
    tramos = re.findall(r"[0-9][0-9.,]*", t)
    if len(tramos) != 1:
        raise ValueError("se esperaba un unico numero")
    return tramos[0]


def _a_decimal(t, formato):
    if formato is not None:
        miles, dec = _FORMATOS[formato]
    else:
        miles = dec = None
    if miles is not None:
        if dec in t and t.count(dec) > 1:
            raise ValueError("mas de un separador decimal")
        ent, _, frac = t.partition(dec)
        if miles in frac:
            raise ValueError("miles despues del decimal")
        grupos = ent.split(miles)
        if len(grupos) > 1 and (not 1 <= len(grupos[0]) <= 3 or any(len(g) != 3 for g in grupos[1:])):
            raise ValueError("agrupacion de miles invalida")
        return Decimal("".join(grupos) + ("." + frac if frac else ""))
    # Sin formato declarado: se deduce solo si no hay ambiguedad.
    p, c = t.rfind("."), t.rfind(",")
    if p >= 0 and c >= 0:
        dec = "." if p > c else ","
        return _a_decimal(t, "en" if dec == "." else "es")
    sep = "." if p >= 0 else "," if c >= 0 else None
    if sep is None:
        return Decimal(t)
    if t.count(sep) > 1:
        return _a_decimal(t, "en" if sep == "," else "es")
    if len(t.split(sep)[1]) == 3:
        raise NumeroAmbiguo(t)
    return _a_decimal(t, "en" if sep == "." else "es")


def normalizar_monto(texto, moneda, formato=None):
    """Texto impreso -> entero de unidades menores como texto. Sin formato, lo ambiguo lanza NumeroAmbiguo."""
    if moneda not in _MONEDAS:
        raise MonedaDesconocida(moneda)
    if formato is not None and formato not in _FORMATOS:
        raise ValueError(f"formato desconocido: {formato}")
    valor = _a_decimal(_limpiar(texto), formato) * (10 ** _MONEDAS[moneda]["exponente"])
    if valor != valor.to_integral_value():
        raise ValueError("mas decimales que la moneda")
    return str(int(valor))


def normalizar_clave(texto):
    """Mayusculas, sin tildes ni simbolos, sin quitar ceros: sirve para proveedor, numero e id fiscal."""
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]", "", sin_tildes.upper())
