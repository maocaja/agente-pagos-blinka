import copy
import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET

from nucleo.api.principal import fabrica_de_servicios
from nucleo.api.sesiones import Sesiones
from nucleo.api.app import crear_app
from nucleo.dominio.auditoria import armar_paquete
from nucleo.dominio.pain001 import orden_a_pain001
from nucleo.dominio.previa import previa_de_mandato
from nucleo.dominio.recibo import orden_desde_recibo
from nucleo.tests.test_t1 import factura, regla, servicio  # noqa: F401

_ruta = Path(__file__).resolve().parents[1] / "auditoria" / "verificar_paquete.py"
_spec = importlib.util.spec_from_file_location("verificar_paquete", _ruta)
script = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(script)


def test_explicacion_r4_con_que_hacer(servicio):
    d = servicio.decidir(factura(cuenta={"pais": "BR", "ultimos4": "9021"}))
    assert d["veredicto"] == "ESCALAR" and "9021" in d["explicacion"]
    assert d["que_hacer"] == "Confirmar con el proveedor antes de pagar."


def test_explicacion_r8_y_pagar_sin_que_hacer(servicio):
    f = factura(id="f_8", senales={"texto_dirigido_al_agente": {"p": 0.99, "origen": "pie de pagina"}})
    d = servicio.decidir(f)
    assert "pie de pagina" in d["explicacion"] and d["que_hacer"].startswith("Ignorar")


def test_pagar_no_lleva_que_hacer(servicio):
    assert servicio.decidir(factura())["que_hacer"] is None


def test_explicacion_r10_con_tope(servicio):
    servicio.m.p["tope_acumulado_proveedor"] = {"activo": True, "monto_menor": "1"}
    d = servicio.decidir(factura())
    assert regla(d, "R10")["estado"] == "falla" and "tope" in d["explicacion"]


def test_r1_escala_por_remitente_inconsistente(servicio):
    d = servicio.decidir(factura(senales={"remitente_inconsistente": {"motivo": "Reply-To distinto"}}))
    assert regla(d, "R1")["estado"] == "falla" and "Reply-To distinto" in d["explicacion"]


def test_previa_v2_contra_v1_cambia_lo_esperado(servicio):
    servicio.m.p["tope_acumulado_proveedor"] = {"activo": False, "monto_menor": "1"}
    d = servicio.decidir(factura())
    assert d["veredicto"] == "PAGAR"
    previa = previa_de_mandato(servicio, {"tope_acumulado_proveedor": {"activo": True, "monto_menor": "1"}})
    assert (previa["evaluadas"], previa["cambian"]) == (1, 1)
    assert (previa["cambios"][0]["antes"], previa["cambios"][0]["despues"]) == ("PAGAR", "ESCALAR")
    assert len(servicio.decisiones) == 1 and servicio.m.p["tope_acumulado_proveedor"]["activo"] is False


def _autorizada(servicio):
    d = servicio.decidir(factura())
    rec = servicio.recibos[d["recibo_id"]]
    assert servicio.verificar_orden(orden_desde_recibo(rec), rec)["autorizada"]
    return rec


def _clave(servicio):
    from nucleo.api.app import _clave_publica
    return _clave_publica(servicio)


def test_script_verifica_paquete_bueno_y_rechaza_alterado(servicio):
    _autorizada(servicio)
    paq = json.loads(json.dumps(armar_paquete(servicio, _clave(servicio), "2026-10-17T12:00:00Z")))
    assert script.verificar(paq) == []
    malo = copy.deepcopy(paq)
    malo["recibos"][0]["monto_menor"] = "1"
    assert script.verificar(malo) == [malo["recibos"][0]["id"]]


def test_pain001_bien_formado_y_simulada(servicio):
    rec = _autorizada(servicio)
    xml = orden_a_pain001(orden_desde_recibo(rec), "Proveedor", "2026-10-17T12:00:00Z")
    raiz = ET.fromstring(xml)
    assert b"SIMULADA" in xml and raiz.tag.endswith("Document")
    assert next(e for e in raiz.iter() if e.tag.endswith("InstdAmt")).get("Ccy") == rec["moneda"]


def test_rutas_paquete_y_pain001(ahora, tmp_path):
    ses = Sesiones(fabrica_de_servicios(lambda: ahora), lambda p: p + "_1")
    from fastapi.testclient import TestClient
    c = TestClient(crear_app(ses, tmp_path / "r.json", tmp_path / "dist"))
    d = c.post("/api/facturas", json=factura()).json()
    assert c.get(f"/api/ordenes/{d['recibo_id']}/pain001").status_code == 409
    rec = c.get(f"/api/recibos/{d['recibo_id']}").json()
    assert c.post("/api/guardian/verificar", json={"orden": orden_desde_recibo(rec), "recibo": rec}).json()["autorizada"]
    r = c.get(f"/api/ordenes/{rec['id']}/pain001")
    assert r.status_code == 200 and ET.fromstring(r.content) is not None
    assert script.verificar(c.get("/api/auditoria/paquete").json()) == []
