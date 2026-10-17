import xml.etree.ElementTree as ET
from xml.parsers import expat

from .base import Documento, Resultado, escalar
from .estructurado import Incompleto, a_resultado, extraccion

_NS = {"cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
       "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"}
_TIPOS = {"Invoice": "factura", "CreditNote": "nota_de_credito"}
_PROVEEDOR = "cac:AccountingSupplierParty/cac:Party"


class EntidadProhibida(Exception):
    pass


def _rechazar_doctype(*_):
    raise EntidadProhibida()


def _sin_doctype(contenido):
    # Un DOCTYPE es la puerta de entidades externas y de expansion; no se admite ninguno.
    parser = expat.ParserCreate()
    parser.StartDoctypeDeclHandler = _rechazar_doctype
    parser.Parse(contenido, True)


def _texto(nodo, ruta):
    hallado = nodo.find(ruta, _NS)
    if hallado is None or not (hallado.text or "").strip():
        raise Incompleto(ruta)
    return hallado.text.strip()


def _opcional(nodo, ruta):
    hallado = nodo.find(ruta, _NS)
    return (hallado.text or "").strip() if hallado is not None else ""


def _lineas(raiz):
    filas = raiz.findall("cac:InvoiceLine", _NS) + raiz.findall("cac:CreditNoteLine", _NS)
    lineas = [{"descripcion": _texto(f, "cac:Item/cbc:Description"), "total": _texto(f, "cbc:LineExtensionAmount")}
              for f in filas]
    impuesto = _opcional(raiz, "cac:TaxTotal/cbc:TaxAmount")
    if lineas and impuesto and impuesto != "0":
        lineas.append({"descripcion": "Impuestos", "total": impuesto})
    return lineas


def leer_ubl(contenido):
    _sin_doctype(contenido)
    raiz = ET.fromstring(contenido)
    nombre_raiz = raiz.tag.rpartition("}")[2]
    tipo = _TIPOS.get(nombre_raiz)
    if tipo is None:
        raise Incompleto("raiz")
    moneda = _texto(raiz, "cbc:DocumentCurrencyCode")
    cuenta = _texto(raiz, "cac:PaymentMeans/cac:PayeeFinancialAccount/cbc:ID")
    pais = _texto(raiz, f"{_PROVEEDOR}/cac:PostalAddress/cac:Country/cbc:IdentificationCode")
    campos = {"tipo_documento": tipo, "numero_factura": _texto(raiz, "cbc:ID"),
              "proveedor": _texto(raiz, f"{_PROVEEDOR}/cac:PartyName/cbc:Name"),
              "id_fiscal": _opcional(raiz, f"{_PROVEEDOR}/cac:PartyTaxScheme/cbc:CompanyID"), "pais": pais,
              "emision": _opcional(raiz, "cbc:IssueDate"), "vencimiento": _opcional(raiz, "cbc:DueDate"),
              "moneda": moneda, "monto_total": _texto(raiz, "cac:LegalMonetaryTotal/cbc:PayableAmount"),
              "ultimos4": cuenta[-4:], "acuerdo_ref": _opcional(raiz, "cac:ContractDocumentReference/cbc:ID")}
    evidencia = {"tipo_documento": nombre_raiz, "numero_factura": campos["numero_factura"],
                 "monto_total": campos["monto_total"], "moneda": moneda, "proveedor": campos["proveedor"],
                 "cuenta": cuenta}
    return extraccion(campos, evidencia, _lineas(raiz))


class AdaptadorXml:
    """Factura electronica UBL con parser estandar, sin modelo ni red."""

    nombre = "xml_ubl"

    def __init__(self, contexto):
        self._contexto = contexto

    def soporta(self, documento: Documento) -> bool:
        return documento.formato == "xml"

    def a_canonica(self, documento: Documento) -> Resultado:
        try:
            ext = leer_ubl(documento.contenido)
        except EntidadProhibida:
            return escalar("xml_con_entidades")
        except (ET.ParseError, expat.ExpatError):
            return escalar("xml_mal_formado")
        except Incompleto as falta:
            return escalar("xml_incompleto", [str(falta)])
        return a_resultado(ext, documento, self._contexto, "xml", "xml")
