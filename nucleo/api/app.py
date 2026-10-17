import base64
import importlib.util
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from ..dominio.mandato import RAIZ_CONTRATO
from ..dominio.servicio import ServicioDecision
from ..infra.firmador import verificar_firma

_ESTADOS = {"pendientes": {"pendiente"}, "pagadas": {"con_recibo", "autorizada"},
            "frenadas": {"frenada"}, "registradas": {"registrada"}}


def _cargar_validador():
    spec = importlib.util.spec_from_file_location("validar_contrato", RAIZ_CONTRATO / "validar.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validar


def _error(status, codigo, mensaje, detalle=None):
    return JSONResponse({"codigo": codigo, "mensaje": mensaje, "detalle": detalle}, status_code=status)


def _rutas_facturas(servicio, validar, esquema) -> APIRouter:
    r = APIRouter()

    @r.post("/api/facturas", status_code=201)
    def crear_factura(factura: dict):
        errores = validar(factura, esquema)
        if errores:
            return _error(422, "cuerpo_invalido", "La factura no cumple el esquema.", {"errores": errores[:10]})
        return servicio.decidir(factura)

    @r.get("/api/decisiones")
    def listar(estado: str = "todas"):
        ds = list(servicio.decisiones.values())
        if estado in _ESTADOS:
            ds = [d for d in ds if d["estado"] in _ESTADOS[estado]]
        return ds

    @r.get("/api/decisiones/{id}")
    def detalle(id: str):
        d = servicio.decisiones.get(id)
        if d is None:
            return _error(404, "no_encontrado", "La decision no existe.")
        return {"decision": d, "factura": servicio.facturas[d["factura_id"]]}

    return r


def _rutas_recibos(servicio, mandato_dict) -> APIRouter:
    r = APIRouter()

    @r.get("/api/mandato")
    def mandato():
        return mandato_dict

    @r.get("/api/recibos/{id}")
    def recibo(id: str):
        rec = servicio.recibos.get(id)
        return rec if rec else _error(404, "no_encontrado", "El recibo no existe.")

    @r.post("/api/recibos/{id}/verificar")
    def verificar(id: str):
        rec = servicio.recibos.get(id)
        if rec is None:
            return _error(404, "no_encontrado", "El recibo no existe.")
        return {"valida": verificar_firma(rec, servicio.firmador.clave_publica), "clave_version": rec["clave_version"]}

    @r.get("/api/clave-publica")
    def clave_publica():
        raw = servicio.firmador.clave_publica.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return {"clave_publica": base64.b64encode(raw).decode("ascii"), "clave_version": servicio.firmador.clave_version}

    return r


def crear_app(servicio: ServicioDecision, mandato_dict: dict) -> FastAPI:
    app = FastAPI(title="Nucleo")
    esquema = json.loads((RAIZ_CONTRATO / "factura-canonica.schema.json").read_text(encoding="utf-8"))
    app.include_router(_rutas_facturas(servicio, _cargar_validador(), esquema))
    app.include_router(_rutas_recibos(servicio, mandato_dict))
    return app
