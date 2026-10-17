#!/usr/bin/env python3
"""Punto de entrada unico de verificacion: determinista, acotado, sin red ni modelos.

  python3 verify.py                correr lo que exista y reportar
  python3 verify.py --gate         puerta de calidad: todo obligatorio, dos corridas identicas
  python3 verify.py --etapa nucleo una sola etapa
Codigo de salida 0 si todo esta en verde; 1 si no.
"""
import calidad
import control
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
P = json.loads((RAIZ / "verify.budget.json").read_text())
UNIDADES = ["nucleo", "lectura", "interfaz", "evaluacion"]
CLAVES_DE_MODELOS = ["ANTHROPIC_API_KEY", "TYPESAFE_API_KEY", "OPENAI_API_KEY"]


def entorno():
    e = dict(os.environ)
    for k in CLAVES_DE_MODELOS:
        e.pop(k, None)
    e.update(PYTHONHASHSEED="0", TZ="UTC", LC_ALL="C", PYTHONDONTWRITEBYTECODE="1", NO_NETWORK="1",
             VERIFY_SEED=str(P["semilla"]), VERIFY_ARENA_MAX=str(P["arena_variantes_max"]),
             VERIFY_RELOJ=P["reloj_congelado"], HYPOTHESIS_PROFILE="verify")
    return e


def leer_junit(ruta):
    huella, total, fallos, omitidas = [], 0, 0, 0
    for caso in ET.parse(ruta).getroot().iter("testcase"):
        estado = "ok"
        for hijo in caso:
            if hijo.tag in ("failure", "error"):
                estado = "falla"
            elif hijo.tag == "skipped" and estado == "ok":
                estado = "omitida"
        total += 1
        fallos += estado == "falla"
        omitidas += estado == "omitida"
        huella.append((f"{caso.get('classname')}::{caso.get('name')}", estado))
    return {"total": total, "fallos": fallos, "omitidas": omitidas}, sorted(huella)


def correr(cmd, cwd, segundos):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, env=entorno(), capture_output=True, text=True, timeout=segundos)
        return r.returncode, r.stdout + r.stderr, time.time() - t0
    except subprocess.TimeoutExpired:
        return 124, f"tiempo agotado ({segundos}s)", time.time() - t0


def etapa_contrato():
    rc, salida, seg = correr([sys.executable, "validar.py"], RAIZ / "contrato", P["etapas"]["contrato"]["segundos"])
    return {"estado": "OK" if rc == 0 else "FALLA", "pruebas": None, "segundos": seg, "nota": "" if rc == 0 else salida[-400:]}, None


def etapa_unidad(nombre):
    cfg = P["etapas"][nombre]
    carpeta = RAIZ / nombre / "tests"
    if not carpeta.is_dir() or not any(carpeta.glob("test_*.py")):
        return {"estado": "PENDIENTE", "pruebas": None, "segundos": 0, "nota": "aun no hay pruebas"}, None
    if importlib.util.find_spec("pytest") is None:
        return {"estado": "FALLA", "pruebas": None, "segundos": 0, "nota": "pytest no esta instalado"}, None
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / "junit.xml"
        cmd = [sys.executable, "-m", "pytest", str(carpeta), "-q", "-p", "no:randomly", "-p", "no:cacheprovider",
               "-o", "junit_family=xunit2", "--junitxml", str(xml)]
        rc, salida, seg = correr(cmd, RAIZ, cfg["segundos"])
        if not xml.exists():
            return {"estado": "FALLA", "pruebas": None, "segundos": seg, "nota": salida[-400:]}, None
        conteo, huella = leer_junit(xml)
    estado, nota = "OK", ""
    if rc != 0 or conteo["fallos"]:
        estado, nota = "FALLA", salida[-400:]
    elif conteo["total"] > cfg["max"]:
        estado, nota = "EXCEDE_PRESUPUESTO", f"{conteo['total']} pruebas; el maximo es {cfg['max']}"
    else:
        hallazgos = calidad.revisar([RAIZ / nombre])
        if hallazgos:
            estado, nota = "CALIDAD", f"{len(hallazgos)} hallazgos; el primero: {hallazgos[0]}"
    return {"estado": estado, "pruebas": conteo, "segundos": seg, "nota": nota}, huella


