"""Mutacion del motor: cada mutante se aplica a una copia de nucleo/ y las pruebas deben fallar."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MUTANTES = Path(__file__).with_name("mutacion") / "mutantes.json"
SALIDA = Path(__file__).with_name("salida") / "mutacion.json"
FALLO = re.compile(r"^FAILED (\S+)", re.M)


def correr_pruebas(tmp: Path, semilla: int):
    env = {**os.environ, "VERIFY_SEED": str(semilla), "PYTHONPATH": str(tmp), "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([sys.executable, "-m", "pytest", "nucleo/tests", "-q", "-p", "no:randomly", "-p", "no:cacheprovider", "--tb=no", "-rf"],
                       cwd=tmp, env=env, capture_output=True, text=True)
    return p.returncode, FALLO.findall(p.stdout)


def preparar(tmp: Path):
    shutil.copytree(RAIZ / "nucleo", tmp / "nucleo", ignore=shutil.ignore_patterns("__pycache__"))
    for otra in ("contrato", "lectura"):
        shutil.copytree(RAIZ / otra, tmp / otra, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(RAIZ / "datos", tmp / "datos", ignore=shutil.ignore_patterns("ocultas"))
    shutil.copytree(RAIZ / "evaluacion" / "salida", tmp / "evaluacion" / "salida")
    shutil.copy(RAIZ / "conftest.py", tmp / "conftest.py")


def aplicar(tmp: Path, m: dict):
    ruta = tmp / m["archivo"]
    texto = ruta.read_text(encoding="utf-8")
    if texto.count(m["original"]) != 1:
        raise SystemExit(f"{m['id']}: el texto original aparece {texto.count(m['original'])} veces en {m['archivo']}")
    ruta.write_text(texto.replace(m["original"], m["mutado"]), encoding="utf-8")
    return ruta, texto


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--semilla", type=int, default=7)
    a = ap.parse_args()
    mutantes = json.loads(MUTANTES.read_text(encoding="utf-8"))
    resultados = []
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        preparar(tmp)
        rc, _ = correr_pruebas(tmp, a.semilla)
        if rc != 0:
            raise SystemExit("las pruebas del nucleo no pasan sin mutar")
        for m in mutantes:
            ruta, original = aplicar(tmp, m)
            rc, fallos = correr_pruebas(tmp, a.semilla)
            ruta.write_text(original, encoding="utf-8")
            resultados.append({"id": m["id"], "archivo": m["archivo"], "rompe": m["rompe"],
                               "atrapado": rc != 0, "pruebas": fallos})
    SALIDA.write_text(json.dumps({"semilla": a.semilla, "mutantes": resultados}, ensure_ascii=False, indent=1), encoding="utf-8")
    vivos = [r for r in resultados if not r["atrapado"]]
    for r in vivos:
        print(f"SOBREVIVE {r['id']} {r['archivo']}: {r['rompe']}")
    print(f"{len(resultados) - len(vivos)}/{len(resultados)} atrapados")
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
