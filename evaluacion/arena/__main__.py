"""python -m evaluacion.arena [--nivel 1|2] [--semilla N]: nivel 1 hasta 500 variantes, nivel 2 hasta 3200 (fuera de verify)."""
import argparse
import json

from .. import aislada
from ..verificador import RAIZ
from . import NIVEL_1_MAX, NIVEL_2_MAX, correr

SALIDA = RAIZ / "evaluacion" / "salida" / "arena.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nivel", type=int, choices=(1, 2), default=2)
    ap.add_argument("--semilla", type=int, default=7)
    a = ap.parse_args()
    doc, errores = correr(NIVEL_1_MAX if a.nivel == 1 else NIVEL_2_MAX, a.semilla)
    assert not aislada.errores_de_esquema(doc), aislada.errores_de_esquema(doc)
    aislada.escribir(SALIDA, doc)
    r = doc["recuentos"]
    print(json.dumps({"ataques": r["lanzadas"], "pagados_indebidamente": r["pagos_indebidos"], "recuentos": r,
                      "errores_del_motor": errores[:10], "n_errores": len(errores)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
