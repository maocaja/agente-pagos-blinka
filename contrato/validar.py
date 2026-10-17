"""Validador minimo de JSON Schema para comprobar los ejemplos del contrato.
Cubre type, required, properties, additionalProperties, enum, pattern e items.
No sustituye a una libreria completa: el test de contrato de U1 debe usar jsonschema."""
import json, re, sys

def tipo_ok(v, t):
    ts = t if isinstance(t, list) else [t]
    for x in ts:
        if x == "null" and v is None: return True
        if x == "string" and isinstance(v, str): return True
        if x == "integer" and isinstance(v, int) and not isinstance(v, bool): return True
        if x == "number" and isinstance(v, (int, float)) and not isinstance(v, bool): return True
        if x == "boolean" and isinstance(v, bool): return True
        if x == "object" and isinstance(v, dict): return True
        if x == "array" and isinstance(v, list): return True
    return False

def validar(v, s, ruta="$"):
    err = []
    if "type" in s and not tipo_ok(v, s["type"]):
        return [f"{ruta}: tipo {type(v).__name__}, se esperaba {s['type']}"]
    if "enum" in s and v not in s["enum"]:
        err.append(f"{ruta}: {v!r} no esta en {s['enum']}")
    if isinstance(v, str) and "pattern" in s and not re.search(s["pattern"], v):
        err.append(f"{ruta}: {v!r} no cumple {s['pattern']}")
    if isinstance(v, dict):
        for k in s.get("required", []):
            if k not in v: err.append(f"{ruta}: falta {k}")
        props = s.get("properties", {})
        ap = s.get("additionalProperties", True)
        for k, x in v.items():
            if k in props: err += validar(x, props[k], f"{ruta}.{k}")
            elif ap is False: err.append(f"{ruta}: propiedad no permitida {k}")
            elif isinstance(ap, dict): err += validar(x, ap, f"{ruta}.{k}")
    if isinstance(v, list) and "items" in s:
        for i, x in enumerate(v): err += validar(x, s["items"], f"{ruta}[{i}]")
    return err

PARES = [
    ("ejemplos/factura-canonica.f11.json", "factura-canonica.schema.json"),
    ("ejemplos/decision.f11.json", "decision.schema.json"),
    ("ejemplos/recibo.pagar.json", "recibo.schema.json"),
    ("ejemplos/aprobacion.ejemplo.json", "aprobacion.schema.json"),
    ("ejemplos/mandato.v1.json", "mandato.schema.json"),
    ("ejemplos/mandato.v2.json", "mandato.schema.json"),
    ("ejemplos/resultados.arena.json", "resultados.schema.json"),
    ("ejemplos/esperado.f11.json", "esperado.schema.json"),
]
if __name__ == "__main__":
    mal = 0
    for ej, es in PARES:
        e = validar(json.load(open(ej)), json.load(open(es)))
        print(("OK   " if not e else "FALLA"), ej, "contra", es)
        for x in e: print("      ", x)
        mal += bool(e)
    sys.exit(1 if mal else 0)
