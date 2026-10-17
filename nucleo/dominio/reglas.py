from dataclasses import dataclass
from datetime import date
from fractions import Fraction

from .dinero import a_base_menor, base_de

REGLAS: dict = {}
AL_FINAL = ("R9",)
_DINERO = ("monto_total", "moneda", "proveedor", "cuenta")


@dataclass(frozen=True)
class Resultado:
    estado: str
    accion: str | None
    aprobable: bool
    evidencia: str
    campo: str | None = None


def cumple(evidencia, campo=None):
    return Resultado("cumple", None, True, evidencia, campo)


def falla(accion, aprobable, evidencia, campo=None):
    return Resultado("falla", accion, aprobable, evidencia, campo)


def regla(id_):
    def reg(fn):
        REGLAS[id_] = fn
        return fn
    return reg


def _causas_lectura(f, m):
    v, p, mo = f["verificaciones"], m.p, f["montos"]
    causas = []
    for campo, c in f["confianza"].items():
        minimo = p["conf_min_dinero"] if campo in _DINERO else p["conf_min_general"]
        if c < minimo:
            causas.append(f"confianza {c} en {campo}, minimo {minimo}")
    causas += [f"verificacion {k} fallida" for k in ("esquema", "dinero_presente", "cita_evidencia") if v[k] == "falla"]
    if v["tipo"] != "ok":
        causas.append("el tipo declarado contradice el texto")
    suma = mo["suma_lineas_menor"]
    if suma is not None and abs(int(mo["total_menor"]) - int(suma)) > int(p["tolerancia_lineas_menor"]):
        causas.append("las lineas no suman el total")
    if v["segunda_lectura"]["estado"] != "coincide":
        causas.append(f"segunda lectura: {v['segunda_lectura']['estado']}")
    if f["documento"]["formato"] == "imagen":
        causas.append("lectura de imagen: confirmar contra el original")
    return causas


def _causa_remitente(f):
    s = f.get("senales", {}).get("remitente_inconsistente")
    return [f"remitente inconsistente: {s['motivo']}"] if s else []


@regla("R1")
def lectura_confiable(f, m, reg):
    causas = _causas_lectura(f, m) + _causa_remitente(f)
    if causas:
        return falla("ESCALAR", False, "Lectura no confiable: " + "; ".join(causas) + ".")
    return cumple("Lecturas coinciden y la confianza supera el minimo.")


@regla("R2a")
def duplicado_exacto(f, m, reg):
    prov = f["proveedor_asignado"]["proveedor_id"]
    num = f["referencias"]["numero_normalizado"]
    h = f["documento"]["hash"]
    for o in reg.facturas:
        if o["id"] == f["id"]:
            continue
        if o["documento"]["hash"] == h:
            return falla("FRENAR", False, f"El archivo es identico al de la factura {o['id']}.", "documento.hash")
        if prov and o["proveedor_asignado"]["proveedor_id"] == prov and o["referencias"]["numero_normalizado"] == num:
            return falla("FRENAR", False, f"El numero {num} del mismo proveedor ya se recibio en {o['id']}.", "referencias.numero_normalizado")
    return cumple("Sin duplicado exacto.")


def _dia(f):
    return date.fromisoformat(f["fechas"]["emision"] or f["documento"]["recibido_en"][:10])


def _parecida(f, o, base, m, reg):
    """Mismo proveedor, otro numero, no frenada, monto dentro de la tolerancia y de la ventana."""
    if (o["id"] == f["id"] or reg.estados.get(o["id"]) == "frenada"
            or o["proveedor_asignado"]["proveedor_id"] != f["proveedor_asignado"]["proveedor_id"]
            or o["referencias"]["numero_normalizado"] == f["referencias"]["numero_normalizado"]):
        return False
    previa = base_de(o, m)
    tol = Fraction(str(m.p["dup_tolerancia_monto_pct"])) / 100
    return (previa is not None and abs(base - previa) <= previa * tol
            and abs((_dia(f) - _dia(o)).days) <= m.p["dup_ventana_dias"])


@regla("R2b")
def duplicado_difuso(f, m, reg):
    base = base_de(f, m)
    if f["proveedor_asignado"]["proveedor_id"] and base is not None:
        for o in reg.facturas:
            if _parecida(f, o, base, m, reg):
                return falla("ESCALAR", True, f"Monto parecido y fecha cercana a la factura {o['id']} del mismo proveedor.", "montos.total_menor")
    return cumple("Sin duplicado difuso.")


@regla("R8")
def texto_dirigido(f, m, reg):
    s = f.get("senales", {}).get("texto_dirigido_al_agente")
    if s and s["p"] >= m.p["umbral_senal_texto"]:
        return falla("ESCALAR", True, f"El documento trae texto dirigido al agente: {s['origen']}", "senales.texto_dirigido_al_agente")
    return cumple("Sin texto dirigido al agente.")


@regla("R9")
def presupuesto(f, m, reg):
    base = base_de(f, m)
    quedan = int(m.p["presupuesto_periodo_menor"]) - reg.libro.acumulado(f["ciclo_id"])
    if base is not None and base > quedan:
        return falla("ESCALAR", False, f"{base} unidades menores base superan lo que queda del periodo ({quedan}).", "montos.total_menor")
    return cumple(f"Cabe en el presupuesto del periodo (quedan {quedan}).")


@regla("R10")
def tope_acumulado(f, m, reg):
    tope = m.p["tope_acumulado_proveedor"]
    pid, base = f["proveedor_asignado"]["proveedor_id"], base_de(f, m)
    if not tope["activo"] or pid is None or base is None:
        return cumple("Tope acumulado inactivo o sin proveedor que acumular.")
    total = reg.libro.acumulado(f["ciclo_id"], pid) + base
    if total > int(tope["monto_menor"]):
        return falla("ESCALAR", True, f"Lo pagado y reservado al proveedor mas esta factura suma {total}, sobre el tope de {tope['monto_menor']}.", "montos.total_menor")
    return cumple(f"El acumulado del proveedor, {total}, esta bajo el tope.")
