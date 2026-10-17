from .errores import FallaCerrada
from .guardian import ContextoGuardian, verificar
from .motor import decidir
from .recibo import emitir_recibo


class ServicioDecision:
    """Casos de uso del nucleo: decide, reserva, emite el recibo y autoriza ordenes. Todo se inyecta."""

    def __init__(self, mandato, registro, ids, nonce, reloj, firmador, requeridas=None):
        self.m, self.reg, self.ids, self.nonce, self.reloj, self.firmador = mandato, registro, ids, nonce, reloj, firmador
        self.libro = registro.libro
        self.requeridas = requeridas
        self.decisiones: dict = {}
        self.facturas: dict = {}
        self.recibos: dict = {}
        self.respuestas: dict = {}

    def modo_de(self, pid) -> str:
        dias = self.reg.dias_de_alta(pid, self.reloj().date()) if pid else None
        niv = self.m.p["nivel_autonomia_defecto"]
        return niv["conocido"] if dias is not None and dias >= self.m.p["dias_proveedor_nuevo"] else niv["nuevo"]

    def idempotente(self, ambito, clave, producir):
        """Misma clave, misma respuesta: un reintento no duplica recibo ni reserva."""
        if clave is None:
            return producir()
        if (ambito, clave) not in self.respuestas:
            self.respuestas[(ambito, clave)] = producir()
        return self.respuestas[(ambito, clave)]

    def _emitir(self, d, f) -> None:
        r = emitir_recibo(d, f, self.m, self.ids, self.nonce, self.reloj, self.firmador)
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
            self._emitir(d, f)
        self.reg.registrar_factura(f, d["estado"])
        self.facturas[f["id"]] = f
        self.decisiones[d["id"]] = d
        return d

    def _hash_factura(self, factura_id):
        f = self.facturas.get(factura_id)
        return f["documento"]["hash"] if f else None

    def verificar_orden(self, orden, recibo, aprobacion=None) -> dict:
        ctx = ContextoGuardian(self.firmador.firma_valida, self._hash_factura, self.m.version, self.reloj(),
                               self.libro.consumir_nonce)
        res = verificar(orden, recibo, aprobacion, ctx)
        self._cerrar_orden(res, recibo)
        return res

    def _cerrar_orden(self, res, recibo) -> None:
        """Autorizada o Denegada. Solo un recibo genuino (verificaciones 1 a 3 en ok) libera su reserva."""
        d = next((x for x in self.decisiones.values() if x["recibo_id"] == recibo.get("id")), None)
        n = next((v["n"] for v in res["verificaciones"] if v["estado"] == "falla"), None)
        if d is None or d["estado"] != "con_recibo":
            return
        if res["autorizada"]:
            d["estado"] = "autorizada"
        elif n in (4, 5):
            self.libro.liberar(recibo["id"])
            d["estado"] = "denegada"
