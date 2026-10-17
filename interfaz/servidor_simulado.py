"""Servidor minimo para trabajar y probar la interfaz sin el nucleo: sirve dist/ y responde con los ejemplos del contrato."""
import copy
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
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


def crear_app() -> FastAPI:
    app = FastAPI(title="Servidor simulado de la interfaz")
    decisiones = {d["id"]: d for d in _decisiones()}
    facturas = {}

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
        return {"decision": decisiones[id], "factura": facturas.get(id) or _ejemplo("factura-canonica.f11.json")}

    @app.get("/api/recibos/{id}")
    def recibo(id: str):
        if not (id in decisiones and decisiones[id]["recibo_id"]):
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
    registrar_ola6(app, decisiones, _ejemplo("aprobacion.ejemplo.json"), _ejemplo("recibo.pagar.json"), _ejemplo("mandato.v2.json"))
    app.mount("/", StaticFiles(directory=RAIZ / "dist", html=True), name="dist")
    return app


app = crear_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
