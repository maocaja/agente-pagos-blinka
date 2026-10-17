"""Asignacion de proveedor del registro maestro: id fiscal, luego nombre; nunca inventa."""
import difflib

from lectura.normalizador.normalizador import normalizar_clave


def _clave_fiscal(texto):
    # El registro trae el tipo delante ("NIT 900.000.111-0"); la factura solo el numero.
    return normalizar_clave((texto or "").split(" ")[-1])


def _ids(registro, campo):
    por_clave = {}
    for prov in registro["proveedores"]:
        claves = [_clave_fiscal(prov.get("id_fiscal"))] if campo == "fiscal" else [
            normalizar_clave(n) for n in [prov["nombre"], *prov.get("alias", [])]]
        for clave in filter(None, claves):
            por_clave.setdefault(clave, set()).add(prov["id"])
    return por_clave


def _pista(nombre_norm, registro):
    claves = _ids(registro, "nombre")
    cerca = difflib.get_close_matches(nombre_norm, list(claves), n=1, cutoff=0.8)
    return sorted(claves[cerca[0]])[0] if cerca else None


def asignar_proveedor(factura, registro):
    emisor = factura["emisor"]
    por_fiscal = _ids(registro, "fiscal").get(_clave_fiscal(emisor.get("id_fiscal")), set())
    nombre_norm = normalizar_clave(emisor.get("nombre", ""))
    por_nombre = _ids(registro, "nombre").get(nombre_norm, set())
    if len(por_fiscal) == 1 and (not por_nombre or por_nombre == por_fiscal):
        return {"proveedor_id": next(iter(por_fiscal)), "metodo": "id_fiscal", "pista": None}
    if por_fiscal or len(por_nombre) > 1:
        return {"proveedor_id": None, "metodo": "conflicto", "pista": None}
    if por_nombre:
        return {"proveedor_id": next(iter(por_nombre)), "metodo": "nombre", "pista": None}
    return {"proveedor_id": None, "metodo": "ninguno", "pista": _pista(nombre_norm, registro)}
