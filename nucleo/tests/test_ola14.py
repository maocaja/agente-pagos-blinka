from nucleo.dominio.recibo import orden_desde_recibo
from nucleo.tests.test_ola4 import _aprobar, _escalada, _f, cliente  # noqa: F401  (fixture)


def test_ciclo_coherente_con_las_reservas_tras_dos_facturas(cliente):
    a = cliente.post("/api/facturas", json=_f("a", "150000", "a", "A")).json()
    b = cliente.post("/api/facturas", json=_f("b", "100000", "b", "B")).json()
    reservado = sum(int(cliente.get(f"/api/recibos/{d['recibo_id']}").json()["monto_base_menor"])
                    for d in (a, b) if d["recibo_id"])
    c = cliente.get("/api/ciclo").json()
    assert c["ciclo_id"] == "2026-10" and c["empresa"] and c["moneda"] == "USD" and reservado > 0
    assert (c["reservado_menor"], c["disponible_menor"]) == (str(reservado), str(int(c["presupuesto_menor"]) - reservado))
    assert len(c["actividad"]) == 2 and c["actividad"][0].keys() == {"hora", "texto"}


def test_historial_tras_aprobar_y_tras_rechazar(cliente):
    d = _escalada(cliente)
    nueva = _aprobar(cliente, d).json()["decision"]
    eventos = lambda i: [e["evento"] for e in cliente.get(f"/api/decisiones/{i}").json()["historial"]]
    assert eventos(d["id"]) == ["recibida", "decidida", "reevaluada"]
    assert eventos(nueva["id"]) == ["recibida", "decidida", "reevaluada", "decidida", "aprobada"]
    otra = cliente.post("/api/facturas", json=_f("c", "250000", "d", "C"), headers={"X-Rol": "analista"}).json()
    cliente.post(f"/api/decisiones/{otra['id']}/rechazar", json={"nota": "no corresponde"}, headers={"X-Rol": "cfo"})
    ultimo = cliente.get(f"/api/decisiones/{otra['id']}").json()["historial"][-1]
    assert (ultimo["evento"], ultimo["actor"], ultimo["nota"]) == ("rechazada", "cfo", "no corresponde")


def test_estado_orden_nunca_es_de_pago_confirmado(cliente):
    d = cliente.post("/api/facturas", json=_f("a", "150000", "a", "A")).json()
    rec = cliente.get(f"/api/recibos/{d['recibo_id']}").json()
    estado = lambda: cliente.get(f"/api/decisiones/{d['id']}").json()["estado_orden"]
    assert estado() is None
    cliente.post("/api/guardian/verificar", json={"orden": orden_desde_recibo(rec), "recibo": rec})
    visto = [estado()]
    cliente.get(f"/api/ordenes/{rec['id']}/pain001")
    visto.append(estado())
    assert visto == ["autorizada", "orden_simulada_emitida"]
