import hashlib
import json
import re
from pathlib import Path

from lectura.adaptadores import validar_canonica

RAIZ = Path(__file__).resolve().parents[2]


def test_18_extracciones_validan_y_sus_citas_estan_en_el_texto():
    archivos = sorted((RAIZ / "lectura" / "extracciones").glob("fac-*.json"))
    assert len(archivos) == 18
    for ruta in archivos:
        fac = json.loads(ruta.read_text(encoding="utf-8"))
        assert validar_canonica(fac) == [], ruta.name
        origen = next((RAIZ / "datos" / "facturas").glob(f"{ruta.stem}-*.txt"))
        texto = re.sub(r"\s+", " ", origen.read_text(encoding="utf-8"))
        assert fac["documento"]["hash"] == hashlib.sha256(origen.read_bytes()).hexdigest(), ruta.name
        for campo, cita in fac["evidencia"].items():
            assert re.sub(r"\s+", " ", cita) in texto, (ruta.name, campo)
