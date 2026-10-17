from xml.etree import ElementTree as ET

from .errores import FallaCerrada
from .mandato import exponentes_moneda

NS = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"


def _decimal(monto_menor: str, moneda: str) -> str:
    exp = exponentes_moneda().get(moneda)
    if exp is None or not str(monto_menor).isdigit():
        raise FallaCerrada(f"monto o moneda no convertible a XML: {monto_menor} {moneda}")
    n = int(monto_menor)
    return f"{n // 10 ** exp}.{n % 10 ** exp:0{exp}d}" if exp else str(n)


def _sub(padre, nombre, texto=None):
    e = ET.SubElement(padre, nombre)
    e.text = texto
    return e


def orden_a_pain001(orden: dict, beneficiario: str, creada_en: str) -> bytes:
    """pain.001 minimo, marcado SIMULADA: nada se envia a ningun banco."""
    raiz = ET.Element("Document", xmlns=NS)
    raiz.append(ET.Comment(" SIMULADA: orden de demostracion, no se envia a ningun banco "))
    cuerpo = _sub(raiz, "CstmrCdtTrfInitn")
    ini = _sub(cuerpo, "GrpHdr")
    _sub(ini, "MsgId", orden["recibo_id"])
    _sub(ini, "CreDtTm", creada_en)
    _sub(ini, "NbOfTxs", "1")
    pago = _sub(cuerpo, "PmtInf")
    _sub(pago, "PmtInfId", "SIMULADA-" + orden["recibo_id"])
    tx = _sub(pago, "CdtTrfTxInf")
    monto = _sub(_sub(tx, "Amt"), "InstdAmt", _decimal(orden["monto_menor"], orden["moneda"]))
    monto.set("Ccy", orden["moneda"])
    _sub(_sub(tx, "Cdtr"), "Nm", beneficiario)
    _sub(_sub(tx, "RmtInf"), "Ustrd", orden["concepto"])
    return ET.tostring(raiz, encoding="utf-8", xml_declaration=True)
