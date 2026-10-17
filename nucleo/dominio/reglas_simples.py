"""Reglas sin logica propia: una fila de datos y una medida; el evaluador es generico."""
from fractions import Fraction

from .dinero import a_base_menor, base_de, convertible, importe
from .reglas import REGLAS, cumple, falla

ESCALAR, FRENAR = "ESCALAR", "FRENAR"


def _proveedor(f, reg):
    pid = f["proveedor_asignado"]["proveedor_id"]
    return reg.proveedor(pid) if pid else None


def _estado_proveedor(f, m, reg):
    p = _proveedor(f, reg)
    if p is None:
        return "no_registrado", {"nombre": f["emisor"]["nombre"]}
    return ("bloqueado" if p["estado"] == "bloqueado" else "activo"), {"nombre": p["nombre"]}


def _cuenta(f, m, reg):
    p, c = _proveedor(f, reg), f.get("cuenta")
    if p is None:
        return "sin_proveedor", {}
    if c is None:
        return "sin_cuenta", {}
    r = p["cuenta"]
    estado = "coincide" if (c["pais"], c["ultimos4"]) == (r["pais"], r["ultimos4"]) else "distinta"
    return estado, {"pais": c["pais"], "u4": c["ultimos4"], "rpais": r["pais"], "ru4": r["ultimos4"]}


def _acuerdo(f, m, reg):
    p = _proveedor(f, reg)
    a = p and p.get("acuerdo")
    base = base_de(f, m)
    if not a:
        return "sin_acuerdo", {}
    if base is None:
        return "no_convertible", {}
    maximo = a_base_menor(a["monto_maximo_menor"], a["moneda"], m)
    pct = m.p["tolerancia_acuerdo_pct"]
    return ("excede" if base * 100 > maximo * (100 + Fraction(str(pct))) else "dentro"), {"base": importe(base, m), "maximo": importe(maximo, m), "pct": pct}


def _monto(f, m, reg):
    base = base_de(f, m)
    if base is None:
        return "no_convertible", {}
    tope, umbral = int(m.p["tope_pago_menor"]), int(m.p["umbral_aprobacion_menor"])
    estado = "sobre_tope" if base > tope else "sobre_umbral" if base > umbral else "dentro"
    return estado, {"base": importe(base, m), "tope": importe(tope, m), "umbral": importe(umbral, m)}


def _moneda(f, m, reg):
    moneda = f["montos"]["moneda"]
    return ("permitida" if convertible(moneda, m) else "no_permitida"), {"moneda": moneda}


_NO_CONVERTIBLE = (None, True, "Sin conversión a la base; la decide R7.")
FILAS = (
    {"id": "R3", "campo": "proveedor_asignado.proveedor_id", "medida": _estado_proveedor, "estados": {
        "activo": (None, True, "{nombre} está en el registro."),
        "no_registrado": (ESCALAR, True, "{nombre} no está en el registro maestro."),
        "bloqueado": (FRENAR, False, "{nombre} está bloqueado en el registro maestro.")}},
    {"id": "R4", "campo": "cuenta", "medida": _cuenta, "estados": {
        "coincide": (None, True, "La cuenta coincide con la registrada."),
        "sin_cuenta": (None, True, "La factura no trae cuenta: el pago va a la registrada."),
        "sin_proveedor": (None, True, "Sin proveedor registrado; lo decide R3."),
        "distinta": (ESCALAR, True, "La cuenta está en {pais} terminada en {u4} y la registrada es de {rpais} terminada en {ru4}.")}},
    {"id": "R5", "campo": "montos.total_menor", "medida": _acuerdo, "estados": {
        "dentro": (None, True, "{base}, dentro de lo acordado ({maximo} más {pct}%)."),
        "excede": (ESCALAR, True, "{base} superan lo acordado ({maximo} más {pct}%)."),
        "sin_acuerdo": (ESCALAR, True, "No hay acuerdo registrado para este proveedor."),
        "no_convertible": _NO_CONVERTIBLE}},
    {"id": "R6", "campo": "montos.total_menor", "medida": _monto, "estados": {
        "dentro": (None, True, "{base}, bajo el umbral de {umbral}."),
        "sobre_umbral": (ESCALAR, True, "{base} superan el umbral de aprobación de {umbral}."),
        "sobre_tope": (FRENAR, False, "{base} superan el tope por pago de {tope}."),
        "no_convertible": _NO_CONVERTIBLE}},
    {"id": "R7", "campo": "montos.moneda", "medida": _moneda, "estados": {
        "permitida": (None, True, "{moneda} es una moneda permitida con tasa."),
        "no_permitida": (FRENAR, False, "{moneda} no es una moneda permitida o no tiene tasa en el mandato.")}},
)


def _evaluador(fila):
    def evaluar(f, m, reg):
        estado, hechos = fila["medida"](f, m, reg)
        accion, aprobable, plantilla = fila["estados"][estado]
        texto = plantilla.format(**hechos)
        return cumple(texto, fila["campo"]) if accion is None else falla(accion, aprobable, texto, fila["campo"])
    return evaluar


for _fila in FILAS:
    REGLAS[_fila["id"]] = _evaluador(_fila)
