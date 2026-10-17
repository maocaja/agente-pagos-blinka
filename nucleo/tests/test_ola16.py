from nucleo.tests.test_ola4 import _escalada, _f, cliente  # noqa: F401  (fixture)

ANALISTA = {"X-Rol": "analista"}


def test_autorizar_pagar_habilita_pain001_y_no_autorizable_da_409(cliente):
    d = cliente.post("/api/facturas", json=_f("a", "150000", "a", "A")).json()
    assert cliente.get(f"/api/ordenes/{d['recibo_id']}/pain001").status_code == 409
    r = cliente.post(f"/api/decisiones/{d['id']}/autorizar", headers=ANALISTA)
    assert r.json()["autorizada"] and len(r.json()["verificaciones"]) == 6
    assert cliente.get(f"/api/decisiones/{d['id']}").json()["estado_orden"] == "autorizada"
    assert cliente.get(f"/api/ordenes/{d['recibo_id']}/pain001").status_code == 200
    assert cliente.post(f"/api/decisiones/{d['id']}/autorizar", headers=ANALISTA).status_code == 409
    pendiente = _escalada(cliente)
    assert cliente.post(f"/api/decisiones/{pendiente['id']}/autorizar", headers=ANALISTA).status_code == 409


def test_actividad_de_pagar_sin_autorizar_no_dice_autorizada(cliente):
    d = cliente.post("/api/facturas", json=_f("a", "150000", "a", "A")).json()
    antes = cliente.get("/api/ciclo").json()["actividad"][0]["texto"]
    assert "Autorizada" not in antes and antes.startswith("Decisión de pagar")
    cliente.post(f"/api/decisiones/{d['id']}/autorizar", headers=ANALISTA)
    assert cliente.get("/api/ciclo").json()["actividad"][0]["texto"].startswith("Autorizada por el guardián")
