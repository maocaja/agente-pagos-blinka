"""Mutaciones de una extraccion canonica; cada una es una funcion registrada (f, rng, mandato) -> f. No tocan el original."""
import hashlib
import json

from lectura.normalizador.normalizador import normalizar_clave

from ..verificador import RAIZ

MUTACIONES: dict = {}
CON_PREVIA = {"numero_reformateado", "duplicado_difuso"}  # solo estas necesitan la factura original ya recibida
REGISTRO = json.loads((RAIZ / "datos/registro-maestro.json").read_text(encoding="utf-8"))["proveedores"]


def mutacion(fn):
    MUTACIONES[fn.__name__] = fn
    return fn


def _total(f, menor):
    f["montos"].update(total_menor=str(menor), suma_lineas_menor=str(menor),
                       lineas=[{"descripcion": "servicio", "total_menor": str(menor)}])
    return f


@mutacion
def borde_umbral(f, rng, m):
    f["montos"]["moneda"] = m["parametros"]["moneda_base"]
    return _total(f, int(m["parametros"]["umbral_aprobacion_menor"]) + rng.choice([-1, 0, 1]))


@mutacion
def borde_tope(f, rng, m):
    f["montos"]["moneda"] = m["parametros"]["moneda_base"]
    return _total(f, int(m["parametros"]["tope_pago_menor"]) + rng.choice([-1, 0, 1]))


@mutacion
def redondeo_de_moneda(f, rng, m):
    p = m["parametros"]
    moneda = rng.choice([c for c in p["monedas_permitidas"] if c != p["moneda_base"]])
    tasa = int(p["tasas_cambio"]["unidades_por_usd"][moneda])
    f["montos"]["moneda"] = moneda
    return _total(f, int(p["umbral_aprobacion_menor"]) * tasa + rng.choice([-1, 0, 1, 2]))


@mutacion
def moneda_sin_tasa(f, rng, m):
    f["montos"]["moneda"] = rng.choice(["EUR", "PEN", "CLP", "XXX", ""])
    return f


@mutacion
def numero_reformateado(f, rng, m):
    n = f["referencias"]["numero"]
    f["referencias"]["numero"] = rng.choice([n.lower(), n.replace("-", " "), n.replace("-", "/0"), " " + n])
    f["referencias"]["numero_normalizado"] = normalizar_clave(f["referencias"]["numero"])
    return f


@mutacion
def cuenta_cambiada(f, rng, m):
    f["cuenta"] = {"pais": rng.choice(["US", "CO", "BR"]), "ultimos4": f"{rng.randrange(10000):04d}"}
    return f


@mutacion
def instruccion_insertada(f, rng, m):
    f.setdefault("senales", {})["texto_dirigido_al_agente"] = {"p": rng.choice([0.3, 0.6, 0.95]), "origen": "texto insertado"}
    return f


@mutacion
def tipo_cambiado(f, rng, m):
    f["documento"]["tipo_documento"] = rng.choice(["proforma", "anticipo", "estado_de_cuenta", "nota_de_credito", "recibo_raro", ""])
    return f


@mutacion
def campo_quitado(f, rng, m):
    campo = rng.choice(["cuenta", "suma", "fiscal", "confianza", "monto_ilegible"])
    if campo == "cuenta":
        f["cuenta"] = None
    elif campo == "suma":
        f["montos"]["suma_lineas_menor"] = None
    elif campo == "fiscal":
        f["emisor"]["id_fiscal"] = None
    elif campo == "confianza":
        f["confianza"]["monto_total"] = 0.4
    else:
        f["montos"]["total_menor"] = "12,5"
    return f


@mutacion
def proveedor_intercambiado(f, rng, m):
    p = rng.choice(REGISTRO)
    f["emisor"].update(nombre=p["nombre"], nombre_normalizado=normalizar_clave(p["nombre"]), id_fiscal=p["id_fiscal"])
    f["proveedor_asignado"] = {"proveedor_id": p["id"], "metodo": "nombre", "pista": None}
    return f


@mutacion
def duplicado_difuso(f, rng, m):
    base = int(f["montos"]["total_menor"] or 0)
    f["referencias"]["numero"] = f["referencias"]["numero_normalizado"] = "OTRO-" + f["referencias"]["numero"]
    return _total(f, base + base * rng.choice([-3, -1, 0, 1, 3]) // 100)


def nuevo_documento(f, i):
    """El hash cambia: cada variante es un archivo distinto salvo que la mutacion pida lo contrario."""
    f["documento"]["hash"] = hashlib.sha256(f"{f['documento']['hash']}~{i}".encode()).hexdigest()
    return f
