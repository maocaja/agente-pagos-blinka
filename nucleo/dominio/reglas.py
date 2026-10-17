from dataclasses import dataclass

from .dinero import a_base_menor

REGLAS: dict = {}
TIPOS_EVALUABLES = ("factura", "cuenta_de_cobro")


@dataclass(frozen=True)
class Resultado:
    estado: str
    accion: str | None
    aprobable: bool
    evidencia: str
    campo: str | None = None


def cumple(evidencia, campo=None):
    return Resultado("cumple", None, True, evidencia, campo)


def regla(id_):
    def reg(fn):
        REGLAS[id_] = fn
        return fn
    return reg


@regla("R2a")
def duplicado_exacto(f, m, reg):
    prov = f["proveedor_asignado"]["proveedor_id"]
    num = f["referencias"]["numero_normalizado"]
    h = f["documento"]["hash"]
    for o in reg.facturas:
        if o["id"] == f["id"]:
            continue
        if o["documento"]["hash"] == h:
            return Resultado("falla", "FRENAR", False, f"El archivo es identico al de la factura {o['id']}.", "documento.hash")
        if prov and o["proveedor_asignado"]["proveedor_id"] == prov and o["referencias"]["numero_normalizado"] == num:
            return Resultado("falla", "FRENAR", False, f"El numero {num} del mismo proveedor ya se recibio en {o['id']}.", "referencias.numero_normalizado")
    return cumple("Sin duplicado exacto.")


@regla("R3")
def beneficiario(f, m, reg):
    pid = f["proveedor_asignado"]["proveedor_id"]
    p = reg.proveedor(pid) if pid else None
    campo = "proveedor_asignado.proveedor_id"
    if p is None:
        return Resultado("falla", "ESCALAR", True, f"{f['emisor']['nombre']} no esta en el registro maestro.", campo)
    if p["estado"] == "bloqueado":
        return Resultado("falla", "FRENAR", False, f"{p['nombre']} esta bloqueado en el registro maestro.", campo)
    return cumple(f"{p['nombre']} esta en el registro.", campo)


@regla("R4")
def cuenta_registrada(f, m, reg):
    p = reg.proveedor(f["proveedor_asignado"]["proveedor_id"])
    c = f.get("cuenta")
    if p is None:
        return Resultado("falla", "ESCALAR", True, "Sin proveedor registrado no hay cuenta contra la cual comparar.", "cuenta")
    if c is None:
        return cumple("La factura no trae cuenta: el pago va a la registrada.", "cuenta")
    r = p["cuenta"]
    if (c["pais"], c["ultimos4"]) != (r["pais"], r["ultimos4"]):
        return Resultado("falla", "ESCALAR", True,
                         f"La cuenta esta en {c['pais']} terminada en {c['ultimos4']} y la registrada es de {r['pais']} terminada en {r['ultimos4']}.", "cuenta")
    return cumple("La cuenta coincide con la registrada.", "cuenta")


@regla("R6")
def monto(f, m, reg):
    mo = f["montos"]
    base = a_base_menor(mo["total_menor"], mo["moneda"], m)
    tope, umbral = int(m.p["tope_pago_menor"]), int(m.p["umbral_aprobacion_menor"])
    campo = "montos.total_menor"
    if base > tope:
        return Resultado("falla", "FRENAR", False, f"{base} unidades menores base superan el tope por pago de {tope}.", campo)
    if base > umbral:
        return Resultado("falla", "ESCALAR", True, f"{base} unidades menores base superan el umbral de aprobacion de {umbral}.", campo)
    return cumple(f"{base} unidades menores base, bajo el umbral de {umbral}.", campo)
