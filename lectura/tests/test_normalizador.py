import pytest
from hypothesis import given, strategies as st

from lectura.normalizador import MonedaDesconocida, NumeroAmbiguo, normalizar_clave, normalizar_monto


def test_formatos_es_en_pt_llegan_al_mismo_entero():
    assert normalizar_monto("7.500,00", "BRL", "pt") == "750000"
    assert normalizar_monto("USD 2,000.00", "USD", "en") == "200000"
    assert normalizar_monto("6.000.000", "COP") == "600000000"
    assert normalizar_monto("12,50", "USD") == "1250"
    assert normalizar_monto("1.500", "CLP", "es") == "1500"


def test_ambiguo_o_invalido_no_se_adivina():
    with pytest.raises(NumeroAmbiguo):
        normalizar_monto("1.200", "USD")
    for malo in ["-300.000", "9?0", "1.2.3,4,5", "12,345.67,8"]:
        with pytest.raises(ValueError):
            normalizar_monto(malo, "COP", "es")
    with pytest.raises(MonedaDesconocida):
        normalizar_monto("10", "XXX")
    with pytest.raises(ValueError):
        normalizar_monto("10,5", "CLP", "es")


def test_clave_normalizada_y_ida_vuelta_de_enteros():
    assert normalizar_clave("px 2301") == normalizar_clave("PX-2301") == "PX2301"
    assert normalizar_clave("Diseño S.A.") == "DISENOSA"
    assert normalizar_clave("INV-0412") == "INV0412"

    @given(st.integers(min_value=0, max_value=10**12))
    def ida_vuelta(n):
        impreso = f"{n // 100:,}.{n % 100:02d}"
        assert normalizar_monto(impreso, "USD", "en") == str(n)

    ida_vuelta()
