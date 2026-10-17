import base64
import copy
import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from nucleo.api.app import crear_app
from nucleo.api.principal import fabrica_de_servicios
from nucleo.api.sesiones import Sesiones
from nucleo.dominio.errores import FallaCerrada
from nucleo.dominio.mandato import RAIZ_CONTRATO
from nucleo.dominio.motor import ids_del_registro
from nucleo.dominio.recibo import orden_desde_recibo, serializar
from nucleo.dominio.reglas import REGLAS
from nucleo.infra.libro import LibroSqlite
from nucleo.tests.test_t1 import factura, regla, servicio  # noqa: F401  (fixture)
from lectura.proveedor import asignar_proveedor

RAIZ = RAIZ_CONTRATO.parent
REGISTRO = json.loads((RAIZ / "datos" / "registro-maestro.json").read_text(encoding="utf-8"))
ESPERADO = {x["caso"]: x["esperado_reglas"] for x in json.loads((RAIZ / "datos" / "esperado.json").read_text(encoding="utf-8"))}
EXTRACCIONES = sorted((RAIZ / "lectura" / "extracciones").glob("fac-*.json"))

# Discrepancias con datos/esperado.json (no se edita): f_09, prov_logos si esta en el registro; f_10 y f_13, R10 aplica
# a todo proveedor; f_12, sin proveedor fallan R3 y R5; f_10, f_15 y f_16, R1 exige que las lineas sumen el total.
VEREDICTO_DISTINTO = {}
REGLAS_DISTINTAS = {
    "f_10": ["R1", "R5", "R10"], "f_12": ["R1", "R3", "R5"], "f_13": ["R6", "R10"],
    "f_15": ["R1", "R4"], "f_16": ["R1"],
}


@pytest.fixture(scope="module")
def corrida(request):
    ahora = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
    s = fabrica_de_servicios(lambda: ahora)("v2")
    salida = {}
    for ruta in EXTRACCIONES:
        f = json.loads(ruta.read_text(encoding="utf-8"))
        f["proveedor_asignado"] = f["proveedor_asignado"] if f["proveedor_asignado"]["proveedor_id"] else asignar_proveedor(f, REGISTRO)
        salida[f["id"]] = s.decidir(f)
    return salida


@pytest.mark.parametrize("caso", sorted(ESPERADO))
def test_18_facturas_contra_esperado(corrida, caso):
    d = corrida[caso]
    fallan = [r["id"] for r in d["reglas"] if r["estado"] == "falla"]
    assert d["veredicto"] == VEREDICTO_DISTINTO.get(caso, ESPERADO[caso]["veredicto"])
    assert fallan == REGLAS_DISTINTAS.get(caso, ESPERADO[caso]["reglas_que_fallan"])


def test_las_11_reglas_del_registro_estan_implementadas():
    assert set(REGLAS) == set(ids_del_registro()) and len(REGLAS) == 11


def _nuevo_recibo(servicio, **cambios):
    r = servicio.recibos[servicio.decidir(factura())["recibo_id"]]
    r = {**copy.deepcopy(r), **cambios}
    r["firma"] = base64.b64encode(servicio.firmador.firmar(serializar(r))).decode("ascii")
    return r


def test_guardian_rechaza_firma_alterada_con_la_respuesta_del_contrato(servicio):
    r = copy.deepcopy(servicio.recibos[servicio.decidir(factura())["recibo_id"]])
    r["monto_menor"] = "750001"
    res = servicio.verificar_orden(orden_desde_recibo(r), r)
    assert res == json.loads((RAIZ_CONTRATO / "ejemplos" / "guardian.rechazo.json").read_text(encoding="utf-8"))


def test_guardian_autoriza_una_vez_y_el_nonce_reutilizado_se_rechaza(servicio):
    d = servicio.decidir(factura())
    r = servicio.recibos[d["recibo_id"]]
    assert servicio.verificar_orden(orden_desde_recibo(r), r)["autorizada"] is True
    assert d["estado"] == "autorizada"
    res = servicio.verificar_orden(orden_desde_recibo(r), r)
    assert (res["autorizada"], res["verificaciones"][5]["estado"]) == (False, "falla")


def test_guardian_hash_y_orden_distintos_al_recibo(servicio):
    r = _nuevo_recibo(servicio, hash_documento="0" * 64)
    assert servicio.verificar_orden(orden_desde_recibo(r), r)["verificaciones"][1]["estado"] == "falla"
    r = _nuevo_recibo(servicio)
    orden = {**orden_desde_recibo(r), "beneficiario_id": "prov_otro"}
    res = servicio.verificar_orden(orden, r)
    assert [v["estado"] for v in res["verificaciones"][:4]] == ["ok", "ok", "falla", "no_evaluada"]


def _aprobacion(servicio, recibo, vence_en):
    ap = {"accion": "aprobar", "recibo_id": recibo["id"], "vence_en": vence_en}
    ap["firma"] = base64.b64encode(servicio.firmador.firmar(serializar(ap))).decode("ascii")
    return ap


