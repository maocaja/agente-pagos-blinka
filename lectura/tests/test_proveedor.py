import json
from pathlib import Path

from lectura.adaptadores import validar_canonica
from lectura.proveedor import asignar_proveedor

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO = json.loads((RAIZ / "datos" / "registro-maestro.json").read_text(encoding="utf-8"))


def _fac(nombre, id_fiscal=""):
    return {"emisor": {"nombre": nombre, "id_fiscal": id_fiscal}}


def test_coincide_por_id_fiscal_aunque_el_registro_traiga_prefijo():
    r = asignar_proveedor(_fac("otro nombre", "900.000.111-0"), REGISTRO)
    assert (r["proveedor_id"], r["metodo"]) == ("prov_andino", "id_fiscal")


def test_coincide_por_nombre_normalizado():
    r = asignar_proveedor(_fac("Marta  Ruiz"), REGISTRO)
    assert (r["proveedor_id"], r["metodo"]) == ("prov_marta", "nombre")


def test_sin_coincidencia_queda_nulo_y_el_conflicto_no_decide():
    assert asignar_proveedor(_fac("Desconocido SA"), REGISTRO)["proveedor_id"] is None
    r = asignar_proveedor(_fac("MARTA RUIZ", "900.000.111-0"), REGISTRO)
    assert (r["proveedor_id"], r["metodo"]) == (None, "conflicto")


def test_18_extracciones_validan_con_proveedor_asignado():
    for ruta in sorted((RAIZ / "lectura" / "extracciones").glob("fac-*.json")):
        fac = json.loads(ruta.read_text(encoding="utf-8"))
        assert validar_canonica(fac) == [], ruta.name
        assert fac["proveedor_asignado"] == asignar_proveedor(fac, REGISTRO), ruta.name
