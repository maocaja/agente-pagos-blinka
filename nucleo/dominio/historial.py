"""Historial y actividad derivados de lo ya registrado en la sesion; no se inventan eventos."""

_ACCION = {"aprobar": "aprobada", "rechazar": "rechazada"}
_TEXTO = {"decidida": "Decision {veredicto} para la factura {factura}",
          "aprobada": "Aprobada por {actor}: factura {factura}",
          "rechazada": "Rechazada por {actor}: factura {factura}"}


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


def actividad(s, limite: int = 5) -> list:
    todos = []
    for d in s.decisiones.values():
        for e in _propios(s, d):
            if e["evento"] in _TEXTO:
                texto = _TEXTO[e["evento"]].format(veredicto=d["veredicto"], factura=d["factura_id"], actor=e["actor"])
                todos.append({"hora": e["hora"], "texto": texto})
    return sorted(todos, key=lambda x: x["hora"])[::-1][:limite]
