"""Sesiones limpias del motor y resultados.json comunes a pentest y arena; el reloj fijo hace repetible la corrida."""
import json
from datetime import datetime, timezone
from pathlib import Path

from nucleo.api.principal import fabrica_de_servicios

from .corrida import comparar
from .corrida.servidor import huella_codigo
from .verificador import RAIZ, Verificador

AHORA = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
ESQUEMA = RAIZ / "contrato/resultados.schema.json"


def mandato(version):
    return json.loads((RAIZ / f"contrato/ejemplos/mandato.{version}.json").read_text(encoding="utf-8"))


def servicio(version):
    return fabrica_de_servicios(lambda: AHORA)(version)


def verificador(version="v2"):
    return Verificador(mandato(version))


def resultados(id_, tipo, semilla, version, casos, no_prueba):
    return {"id": id_, "tipo": tipo, "semilla": semilla, "mandato_version": version,
            "huella_codigo": huella_codigo(RAIZ / "nucleo"), "fecha": AHORA.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "recuentos": comparar.recuentos(casos), "casos": casos, "no_prueba": no_prueba}


def escribir(ruta: Path, doc):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def errores_de_esquema(doc):
    import importlib.util
    spec = importlib.util.spec_from_file_location("validar_contrato", RAIZ / "contrato/validar.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validar(doc, json.loads(ESQUEMA.read_text(encoding="utf-8")))
