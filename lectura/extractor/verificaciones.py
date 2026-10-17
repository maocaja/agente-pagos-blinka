import json
import re
from pathlib import Path

from lectura.normalizador.normalizador import normalizar_monto

_MONEDAS = json.loads(
    (Path(__file__).resolve().parents[2] / "contrato" / "monedas.json").read_text(encoding="utf-8")
)["monedas"]


def _compacto(texto):
    return re.sub(r"\s+", " ", texto).strip()


def citas_en_texto(extraccion, texto):
    """Toda cita de evidencia debe existir y aparecer literal en el texto local."""
    base = _compacto(texto)
    citas = extraccion["evidencia"].values()
    return "ok" if all(c.strip() and _compacto(c) in base for c in citas) else "falla"


def moneda_valida(extraccion):
    return "ok" if extraccion["moneda"] in _MONEDAS else "falla"


def totales_cuadran(extraccion):
    """Las lineas suman el total; sin lineas no aplica; un numero ambiguo cuenta como falla."""
    if not extraccion["lineas"]:
        return "no_aplica"
    moneda = extraccion["moneda"]
    try:
        total = int(normalizar_monto(extraccion["monto_total"], moneda))
        suma = sum(int(normalizar_monto(x["total"], moneda)) for x in extraccion["lineas"])
    except ValueError:
        return "falla"
    return "ok" if suma == total else "falla"
