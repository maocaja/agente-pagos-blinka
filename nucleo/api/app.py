import base64
import importlib.util
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from fastapi import APIRouter, Depends, FastAPI, Header, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from ..dominio.mandato import RAIZ_CONTRATO
from .rutas_acciones import rutas_acciones
from .rutas_evaluacion import rutas_evaluacion
from .rutas_informes import rutas_informes
from .rutas_muestras import rutas_muestras
from .sesiones import Sesiones

_ESTADOS = {"pendientes": {"pendiente"}, "pagadas": {"con_recibo", "autorizada"},
            "frenadas": {"frenada"}, "registradas": {"registrada"}}


class SesionInvalida(Exception):
    pass


def _cargar_validador():
    spec = importlib.util.spec_from_file_location("validar_contrato", RAIZ_CONTRATO / "validar.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validar


def _error(status, codigo, mensaje, detalle=None):
    return JSONResponse({"codigo": codigo, "mensaje": mensaje, "detalle": detalle}, status_code=status)


def _clave_publica(servicio) -> dict:
    raw = servicio.firmador.clave_publica.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return {"clave_publica": base64.b64encode(raw).decode("ascii"), "clave_version": servicio.firmador.clave_version}


def _rutas_sesion(sesiones: Sesiones) -> APIRouter:
    r = APIRouter()

    @r.post("/api/sesion", status_code=201)
    def crear(mandato: str = "v2"):
        if mandato not in ("v1", "v2"):
            return _error(422, "cuerpo_invalido", "El mandato debe ser v1 o v2.")
        sid = sesiones.crear(mandato)
        s = sesiones.obtener(sid)
        return {"sesion_id": sid, **_clave_publica(s), "mandato_version": s.m.version,
                "ciclo_id": s.reg.ciclo_id, "lectura": "en_vivo" if os.environ.get("ANTHROPIC_API_KEY") else "guardada"}

    @r.post("/api/sesion/reiniciar")
    def reiniciar(x_sesion_id: str | None = Header(None)):
        if not sesiones.reiniciar(x_sesion_id):
            raise SesionInvalida()
        return {"reiniciada": True}

    return r


def _procesar_factura(validar, esquema):
    def procesar(servicio, factura, clave, rol):
        errores = validar(factura, esquema)
        if errores:
            return _error(422, "cuerpo_invalido", "La factura no cumple el esquema.", {"errores": errores[:10]})
        servicio.cargadores.setdefault(factura["id"], rol or "sistema")
        return servicio.idempotente("decision", clave, lambda: servicio.decidir(factura))
    return procesar


def _rutas_facturas(procesar, dep) -> APIRouter:
    r = APIRouter()

    @r.post("/api/facturas", status_code=201)
    def crear_factura(factura: dict, servicio=Depends(dep), idempotency_key: str | None = Header(None),
                      x_rol: str | None = Header(None)):
        return procesar(servicio, factura, idempotency_key, x_rol)

    @r.get("/api/decisiones")
    def listar(estado: str = "todas", servicio=Depends(dep)):
        ds = list(servicio.decisiones.values())
        if estado in _ESTADOS:
            ds = [d for d in ds if d["estado"] in _ESTADOS[estado]]
        return ds

    @r.get("/api/decisiones/{id}")
    def detalle(id: str, servicio=Depends(dep)):
        d = servicio.decisiones.get(id)
        if d is None:
            return _error(404, "no_encontrado", "La decision no existe.")
        return {"decision": d, "factura": servicio.facturas[d["factura_id"]]}

    return r


def _rutas_recibos(dep) -> APIRouter:
    r = APIRouter()

    @r.get("/api/mandato")
    def mandato(servicio=Depends(dep)):
        return servicio.m.doc

    @r.get("/api/proveedores")
    def proveedores(servicio=Depends(dep)):
        return [{"id": p["id"], "nombre": p["nombre"], "estado": p["estado"], "nivel_autonomia": servicio.modo_de(p["id"])}
                for p in servicio.reg.proveedores()]

    @r.get("/api/recibos/{id}")
    def recibo(id: str, servicio=Depends(dep)):
        rec = servicio.recibos.get(id)
        return rec if rec else _error(404, "no_encontrado", "El recibo no existe.")

    @r.post("/api/recibos/{id}/verificar")
    def verificar(id: str, servicio=Depends(dep)):
        rec = servicio.recibos.get(id)
        if rec is None:
            return _error(404, "no_encontrado", "El recibo no existe.")
        return {"valida": servicio.firmador.firma_valida(rec), "clave_version": rec["clave_version"]}

    @r.get("/api/clave-publica")
    def clave_publica(servicio=Depends(dep)):
        return _clave_publica(servicio)

    @r.post("/api/guardian/verificar")
    def guardian(cuerpo: dict, servicio=Depends(dep), idempotency_key: str | None = Header(None)):
        if not isinstance(cuerpo.get("orden"), dict) or not isinstance(cuerpo.get("recibo"), dict):
            return _error(422, "cuerpo_invalido", "Se exigen orden y recibo.")
        return servicio.idempotente("guardian", idempotency_key, lambda: servicio.verificar_orden(
            cuerpo["orden"], cuerpo["recibo"], cuerpo.get("aprobacion")))

    return r


RESULTADOS_SET = RAIZ_CONTRATO.parent / "evaluacion" / "salida" / "resultados-set.json"
INTERFAZ_DIST = RAIZ_CONTRATO.parent / "interfaz" / "dist"


def crear_app(sesiones: Sesiones, ruta_resultados: Path = RESULTADOS_SET, ruta_interfaz: Path = INTERFAZ_DIST) -> FastAPI:
    app = FastAPI(title="Nucleo")
    esquema = json.loads((RAIZ_CONTRATO / "factura-canonica.schema.json").read_text(encoding="utf-8"))

    def servicio_de(x_sesion_id: str | None = Header(None)):
        s = sesiones.obtener(x_sesion_id)
        if s is None:
            raise SesionInvalida()
        return s

    @app.exception_handler(SesionInvalida)
    def _sesion_invalida(request: Request, exc: SesionInvalida):
        return _error(401, "sesion_invalida", "La sesion no existe o vencio.")

    app.include_router(_rutas_sesion(sesiones))
    procesar = _procesar_factura(_cargar_validador(), esquema)
    app.include_router(_rutas_facturas(procesar, servicio_de))
    app.include_router(rutas_muestras(servicio_de, procesar))
    app.include_router(_rutas_recibos(servicio_de))
    app.include_router(rutas_acciones(servicio_de, ruta_resultados))
    app.include_router(rutas_informes(servicio_de, _clave_publica))
    app.include_router(rutas_evaluacion(ruta_resultados.parent))
    if ruta_interfaz.is_dir():
        app.mount("/", StaticFiles(directory=ruta_interfaz, html=True), name="interfaz")  # al final: /api manda
    return app
