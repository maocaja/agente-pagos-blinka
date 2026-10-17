import json

from evaluacion.corrida_documentos import correr

from .ayudas import RAIZ

IMAGEN_O_TRAMPA = {"d_03", "d_04", "d_05", "d_06", "d_07", "d_10", "d_11", "d_13", "d_14", "d_15"}
SUBCONJUNTO = {"d_02", "d_03", "d_07", "d_10"}


def test_subconjunto_corre_sin_red_y_escribe_la_salida(tmp_path):
    r = correr(tmp_path, SUBCONJUNTO)
    assert r["documentos"] == len(SUBCONJUNTO)
    assert json.loads((tmp_path / "documentos.json").read_text(encoding="utf-8")) == r


def test_salida_tiene_la_forma_esperada(tmp_path):
    r = correr(tmp_path, SUBCONJUNTO)
    assert {"mandato_version", "documentos", "coinciden", "pagados", "discrepancias", "casos"} <= set(r)
    for c in r["casos"]:
        assert {"caso", "archivo", "motor", "esperado_reglas", "coincide", "motivos"} <= set(c)
        assert c["coincide"] == (not c["motivos"])


def test_ningun_documento_de_imagen_o_trampa_da_pagar(tmp_path):
    r = correr(tmp_path, IMAGEN_O_TRAMPA)
    assert set(r["pagados"]).isdisjoint(IMAGEN_O_TRAMPA), (RAIZ, r["pagados"])
