import base64
import copy
import importlib.util
import itertools
import json
from datetime import datetime, timezone

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from nucleo.api.app import crear_app
from nucleo.api.sesiones import Sesiones
from nucleo.dominio.motor import decidir
from nucleo.dominio.reglas import REGLAS
from nucleo.dominio.mandato import RAIZ_CONTRATO, cargar_mandato, ruta_ejemplo
from nucleo.dominio.registro_maestro import RegistroMaestro
from nucleo.dominio.servicio import ServicioDecision
from nucleo.infra.firmador import FirmadorEd25519, verificar_firma
from nucleo.infra.libro import LibroSqlite
from nucleo.tests import REGISTRO

_spec = importlib.util.spec_from_file_location("validar_c", RAIZ_CONTRATO / "validar.py")
_v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v)


def esquema(nombre):
    return json.loads((RAIZ_CONTRATO / nombre).read_text(encoding="utf-8"))


def factura(**cambios):
    f = json.loads((RAIZ_CONTRATO / "ejemplos" / "factura-canonica.f11.json").read_text(encoding="utf-8"))
    f["cuenta"] = {"pais": "BR", "ultimos4": "8830"}
    for ruta, valor in cambios.items():
        *padres, hoja = ruta.split("__")
        o = f
        for p in padres:
            o = o[p]
        o[hoja] = valor
    return f


@pytest.fixture
def servicio(ahora):
    n = itertools.count(1)
    return ServicioDecision(
        cargar_mandato(ruta_ejemplo("v2")), RegistroMaestro.desde_archivo(REGISTRO, LibroSqlite()),
        lambda p: f"{p}_{next(n):03d}", lambda: f"n_{next(n):03d}", lambda: ahora,
        FirmadorEd25519(Ed25519PrivateKey.from_private_bytes(bytes(range(32))), "k1"))


def regla(d, id_):
    return next(r for r in d["reglas"] if r["id"] == id_)


def test_r2a_cumple_y_falla_por_numero_y_por_hash(servicio):
    assert regla(servicio.decidir(factura()), "R2a")["estado"] == "cumple"
    d = servicio.decidir(factura(id="f_12", documento__hash="b" * 64))
    assert (regla(d, "R2a")["estado"], d["veredicto"]) == ("falla", "FRENAR")
    assert regla(d, "R2a")["campo_origen"] == "referencias.numero_normalizado"
    d = servicio.decidir(factura(id="f_13", referencias__numero_normalizado="OTRO"))
    assert regla(d, "R2a")["campo_origen"] == "documento.hash"


def test_r3_registrado_no_registrado_y_bloqueado(servicio):
    assert regla(servicio.decidir(factura()), "R3")["estado"] == "cumple"
    d = servicio.decidir(factura(id="f_2", proveedor_asignado={"proveedor_id": None, "metodo": "ninguno", "pista": None}))
    assert (regla(d, "R3")["accion_si_falla"], regla(d, "R3")["aprobable"]) == ("ESCALAR", True)
    d = servicio.decidir(factura(id="f_3", proveedor_asignado={"proveedor_id": "prov_bloqueado", "metodo": "id_fiscal", "pista": None}))
    assert (regla(d, "R3")["accion_si_falla"], d["veredicto"]) == ("FRENAR", "FRENAR")


def test_r4_cuenta_igual_distinta_y_ausente(servicio):
    assert regla(servicio.decidir(factura()), "R4")["estado"] == "cumple"
    d = servicio.decidir(factura(id="f_2", cuenta={"pais": "CO", "ultimos4": "4821"}, documento__hash="c" * 64, referencias__numero_normalizado="Q"))
    assert regla(d, "R4")["estado"] == "falla" and "BR" in regla(d, "R4")["evidencia"]
    assert (d["veredicto"], d["estado"]) == ("ESCALAR", "pendiente")
    assert regla(servicio.decidir(factura(id="f_3", cuenta=None, documento__hash="d" * 64, referencias__numero_normalizado="Z")), "R4")["estado"] == "cumple"


def test_r6_bajo_umbral_sobre_umbral_y_sobre_tope(servicio):
    assert regla(servicio.decidir(factura()), "R6")["estado"] == "cumple"
    d = servicio.decidir(factura(id="f_2", montos__total_menor="2000000", referencias__numero_normalizado="A"))
    assert regla(d, "R6")["accion_si_falla"] == "ESCALAR"
    d = servicio.decidir(factura(id="f_3", montos__total_menor="6000000", referencias__numero_normalizado="B"))
    assert (regla(d, "R6")["accion_si_falla"], regla(d, "R6")["aprobable"]) == ("FRENAR", False)


