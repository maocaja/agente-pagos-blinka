from types import SimpleNamespace

from nucleo.dominio.dinero import base_de
from nucleo.dominio.motor import evaluar_reglas
from nucleo.dominio.recibo import orden_desde_recibo
from nucleo.dominio.reglas import REGLAS
from nucleo.tests.test_ola2 import _aprobacion, _nuevo_recibo
from nucleo.tests.test_t1 import factura, servicio  # noqa: F401  (fixture)


def _regla_rota(f, m, reg):
    raise ValueError("dato corrupto")


def test_regla_que_lanza_excepcion_falla_cerrado_a_escalar(servicio):
    res = dict(evaluar_reglas(factura(), servicio.m, servicio.reg, {**REGLAS, "R9": _regla_rota}))
    assert (res["R9"].estado, res["R9"].accion, res["R9"].aprobable) == ("falla", "ESCALAR", False)


def test_r9_limite_exacto_del_presupuesto(servicio):
    f = factura()
    base = base_de(f, servicio.m)
    reg = SimpleNamespace(libro=SimpleNamespace(acumulado=lambda ciclo: 0))

    def con_presupuesto(p):
        m = servicio.m.__class__(servicio.m.version, servicio.m.estado, {**servicio.m.p, "presupuesto_periodo_menor": str(p)}, servicio.m.doc)
        return REGLAS["R9"](f, m, reg).estado

    assert (con_presupuesto(base), con_presupuesto(base - 1)) == ("cumple", "falla")


def test_guardian_deniega_frenar_aunque_traiga_aprobacion_valida(servicio):
    r = _nuevo_recibo(servicio, veredicto="FRENAR", modo_autonomia="sombra")
    res = servicio.verificar_orden(orden_desde_recibo(r), r, _aprobacion(servicio, r, "2026-10-18T11:00:00Z"))
    assert (res["autorizada"], res["verificaciones"][3]["estado"]) == (False, "falla")


def test_guardian_deniega_recibo_vencido_con_el_reloj_inyectado(servicio):
    r = _nuevo_recibo(servicio, vence_en="2026-10-17T11:00:00Z")
    res = servicio.verificar_orden(orden_desde_recibo(r), r)
    assert (res["autorizada"], res["verificaciones"][4]["estado"]) == (False, "falla")
