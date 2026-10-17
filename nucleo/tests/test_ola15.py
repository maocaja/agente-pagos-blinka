from nucleo.dominio.dinero import importe
from nucleo.dominio.mandato import cargar_mandato, ruta_ejemplo
from nucleo.tests.test_ola5 import _cliente_muestras, _con_sesion


def test_foto_de_cuenta_cambiada_tiene_r4_como_razon_principal(tmp_path):
    c = _cliente_muestras(tmp_path)
    d = c.post("/api/muestras/foto-04-andino-cambio-cuenta/cargar", headers=_con_sesion(c)).json()
    assert d["explicacion"].startswith("La cuenta") and "Además:" in d["explicacion"]
    assert d["que_hacer"].startswith("Confirmar la cuenta con el proveedor")
    assert "unidades menores" not in d["explicacion"]
    actividad = c.get("/api/ciclo", headers=_con_sesion(c)).json()["actividad"]
    assert all("_" not in a["texto"] for a in actividad)


def test_importe_legible_en_moneda_base():
    m = cargar_mandato(ruta_ejemplo("v1"))
    assert importe(357000, m) == "USD 3.570" and importe(1250, m) == "USD 12,50"


def test_archivo_original_se_sirve_y_rechaza_rutas_ajenas(tmp_path):
    c = _cliente_muestras(tmp_path)
    r = c.get("/api/muestras/foto-04-andino-cambio-cuenta/archivo")
    assert r.status_code == 200 and r.headers["content-type"] == "image/jpeg"
    assert c.get("/api/muestras/..%2F..%2Fcontrato%2Fmonedas.json/archivo").status_code == 404
    assert c.get("/api/muestras/no-existe/archivo").status_code == 404
