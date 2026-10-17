"""Corrida final con las 4 ocultas: sello -> lectura manual congelada -> API del nucleo -> comparacion.

  python -m evaluacion.corrida_ocultas [--ocultas DIR] [--salida DIR]
Una sola corrida: no corrige nada, solo reporta las diferencias.
"""
import argparse
import hashlib
import json
from pathlib import Path

from .corrida import servidor
from .verificador import RAIZ, orden_regla

LECTURAS = Path(__file__).resolve().parent / "ocultas_lecturas"


def _json(ruta):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


def sello_roto(carpeta):
    esperado = _json(carpeta / "SELLO.json")["archivos"]
    return [n for n, h in esperado.items() if hashlib.sha256((carpeta / n).read_bytes()).hexdigest() != h]


def _fila(esperado, factura, estado, d):
    falla = [r for r in d.get("reglas", []) if r["estado"] == "falla"]
    reglas = sorted((r["id"] for r in falla), key=orden_regla)
    motivos = []
    if "veredicto" not in d:
        motivos.append(f"la API no devolvio una decision (HTTP {estado})")
    if d.get("veredicto") != esperado["veredicto"]:
        motivos.append(f"veredicto {d.get('veredicto')} contra esperado {esperado['veredicto']}")
    if reglas != esperado["reglas_que_fallan"]:
        motivos.append(f"reglas {reglas} contra esperadas {esperado['reglas_que_fallan']}")
    return {"orden": esperado["orden"], "archivo": esperado["archivo"], "motor": {"veredicto": d.get("veredicto"), "reglas": reglas},
            "esperado": {"veredicto": esperado["veredicto"], "reglas": esperado["reglas_que_fallan"]},
            "coincide": not motivos, "motivos": motivos,
            "evidencia": [{"regla": r["id"], "dato": r["campo_origen"], "detalle": r["evidencia"]} for r in falla],
            "cuenta_leida": factura["cuenta"], "motivo_corto": d.get("motivo_corto")}


def correr(ocultas, salida):
    rotos = sello_roto(ocultas)
    if rotos:
        raise SystemExit(f"SELLO roto, no se corre: {rotos}")
    filas, mandato = [], None
    for e in _json(ocultas / "esperado-ocultas.json"):
        factura = _json(LECTURAS / (Path(e["archivo"]).stem + ".json"))
        sesion = servidor.Sesion(servidor.arrancar())
        mandato = sesion.mandato()["version"]
        estado, d = sesion.enviar(factura)
        filas.append(_fila(e, factura, estado, d))
    resultado = {"mandato_version": mandato, "sello": "ok", "documentos": len(filas), "coinciden": sum(f["coincide"] for f in filas),
                 "pagados": [f["orden"] for f in filas if f["motor"]["veredicto"] == "PAGAR"],
                 "discrepancias": [f for f in filas if not f["coincide"]], "casos": filas}
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "ocultas.json").write_text(json.dumps(resultado, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return resultado


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ocultas", default=str(RAIZ / "datos/ocultas"))
    ap.add_argument("--salida", default=str(RAIZ / "evaluacion/salida"))
    a = ap.parse_args()
    r = correr(Path(a.ocultas), Path(a.salida))
    print(json.dumps({k: r[k] for k in ("mandato_version", "documentos", "coinciden", "pagados")}, ensure_ascii=False))
    for f in r["discrepancias"]:
        print(f["orden"], f["archivo"], "|", "; ".join(f["motivos"]))


if __name__ == "__main__":
    main()
