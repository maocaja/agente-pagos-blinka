from .errores import FallaCerrada
from .guardian import ContextoGuardian, verificar
from .historial import actividad
from .motor import decidir
from .notificaciones import cargar_datos
from .operacion import anotar
from .recibo import emitir_recibo


class ServicioDecision:
    """Casos de uso del nucleo: decide, reserva, emite el recibo y autoriza ordenes. Todo se inyecta."""

    def __init__(self, mandato, registro, ids, nonce, reloj, firmador, requeridas=None, avisos=None, sesion_id="defecto"):
        self.m, self.reg, self.ids, self.nonce, self.reloj, self.firmador = mandato, registro, ids, nonce, reloj, firmador
        self.libro = registro.libro
        self.requeridas, self.avisos, self.sesion_id = requeridas, avisos, sesion_id
        self.evento_de = cargar_datos()["por_veredicto"]
        self.decisiones: dict = {}
        self.facturas: dict = {}
        self.recibos: dict = {}
        self.respuestas: dict = {}
        self.aprobaciones: dict = {}
        self.cargadores: dict = {}
        self.ordenes_emitidas: set = set()
        self.autorizadas: dict = {}

    def modo_de(self, pid) -> str:
        dias = self.reg.dias_de_alta(pid, self.reloj().date()) if pid else None
        niv = self.m.p["nivel_autonomia_defecto"]
        return niv["conocido"] if dias is not None and dias >= self.m.p["dias_proveedor_nuevo"] else niv["nuevo"]

    def ciclo(self) -> dict:
        ciclo_id, presupuesto = self.reg.ciclo_id, int(self.m.p["presupuesto_periodo_menor"])
        reservado = self.libro.acumulado(ciclo_id)
        return {"ciclo_id": ciclo_id, "empresa": self.reg.empresa or self.m.doc["empresa_id"],
                "moneda": self.m.p["moneda_base"], "presupuesto_menor": str(presupuesto),
                "reservado_menor": str(reservado), "disponible_menor": str(presupuesto - reservado),
                "actividad": actividad(self)}

    def idempotente(self, ambito, clave, producir):
        """Misma clave, misma respuesta: un reintento no duplica recibo ni reserva."""
        if clave is None:
            return producir()
        if (ambito, clave) not in self.respuestas:
            self.respuestas[(ambito, clave)] = producir()
        return self.respuestas[(ambito, clave)]

    def emitir(self, d, f, fallas_aprobadas=()) -> None:
        r = emitir_recibo(d, f, self.m, self.ids, self.nonce, self.reloj, self.firmador, fallas_aprobadas)
        try:
            self.libro.reservar(r["id"], r["nonce"], r["beneficiario_id"], f["ciclo_id"],
                                int(r["monto_base_menor"]), int(self.m.p["presupuesto_periodo_menor"]))
        except FallaCerrada as e:
            d.update(veredicto="ESCALAR", estado="pendiente", motivo_corto=str(e))
            return
        self.recibos[r["id"]] = r
        d["recibo_id"] = r["id"]

    def decidir(self, f) -> dict:
        d = decidir(f, self.m, self.reg, self.ids, self.reloj, self.modo_de(f["proveedor_asignado"]["proveedor_id"]),
                    requeridas=self.requeridas)
        if d["veredicto"] == "PAGAR":
            self.emitir(d, f)
        self.reg.registrar_factura(f, d["estado"])
        self.facturas[f["id"]] = f
        self.decisiones[d["id"]] = d
        anotar("decision", sesion=self.sesion_id, decision=d["id"], recibo=d["recibo_id"], veredicto=d["veredicto"], estado=d["estado"])
        if d["veredicto"] in self.evento_de:
            self.avisar(self.evento_de[d["veredicto"]], d)
        return d

    def asignar_sesion(self, sid) -> None:
        self.sesion_id = sid
        if self.avisos:
            self.avisos.sesion_id = sid

    def avisar(self, evento, d, **extra) -> None:
        if self.avisos:
            self.avisos.avisar(evento, self, d, **extra)

    def _decision_de(self, recibo_id):
        return next((x for x in self.decisiones.values() if x["recibo_id"] == recibo_id), None)

    def _hash_factura(self, factura_id):
        f = self.facturas.get(factura_id)
        return f["documento"]["hash"] if f else None

    def verificar_orden(self, orden, recibo, aprobacion=None) -> dict:
        ctx = ContextoGuardian(self.firmador.firma_valida, self._hash_factura, self.m.version, self.reloj(),
                               self.libro.consumir_nonce)
        res = verificar(orden, recibo, aprobacion, ctx)
        self._cerrar_orden(res, recibo)
        self._anotar_orden(res, recibo)
        return res

    def _anotar_orden(self, res, recibo) -> None:
        d = self._decision_de(recibo.get("id"))
        anotar("autorizacion" if res["autorizada"] else "denegacion", sesion=self.sesion_id,
               decision=(d or {}).get("id"), recibo=recibo.get("id"), autorizada=res["autorizada"])
        if res["autorizada"]:
            return self.avisar("autorizada", d)
        falla = next((v["nombre"] for v in res["verificaciones"] if v["estado"] == "falla"), "")
        self.avisar("denegacion_guardian", d, falla=falla)

    def _cerrar_orden(self, res, recibo) -> None:
        """Autorizada o Denegada. Solo un recibo genuino (verificaciones 1 a 3 en ok) libera su reserva."""
        d = self._decision_de(recibo.get("id"))
        n = next((v["n"] for v in res["verificaciones"] if v["estado"] == "falla"), None)
        if d is None or d["estado"] != "con_recibo":
            return
        if res["autorizada"]:
            d["estado"] = "autorizada"
            self.autorizadas[d["id"]] = self.reloj().strftime("%Y-%m-%dT%H:%M:%SZ")
        elif n in (4, 5):
            self.libro.liberar(recibo["id"])
            d["estado"] = "denegada"
