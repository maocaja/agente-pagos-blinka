"""Una funcion por regla, registrada por id; cada una devuelve (accion, evidencia) si falla."""
import re
from dataclasses import dataclass
from datetime import date

from .estado import Estado

REGLAS = {}
FINALES = ("R9",)
CAMPOS_DINERO = ("monto_total", "moneda", "proveedor", "cuenta")
CAMPOS_GENERALES = ("tipo_documento", "numero_factura")


def regla(id_):
    def registrar(fn):
        REGLAS[id_] = fn
        return fn
    return registrar


def normalizar(texto):
    return re.sub(r"[^A-Z0-9]", "", (texto or "").upper())


@dataclass
class Contexto:
    f: dict
    p: dict
    registro: dict
    monedas: dict
    estado: Estado
    prov: dict
    base: int
    periodo: str
    fallas: dict

    def dias_desde(self, otra):
        return abs((date.fromisoformat(self.f["documento"]["recibido_en"][:10]) - date.fromisoformat(otra)).days)


def _lectura_incompleta(f, p):
    conf, falta = f.get("confianza") or {}, []
    for campo in CAMPOS_DINERO + CAMPOS_GENERALES:
        if campo == "cuenta" and not (f.get("cuenta") or {}).get("ultimos4"):
            continue
        minimo = p["conf_min_dinero"] if campo in CAMPOS_DINERO else p["conf_min_general"]
        if not isinstance(conf.get(campo), (int, float)) or conf[campo] < minimo:
            falta.append(f"confianza de {campo} bajo el minimo")
    return falta


def _campos_faltantes(f):
    m = f["montos"]
    vacios = [("numero", f["referencias"].get("numero")), ("monto", m.get("total_menor") not in (None, "", "0")),
              ("moneda", m.get("moneda")), ("proveedor", (f.get("emisor") or {}).get("nombre"))]
    return [f"falta {k}" for k, v in vacios if not v]


def _suma_descuadrada(f, p):
    m = f["montos"]
    suma = sum(int(x["total_menor"]) for x in m["lineas"]) if m.get("lineas") else m.get("suma_lineas_menor")
    if suma is None or m.get("total_menor") in (None, ""):
        return []
    return ["la suma de lineas no cuadra con el total"] if abs(int(suma) - int(m["total_menor"])) > int(p["tolerancia_lineas_menor"]) else []


def _verificaciones_malas(f):
    v = f.get("verificaciones") or {}
    malas = [f"{k} no esta ok" for k in ("esquema", "dinero_presente", "cita_evidencia") if v.get(k) != "ok"]
    if (v.get("segunda_lectura") or {}).get("estado") != "coincide":
        malas.append("las lecturas no coinciden o no hay segunda lectura")
    return malas


@regla("R1")
def lectura_confiable(c):
    motivos = (_lectura_incompleta(c.f, c.p) + _campos_faltantes(c.f)
               + _suma_descuadrada(c.f, c.p) + _verificaciones_malas(c.f))
    return ("ESCALAR", "; ".join(motivos)) if motivos else None


@regla("R2a")
def duplicado_exacto(c):
    num, h = normalizar(c.f["referencias"].get("numero")), c.f["documento"].get("hash")
    mismo_numero = any(num and r.numero == num for r in c.estado.del_proveedor(c.prov and c.prov["id"]))
    if mismo_numero or any(h and r.hash == h for r in c.estado.recibidas):
        return ("FRENAR", "mismo proveedor y numero, o mismo archivo, ya recibido")
    return None


@regla("R2b")
def duplicado_difuso(c):
    num, pct, dias = normalizar(c.f["referencias"].get("numero")), c.p["dup_tolerancia_monto_pct"], c.p["dup_ventana_dias"]
    for r in c.estado.del_proveedor(c.prov and c.prov["id"]):
        cercano = c.base is not None and abs(c.base - r.base_menor) * 100 <= pct * r.base_menor
        if r.numero != num and r.tipo in ("factura", "cuenta_de_cobro") and r.veredicto != "FRENAR" and cercano \
                and c.dias_desde(r.fecha) <= dias:
            return ("ESCALAR", f"monto parecido a {r.numero} dentro de {dias} dias")
    return None


@regla("R3")
def beneficiario_permitido(c):
    if c.prov is None:
        return ("ESCALAR", "el proveedor no esta en el registro maestro")
    return ("FRENAR", "proveedor bloqueado") if c.prov["estado"] == "bloqueado" else None


@regla("R4")
def cuenta_registrada(c):
    cuenta, reg = c.f.get("cuenta") or {}, (c.prov or {}).get("cuenta")
    if not cuenta.get("ultimos4") or reg is None:
        return None
    if (cuenta["ultimos4"], cuenta.get("pais")) != (reg["ultimos4"], reg["pais"]):
        return ("ESCALAR", "la cuenta de la factura difiere de la registrada")
    return None


@regla("R5")
def coincide_con_lo_acordado(c):
    acuerdo = (c.prov or {}).get("acuerdo")
    if not acuerdo:
        return ("ESCALAR", "no hay acuerdo registrado")
    limite = int(acuerdo["monto_maximo_menor"]) * (100 + c.p["tolerancia_acuerdo_pct"])
    if c.base is None or c.base * 100 > limite:
        return ("ESCALAR", "el monto supera el acuerdo mas la tolerancia")
    return None


@regla("R6")
def monto(c):
    if c.base is None:
        return ("FRENAR", "no se puede convertir el monto a la moneda base")
    if c.base > int(c.p["tope_pago_menor"]):
        return ("FRENAR", "supera el tope por pago")
    return ("ESCALAR", "supera el umbral de aprobacion") if c.base > int(c.p["umbral_aprobacion_menor"]) else None


@regla("R7")
def moneda(c):
    m = c.f["montos"]["moneda"]
    sin_tasa = m not in c.p["tasas_cambio"]["unidades_por_usd"]
    return ("FRENAR", f"moneda {m} no permitida o sin tasa") if m not in c.p["monedas_permitidas"] or sin_tasa else None


@regla("R8")
def texto_dirigido_al_agente(c):
    senal = (c.f.get("senales") or {}).get("texto_dirigido_al_agente")
    return ("ESCALAR", "el documento trae instrucciones al agente") if senal and senal["p"] >= c.p["umbral_senal_texto"] else None


@regla("R9")
def presupuesto(c):
    if c.fallas:
        return None
    restante = int(c.p["presupuesto_periodo_menor"]) - c.estado.reservado(c.periodo)
    return ("ESCALAR", "el monto supera lo que queda del presupuesto") if c.base is None or c.base > restante else None


@regla("R10")
def tope_acumulado(c):
    cfg = c.p["tope_acumulado_proveedor"]
    if not cfg["activo"] or c.prov is None:
        return None
    previo = c.estado.reservado(c.periodo, c.prov["id"])
    return ("ESCALAR", "el acumulado del proveedor supera el tope") if c.base is None or previo + c.base > int(cfg["monto_menor"]) else None
