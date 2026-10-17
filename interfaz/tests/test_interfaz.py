import json
import re
import sys
from pathlib import Path

from fastapi.testclient import TestClient

RAIZ = Path(__file__).resolve().parents[1]
CONTRATO = RAIZ.parent / "contrato"
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(CONTRATO))

from servidor_simulado import app, crear_app  # noqa: E402
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
    rec = cliente.get("/api/recibos/rec_01").json()
    assert validar(rec, _esquema("recibo.schema.json")) == []
    assert cliente.post("/api/recibos/rec_01/verificar").json()["valida"] is True
    assert cliente.get("/api/recibos/dec_02").status_code == 404


def test_guardian_autoriza_el_original_y_rechaza_la_copia_alterada():
    rec = cliente.get("/api/recibos/rec_01").json()
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


def test_simulador_devuelve_la_forma_de_resultados_y_v1_tiene_hueco():
    esquema = _esquema("resultados.schema.json")
    v1 = cliente.post("/api/pentest/ejecutar", json={"mandato_base": "v1", "semilla": 7}).json()
    v2 = cliente.post("/api/pentest/ejecutar", json={"mandato_base": "v2", "semilla": 7}).json()
    arena = cliente.post("/api/arena/ejecutar", json={"semilla": 7}).json()
    for r in (v1, v2, arena):
        assert validar(r, esquema) == []
    assert v1["recuentos"]["pagos_indebidos"] == 1 and v2["recuentos"]["pagos_indebidos"] == 0
    assert arena["recuentos"]["pagos_indebidos"] == 0 and arena["no_prueba"]
    assert cliente.post("/api/sesion").json()["lectura"] == "guardada"


def test_ataque_agrupa_casos_por_estrategia_con_los_archivos_reales():
    codigo = (RAIZ / "dist" / "paginas.js").read_text(encoding="utf-8")
    assert 'c.id.split("-")[0]' in codigo
    ids = [c["id"] for c in cliente.post("/api/pentest/ejecutar", json={"mandato_base": "v1"}).json()["casos"]]
    assert {i.split("-")[0] for i in ids} == {f"E{n}" for n in range(1, 7)}
    assert all(f'{k}: "' in codigo for k in {i.split("-")[0] for i in ids})


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


def test_aprobar_solo_cfo_reevalua_y_emite_recibo_nuevo():
    cliente.post("/api/sesion/reiniciar")
    assert cliente.post("/api/decisiones/dec_11/aprobar", json={"nota": "ok"}, headers={"X-Rol": "analista"}).status_code == 403
    r = cliente.post("/api/decisiones/dec_11/aprobar", json={"nota": "ok"}, headers={"X-Rol": "cfo"}).json()
    assert validar(r["decision"], _esquema("decision.schema.json")) == []
    assert validar(r["aprobacion"], _esquema("aprobacion.schema.json")) == []
    assert r["decision"]["reevaluacion_de"] == "dec_11" and r["decision"]["recibo_id"]
    assert cliente.post("/api/decisiones/dec_11/aprobar", json={"nota": "ok"}, headers={"X-Rol": "cfo"}).status_code == 409


def test_rechazar_exige_nota_y_deja_la_decision_rechazada():
    cliente.post("/api/muestras/m_01/cargar")
    h = {"X-Rol": "cfo"}
    assert cliente.post("/api/decisiones/dec_m1/rechazar", json={"nota": " "}, headers=h).status_code == 422
    d = cliente.post("/api/decisiones/dec_m1/rechazar", json={"nota": "No coincide"}, headers=h).json()
    assert d["estado"] == "rechazada" and validar(d, _esquema("decision.schema.json")) == []


def test_vista_previa_del_mandato_no_persiste():
    antes = cliente.get("/api/mandato").json()
    previa = cliente.post("/api/mandato/previa", json={"parametros": {"umbral_aprobacion_menor": "9999999"}}).json()
    assert previa["cambian"] == len(previa["cambios"]) >= 0 and previa["evaluadas"] >= previa["cambian"]
    assert cliente.get("/api/mandato").json() == antes
    assert cliente.post("/api/mandato/previa", json={"parametros": {"inventado": "1"}}).status_code == 422


def test_auditoria_paquete_y_pain001_simulada():
    paq = cliente.get("/api/auditoria/paquete")
    assert "attachment" in paq.headers["content-disposition"]
    assert {"formato", "generado_en", "clave_publica", "clave_version", "recibos", "mandatos"} <= paq.json().keys()
    assert validar(paq.json()["recibos"][0], _esquema("recibo.schema.json")) == []
    xml = cliente.get("/api/ordenes/rec_01/pain001")
    assert "SIMULADA" in xml.text and cliente.get("/api/ordenes/otro/pain001").status_code == 404


def test_paginas_nuevas_enlazan_descargas_normales():
    html = cliente.get("/").text
    nav = (RAIZ / "dist" / "nav.js").read_text(encoding="utf-8")
    assert 'href: "/api/auditoria/paquete"' in nav and "pain001" in html and 'data-testid="que-hacer"' in html


def test_sesion_persistente_y_cabecera_limpia():
    api = (RAIZ / "dist" / "api.js").read_text(encoding="utf-8")
    assert 'memoria.leer("sesion")' in api and "sessionStorage" in api
    html = cliente.get("/").text
    assert "rol simulado" not in html and 'data-testid="cambiar-tema"' not in html
    assert 'data-testid="cargar-set-ejemplo"' in html and "Pendientes de aprobación" in (RAIZ / "dist" / "app.js").read_text(encoding="utf-8")


def test_set_curado_y_cifra_honesta():
    ids = json.loads((RAIZ / "dist" / "demo-set.json").read_text(encoding="utf-8"))["ids"]
    assert 10 <= len(ids) <= 12 and len(set(ids)) == len(ids)
    assert "ataques probados" not in (RAIZ / "dist" / "app.js").read_text(encoding="utf-8")


def test_ciclo_y_historial_tras_rechazar():
    cliente = TestClient(crear_app())
    ciclo = cliente.get("/api/ciclo").json()
    assert set(ciclo) == {"ciclo_id", "empresa", "moneda", "presupuesto_menor", "reservado_menor", "disponible_menor", "actividad"}
    cliente.post("/api/decisiones/dec_11/rechazar", json={"nota": "Cuenta no confirmada"}, headers={"X-Rol": "cfo"})
    det = cliente.get("/api/decisiones/dec_11").json()
    assert det["historial"][-1]["nota"] == "Cuenta no confirmada" and det["estado_orden"] is None


def test_interfaz_nombra_autorizadas_y_no_pagadas():
    html = (RAIZ / "dist" / "app.js").read_text(encoding="utf-8")
    assert "Autorizadas para pago" in html and '"Pagados"' not in html