def test_r6_redondea_al_alza_en_el_umbral(servicio):
    # 1500001 BRL menores = 300000,2 USD menores: al alza 300001 supera el umbral de 300000; a la baja pasaria.
    d = servicio.decidir(factura(montos__total_menor="1500001"))
    assert regla(d, "R6")["estado"] == "falla"


def test_precedencia_frenar_sobre_escalar_y_decision_valida(servicio):
    d = servicio.decidir(factura(cuenta={"pais": "CO", "ultimos4": "1"}, montos__total_menor="6000000"))
    assert d["veredicto"] == "FRENAR" and d["sin_orden"] and d["recibo_id"] is None
    assert regla(d, "R4")["estado"] == "falla"
    assert _v.validar(d, esquema("decision.schema.json")) == []


def test_falla_cerrado_moneda_sin_tasa_y_mandato_v1_sin_valores_quemados(servicio):
    d = servicio.decidir(factura(montos__moneda="EUR"))
    assert (d["veredicto"], regla(d, "R7")["aprobable"], regla(d, "R6")["estado"]) == ("FRENAR", False, "cumple")
    assert cargar_mandato(ruta_ejemplo("v1")).p["tope_acumulado_proveedor"]["activo"] is False
    assert cargar_mandato(ruta_ejemplo("v2")).p["tope_acumulado_proveedor"]["activo"] is True


def test_pagar_emite_recibo_firmado_valido_contra_esquema(servicio, ahora):
    d = servicio.decidir(factura())
    assert d["veredicto"] == "PAGAR" and d["estado"] == "con_recibo"
    r = servicio.recibos[d["recibo_id"]]
    assert _v.validar(r, esquema("recibo.schema.json")) == []
    assert (r["nonce"][:2], r["clave_version"], r["monto_base_menor"]) == ("n_", "k1", "150000")
    assert r["vence_en"] == "2026-10-18T12:00:00Z"
    assert verificar_firma(r, servicio.firmador.clave_publica)


def test_recibo_alterado_un_byte_no_verifica(servicio):
    d = servicio.decidir(factura())
    r = copy.deepcopy(servicio.recibos[d["recibo_id"]])
    r["monto_menor"] = "750001"
    assert not verificar_firma(r, servicio.firmador.clave_publica)


def _sin(regla_id):
    return {k: v for k, v in REGLAS.items() if k != regla_id}


def _decidir_sin(servicio, f, regla_id):
    return decidir(f, servicio.m, servicio.reg, servicio.ids, servicio.reloj, "autonomo", reglas=_sin(regla_id))


def test_falla_cerrado_regla_del_registro_no_implementada(servicio):
    d = _decidir_sin(servicio, factura(), "R1")
    faltante = next(r for r in d["reglas"] if r["evidencia"] == "Regla R1 no implementada")
    assert (d["veredicto"], d["recibo_id"], faltante["aprobable"]) == ("ESCALAR", None, False)
    assert d["motivo_corto"] == "Regla R1 no implementada"


def test_frenar_gana_a_escalar_aunque_falte_una_regla(servicio):
    f = factura(id="f_2", proveedor_asignado={"proveedor_id": "prov_bloqueado", "metodo": "id_fiscal", "pista": None})
    d = _decidir_sin(servicio, f, "R1")
    assert (d["veredicto"], d["estado"]) == ("FRENAR", "frenada")


def test_escalar_no_emite_recibo(servicio):
    d = servicio.decidir(factura(cuenta={"pais": "CO", "ultimos4": "1"}))
    assert d["veredicto"] == "ESCALAR" and d["recibo_id"] is None and not servicio.recibos


def test_recibo_con_otra_clave_no_verifica(servicio):
    r = servicio.recibos[servicio.decidir(factura())["recibo_id"]]
    otra = FirmadorEd25519(Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33))), "k2")
    assert not verificar_firma(r, otra.clave_publica)


def test_api_post_y_consulta_de_decision(servicio):
    c = TestClient(crear_app(Sesiones(lambda version: servicio, lambda p: p + "_1")))
    r = c.post("/api/facturas", json=factura())
    assert r.status_code == 201 and r.json()["veredicto"] == "PAGAR"
    did = r.json()["id"]
    assert c.get(f"/api/decisiones/{did}").json()["factura"]["id"] == "f_11"
    assert [d["id"] for d in c.get("/api/decisiones?estado=pagadas").json()] == [did]
    assert c.get("/api/mandato").json()["version"] == "v2"
    assert c.post("/api/facturas", json={"id": "x"}).status_code == 422
