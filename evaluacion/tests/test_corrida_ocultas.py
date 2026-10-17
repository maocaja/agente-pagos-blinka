import json

from contrato.validar import validar

from .ayudas import RAIZ

SALIDA = RAIZ / "evaluacion/salida/ocultas.json"
LECTURAS = sorted((RAIZ / "evaluacion/ocultas_lecturas").glob("*.json"))


def _json(ruta):
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_lecturas_ocultas_validan_contra_el_esquema_canonico():
    esquema = _json(RAIZ / "contrato/factura-canonica.schema.json")
    assert len(LECTURAS) == 4
    assert [e for ruta in LECTURAS for e in validar(_json(ruta), esquema)] == []


def test_ninguna_oculta_paga_si_su_esperado_no_es_pagar():
    r = _json(SALIDA)
    assert r["documentos"] == 4 and r["sello"] == "ok"
    for c in r["casos"]:
        assert c["motor"]["veredicto"] != "PAGAR" or c["esperado"]["veredicto"] == "PAGAR", c["archivo"]
