import base64
import json
from datetime import timedelta

from .dinero import a_base_menor


def serializar(recibo: dict) -> bytes:
    """Bytes firmados: el recibo sin firma, claves ordenadas."""
    sin = {k: v for k, v in recibo.items() if k != "firma"}
    return json.dumps(sin, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def emitir_recibo(decision, f, m, ids, nonce, reloj, firmador, fallas_aprobadas=()) -> dict:
    ahora = reloj()
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    mo = f["montos"]
    r = {
        "id": ids("rec"), "decision_id": decision["id"], "factura_id": f["id"],
        "hash_documento": f["documento"]["hash"], "beneficiario_id": f["proveedor_asignado"]["proveedor_id"],
        "monto_menor": mo["total_menor"], "moneda": mo["moneda"],
        "monto_base_menor": str(a_base_menor(mo["total_menor"], mo["moneda"], m)),
        "veredicto": decision["veredicto"], "modo_autonomia": decision["modo_autonomia"],
        "reglas": [{"id": x["id"], "estado": x["estado"]} for x in decision["reglas"]],
        "fallas_aprobadas": list(fallas_aprobadas), "mandato_version": m.version, "nonce": nonce(),
        "emitido_en": ahora.strftime(fmt),
        "vence_en": (ahora + timedelta(hours=m.p["vigencia_recibo_h"])).strftime(fmt),
        "clave_version": firmador.clave_version,
    }
    r["firma"] = base64.b64encode(firmador.firmar(serializar(r))).decode("ascii")
    return r


def orden_desde_recibo(recibo: dict) -> dict:
    """Sin recibo no hay orden: es la unica forma de construirla."""
    return {"recibo_id": recibo["id"], "beneficiario_id": recibo["beneficiario_id"],
            "monto_menor": recibo["monto_menor"], "moneda": recibo["moneda"],
            "concepto": f"Pago de la factura {recibo['factura_id']}"}
