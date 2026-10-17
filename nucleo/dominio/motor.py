import json
from functools import lru_cache

from . import reglas_simples  # noqa: F401  registra R3 a R7
from .errores import FallaCerrada
from .explicacion import clave_razon, explicar
from .mandato import RAIZ_CONTRATO
from .reglas import AL_FINAL, REGLAS, Resultado

PRECEDENCIA = ("FRENAR", "ESCALAR")
ESTADO_DE = {"FRENAR": "frenada", "ESCALAR": "pendiente", "PAGAR": "con_recibo", "REGISTRAR": "registrada"}
# Politica por tipo: "fijo" no evalua reglas; "si_cumple" es el veredicto cuando todas pasan.
POLITICA_TIPO = {
    "factura": {"si_cumple": "PAGAR"},
    "cuenta_de_cobro": {"si_cumple": "PAGAR"},
    "nota_de_credito": {"si_cumple": "REGISTRAR", "motivo": "Nota de credito: se registra a favor del proveedor, sin orden."},
    "proforma": {"si_cumple": "ESCALAR", "motivo": "Proforma: la decide una persona."},
    "anticipo": {"si_cumple": "ESCALAR", "motivo": "Anticipo: lo decide una persona."},
    "estado_de_cuenta": {"fijo": ("FRENAR", "No es una factura.")},
}
TIPO_DESCONOCIDO = ("ESCALAR", "Tipo de documento no soportado.")


@lru_cache(maxsize=1)
def _registro() -> dict:
    datos = json.loads((RAIZ_CONTRATO / "reglas.registro.json").read_text(encoding="utf-8"))
    return {r["id"]: r["tipos"] for r in datos["reglas"]}


def ids_del_registro() -> tuple:
    return tuple(_registro())


def fallas_por_regla_faltante(registradas, requeridas) -> list:
    """Una regla del registro del contrato sin implementar nunca puede dejar pasar un PAGAR."""
    return [(i, Resultado("falla", "ESCALAR", False, f"Regla {i} no implementada", None))
            for i in requeridas if i not in registradas]


def _correr(f, m, reg, reglas, ids) -> list:
    salida = []
    for i in ids:
        try:
            r = reglas[i](f, m, reg)
        except (FallaCerrada, KeyError, TypeError, ValueError) as e:
            r = Resultado("falla", "ESCALAR", False, f"No se pudo evaluar: {e}", None)
        salida.append((i, r))
    return salida


def evaluar_reglas(f, m, reg, reglas=None, requeridas=None) -> list:
    """Corre las reglas del tipo sin cortocircuito; las de AL_FINAL solo si nada fallo antes."""
    reglas = REGLAS if reglas is None else reglas
    tipo = f["documento"]["tipo_documento"]
    aplican = [i for i, tipos in _registro().items() if tipo in tipos]
    pedidas = [i for i in (ids_del_registro() if requeridas is None else requeridas) if i in aplican]
    salida = fallas_por_regla_faltante(reglas, pedidas)
    salida += _correr(f, m, reg, reglas, [i for i in aplican if i in reglas and i not in AL_FINAL])
    if not any(r.estado == "falla" for _, r in salida):
        salida += _correr(f, m, reg, reglas, [i for i in AL_FINAL if i in aplican and i in reglas])
    orden = list(_registro())
    return sorted(salida, key=lambda x: orden.index(x[0]) if x[0] in orden else len(orden))


def agregar(resultados, si_cumple="PAGAR") -> str:
    acciones = {r.accion for _, r in resultados if r.estado == "falla"}
    return next((a for a in PRECEDENCIA if a in acciones), si_cumple)


def _veredicto(f, m, reg, reglas, requeridas):
    pol = POLITICA_TIPO.get(f.get("documento", {}).get("tipo_documento"))
    if pol is None or "fijo" in pol:
        return (TIPO_DESCONOCIDO if pol is None else pol["fijo"]) + ([],)
    res = evaluar_reglas(f, m, reg, reglas, requeridas)
    fallas = [(i, r) for i, r in res if r.estado == "falla"]
    top = min(fallas, key=lambda x: clave_razon(x[0], x[1].accion), default=None)
    motivo = top[1].evidencia if top else pol.get("motivo", "Cumple las reglas evaluadas.")
    return agregar(res, pol["si_cumple"]), motivo, res


def decidir(f, m, reg, ids, reloj, modo_autonomia, reglas=None, requeridas=None) -> dict:
    veredicto, motivo, res = _veredicto(f, m, reg, reglas, requeridas)
    explicacion, que_hacer = explicar(veredicto, motivo, [{"id": i, "estado": r.estado, "accion_si_falla": r.accion, "evidencia": r.evidencia} for i, r in res])
    return {
        "id": ids("dec"), "factura_id": f["id"], "ciclo_id": f["ciclo_id"], "mandato_version": m.version,
        "veredicto": veredicto, "motivo_corto": motivo, "explicacion": explicacion, "que_hacer": que_hacer,
        "reglas": [{"id": i, "estado": r.estado, "accion_si_falla": r.accion if r.estado == "falla" else None,
                    "aprobable": r.aprobable, "evidencia": r.evidencia, "campo_origen": r.campo} for i, r in res],
        "modo_autonomia": modo_autonomia, "estado": ESTADO_DE[veredicto],
        "creada_en": reloj().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reevaluacion_de": None, "recibo_id": None, "sin_orden": veredicto in ("FRENAR", "REGISTRAR"),
    }
