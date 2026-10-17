"""Rutas simuladas de la Ola 6 (aprobar, rechazar, vista previa del mandato, auditoria), con datos del contrato."""
import copy

from fastapi import Body, FastAPI, Header
from fastapi.responses import JSONResponse, Response

PAIN001 = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<Document><!-- SIMULADA: no mueve dinero -->'
    "<CstmrCdtTrfInitn><PmtInf><CdtTrfTxInf><Amt><InstdAmt Ccy=\"{moneda}\">{monto}</InstdAmt></Amt>"
    "<RmtInf><Ustrd>SIMULADA {recibo}</Ustrd></RmtInf></CdtTrfTxInf></PmtInf></CstmrCdtTrfInitn></Document>"
)


def _error(estado: int, codigo: str, mensaje: str) -> JSONResponse:
    return JSONResponse({"codigo": codigo, "mensaje": mensaje, "detalle": None}, status_code=estado)


def _cfo_sobre_escalada(decisiones: dict, id: str, rol: str):
    if rol != "cfo":
        return _error(403, "rol_no_permitido", "Solo el CFO puede aprobar o rechazar.")
    d = decisiones.get(id)
    if d is None:
        return _error(404, "no_encontrado", "Decision no encontrada")
    if d["veredicto"] != "ESCALAR" or d["estado"] != "pendiente":
        return _error(409, "estado_cambio", "La decision ya no esta pendiente de aprobacion.")
    return None


def _rutas_decidir(app, decisiones, base_aprobacion):
    @app.post("/api/decisiones/{id}/aprobar")
    def aprobar(id: str, cuerpo: dict = Body(default_factory=dict), x_rol: str = Header(default="analista")):
        if (fallo := _cfo_sobre_escalada(decisiones, id, x_rol)):
            return fallo
        previa = decisiones[id]
        previa["estado"] = "reevaluada"
        nueva = copy.deepcopy(previa)
        nueva.update(id=id + "_r", veredicto="PAGAR", estado="con_recibo", recibo_id="rec_01", reevaluacion_de=id,
                     motivo_corto="Aprobada por el CFO; cumple al reevaluar.",
                     explicacion="El CFO aprobo la falla y al reevaluar cumple todas las reglas.", que_hacer=None)
        decisiones[nueva["id"]] = nueva
        aprobacion = dict(base_aprobacion, decision_id=id, nota=cuerpo.get("nota") or "Aprobada.")
        return {"decision": nueva, "aprobacion": aprobacion}

    @app.post("/api/decisiones/{id}/rechazar")
    def rechazar(id: str, cuerpo: dict = Body(default_factory=dict), x_rol: str = Header(default="analista")):
        if (fallo := _cfo_sobre_escalada(decisiones, id, x_rol)):
            return fallo
        if not (cuerpo.get("nota") or "").strip():
            return _error(422, "invalido", "La nota es obligatoria al rechazar.")
        decisiones[id].update(estado="rechazada", que_hacer=None)
        return decisiones[id]


def _veredicto_nuevo(d: dict, parametros: dict, vigente: dict) -> str:
    umbral = parametros.get("umbral_aprobacion_menor")
    sube = umbral is not None and int(umbral) > int(vigente["umbral_aprobacion_menor"])
    return "PAGAR" if d["veredicto"] == "ESCALAR" and sube else d["veredicto"]


def _rutas_mandato(app, decisiones, mandato):
    @app.post("/api/mandato/previa")
    def previa(cuerpo: dict = Body(default_factory=dict)):
        parametros = cuerpo.get("parametros")
        desconocidos = [k for k in (parametros or {}) if k not in mandato["parametros"]]
        if not parametros or desconocidos or not all(str(v).isdigit() for v in parametros.values() if not isinstance(v, (dict, list))):
            return _error(422, "invalido", "Parametros no validos para la vista previa.")
        vigente = mandato["parametros"]
        cambios = [{"factura_id": d["factura_id"], "antes": d["veredicto"], "despues": nuevo,
                    "explicacion": "Con el umbral nuevo la factura queda dentro de lo que se paga sin aprobacion."}
                   for d in decisiones.values() if (nuevo := _veredicto_nuevo(d, parametros, vigente)) != d["veredicto"]]
        return {"mandato_vigente": mandato["version"], "evaluadas": len(decisiones), "cambian": len(cambios), "cambios": cambios}


def _rutas_auditoria(app, recibo, mandato):
    @app.get("/api/auditoria/paquete")
    def paquete():
        cuerpo = {"formato": "paquete-auditoria-1", "generado_en": "2026-10-17T12:00:00Z", "clave_publica": "base64...",
                  "clave_version": recibo["clave_version"], "recibos": [recibo], "mandatos": {mandato["version"]: mandato}}
        return JSONResponse(cuerpo, headers={"Content-Disposition": 'attachment; filename="paquete-auditoria.json"'})

    @app.get("/api/ordenes/{id}/pain001")
    def pain001(id: str):
        if id != recibo["id"]:
            return _error(404, "no_encontrado", "Orden no encontrada")
        xml = PAIN001.format(moneda=recibo["moneda"], monto=recibo["monto_menor"], recibo=id)
        return Response(xml, media_type="application/xml", headers={"Content-Disposition": f'attachment; filename="{id}-pain001.xml"'})


def registrar_ola6(app: FastAPI, decisiones: dict, base_aprobacion: dict, recibo: dict, mandato: dict):
    _rutas_decidir(app, decisiones, base_aprobacion)
    _rutas_mandato(app, decisiones, mandato)
    _rutas_auditoria(app, recibo, mandato)
