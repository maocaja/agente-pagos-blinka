"""Historial y actividad derivados de lo ya registrado en la sesion; no se inventan eventos."""

from .dinero import base_de, importe
from .errores import FallaCerrada
from .explicacion import fallas_por_precedencia

_ACCION = {"aprobar": "aprobada", "rechazar": "rechazada"}
_VEREDICTO = {"PAGAR": "Autorizada", "FRENAR": "Frenada", "ESCALAR": "Escalada", "REGISTRAR": "Registrada"}
_TEXTO = {"decidida": "{veredicto}: {detalle}{regla}",
          "aprobada": "Aprobada por {actor}: {detalle}",
          "rechazada": "Rechazada por {actor}: {detalle}"}


def _ev(hora, evento, actor, nota=None) -> dict:
    return {"hora": hora, "evento": evento, "actor": actor, "nota": nota or None}


def _propios(s, d) -> list:
    """Eventos de esta decision, en orden cronologico, sin la cadena de reevaluacion."""
    previa = d.get("reevaluacion_de")
    ev = [] if previa else [_ev(d["creada_en"], "recibida", s.cargadores.get(d["factura_id"], "sistema"))]
    ev.append(_ev(d["creada_en"], "decidida", "motor", d["motivo_corto"]))
    for ap in s.aprobaciones.values():
        if ap["decision_id"] == d["id"]:
            ev.append(_ev(ap["emitida_en"], _ACCION[ap["accion"]], ap["rol"], ap["nota"]))
    sucesora = next((x for x in s.decisiones.values() if x.get("reevaluacion_de") == d["id"]), None)
    if sucesora:
        ev.append(_ev(sucesora["creada_en"], "reevaluada", "motor"))
    return ev


def historial_de(s, d) -> list:
    previa = s.decisiones.get(d.get("reevaluacion_de"))
    return (historial_de(s, previa) if previa else []) + _propios(s, d)


def estado_orden(s, d):
    if d["estado"] != "autorizada":
        return None
    return "orden_simulada_emitida" if d["recibo_id"] in s.ordenes_emitidas else "autorizada"


def _detalle(s, d) -> tuple:
    """Proveedor e importe legibles (no el id de la factura) y la regla que decide, si falla alguna."""
    f = s.facturas.get(d["factura_id"]) or {}
    nombre = (f.get("emisor") or {}).get("nombre") or d["factura_id"]
    try:
        base = base_de(f, s.m)
    except (KeyError, FallaCerrada):
        base = None
    detalle = nombre if base is None else f"{nombre}, {importe(base, s.m)}"
    fallas = fallas_por_precedencia(d["reglas"])
    return detalle, f" ({fallas[0]['id']})" if fallas else ""


def actividad(s, limite: int = 5) -> list:
    todos = []
    for d in s.decisiones.values():
        for e in _propios(s, d):
            if e["evento"] in _TEXTO:
                detalle, regla = _detalle(s, d)
                texto = _TEXTO[e["evento"]].format(veredicto=_VEREDICTO.get(d["veredicto"], d["veredicto"]), detalle=detalle,
                                                   regla=regla, actor=e["actor"])
                todos.append({"hora": e["hora"], "texto": texto})
    return sorted(todos, key=lambda x: x["hora"])[::-1][:limite]
