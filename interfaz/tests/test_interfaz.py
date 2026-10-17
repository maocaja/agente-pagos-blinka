import json
import re
import sys
from pathlib import Path

from fastapi.testclient import TestClient

RAIZ = Path(__file__).resolve().parents[1]
CONTRATO = RAIZ.parent / "contrato"
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(CONTRATO))

from servidor_simulado import app  # noqa: E402
from validar import validar  # noqa: E402

cliente = TestClient(app)


def _esquema(nombre):
    return json.loads((CONTRATO / nombre).read_text(encoding="utf-8"))


def test_ninguna_pagina_usa_html_crudo():
    prohibido = re.compile(r"x-html|innerHTML|outerHTML|insertAdjacentHTML|document\.write")
    for f in list((RAIZ / "dist").glob("*.html")) + [RAIZ / "dist" / "app.js", RAIZ / "dist" / "api.js"]:
        assert not prohibido.search(f.read_text(encoding="utf-8")), f.name


def test_decisiones_validan_contra_el_contrato():
    esquema = _esquema("decision.schema.json")
    lista = cliente.get("/api/decisiones").json()
    assert {d["veredicto"] for d in lista} >= {"PAGAR", "FRENAR", "ESCALAR"}
    for d in lista:
        assert validar(d, esquema) == []


def test_recibo_validan_y_verifican():
    rec = cliente.get("/api/recibos/dec_01").json()
    assert validar(rec, _esquema("recibo.schema.json")) == []
    assert cliente.post("/api/recibos/dec_01/verificar").json()["valida"] is True
    assert cliente.get("/api/recibos/dec_02").status_code == 404


def test_guardian_autoriza_el_original_y_rechaza_la_copia_alterada():
    rec = cliente.get("/api/recibos/dec_01").json()
    orden = {"recibo_id": rec["id"], "beneficiario_id": rec["beneficiario_id"], "monto_menor": rec["monto_menor"], "moneda": rec["moneda"], "concepto": "x"}
    ok = cliente.post("/api/guardian/verificar", json={"orden": orden, "recibo": rec}).json()
    assert ok["autorizada"] and len(ok["verificaciones"]) == 6
    rec["monto_menor"] = "1"
    mal = cliente.post("/api/guardian/verificar", json={"orden": orden, "recibo": rec}).json()
    assert not mal["autorizada"] and mal["verificaciones"][0]["estado"] == "falla"


def test_pagina_servida_sin_cdn():
    html = cliente.get("/").text
    assert 'data-testid="lista-decisiones"' in html
    assert "http://" not in html and "https://" not in html