def test_guardian_veredicto_y_modo_exigen_aprobacion_firmada(servicio):
    frenado = _nuevo_recibo(servicio, veredicto="FRENAR")
    assert servicio.verificar_orden(orden_desde_recibo(frenado), frenado)["verificaciones"][3]["estado"] == "falla"
    sombra = _nuevo_recibo(servicio, modo_autonomia="sombra")
    assert servicio.verificar_orden(orden_desde_recibo(sombra), sombra)["verificaciones"][3]["estado"] == "falla"
    vencida = _nuevo_recibo(servicio, modo_autonomia="sombra")
    ap = _aprobacion(servicio, vencida, "2026-10-17T11:00:00Z")
    assert servicio.verificar_orden(orden_desde_recibo(vencida), vencida, ap)["autorizada"] is False
    buena = _nuevo_recibo(servicio, modo_autonomia="sombra")
    ap = _aprobacion(servicio, buena, "2026-10-18T11:00:00Z")
    assert servicio.verificar_orden(orden_desde_recibo(buena), buena, ap)["autorizada"] is True


def test_guardian_mandato_vencido_deniega_y_libera_la_reserva(servicio):
    d = servicio.decidir(factura())
    r = servicio.recibos[d["recibo_id"]]
    antes = servicio.libro.acumulado("2026-10")
    servicio.m = servicio.m.__class__("v3", servicio.m.estado, servicio.m.p, servicio.m.doc)
    res = servicio.verificar_orden(orden_desde_recibo(r), r)
    assert res["verificaciones"][4]["estado"] == "falla" and d["estado"] == "denegada"
    assert (antes, servicio.libro.acumulado("2026-10")) == (150000, 0)
    assert servicio.libro.consumir_nonce(r["nonce"], r["id"]) is False


def test_reserva_atomica_con_nonce_y_tope_del_periodo():
    libro = LibroSqlite()
    libro.reservar("r1", "n1", "prov_a", "2026-10", 600000, 900000)
    with pytest.raises(FallaCerrada):
        libro.reservar("r2", "n2", "prov_a", "2026-10", 600000, 900000)
    with pytest.raises(FallaCerrada):
        libro.reservar("r3", "n1", "prov_a", "2026-10", 1, 900000)
    assert libro.acumulado("2026-10") == 600000


def test_registro_de_solo_adicion_no_admite_update_ni_delete():
    libro = LibroSqlite()
    libro.reservar("r1", "n1", "prov_a", "2026-10", 5, 10)
    for sql in ("UPDATE movimientos SET monto = 0", "DELETE FROM movimientos"):
        with pytest.raises(sqlite3.DatabaseError):
            libro._c.execute(sql)


def test_mandato_v1_sin_tope_acumulado_y_v2_con_facturas_partidas():
    ahora = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
    resultados = {}
    for version in ("v1", "v2"):
        s = fabrica_de_servicios(lambda: ahora)(version)
        cloud = {"proveedor_id": "prov_cloud", "metodo": "id_fiscal", "pista": None}
        base = dict(montos__moneda="USD", proveedor_asignado=cloud, cuenta={"pais": "US", "ultimos4": "6052"})
        a = s.decidir(factura(id="a", montos__total_menor="150000", montos__suma_lineas_menor="150000", documento__hash="a" * 64, referencias__numero_normalizado="A", **base))
        b = s.decidir(factura(id="b", montos__total_menor="200000", montos__suma_lineas_menor="200000", documento__hash="b" * 64, referencias__numero_normalizado="B", **base))
        resultados[version] = (a["veredicto"], b["veredicto"], regla(b, "R10")["estado"])
    assert resultados == {"v1": ("PAGAR", "PAGAR", "cumple"), "v2": ("PAGAR", "ESCALAR", "falla")}


def test_tipo_desconocido_o_dato_roto_nunca_paga(servicio):
    d = servicio.decidir(factura(documento__tipo_documento="recibo_raro"))
    assert (d["veredicto"], d["recibo_id"]) == ("ESCALAR", None)
    roto = factura(id="f_2", montos__total_menor="no-es-numero")
    assert servicio.decidir(roto)["veredicto"] != "PAGAR"


def test_api_sesion_guardian_e_idempotencia():
    ahora = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
    c = TestClient(crear_app(Sesiones(fabrica_de_servicios(lambda: ahora), lambda p: p + "_1")))
    r = c.post("/api/sesion?mandato=v1")
    sid = r.json()["sesion_id"]
    assert (r.status_code, r.json()["mandato_version"], r.json()["ciclo_id"]) == (201, "v1", "2026-10")
    h = {"X-Sesion-Id": sid, "Idempotency-Key": "k1"}
    d1, d2 = (c.post("/api/facturas", json=factura(), headers=h).json() for _ in range(2))
    assert d1["id"] == d2["id"] and len(c.get("/api/decisiones", headers=h).json()) == 1
    rec = c.get(f"/api/recibos/{d1['recibo_id']}", headers=h).json()
    res = c.post("/api/guardian/verificar", json={"orden": orden_desde_recibo(rec), "recibo": rec}, headers=h).json()
    assert res["autorizada"] is True and len(res["verificaciones"]) == 6
    assert c.get("/api/proveedores", headers=h).json()[0].keys() >= {"id", "nombre", "estado", "nivel_autonomia"}
    assert c.get("/api/decisiones", headers={"X-Sesion-Id": "s_inexistente"}).status_code == 401
    assert c.post("/api/sesion/reiniciar", headers=h).status_code == 200
    assert c.get("/api/decisiones", headers=h).json() == []
