import importlib.util
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
ESPERADOS = json.loads((RAIZ / "datos" / "esperado-documentos.json").read_text(encoding="utf-8"))
MANIFIESTO = json.loads((RAIZ / "datos" / "documentos" / "manifiesto.json").read_text(encoding="utf-8"))
ESQUEMA = json.loads((RAIZ / "contrato" / "esperado.schema.json").read_text(encoding="utf-8"))

_spec = importlib.util.spec_from_file_location("validar", RAIZ / "contrato" / "validar.py")
_validar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validar)


@pytest.mark.parametrize("e", ESPERADOS, ids=[e["caso"] for e in ESPERADOS])
def test_esperado_de_documento_valido(e):
    assert _validar.validar(e, ESQUEMA) == []
    assert (RAIZ / "datos" / e["archivo"]).is_file()


def test_cada_documento_del_manifiesto_tiene_esperado():
    esperados = {e["archivo"] for e in ESPERADOS}
    assert esperados == {"documentos/" + d["archivo"] for d in MANIFIESTO["documentos"]}
    assert len({e["caso"] for e in ESPERADOS}) == len(ESPERADOS)


def test_imagen_nunca_paga_y_trampas_no_pagan():
    formato = {"documentos/" + d["archivo"]: d for d in MANIFIESTO["documentos"]}
    for e in ESPERADOS:
        d = formato[e["archivo"]]
        if d["formato"] in ("jpg", "pdf-escaneado") or d["trampa"].startswith(("manipulacion", "cambio de cuenta")):
            assert e["esperado_extremo_a_extremo"]["veredicto"] in ("ESCALAR", "FRENAR"), e["caso"]
            assert e["esperado_reglas"]["veredicto"] != "PAGAR" or d["formato"] in ("jpg", "pdf-escaneado")
