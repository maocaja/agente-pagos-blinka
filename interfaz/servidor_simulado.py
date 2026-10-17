"""Servidor minimo para trabajar y probar la interfaz sin el nucleo: sirve dist/ y responde con los ejemplos del contrato."""
import copy
import json
from pathlib import Path

from datetime import datetime, timezone

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from rutas_ola4 import registrar_ola4
from rutas_ola6 import registrar_ola6

RAIZ = Path(__file__).resolve().parent
EJEMPLOS = RAIZ.parent / "contrato" / "ejemplos"


def _ejemplo(nombre: str) -> dict:
    return json.loads((EJEMPLOS / nombre).read_text(encoding="utf-8"))


def _variante(base: dict, id_: str, veredicto: str, motivo: str, **extra) -> dict:
    d = copy.deepcopy(base)
    d.update(id=id_, veredicto=veredicto, motivo_corto=motivo, explicacion=motivo, que_hacer=None, **extra)
    return d


def _decisiones() -> list[dict]:
    base = _ejemplo("decision.f11.json")
    pagar = _variante(base, "dec_01", "PAGAR", "Cumple todas las reglas.", factura_id="f_01", estado="con_recibo", recibo_id="rec_01")
    frenar = _variante(base, "dec_02", "FRENAR", "El proveedor no esta en el registro.", factura_id="f_02", estado="frenada", sin_orden=True)
    frenar["que_hacer"] = "Pedir al proveedor que se registre antes de volver a enviar la factura."
    base = dict(base, explicacion="La cuenta de la factura (CO) no es la registrada (BR); no se paga sin que una persona lo confirme.",
                que_hacer="Confirmar la cuenta con el proveedor por un canal conocido y luego aprobar o rechazar.")
    return [base, pagar, frenar]


def _guardian(recibo: dict) -> dict:
    original = _ejemplo("recibo.pagar.json")
    rechazo = _ejemplo("guardian.rechazo.json")
    if recibo != original:
        return rechazo
    nombres = [v["nombre"] for v in rechazo["verificaciones"]]
    return {"autorizada": True, "motivo": None,
            "verificaciones": [{"n": i + 1, "nombre": n, "estado": "ok", "motivo": None} for i, n in enumerate(nombres)]}


def _historial(d: dict, resoluciones: dict) -> list[dict]:
    base = [{"hora": d["creada_en"], "evento": "Recibida", "actor": "Sistema", "nota": ""},
            {"hora": d["creada_en"], "evento": f"Decidida por el motor: {d['veredicto']}", "actor": "Motor de reglas", "nota": d["motivo_corto"]}]
    return base + resoluciones.get(d["id"], []) + ([{"hora": d["creada_en"], "evento": "Recibo emitido", "actor": "Sistema", "nota": ""}] if d.get("recibo_id") else [])


def _estado_orden(d: dict, autorizadas: set):
    return "autorizada" if d["id"] in autorizadas else None


def _rutas_ciclo(app, decisiones, facturas, resoluciones):
    @app.get("/api/ciclo")
    def ciclo():
        total = lambda i: int((facturas.get(i) or _ejemplo("factura-canonica.f11.json"))["montos"]["total_menor"])
        reservado = sum(total(i) for i, d in decisiones.items() if d.get("recibo_id"))
        eventos = [dict(e, id=i) for i, d in decisiones.items() for e in _historial(d, resoluciones)]
        recientes = sorted(eventos, key=lambda e: e["hora"], reverse=True)[:6]
        return {"ciclo_id": "2026-10", "empresa": "Empresa de demostracion SA", "moneda": "BRL", "presupuesto_menor": "5000000",
                "reservado_menor": str(reservado), "disponible_menor": str(5000000 - reservado),
                "actividad": [{"hora": e["hora"], "texto": f"{e['evento']} ({e['id']})"} for e in recientes]}


