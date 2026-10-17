"""Corrida del set multicanal: lectura congelada -> API del nucleo -> comparacion con los esperados.

  python -m evaluacion.corrida_documentos [--salida DIR] [--casos d_01,d_02]
"""
import argparse
import json
from pathlib import Path

from .corrida import servidor
from .verificador import RAIZ, orden_regla


def _esperados():
    return json.loads((RAIZ / "datos/esperado-documentos.json").read_text(encoding="utf-8"))


def _fila(sesion, esperado, lecturas):
    ruta = lecturas / (Path(esperado["archivo"]).stem + ".json")
    estado, d = sesion.enviar(json.loads(ruta.read_text(encoding="utf-8")))
    reglas = sorted((r["id"] for r in d.get("reglas", []) if r["estado"] == "falla"), key=orden_regla)
    er, ee = esperado["esperado_reglas"], esperado["esperado_extremo_a_extremo"]
    motivos = []
    if "veredicto" not in d:
        motivos.append(f"la API no devolvio una decision (HTTP {estado})")
    if d.get("veredicto") != er["veredicto"]:
        motivos.append(f"veredicto {d.get('veredicto')} contra esperado_reglas {er['veredicto']}")
    if d.get("veredicto") != ee["veredicto"]:
        motivos.append(f"veredicto {d.get('veredicto')} contra extremo_a_extremo {ee['veredicto']}")
    if reglas != er["reglas_que_fallan"]:
        motivos.append(f"reglas {reglas} contra esperadas {er['reglas_que_fallan']}")
    return {"caso": esperado["caso"], "archivo": esperado["archivo"], "motor": {"veredicto": d.get("veredicto"), "reglas": reglas},
            "esperado_reglas": {"veredicto": er["veredicto"], "reglas": er["reglas_que_fallan"]},
            "esperado_extremo_a_extremo": ee["veredicto"], "coincide": not motivos, "motivos": motivos}


def correr(salida, casos=None, lecturas=None):
    lecturas = lecturas or RAIZ / "lectura/extracciones_multicanal"
    sesion = servidor.Sesion(servidor.arrancar())
    filas = [_fila(sesion, e, lecturas) for e in _esperados() if casos is None or e["caso"] in casos]
    resultado = {"mandato_version": sesion.mandato()["version"], "documentos": len(filas),
                 "coinciden": sum(f["coincide"] for f in filas),
                 "pagados": [f["caso"] for f in filas if f["motor"]["veredicto"] == "PAGAR"],
                 "discrepancias": [f for f in filas if not f["coincide"]], "casos": filas}
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "documentos.json").write_text(json.dumps(resultado, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return resultado


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=str(RAIZ / "evaluacion" / "salida"))
    ap.add_argument("--casos", default="")
    a = ap.parse_args()
    r = correr(Path(a.salida), set(a.casos.split(",")) if a.casos else None)
    print(json.dumps({k: r[k] for k in ("mandato_version", "documentos", "coinciden", "pagados")}, ensure_ascii=False))
    for f in r["discrepancias"]:
        print(f["caso"], f["archivo"], "|", "; ".join(f["motivos"]))


if __name__ == "__main__":
    main()
