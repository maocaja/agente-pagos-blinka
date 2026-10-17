import os

from fastapi import APIRouter, Depends, Header

from ..dominio.aprobacion import CAPACIDADES
from ..dominio.errores import ErrorAccion
from .rutas_acciones import _responder

VERSION_API = "1.1.0-rc6"


def lectura_actual() -> str:
    return "en_vivo" if os.environ.get("ANTHROPIC_API_KEY") else "guardada"


def _libro_responde(s) -> str:
    try:
        s.libro.acumulado(s.reg.ciclo_id)
        return "ok"
    except Exception:  # la salud informa el fallo, no lo propaga
        return "falla"


def rutas_notificaciones(dep) -> APIRouter:
    r = APIRouter()

    @r.get("/api/notificaciones")
    def bandeja(servicio=Depends(dep)):
        return list(servicio.avisos.bandeja) if servicio.avisos else []

    @r.post("/api/notificaciones/prueba")
    def prueba(servicio=Depends(dep), x_rol: str | None = Header(None)):
        try:
            if x_rol not in CAPACIDADES["probar_aviso"]:
                raise ErrorAccion(403, "rol_no_permitido", f"El rol {x_rol or 'sin rol'} no puede probar los avisos.")
            return servicio.avisos.prueba()
        except ErrorAccion as e:
            return _responder(e)

    @r.get("/api/salud")
    def salud(servicio=Depends(dep)):
        libro = _libro_responde(servicio)
        canales = servicio.avisos.estado_canales() if servicio.avisos else {"telegram": "simulado", "correo": "simulado"}
        return {"estado": "ok" if libro == "ok" else "degradado", "version": VERSION_API, "mandato": servicio.m.version,
                "lectura": lectura_actual(), "libro": libro, "notificaciones": canales}

    return r
