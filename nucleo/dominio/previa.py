from .errores import ErrorAccion
from .mandato import Mandato
from .motor import decidir


def _mandato_propuesto(actual: Mandato, cambios) -> Mandato:
    if not isinstance(cambios, dict) or not cambios:
        raise ErrorAccion(422, "cuerpo_invalido", "Se exigen cambios sobre los parametros del mandato.")
    desconocidos = sorted(set(cambios) - set(actual.p))
    if desconocidos:
        raise ErrorAccion(422, "cuerpo_invalido", "Parametros que el mandato no tiene.", {"parametros": desconocidos})
    return Mandato(f"{actual.version}-previa", "propuesto", {**actual.p, **cambios}, actual.doc)


def _veredicto(s, f, m):
    return decidir(f, m, s.reg, lambda p: f"{p}_previa", s.reloj, s.modo_de(f["proveedor_asignado"]["proveedor_id"]),
                   requeridas=s.requeridas)


def previa_de_mandato(s, cambios) -> dict:
    """Reevalua las facturas de la sesion con y sin los cambios; no guarda nada. Ambos lados se evaluan igual, asi el efecto de las reservas propias se cancela."""
    propuesto = _mandato_propuesto(s.m, cambios)
    filas = []
    for f in s.facturas.values():
        antes, despues = _veredicto(s, f, s.m), _veredicto(s, f, propuesto)
        if antes["veredicto"] != despues["veredicto"]:
            filas.append({"factura_id": f["id"], "antes": antes["veredicto"], "despues": despues["veredicto"],
                          "explicacion": despues["explicacion"]})
    return {"mandato_vigente": s.m.version, "evaluadas": len(s.facturas), "cambian": len(filas), "cambios": filas}
