from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from ..dominio.auditoria import armar_paquete
from ..dominio.errores import ErrorAccion
from ..dominio.pain001 import orden_a_pain001
from ..dominio.previa import previa_de_mandato
from ..dominio.recibo import orden_desde_recibo

_FMT = "%Y-%m-%dT%H:%M:%SZ"


def _error(e: ErrorAccion):
    return JSONResponse({"codigo": e.codigo, "mensaje": e.mensaje, "detalle": e.detalle}, status_code=e.status)


def _orden_autorizada(s, id_):
    rec = s.recibos.get(id_)
    d = next((x for x in s.decisiones.values() if x["recibo_id"] == id_), None)
    if rec is None or d is None:
        raise ErrorAccion(404, "no_encontrado", "La orden no existe.")
    if d["estado"] != "autorizada":
        raise ErrorAccion(409, "conflicto", "La orden no esta autorizada por el guardian.")
    return rec


def rutas_informes(dep, clave_publica) -> APIRouter:
    r = APIRouter()

    @r.post("/api/mandato/previa")
    def previa(cuerpo: dict, servicio=Depends(dep)):
        try:
            return previa_de_mandato(servicio, cuerpo.get("parametros"))
        except ErrorAccion as e:
            return _error(e)

    @r.get("/api/auditoria/paquete")
    def paquete(servicio=Depends(dep)):
        return armar_paquete(servicio, clave_publica(servicio), servicio.reloj().strftime(_FMT))

    @r.get("/api/ordenes/{id}/pain001")
    def pain001(id: str, servicio=Depends(dep)):
        try:
            rec = _orden_autorizada(servicio, id)
        except ErrorAccion as e:
            return _error(e)
        prov = servicio.reg.proveedor(rec["beneficiario_id"])
        xml = orden_a_pain001(orden_desde_recibo(rec), prov["nombre"] if prov else rec["beneficiario_id"],
                              servicio.reloj().strftime(_FMT))
        return Response(xml, media_type="application/xml")

    return r
