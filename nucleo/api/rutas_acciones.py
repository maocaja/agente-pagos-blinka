import json
from pathlib import Path

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse

from ..dominio import aprobacion
from ..dominio.errores import ErrorAccion


def _responder(e: ErrorAccion):
    return JSONResponse({"codigo": e.codigo, "mensaje": e.mensaje, "detalle": e.detalle}, status_code=e.status)


def _accion(servicio, nombre, id_, cuerpo, rol, clave):
    """Idempotente solo en exito: un error no se guarda y el reintento reevalua."""
    llave = (f"{nombre}:{id_}", clave)
    if clave is not None and llave in servicio.respuestas:
        return servicio.respuestas[llave]
    try:
        r = getattr(aprobacion, nombre)(servicio, id_, rol, cuerpo.get("nota", ""))
    except ErrorAccion as e:
        return _responder(e)
    if clave is not None:
        servicio.respuestas[llave] = r
    return r


def _leer_resultados(ruta: Path | None):
    try:
        return json.loads(ruta.read_text(encoding="utf-8")) if ruta and ruta.is_file() else None
    except (OSError, ValueError):
        return None


def _pct(parte, total) -> str:
    return f"{round(100 * parte / total)}%" if total else "0%"


def _marcador(ds, res) -> dict:
    """Esquema del contrato; lo que la sesion y el resultado guardado no dan va en null, 0 o 0/0."""
    rec = (res or {}).get("recuentos", {})
    lanzadas = rec.get("lanzadas", len(ds))
    ok = sum(1 for c in (res or {}).get("casos", []) if c.get("clase") == "verificada")
    autonomas = sum(1 for d in ds if d["veredicto"] == "PAGAR" and d["modo_autonomia"] == "autonomo")
    return {"casos": lanzadas, "verificados": rec.get("verificadas", 0),
            "pagos_indebidos": rec.get("pagos_indebidos"), "frenadas_escalables": rec.get("frenadas_escalables"),
            "desvios_conservadores": rec.get("desvios_conservadores"),
            "aciertos_reglas": "0/0", "aciertos_extremo_a_extremo": f"{ok}/{lanzadas}" if res else "0/0",
            "autonomia": _pct(autonomas, len(ds)), "escalada_innecesaria": "0%",
            "pendientes": sum(1 for d in ds if d["estado"] == "pendiente"),
            "costo": {"lecturas_guardadas_microusd": "0", "sesion_microusd": "0"}}


def rutas_acciones(dep, ruta_resultados: Path | None) -> APIRouter:
    r = APIRouter()

    @r.post("/api/decisiones/{id}/aprobar")
    def aprobar(id: str, cuerpo: dict, servicio=Depends(dep), x_rol: str | None = Header(None),
                idempotency_key: str | None = Header(None)):
        return _accion(servicio, "aprobar", id, cuerpo, x_rol, idempotency_key)

    @r.post("/api/decisiones/{id}/rechazar")
    def rechazar(id: str, cuerpo: dict, servicio=Depends(dep), x_rol: str | None = Header(None),
                 idempotency_key: str | None = Header(None)):
        return _accion(servicio, "rechazar", id, cuerpo, x_rol, idempotency_key)

    @r.post("/api/decisiones/{id}/autorizar")
    def autorizar(id: str, servicio=Depends(dep), x_rol: str | None = Header(None),
                  idempotency_key: str | None = Header(None)):
        return _accion(servicio, "autorizar", id, {}, x_rol, idempotency_key)

    @r.get("/api/marcador")
    def marcador(servicio=Depends(dep)):
        return _marcador(list(servicio.decisiones.values()), _leer_resultados(ruta_resultados))

    return r
