"""Servidor minimo para trabajar y probar la interfaz sin el nucleo: sirve dist/ y responde con los ejemplos del contrato."""
import copy
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

RAIZ = Path(__file__).resolve().parent
EJEMPLOS = RAIZ.parent / "contrato" / "ejemplos"


def _ejemplo(nombre: str) -> dict:
    return json.loads((EJEMPLOS / nombre).read_text(encoding="utf-8"))


def _variante(base: dict, id_: str, veredicto: str, motivo: str, **extra) -> dict:
    d = copy.deepcopy(base)
    d.update(id=id_, veredicto=veredicto, motivo_corto=motivo, **extra)
    return d


def _decisiones() -> list[dict]:
    base = _ejemplo("decision.f11.json")
    pagar = _variante(base, "dec_01", "PAGAR", "Cumple todas las reglas.", factura_id="f_01", estado="con_recibo", recibo_id="rec_01")
    frenar = _variante(base, "dec_02", "FRENAR", "El proveedor no esta en el registro.", factura_id="f_02", estado="frenada", sin_orden=True)
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

    @app.post("/api/sesion", status_code=201)
    def sesion():
        return {"sesion_id": "s_01", "clave_publica": "base64...", "clave_version": "k1", "mandato_version": "v2", "ciclo_id": "2026-10"}

    @app.get("/api/decisiones")
    def listar(estado: str = "todas"):
        return list(decisiones.values())

    @app.get("/api/decisiones/{id}")
    def detalle(id: str):
        if id not in decisiones:
            raise HTTPException(404, "Decision no encontrada")
        return {"decision": decisiones[id], "factura": _ejemplo("factura-canonica.f11.json")}

    @app.get("/api/recibos/{id}")
    def recibo(id: str):
        if id != "dec_01":
            raise HTTPException(404, "Recibo no encontrado")
        return _ejemplo("recibo.pagar.json")

    @app.post("/api/recibos/{id}/verificar")
    def verificar(id: str):
        return {"valida": True, "clave_version": "k1"}

    @app.post("/api/guardian/verificar")
    def guardian(cuerpo: dict):
        return _guardian(cuerpo.get("recibo", {}))

    app.mount("/", StaticFiles(directory=RAIZ / "dist", html=True), name="dist")
    return app


app = crear_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
