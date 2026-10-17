"""Arena de ataques sin modelo: variantes con semilla de las extracciones guardadas, contra el motor y el verificador."""
import copy
import json
import random

from .. import aislada
from ..corrida.comparar import NO_PRUEBA, clasificar
from ..verificador import RAIZ
from .mutaciones import CON_PREVIA, MUTACIONES, nuevo_documento

NIVEL_1_MAX = 500
NIVEL_2_MAX = 3200
NO_PRUEBA_ARENA = [
    "La lectura real del modelo: las variantes mutan lecturas guardadas, no documentos",
    "Los documentos originales (PDF, correo, chat, imagen) no se mutan: no hay extractor en vivo",
    "El detector de texto dirigido al agente: lectura/ no tiene uno, la senal se inyecta ya calculada",
    "Que todo PAGAR tenga su monto, moneda, numero y proveedor respaldados en el texto mutado",
] + NO_PRUEBA[2:4]


def bases():
    return [json.loads(r.read_text(encoding="utf-8")) for r in sorted((RAIZ / "lectura/extracciones").glob("fac-*.json"))]


def variantes(n, semilla, version="v2"):
    """Lista de (id, base, mutacion, factura mutada); depende solo de la semilla."""
    rng, origen, m = random.Random(semilla), bases(), aislada.mandato(version)
    nombres = sorted(MUTACIONES)
    sal = []
    for i in range(n):
        base, nombre = origen[rng.randrange(len(origen))], nombres[rng.randrange(len(nombres))]
        f = nuevo_documento(MUTACIONES[nombre](copy.deepcopy(base), rng, m), i)
        f["id"] = f"{base['id']}~{i}"
        sal.append((f["id"], base, nombre, f))
    return sal


def _decidir(s, f):
    s.cargadores.setdefault(f["id"], "analista")
    try:
        return s.decidir(f)["veredicto"]
    except Exception as e:  # noqa: BLE001  # calidad-ok: cualquier fallo del motor es un hallazgo, no un pago
        return "ERROR:" + type(e).__name__


def _evaluar(v, f):
    return v.evaluar(f)["veredicto"]


def correr_variante(base, f, version, con_previa):
    """Sesion limpia; la base va antes solo si la mutacion ataca un duplicado. Cuenta el veredicto de la variante."""
    s, v = aislada.servicio(version), aislada.verificador(version)
    if con_previa:
        _decidir(s, base)
        _evaluar(v, base)
    return _decidir(s, f), _evaluar(v, f)


def correr(n, semilla, version="v2"):
    casos, errores = [], []
    for id_, base, nombre, f in variantes(n, semilla, version):
        motor, oraculo = correr_variante(base, f, version, nombre in CON_PREVIA)
        if motor.startswith("ERROR"):
            errores.append({"id": id_, "mutacion": nombre, "error": motor})
            casos.append({"id": id_, "veredicto_motor": "ESCALAR", "veredicto_verificador": oraculo, "clase": "otra"})
            continue
        casos.append({"id": id_, "veredicto_motor": motor, "veredicto_verificador": oraculo, "clase": clasificar(motor, oraculo)})
    doc = aislada.resultados(f"arena-{version}-s{semilla}-n{n}", "arena", semilla, version, casos, NO_PRUEBA_ARENA)
    return doc, errores
