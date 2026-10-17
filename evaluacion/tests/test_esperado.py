import importlib.util
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
ESPERADOS = json.loads((RAIZ / "datos" / "esperado.json").read_text(encoding="utf-8"))
ESQUEMA = json.loads((RAIZ / "contrato" / "esperado.schema.json").read_text(encoding="utf-8"))

# validar.py del contrato: no hay jsonschema instalado en el entorno
_spec = importlib.util.spec_from_file_location("validar", RAIZ / "contrato" / "validar.py")
_validar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validar)

TRAMPAS = {
    "duplicado": "R2a",
    "beneficiario_nuevo": "R3",
    "no_cuadra_con_lo_acordado": "R5",
    "monto_sobre_el_limite": "R6",
    "presupuesto_insuficiente": "R9",
}


@pytest.mark.parametrize("e", ESPERADOS, ids=[e["caso"] for e in ESPERADOS])
def test_esperado_valido_con_dos_veredictos(e):
    assert _validar.validar(e, ESQUEMA) == []
    assert (RAIZ / "datos" / e["archivo"]).is_file()
    assert e["esperado_reglas"]["veredicto"] and e["esperado_extremo_a_extremo"]["veredicto"]


def test_cobertura_de_casos_trampa():
    fallan = {r for e in ESPERADOS for r in e["esperado_reglas"]["reglas_que_fallan"]}
    assert set(TRAMPAS.values()) <= fallan


def test_set_completo_y_f07_f17():
    por_caso = {e["caso"]: e for e in ESPERADOS}
    assert len(ESPERADOS) == 18 and len(por_caso) == 18
    assert por_caso["f_07"]["esperado_reglas"]["veredicto"] == "ESCALAR"
    assert por_caso["f_17"]["esperado_reglas"]["veredicto"] == "REGISTRAR"
    assert por_caso["f_18"]["esperado_reglas"]["veredicto"] == "FRENAR"
