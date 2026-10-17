from .errores import FallaCerrada
from .reglas import REGLAS, TIPOS_EVALUABLES, Resultado

PRECEDENCIA = ("FRENAR", "ESCALAR")
# Tipos que no se evalúan por reglas: resultado fijo. Lo no listado ni evaluable es ESCALAR.
POLITICA_TIPO = {"estado_de_cuenta": ("FRENAR", "No es una factura.")}


def evaluar_reglas(f, m, reg, reglas=None) -> list:
    """Corre todas las reglas sin cortocircuito; una excepcion es falla ESCALAR no aprobable."""
    salida = []
    for id_, fn in (reglas or REGLAS).items():
        try:
            r = fn(f, m, reg)
        except (FallaCerrada, KeyError, TypeError, ValueError) as e:
            r = Resultado("falla", "ESCALAR", False, f"No se pudo evaluar: {e}", None)
        salida.append((id_, r))
    return salida


def agregar(resultados) -> str:
    acciones = {r.accion for _, r in resultados if r.estado == "falla"}
    for a in PRECEDENCIA:
        if a in acciones:
            return a
    return "PAGAR"


def decidir(f, m, reg, ids, reloj, modo_autonomia, reglas=None) -> dict:
    tipo = f.get("documento", {}).get("tipo_documento")
    fijo = POLITICA_TIPO.get(tipo)
    if tipo in TIPOS_EVALUABLES:
        res = evaluar_reglas(f, m, reg, reglas)
        veredicto = agregar(res)
        fallas = [(i, r) for i, r in res if r.estado == "falla"]
        top = next((x for a in PRECEDENCIA for x in fallas if x[1].accion == a), None)
        motivo = top[1].evidencia if top else "Cumple las reglas evaluadas."
    else:
        veredicto, motivo = fijo or ("ESCALAR", "Tipo de documento no soportado.")
        res = []
    estado = {"FRENAR": "frenada", "ESCALAR": "pendiente", "PAGAR": "con_recibo"}[veredicto]
    return {
        "id": ids("dec"), "factura_id": f["id"], "ciclo_id": f["ciclo_id"], "mandato_version": m.version,
        "veredicto": veredicto, "motivo_corto": motivo,
        "reglas": [{"id": i, "estado": r.estado, "accion_si_falla": r.accion if r.estado == "falla" else None,
                    "aprobable": r.aprobable, "evidencia": r.evidencia, "campo_origen": r.campo} for i, r in res],
        "modo_autonomia": modo_autonomia, "estado": estado,
        "creada_en": reloj().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reevaluacion_de": None, "recibo_id": None, "sin_orden": veredicto in ("FRENAR", "REGISTRAR"),
    }
