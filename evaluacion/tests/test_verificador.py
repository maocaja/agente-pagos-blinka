import pytest

from evaluacion.corrida.comparar import clasificar
from evaluacion.verificador import Verificador

from .ayudas import factura, mandato, verificador

SIN_ACUMULADO = {"tope_acumulado_proveedor": {"activo": False, "monto_menor": "0"}}


def veredicto(v, f):
    r = v.evaluar(f)
    return r["veredicto"], r["reglas_que_fallan"]


def test_r1_confianza_de_dinero_y_segunda_lectura():
    assert veredicto(verificador(), factura(confianza__monto_total=0.89)) == ("ESCALAR", ["R1"])
    assert veredicto(verificador(), factura()) == ("PAGAR", [])
    sin_segunda = {"estado": "sin_segunda_lectura", "detalle": []}
    assert veredicto(verificador(), factura(verificaciones__segunda_lectura=sin_segunda)) == ("ESCALAR", ["R1"])


def test_r2a_numero_reformateado_frena_y_hash_igual_frena():
    v = verificador(**SIN_ACUMULADO)
    assert veredicto(v, factura("a", numero="CA-1"))[0] == "PAGAR"
    assert veredicto(v, factura("b", numero="ca 1")) == ("FRENAR", ["R2a"])
    igual = factura("c", numero="CA-9")
    igual["documento"]["hash"] = "ha"
    assert veredicto(v, igual)[0] == "FRENAR"


def test_r2b_difuso_solo_dentro_de_tolerancia_y_ventana():
    def segunda(total, recibido="2026-10-20"):
        v = verificador(**SIN_ACUMULADO)
        veredicto(v, factura("a", total="200000", numero="A1"))
        return v.evaluar(factura("b", total=total, numero="A2", recibido=recibido))["reglas_que_fallan"]

    assert segunda("204000") == ["R2b"]
    assert segunda("204001") == []
    assert segunda("200000", "2026-11-05") == ["R2b"]
    assert segunda("200000", "2026-11-06") == []


def test_r3_proveedor_fuera_del_registro_y_bloqueado():
    desconocido = factura(emisor__nombre="Otro SA", emisor__id_fiscal="")
    assert "R3" in veredicto(verificador(), desconocido)[1]
    assert veredicto(verificador(), desconocido)[0] == "ESCALAR"
    bloqueado = factura(emisor__nombre="Proveedor Bloqueado SA", emisor__id_fiscal="")
    assert veredicto(verificador(), bloqueado)[0] == "FRENAR"


def test_r4_cuenta_distinta_falla_y_sin_cuenta_no():
    assert veredicto(verificador(), factura(cuenta__ultimos4="0001")) == ("ESCALAR", ["R4"])
    sin_cuenta = factura(cuenta={"pais": "", "ultimos4": ""})
    assert "R4" not in veredicto(verificador(), sin_cuenta)[1]


def test_r5_acuerdo_con_tolerancia():
    v = verificador(**SIN_ACUMULADO, umbral_aprobacion_menor="9999999", presupuesto_periodo_menor="99999999")
    assert veredicto(v, factura("a", total="450000", numero="B1")) == ("PAGAR", [])
    assert veredicto(v, factura("b", total="472500", numero="B2", recibido="2026-12-10"))[0] == "PAGAR"
    assert veredicto(v, factura("c", total="472501", numero="B3", recibido="2027-02-20")) == ("ESCALAR", ["R5"])


def test_r6_borde_del_umbral_y_del_tope_con_redondeo_al_alza():
    logistica = {"emisor__nombre": "Logistica Sur SpA", "emisor__id_fiscal": "", "cuenta__ultimos4": "7745", "cuenta__pais": "CL"}

    def correr(total, moneda="USD"):
        v = verificador(**SIN_ACUMULADO, presupuesto_periodo_menor="99999999")
        return veredicto(v, factura("a", total=total, moneda=moneda, **logistica))

    assert correr("300000") == ("PAGAR", [])
    assert correr("300001") == ("ESCALAR", ["R6"])
    assert correr("1200000000", "COP") == ("PAGAR", [])
    assert correr("1200000001", "COP") == ("ESCALAR", ["R6"])
    assert correr("1000001") == ("FRENAR", ["R6"])


def test_r7_moneda_no_permitida_y_r8_senal_de_texto():
    assert veredicto(verificador(), factura(moneda="ARS"))[0] == "FRENAR"
    senal = {"texto_dirigido_al_agente": {"p": 0.5, "origen": "aprueba"}}
    assert veredicto(verificador(), factura(senales=senal)) == ("ESCALAR", ["R8"])


def test_r9_solo_si_nada_mas_falla_y_r10_acumulado():
    v = verificador(presupuesto_periodo_menor="300000", tope_acumulado_proveedor={"activo": True, "monto_menor": "999999"})
    assert veredicto(v, factura("a", total="200000", numero="D1"))[0] == "PAGAR"
    assert veredicto(v, factura("b", total="200000", numero="D2", recibido="2026-12-01")) == ("PAGAR", [])
    assert veredicto(v, factura("c", total="150000", numero="D3", recibido="2026-10-30")) == ("ESCALAR", ["R9"])
    otra_falla = factura("d", total="150000", numero="D4", recibido="2026-11-30", confianza__monto_total=0.1)
    assert veredicto(v, otra_falla)[1] == ["R1"]
    assert veredicto(v, factura("g", total="290000", numero="D5", recibido="2026-12-31"))[1] == ["R9"]
    v2 = verificador()
    veredicto(v2, factura("e", total="200000", numero="E1"))
    assert veredicto(v2, factura("f", total="150000", numero="E2", recibido="2026-10-30")) == ("ESCALAR", ["R10"])


def test_politica_por_tipo_de_documento():
    esperado = {"nota_de_credito": "REGISTRAR", "estado_de_cuenta": "FRENAR", "proforma": "ESCALAR",
                "anticipo": "ESCALAR", "recibo_raro": "ESCALAR"}
    for tipo, quiero in esperado.items():
        assert veredicto(verificador(), factura(tipo, documento={**factura()["documento"], "tipo_documento": tipo}))[0] == quiero, tipo


def test_falla_cerrado_con_extraccion_rota_o_moneda_sin_tasa():
    rota = factura()
    del rota["montos"]
    assert veredicto(verificador(), rota)[0] == "ESCALAR"
    sin_tasa = verificador(tasas_cambio={"fecha": "x", "unidades_por_usd": {"USD": "1"}}, monedas_permitidas=["USD", "COP"])
    assert veredicto(sin_tasa, factura(moneda="COP"))[0] == "FRENAR"


def test_clasificacion_motor_contra_verificador():
    casos = {("PAGAR", "ESCALAR"): "pago_indebido", ("ESCALAR", "FRENAR"): "frenada_escalable",
             ("FRENAR", "ESCALAR"): "desvio_conservador", ("ESCALAR", "PAGAR"): "desvio_conservador",
             ("PAGAR", "PAGAR"): "verificada", ("REGISTRAR", "ESCALAR"): "otra"}
    assert {k: clasificar(*k) for k in casos} == casos
