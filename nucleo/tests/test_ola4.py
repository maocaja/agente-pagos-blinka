import json
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from nucleo.api.app import crear_app
from nucleo.api.principal import fabrica_de_servicios
from nucleo.api.sesiones import Sesiones
from nucleo.dominio.recibo import orden_desde_recibo
from nucleo.tests.test_t1 import factura

CLOUD = {"proveedor_id": "prov_cloud", "metodo": "id_fiscal", "pista": None}


def _f(id_, monto, hash_, num):
    return factura(id=id_, montos__total_menor=monto, montos__suma_lineas_menor=monto, montos__moneda="USD",
                   documento__hash=hash_ * 64, referencias__numero_normalizado=num, proveedor_asignado=CLOUD,
                   cuenta={"pais": "US", "ultimos4": "6052"})


@pytest.fixture
def cliente(tmp_path):
    ahora = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
    resultados = tmp_path / "r.json"
    resultados.write_text('{"id": "set-x"}', encoding="utf-8")
    sesiones = Sesiones(fabrica_de_servicios(lambda: ahora), lambda p: p + "_1")
    c = TestClient(crear_app(sesiones, resultados, tmp_path / "dist"))
    c.libro = sesiones.defecto.libro
    return c


def _escalada(c, monto="200000", **h):
    c.post("/api/facturas", json=_f("a", "150000", "a", "A"), headers={"X-Rol": "analista"})
    d = c.post("/api/facturas", json=_f("b", monto, "b", "B"), headers={"X-Rol": "analista", **h}).json()
    assert d["veredicto"] == "ESCALAR"
    return d


def _aprobar(c, d, rol="cfo", clave="k", nota="ok"):
    return c.post(f"/api/decisiones/{d['id']}/aprobar", json={"nota": nota}, headers={"X-Rol": rol, "Idempotency-Key": clave})


def test_aprobar_reevalua_y_da_recibo_nuevo_que_el_guardian_acepta(cliente):
    d = _escalada(cliente)
    r = _aprobar(cliente, d)
    cuerpo = r.json()
    nueva, ap = cuerpo["decision"], cuerpo["aprobacion"]
    assert (r.status_code, nueva["reevaluacion_de"], nueva["estado"]) == (200, d["id"], "con_recibo")
    rec = cliente.get(f"/api/recibos/{nueva['recibo_id']}").json()
    assert (rec["veredicto"], rec["fallas_aprobadas"], ap["recibo_id"]) == ("ESCALAR", ["R10"], rec["id"])
    assert cliente.get(f"/api/decisiones/{d['id']}").json()["decision"]["estado"] == "reevaluada"
    g = cliente.post("/api/guardian/verificar", json={"orden": orden_desde_recibo(rec), "recibo": rec, "aprobacion": ap})
    assert g.json()["autorizada"] is True


def test_r9_no_se_supera_aprobando(cliente):
    cliente.libro.reservar("x", "nx", "prov_otro", "2026-10", 800000, 900000)
    d = cliente.post("/api/facturas", json=_f("g", "150000", "c", "G")).json()
    assert d["veredicto"] == "ESCALAR" and cliente.get(f"/api/recibos/{d['id']}").status_code == 404
    r = _aprobar(cliente, d)
    assert (r.status_code, r.json()["codigo"], r.json()["detalle"]["reglas"]) == (409, "no_aprobable", ["R9"])


def test_rechazar_exige_nota_y_cierra_la_decision(cliente):
    d = _escalada(cliente)
    url = f"/api/decisiones/{d['id']}/rechazar"
    assert cliente.post(url, json={"nota": " "}, headers={"X-Rol": "cfo"}).status_code == 422
    r = cliente.post(url, json={"nota": "no corresponde"}, headers={"X-Rol": "cfo"})
    assert (r.status_code, r.json()["estado"]) == (200, "rechazada")
    assert _aprobar(cliente, d).status_code == 409


def test_rol_incorrecto_o_quien_cargo_no_decide(cliente):
    d = _escalada(cliente)
    assert _aprobar(cliente, d, rol="analista").status_code == 403
    assert cliente.post(f"/api/decisiones/{d['id']}/aprobar", json={}).status_code == 403
    d2 = cliente.post("/api/facturas", json=_f("c", "250000", "d", "C"), headers={"X-Rol": "cfo"}).json()
    assert _aprobar(cliente, d2).status_code == 403


def test_idempotencia_de_aprobar(cliente):
    d = _escalada(cliente)
    r1, r2 = _aprobar(cliente, d, clave="mismo").json(), _aprobar(cliente, d, clave="mismo").json()
    assert r1["decision"]["recibo_id"] == r2["decision"]["recibo_id"]
    assert len([x for x in cliente.get("/api/decisiones").json() if x["recibo_id"]]) == 2


def test_marcador_sigue_el_esquema_del_contrato(cliente):
    _escalada(cliente)
    m = cliente.get("/api/marcador").json()
    assert (m["casos"], m["verificados"], m["pendientes"], m["autonomia"]) == (2, 0, 1, "50%")
    assert m["pagos_indebidos"] is None
    assert set(m) >= {"aciertos_reglas", "aciertos_extremo_a_extremo", "escalada_innecesaria", "costo"}


def test_factura_sin_rol_queda_como_sistema_y_no_bloquea(cliente):
    cliente.post("/api/facturas", json=_f("a", "150000", "a", "A"))
    d = cliente.post("/api/facturas", json=_f("b", "200000", "b", "B")).json()
    assert _aprobar(cliente, d).status_code == 200


def test_sirve_la_interfaz_sin_romper_api(tmp_path):
    (tmp_path / "index.html").write_text("<p>hola</p>", encoding="utf-8")
    ahora = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
    c = TestClient(crear_app(Sesiones(fabrica_de_servicios(lambda: ahora), lambda p: p), tmp_path / "x.json", tmp_path))
    assert c.get("/").text == "<p>hola</p>" and c.get("/api/marcador").json()["casos"] == 0
