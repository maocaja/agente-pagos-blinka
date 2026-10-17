"""Corre las extracciones contra la API del nucleo y contra el verificador; escribe los resultados.

  python -m evaluacion.corrida [--salida DIR]
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from ..verificador import RAIZ, Verificador, orden_regla
from . import comparar, servidor

NO_VALIDO = "la API no devolvio una decision"


def correr(salida, extracciones=None):
    esperados = {e["caso"]: e for e in json.loads((RAIZ / "datos/esperado.json").read_text(encoding="utf-8"))}
    rutas = sorted((extracciones or RAIZ / "lectura/extracciones").glob("fac-*.json"))
    sesion = servidor.Sesion(servidor.arrancar())
    mandato = sesion.mandato()
    verificador, filas = Verificador(mandato), []
    for ruta in rutas:
        f = json.loads(ruta.read_text(encoding="utf-8"))
        estado, d = sesion.enviar(f)
        if "veredicto" not in d:
            raise SystemExit(f"{f['id']}: {NO_VALIDO} (HTTP {estado})")
        v = verificador.evaluar(f)
        filas.append({"id": f["id"],
                      "motor": {"veredicto": d["veredicto"], "reglas": sorted((r["id"] for r in d["reglas"] if r["estado"] == "falla"), key=orden_regla)},
                      "verificador": {"veredicto": v["veredicto"], "reglas": v["reglas_que_fallan"], "motivo": v["motivo"]}})
    casos = comparar.casos_resultado(filas)
    huella = servidor.huella_codigo(RAIZ / "nucleo")
    resultados = {"id": f"set-{mandato['version']}-{huella[7:15]}", "tipo": "set", "semilla": None,
                  "mandato_version": mandato["version"], "huella_codigo": huella,
                  "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "recuentos": comparar.recuentos(casos), "casos": casos, "no_prueba": comparar.NO_PRUEBA}
    extra = {"resumen": comparar.resumen(filas, esperados), "discrepancias": comparar.discrepancias(filas, esperados)}
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "resultados-set.json").write_text(json.dumps(resultados, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (salida / "discrepancias-set.json").write_text(json.dumps(extra, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return resultados, extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=str(RAIZ / "evaluacion" / "salida"))
    resultados, extra = correr(Path(ap.parse_args().salida))
    print(json.dumps({"recuentos": resultados["recuentos"], "resumen": extra["resumen"],
                      "discrepancias": len(extra["discrepancias"])}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
