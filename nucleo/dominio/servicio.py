from .motor import decidir
from .recibo import emitir_recibo


class ServicioDecision:
    """Caso de uso de T1: decide una factura y, si es PAGAR, emite el recibo. Todo se inyecta."""

    def __init__(self, mandato, registro, ids, nonce, reloj, firmador):
        self.m, self.reg, self.ids, self.nonce, self.reloj, self.firmador = mandato, registro, ids, nonce, reloj, firmador
        self.decisiones: dict = {}
        self.facturas: dict = {}
        self.recibos: dict = {}

    def modo_autonomia(self, f) -> str:
        pid = f["proveedor_asignado"]["proveedor_id"]
        dias = self.reg.dias_de_alta(pid, self.reloj().date()) if pid else None
        niv = self.m.p["nivel_autonomia_defecto"]
        return niv["conocido"] if dias is not None and dias >= self.m.p["dias_proveedor_nuevo"] else niv["nuevo"]

    def decidir(self, f) -> dict:
        d = decidir(f, self.m, self.reg, self.ids, self.reloj, self.modo_autonomia(f))
        if d["veredicto"] == "PAGAR":
            r = emitir_recibo(d, f, self.m, self.ids, self.nonce, self.reloj, self.firmador)
            self.recibos[r["id"]] = r
            d["recibo_id"] = r["id"]
        self.reg.registrar_factura(f)
        self.facturas[f["id"]] = f
        self.decisiones[d["id"]] = d
        return d
