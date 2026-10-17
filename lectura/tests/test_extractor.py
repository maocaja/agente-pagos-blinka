import copy
import hashlib
import json
import urllib.error
from pathlib import Path

import pytest

from lectura.extractor import (ClienteAnthropic, ClienteCongelado, ContadorGasto, Extractor, FallaCliente,
                               Respuesta, cargar_modelos)

RAIZ = Path(__file__).resolve().parents[2]
FACTURAS = RAIZ / "datos" / "facturas"
MODELOS = cargar_modelos()


def _texto(prefijo):
    return next(FACTURAS.glob(f"{prefijo}-*.txt")).read_text(encoding="utf-8")


def _extractor(cliente, tope=10_000_000):
    return Extractor(cliente, ContadorGasto(tope, MODELOS), MODELOS)


class Falso:
    def __init__(self, contenido=None, falla=None, ti=1000, to=500):
        self.contenido, self.falla, self.ti, self.to = contenido, falla, ti, to

    def leer(self, modelo_id, instruccion, texto):
        if self.falla:
            raise self.falla
        return Respuesta(self.contenido, self.ti, self.to)


def _congelada(prefijo):
    return ClienteCongelado().leer("x", "", _texto(prefijo)).contenido


def test_iva_aparece_como_linea_y_las_lineas_suman():
    for n in ("14", "15", "16"):
        f = json.loads((RAIZ / "lectura" / "extracciones" / f"fac-{n}.json").read_text(encoding="utf-8"))
        m = f["montos"]
        assert m["lineas"][-1]["descripcion"].startswith(("IVA", "Impuestos"))
        assert int(m["suma_lineas_menor"]) == sum(int(x["total_menor"]) for x in m["lineas"])
        # fac-14 no cuadra a proposito: el recargo por mora no es una linea.
        assert (m["suma_lineas_menor"] == m["total_menor"]) == (n != "14")


def test_extraccion_guarda_version_hash_modelo_y_costo():
    r = _extractor(Falso(_congelada("fac-16"))).extraer(_texto("fac-16"))
    meta = r.factura["meta"]
    prompt = (RAIZ / "lectura" / "prompts" / "extractor.v1.md").read_bytes()
    assert meta["prompt_version"] == "v1" and meta["prompt_hash"] == hashlib.sha256(prompt).hexdigest()
    assert meta["modelo"] == "claude-haiku-5-5" and meta["costo_microusd"] == "350"
    assert r.factura["verificaciones"] == {"cita_evidencia": "ok", "moneda": "ok", "suma_lineas": "ok"}


def test_cliente_congelado_sin_lectura_escala():
    r = _extractor(ClienteCongelado()).extraer("factura inventada")
    assert r.escala and r.motivo == "sin_lectura_congelada"


def test_tope_de_gasto_escala_antes_y_despues_de_superarlo():
    ex = _extractor(Falso(_congelada("fac-16")), tope=300)
    assert ex.extraer(_texto("fac-16")).motivo == "tope_de_gasto"
    assert _extractor(Falso(_congelada("fac-16")), tope=350).extraer(_texto("fac-16")).escala is False
    ex = _extractor(Falso(_congelada("fac-16")), tope=350)
    ex.extraer(_texto("fac-16"))
    assert ex.extraer(_texto("fac-16")).motivo == "tope_de_gasto"


def test_cada_falla_del_cliente_escala_y_cuenta_sus_tokens():
    for motivo in ("refusal", "truncado", "json_invalido", "timeout", "http_4xx"):
        ex = _extractor(Falso(falla=FallaCliente(motivo, 100, 50)))
        r = ex.extraer("texto")
        assert r.escala and r.motivo == motivo and ex._contador.tokens_entrada == 100


def test_cita_ausente_y_moneda_invalida_escalan():
    mala = copy.deepcopy(_congelada("fac-16"))
    mala["evidencia"]["numero_factura"] = "CV-99 inexistente"
    assert _extractor(Falso(mala)).extraer(_texto("fac-16")).motivo == "cita_no_encontrada"
    mala = copy.deepcopy(_congelada("fac-16"))
    mala["moneda"] = "OTRA"
    assert _extractor(Falso(mala)).extraer(_texto("fac-16")).motivo == "moneda_invalida"


def test_salida_fuera_del_esquema_y_totales_que_no_cuadran():
    assert _extractor(Falso({"x": 1})).extraer("t").motivo == "json_invalido"
    r = _extractor(Falso(_congelada("fac-14"))).extraer(_texto("fac-14"))
    assert r.factura["verificaciones"]["suma_lineas"] == "falla"


def test_cliente_real_sin_clave_timeout_y_4xx_sin_red(monkeypatch):
    def urlopen(*a, **k):
        raise error

    monkeypatch.setattr("urllib.request.urlopen", urlopen)
    cli = ClienteAnthropic("https://x.invalid", 100, 1, 0, entorno={"ANTHROPIC_API_KEY": "k"})
    error = TimeoutError()
    with pytest.raises(FallaCliente) as e:
        cli.leer("m", "i", "t")
    assert e.value.motivo == "timeout"
    error = urllib.error.HTTPError("u", 400, "bad", {}, None)
    with pytest.raises(FallaCliente) as e:
        cli.leer("m", "i", "t")
    assert e.value.motivo == "http_4xx"
    with pytest.raises(FallaCliente) as e:
        ClienteAnthropic("https://x.invalid", 100, 1, 0, entorno={}).leer("m", "i", "t")
    assert e.value.motivo == "sin_clave"
