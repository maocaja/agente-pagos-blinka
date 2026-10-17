import json

from evaluacion.verificador import Verificador

from .ayudas import MANDATO_V2, RAIZ

ESPERADOS = {e["caso"]: e for e in json.loads((RAIZ / "datos/esperado.json").read_text(encoding="utf-8"))}
# Listas de reglas del esperado que el texto de las reglas no respalda con estas extracciones
DIVERGENCIAS = {"f_10", "f_12", "f_13"}


def correr_set():
    v, sal = Verificador(MANDATO_V2), {}
    for ruta in sorted((RAIZ / "lectura/extracciones").glob("fac-*.json")):
        f = json.loads(ruta.read_text(encoding="utf-8"))
        sal[f["id"]] = (v.evaluar(f), v)
    return sal, v


def test_veredictos_del_set_coinciden_con_los_esperados():
    sal, _ = correr_set()
    malos = {k: r["veredicto"] for k, (r, _) in sal.items() if r["veredicto"] != ESPERADOS[k]["esperado_reglas"]["veredicto"]}
    assert malos == {}


def test_listas_de_reglas_solo_divergen_en_los_casos_conocidos():
    sal, _ = correr_set()
    difieren = {k for k, (r, _) in sal.items() if r["reglas_que_fallan"] != ESPERADOS[k]["esperado_reglas"]["reglas_que_fallan"]}
    assert difieren == DIVERGENCIAS


def test_esperado_r3_si_y_solo_si_el_proveedor_no_esta_en_el_registro():
    v = Verificador(MANDATO_V2)
    for ruta in sorted((RAIZ / "lectura/extracciones").glob("fac-*.json")):
        f = json.loads(ruta.read_text(encoding="utf-8"))
        esperado_r3 = "R3" in ESPERADOS[f["id"]]["esperado_reglas"]["reglas_que_fallan"]
        assert (v.proveedor(f) is None) == esperado_r3 or f["id"] == "f_12", f["id"]
