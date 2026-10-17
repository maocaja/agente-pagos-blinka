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
    for f in list((RAIZ / "dist").glob("*.html")) + list((RAIZ / "dist").glob("*.js")):
        if f.name == "alpine.min.js":
            continue
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


def test_navegacion_enlaza_paginas_existentes():
    nav = (RAIZ / "dist" / "nav.js").read_text(encoding="utf-8")
    destinos = re.findall(r'href: "([a-z]+\.html)"', nav) + [d.split("?")[0] for d in re.findall(r'pagina: "([^"]+)"', nav)]
    assert len(destinos) >= 10
    for d in set(destinos):
        assert cliente.get("/" + d).status_code == 200, d


def test_mandato_y_marcador_validan_contra_el_contrato():
    assert validar(cliente.get("/api/mandato").json(), _esquema("mandato.schema.json")) == []
    m = cliente.get("/api/marcador").json()
    assert m["pagos_indebidos"] == 0 and m["aciertos_reglas"] != m["aciertos_extremo_a_extremo"]
    assert {p["nivel_autonomia"] for p in cliente.get("/api/proveedores").json()} == {"autonomo", "sombra"}


def test_pentest_v1_tiene_hueco_y_v2_lo_cierra():
    v1 = cliente.post("/api/pentest/ejecutar", json={"mandato_base": "v1", "semilla": 7}).json()
    v2 = cliente.post("/api/pentest/ejecutar", json={"mandato_base": "v2", "semilla": 7}).json()
    assert len(v1["estrategias"]) == 6 and [e["hueco"] for e in v1["estrategias"]].count(True) == 1
    assert not any(e["hueco"] for e in v2["estrategias"])
    arena = cliente.post("/api/arena/ejecutar", json={"semilla": 7}).json()
    assert arena["pagos_indebidos"] == 0 and arena["no_prueba"]


def test_muestras_cargan_decisiones_validas_con_la_regla_que_detuvo():
    esquema = _esquema("decision.schema.json")
    muestras = cliente.get("/api/muestras").json()
    assert {m["tipo"] for m in muestras} == {"correo", "chat", "pdf", "foto"}
    detuvo = set()
    for m in muestras:
        d = cliente.post(f"/api/muestras/{m['id']}/cargar").json()
        assert validar(d, esquema) == []
        assert cliente.get(f"/api/decisiones/{d['id']}").json()["factura"]["id"] == d["factura_id"]
        detuvo |= {r["id"] for r in d["reglas"] if r["estado"] == "falla"}
    assert detuvo == {"R8", "R4"}


def test_reiniciar_quita_las_muestras_cargadas():
    cliente.post("/api/muestras/m_01/cargar")
    assert cliente.post("/api/sesion/reiniciar").status_code == 200
    assert not any(d["id"].startswith("dec_m") for d in cliente.get("/api/decisiones").json())
