import base64
from datetime import timedelta

from .errores import ErrorAccion
from .motor import decidir
from .recibo import orden_desde_recibo, serializar

# Capacidades por rol: el servidor valida aunque la interfaz oculte el boton.
CAPACIDADES = {"aprobar": {"cfo"}, "rechazar": {"cfo"}, "autorizar": {"analista", "cfo"}}
_FMT = "%Y-%m-%dT%H:%M:%SZ"


def _fallas(d) -> list:
    return [r for r in d["reglas"] if r["estado"] == "falla"]


def _autorizar(s, accion, rol, factura_id):
    if rol not in CAPACIDADES[accion]:
        raise ErrorAccion(403, "rol_no_permitido", f"El rol {rol or 'sin rol'} no puede {accion}.")
    if s.cargadores.get(factura_id) == rol:
        raise ErrorAccion(403, "rol_no_permitido", "Quien cargo la factura no la aprueba ni la rechaza.")


def _pendiente(s, id_) -> dict:
    d = s.decisiones.get(id_)
    if d is None:
        raise ErrorAccion(404, "no_encontrado", "La decision no existe.")
    if d["estado"] != "pendiente":
        raise ErrorAccion(409, "conflicto", f"La decision esta {d['estado']}, no pendiente.")
    return d


def _aprobacion(s, accion, decision_id, recibo_id, rol, nota, ids_fallas) -> dict:
    ahora = s.reloj()
    ap = {"id": s.ids("apr"), "decision_id": decision_id, "recibo_id": recibo_id, "accion": accion, "rol": rol,
          "usuario_simulado": True, "nota": nota, "fallas_cubiertas": ids_fallas,
          "emitida_en": ahora.strftime(_FMT),
          "vence_en": (ahora + timedelta(hours=s.m.p["vigencia_recibo_h"])).strftime(_FMT)}
    ap["firma"] = base64.b64encode(s.firmador.firmar(serializar(ap))).decode("ascii")
    s.aprobaciones[ap["id"]] = ap
    return ap


def _reevaluar(s, previa) -> dict:
    f = s.facturas[previa["factura_id"]]
    nueva = decidir(f, s.m, s.reg, s.ids, s.reloj, s.modo_de(f["proveedor_asignado"]["proveedor_id"]),
                    requeridas=s.requeridas)
    nueva["reevaluacion_de"] = previa["id"]
    fallas = _fallas(nueva)
    if nueva["veredicto"] != "ESCALAR" or not nueva["reglas"] or any(not r["aprobable"] for r in fallas):
        raise ErrorAccion(409, "no_aprobable", nueva["motivo_corto"],
                          {"reglas": [r["id"] for r in fallas if not r["aprobable"]]})
    nuevas = {r["id"] for r in fallas} - {r["id"] for r in _fallas(previa)}
    if nuevas:
        raise ErrorAccion(409, "reevaluacion_distinta", "La reevaluacion trae fallas que la persona no vio.",
                          {"reglas": sorted(nuevas)})
    return nueva


def aprobar(s, decision_id, rol, nota) -> dict:
    d = _pendiente(s, decision_id)
    _autorizar(s, "aprobar", rol, d["factura_id"])
    nueva = _reevaluar(s, d)
    ids_fallas = [r["id"] for r in _fallas(nueva)]
    s.emitir(nueva, s.facturas[d["factura_id"]], ids_fallas)
    if nueva["recibo_id"] is None:
        raise ErrorAccion(409, "no_aprobable", nueva["motivo_corto"])
    nueva["estado"], d["estado"] = "con_recibo", "reevaluada"
    s.decisiones[nueva["id"]] = nueva
    return {"decision": nueva, "aprobacion": _aprobacion(s, "aprobar", nueva["id"], nueva["recibo_id"], rol, nota, ids_fallas)}


def rechazar(s, decision_id, rol, nota) -> dict:
    d = _pendiente(s, decision_id)
    _autorizar(s, "rechazar", rol, d["factura_id"])
    if not nota or not nota.strip():
        raise ErrorAccion(422, "cuerpo_invalido", "La nota es obligatoria al rechazar.")
    d["estado"] = "rechazada"
    _aprobacion(s, "rechazar", d["id"], None, rol, nota, [r["id"] for r in _fallas(d)])
    return d


def autorizar(s, decision_id, rol, nota="") -> dict:
    """Pide al guardian la orden de una decision con recibo; no replica sus verificaciones."""
    d = s.decisiones.get(decision_id)
    if d is None:
        raise ErrorAccion(404, "no_encontrado", "La decision no existe.")
    if rol not in CAPACIDADES["autorizar"]:
        raise ErrorAccion(403, "rol_no_permitido", f"El rol {rol or 'sin rol'} no puede autorizar.")
    if d["estado"] != "con_recibo" or d["veredicto"] == "FRENAR":
        raise ErrorAccion(409, "conflicto", f"La decision esta {d['estado']} ({d['veredicto']}): no es autorizable.")
    recibo = s.recibos[d["recibo_id"]]
    aprobacion = next((a for a in s.aprobaciones.values() if a["recibo_id"] == recibo["id"] and a["accion"] == "aprobar"), None)
    return s.verificar_orden(orden_desde_recibo(recibo), recibo, aprobacion)
