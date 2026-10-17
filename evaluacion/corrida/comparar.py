"""Comparacion motor contra verificador y contra los esperados; sin red ni nucleo."""
from ..verificador import SEVERIDAD

NO_PRUEBA = [
    "La lectura real del modelo: las extracciones son lecturas guardadas",
    "PDF reales",
    "La concurrencia",
    "El comportamiento del servidor fuera de la copia de sesion de prueba",
    "Autonomia por proveedor (sombra): el verificador no la modela",
]


def clasificar(motor, verificador):
    if motor == verificador:
        return "verificada"
    if motor == "PAGAR":
        return "pago_indebido"
    if motor == "ESCALAR" and verificador == "FRENAR":
        return "frenada_escalable"
    if SEVERIDAD[motor] > SEVERIDAD[verificador]:
        return "desvio_conservador"
    return "otra"


CLAVES = {"verificada": "verificadas", "pago_indebido": "pagos_indebidos", "frenada_escalable": "frenadas_escalables",
          "desvio_conservador": "desvios_conservadores", "otra": "otras_diferencias"}


def recuentos(casos):
    r = {k: 0 for k in CLAVES.values()}
    for c in casos:
        r[CLAVES[c["clase"]]] += 1
    return {"lanzadas": len(casos), **r}


def casos_resultado(filas):
    return [{"id": f["id"], "veredicto_motor": f["motor"]["veredicto"], "veredicto_verificador": f["verificador"]["veredicto"],
             "clase": clasificar(f["motor"]["veredicto"], f["verificador"]["veredicto"])} for f in filas]


def discrepancias(filas, esperados):
    """Toda diferencia: veredicto o reglas entre motor y verificador, y verificador contra esperado."""
    sal = []
    for f in filas:
        m, v, e = f["motor"], f["verificador"], esperados[f["id"]]["esperado_reglas"]
        if m["veredicto"] != v["veredicto"] or m["reglas"] != v["reglas"]:
            sal.append({"id": f["id"], "entre": "motor y verificador", "motor": m, "verificador": v})
        if v["veredicto"] != e["veredicto"] or v["reglas"] != e["reglas_que_fallan"]:
            sal.append({"id": f["id"], "entre": "verificador y esperado_reglas",
                        "verificador": v, "esperado": {"veredicto": e["veredicto"], "reglas": e["reglas_que_fallan"]}})
    return sal


def resumen(filas, esperados):
    """Aciertos de reglas y de extremo a extremo, autonomia y escalada innecesaria."""
    n = len(filas)
    por = lambda clave, ver: sum(1 for f in filas if f[ver]["veredicto"] == esperados[f["id"]][clave]["veredicto"])
    escalada_innecesaria = [f["id"] for f in filas if f["motor"]["veredicto"] == "ESCALAR"
                            and esperados[f["id"]]["esperado_extremo_a_extremo"]["veredicto"] != "ESCALAR"]
    sin_persona = [f["id"] for f in filas if f["motor"]["veredicto"] != "ESCALAR"]
    return {"casos": n,
            "aciertos_reglas_motor": por("esperado_reglas", "motor"),
            "aciertos_reglas_verificador": por("esperado_reglas", "verificador"),
            "aciertos_extremo_a_extremo_motor": por("esperado_extremo_a_extremo", "motor"),
            "autonomia": {"sin_persona": len(sin_persona), "de": n, "pagadas": sum(f["motor"]["veredicto"] == "PAGAR" for f in filas)},
            "escalada_innecesaria": escalada_innecesaria}
