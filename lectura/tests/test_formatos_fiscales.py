import json
from pathlib import Path

from lectura.adaptadores import Documento, documento_desde_archivo, registro_multicanal
from lectura.adaptadores.lote_csv import AdaptadorCsvLote

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "datos" / "documentos"
REGISTRO = json.loads((RAIZ / "datos" / "registro-maestro.json").read_text(encoding="utf-8"))
CONTEXTO = {"ciclo_id": "2026-10", "recibido_en": "2026-10-12T09:00:00Z", "registro": REGISTRO}


def _xml(nombre):
    return registro_multicanal(contexto=CONTEXTO).convertir(documento_desde_archivo(DOCS / "xml" / nombre))


def _lote(nombre):
    return AdaptadorCsvLote(CONTEXTO).a_canonicas(documento_desde_archivo(DOCS / "csv" / nombre))


def test_ubl_valido_entrega_la_canonica_en_unidades_menores():
    r = _xml("xml-01-andino-ubl.xml")
    f = r.factura
    assert not r.escala and f["montos"]["total_menor"] == "180000" and f["montos"]["suma_lineas_menor"] is None
    assert f["proveedor_asignado"]["proveedor_id"] == "prov_andino" and f["cuenta"]["ultimos4"] == "4417"
    assert f["documento"]["formato"] == "xml" and f["lectura"]["metodo"] == "parser"


def test_xml_con_entidad_externa_se_rechaza():
    r = _xml("xml-03-pixel-entidad-externa.xml")
    assert r.escala and r.motivo == "xml_con_entidades"


def test_ubl_con_totales_incoherentes_escala():
    r = _xml("xml-02-cloud-totales-incoherentes.xml")
    assert r.escala and r.motivo == "totales_incoherentes"


def test_xml_mal_formado_o_incompleto_escala():
    reg = registro_multicanal(contexto=CONTEXTO)
    assert reg.convertir(Documento(id="m", contenido=b"<Invoice><x>", formato="xml")).motivo == "xml_mal_formado"
    raiz_ajena = Documento(id="i", contenido=b"<Otro/>", formato="xml")
    assert reg.convertir(raiz_ajena).motivo == "xml_incompleto"


def test_lote_partido_produce_una_factura_por_fila_del_mismo_proveedor():
    rs = _lote("csv-01-andino-partida.csv")
    assert [r.factura["referencias"]["numero"] for r in rs] == ["AND-3201-A", "AND-3201-B", "AND-3201-C"]
    assert {r.factura["proveedor_asignado"]["proveedor_id"] for r in rs} == {"prov_andino"}
    assert [r.factura["montos"]["total_menor"] for r in rs] == ["70000"] * 3
    assert len({r.factura["id"] for r in rs}) == 3 and rs[0].factura["documento"]["canal"] == "hoja"


def test_fila_invalida_escala_sola_sin_tumbar_el_lote():
    ok, mala, ambigua = _lote("csv-02-mixto-fila-invalida.csv")
    assert not ok.escala and mala.motivo == "fila_invalida" and mala.detalle == ["fila 2", "monto"]
    assert not ambigua.escala and ambigua.factura["montos"]["total_menor"] == "120050"


def test_csv_de_varias_filas_por_el_registro_escala_y_el_tipo_sin_contexto_no_se_soporta():
    doc = documento_desde_archivo(DOCS / "csv" / "csv-01-andino-partida.csv")
    assert registro_multicanal(contexto=CONTEXTO).convertir(doc).motivo == "lote_de_varias_filas"
    assert registro_multicanal().convertir(doc).motivo == "tipo_no_soportado"


def test_reply_to_distinto_marca_remitente_inconsistente_y_el_resto_no():
    reg = registro_multicanal()
    f = reg.convertir(documento_desde_archivo(DOCS / "eml-05-devnorte-replyto.eml")).factura
    assert "correo-externo.example" in f["senales"]["remitente_inconsistente"]["motivo"]
    limpio = reg.convertir(documento_desde_archivo(DOCS / "eml-08-logistica-pie-instruccion.eml")).factura
    assert "remitente_inconsistente" not in limpio["senales"]