def _rutas_notificaciones(app, decisiones):
    pruebas = []
    eventos = {"ESCALAR": ("escalada pendiente", "Escalada pendiente de aprobacion."), "FRENAR": ("factura frenada", "Factura frenada por las reglas.")}

    def entrada(evento, canal, texto, hora):
        return {"hora": hora, "evento": evento, "canal": canal, "destino": "***" + canal[:3], "estado": "simulada", "texto": texto}

    @app.get("/api/notificaciones")
    def notificaciones():
        base = [entrada(eventos[d["veredicto"]][0], c, f"{eventos[d['veredicto']][1]} {d['id']}", d["creada_en"])
                for d in decisiones.values() if d["veredicto"] in eventos for c in ("correo", "telegram")]
        return sorted(base + pruebas, key=lambda e: e["hora"], reverse=True)

    @app.post("/api/notificaciones/prueba")
    def prueba(x_rol: str = Header("analista")):
        if x_rol not in ("analista", "cfo"):
            return JSONResponse({"codigo": "rol_no_permitido", "mensaje": "Rol no permitido.", "detalle": None}, status_code=403)
        e = entrada("prueba", "telegram", "Prueba: el sistema esta vivo.", datetime.now(timezone.utc).isoformat())
        pruebas.append(e)
        return e

    @app.get("/api/salud")
    def salud():
        return {"estado": "operativo", "version": "1.1.0-rc6", "mandato": "v2", "lectura": "guardada",
                "libro": "ok", "notificaciones": {"telegram": "simulado", "correo": "simulado"}}


def crear_app() -> FastAPI:
    app = FastAPI(title="Servidor simulado de la interfaz")
    decisiones = {d["id"]: d for d in _decisiones()}
    facturas = {}
    resoluciones = {}
    autorizadas = set()

    @app.post("/api/sesion", status_code=201)
    def sesion():
        return {"sesion_id": "s_01", "clave_publica": "base64...", "clave_version": "k1", "mandato_version": "v2", "ciclo_id": "2026-10", "lectura": "guardada"}

    @app.get("/api/decisiones")
    def listar(estado: str = "todas"):
        return list(decisiones.values())

    @app.get("/api/decisiones/{id}")
    def detalle(id: str):
        if id not in decisiones:
            raise HTTPException(404, "Decision no encontrada")
        return {"decision": decisiones[id], "factura": facturas.get(id) or _ejemplo("factura-canonica.f11.json"),
                "historial": _historial(decisiones[id], resoluciones), "estado_orden": _estado_orden(decisiones[id], autorizadas)}

    @app.post("/api/decisiones/{id}/autorizar")
    def autorizar(id: str):
        d = decisiones.get(id)
        if d is None:
            raise HTTPException(404, "Decision no encontrada")
        if not d.get("recibo_id"):
            return JSONResponse({"codigo": "conflicto", "mensaje": "La decision no tiene recibo que autorizar.", "detalle": None}, status_code=409)
        autorizadas.add(id)
        return _guardian(_ejemplo("recibo.pagar.json"))

    @app.get("/api/recibos/{id}")
    def recibo(id: str):
        if not any(d["recibo_id"] == id for d in decisiones.values()):
            raise HTTPException(404, "Recibo no encontrado")
        return _ejemplo("recibo.pagar.json")

    @app.post("/api/recibos/{id}/verificar")
    def verificar(id: str):
        return {"valida": True, "clave_version": "k1"}

    @app.post("/api/guardian/verificar")
    def guardian(cuerpo: dict):
        return _guardian(cuerpo.get("recibo", {}))

    registrar_ola4(app, decisiones, facturas, _ejemplo("decision.f11.json"), _ejemplo("factura-canonica.f11.json"),
                   _ejemplo("mandato.v2.json"))
    registrar_ola6(app, decisiones, _ejemplo("aprobacion.ejemplo.json"), _ejemplo("recibo.pagar.json"), _ejemplo("mandato.v2.json"), resoluciones)
    _rutas_ciclo(app, decisiones, facturas, resoluciones)
    _rutas_notificaciones(app, decisiones)
    app.mount("/", StaticFiles(directory=RAIZ / "dist", html=True), name="dist")
    return app


app = crear_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
