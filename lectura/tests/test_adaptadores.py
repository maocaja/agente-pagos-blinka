from pathlib import Path

from lectura.adaptadores import Documento, Registro, documento_desde_archivo, registro_por_defecto

FACTURAS = Path(__file__).resolve().parents[2] / "datos" / "facturas"


def test_texto_entrega_la_canonica_validada_por_hash():
    r = registro_por_defecto().convertir(documento_desde_archivo(FACTURAS / "fac-11-invoice-cloud-instruccion.txt"))
    assert not r.escala
    assert r.factura["referencias"]["numero_normalizado"] == "CA403"
    assert r.factura["montos"]["total_menor"] == "80000"


def test_tipo_desconocido_y_texto_sin_lectura_escalan():
    reg = registro_por_defecto()
    r = reg.convertir(Documento(id="x", contenido=b"%PDF-1.7", formato="pdf"))
    assert r.escala and r.motivo == "tipo_no_soportado"
    r = reg.convertir(Documento(id="y", contenido=b"factura inventada", formato="texto"))
    assert r.escala and r.motivo == "sin_lectura_congelada"


def test_adaptador_que_falla_o_entrega_algo_invalido_escala():
    class Roto:
        nombre = "roto"
        def soporta(self, d): return True
        def a_canonica(self, d): raise RuntimeError("boom")

    class Invalido(Roto):
        nombre = "invalido"
        def a_canonica(self, d):
            from lectura.adaptadores import Resultado
            return Resultado({"id": "f"})

    d = Documento(id="z", contenido=b"a", formato="texto")
    assert Registro([Roto()]).convertir(d).motivo == "error_de_adaptador"
    assert Registro([Invalido()]).convertir(d).motivo == "esquema_invalido"