def etapa_mutacion():
    script = RAIZ / "evaluacion" / "mutacion.py"
    if not script.exists():
        return {"estado": "PENDIENTE", "pruebas": None, "segundos": 0, "nota": "aun no existe evaluacion/mutacion.py"}, None
    rc, salida, seg = correr([sys.executable, str(script), "--semilla", str(P["semilla"])], RAIZ, P["etapas"]["mutacion"]["segundos"])
    return {"estado": "OK" if rc == 0 else "FALLA", "pruebas": None, "segundos": seg, "nota": "" if rc == 0 else salida[-400:]}, None


def una_corrida(etapas):
    res, huellas = {}, {}
    for e in etapas:
        if e == "contrato":
            res[e], huellas[e] = etapa_contrato()
        elif e == "mutacion":
            res[e], huellas[e] = etapa_mutacion()
        else:
            res[e], huellas[e] = etapa_unidad(e)
    return res, huellas


def commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True, text=True).stdout.strip() or None
    except OSError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true", help="puerta de calidad")
    ap.add_argument("--etapa", choices=["contrato"] + UNIDADES + ["mutacion"])
    ap.add_argument("--informe", default=str(RAIZ / "verify-report.json"))
    a = ap.parse_args()
    etapas = [a.etapa] if a.etapa else ["contrato"] + UNIDADES + (["mutacion"] if a.gate else [])
    corridas = 2 if a.gate else 1

    resultados = [una_corrida(etapas) for _ in range(corridas)]
    res, huellas = resultados[0]
    problemas = []
    if corridas == 2:
        for e in etapas:
            if resultados[1][1][e] != huellas[e]:
                res[e]["estado"] = "NO_DETERMINISTA"
                res[e]["nota"] = "dos corridas dieron resultados distintos"
    total = sum(r["pruebas"]["total"] for r in res.values() if r["pruebas"])
    if total > P["total_max"]:
        problemas.append(f"{total} pruebas en total; el maximo es {P['total_max']}")
    segundos = sum(r["segundos"] for r in res.values()) * corridas
    if segundos > P["segundos_max_total"]:
        problemas.append(f"{segundos:.0f} s en total; el maximo es {P['segundos_max_total']}")
    if a.gate:
        problemas += [f"CONTROL: {x}" for x in control.revisar()]
    for e, r in res.items():
        if r["estado"] == "PENDIENTE" and a.gate:
            problemas.append(f"etapa {e} pendiente: en la puerta de calidad es obligatoria")
        elif r["estado"] not in ("OK", "PENDIENTE"):
            problemas.append(f"etapa {e}: {r['estado']}")
        if a.gate and r["pruebas"] and r["pruebas"]["omitidas"]:
            problemas.append(f"etapa {e}: {r['pruebas']['omitidas']} pruebas omitidas")

    print(f"verify {'(puerta de calidad)' if a.gate else ''} semilla={P['semilla']} corridas={corridas}")
    for e in etapas:
        r = res[e]
        n = f"{r['pruebas']['total']} pruebas" if r["pruebas"] else "-"
        print(f"  {e:<11} {r['estado']:<18} {n:<12} {r['segundos']:.1f}s  {r['nota'][:90]}")
    print(f"  total: {total} pruebas (maximo {P['total_max']}), {segundos:.1f}s")
    for p in problemas:
        print("  PROBLEMA:", p)

    informe = {"commit": commit(), "gate": a.gate, "semilla": P["semilla"], "corridas": corridas,
               "etapas": res, "total_pruebas": total, "segundos": round(segundos, 1), "problemas": problemas,
               "verde": not problemas}
    Path(a.informe).write_text(json.dumps(informe, indent=2, ensure_ascii=False) + "\n")
    print("VERDE" if not problemas else "ROJO")
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
