import copy
import json
from pathlib import Path

from evaluacion.verificador import Verificador

RAIZ = Path(__file__).resolve().parents[2]
MANDATO_V2 = json.loads((RAIZ / "contrato/ejemplos/mandato.v2.json").read_text(encoding="utf-8"))
BASE = json.loads((RAIZ / "lectura/extracciones/fac-04.json").read_text(encoding="utf-8"))  # Cloud, USD 2.000


def mandato(**parametros):
    m = copy.deepcopy(MANDATO_V2)
    m["parametros"].update(parametros)
    return m


def verificador(**parametros):
    return Verificador(mandato(**parametros))


def factura(id_="x1", total="200000", numero="CA-1", recibido="2026-10-06", moneda="USD", **cambios):
    f = copy.deepcopy(BASE)
    f["id"], f["documento"]["hash"], f["documento"]["recibido_en"] = id_, "h" + id_, recibido + "T10:00:00Z"
    f["referencias"]["numero"] = numero
    f["montos"].update(moneda=moneda, total_menor=total, suma_lineas_menor=total, lineas=[{"descripcion": "x", "total_menor": total}])
    for ruta, valor in cambios.items():
        destino = f
        *camino, hoja = ruta.split("__")
        for k in camino:
            destino = destino[k]
        destino[hoja] = valor
    return f
