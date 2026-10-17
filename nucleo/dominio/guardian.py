from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

NOMBRES = (
    "La firma del recibo es valida",
    "El hash de la factura coincide",
    "Monto y beneficiario son los del recibo",
    "PAGAR en modo autonomo, o ESCALAR con aprobacion vigente, o PAGAR en sombra con aprobacion; nunca FRENAR",
    "El mandato del recibo sigue vigente",
    "El recibo no se uso antes",
)


@dataclass(frozen=True)
class ContextoGuardian:
    firma_valida: Callable[[dict], bool]
    hash_documento: Callable[[str], str | None]
    mandato_vigente: str
    ahora: datetime
    consumir_nonce: Callable[[str, str], bool]


def _t(texto: str) -> datetime:
    return datetime.strptime(texto, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _c1(orden, r, ap, ctx):
    return None if ctx.firma_valida(r) else "La firma no corresponde al contenido del recibo."


def _c2(orden, r, ap, ctx):
    return None if ctx.hash_documento(r["factura_id"]) == r["hash_documento"] else "El hash del recibo no es el del documento de la factura."


def _c3(orden, r, ap, ctx):
    campos = ("monto_menor", "moneda", "beneficiario_id")
    if orden["recibo_id"] != r["id"] or any(orden[c] != r[c] for c in campos):
        return "La orden de pago no coincide con el monto, la moneda o el beneficiario del recibo."


def _aprobacion_invalida(r, ap, ctx):
    if ap is None:
        return "Se exige una aprobacion humana y no hay ninguna."
    if ap["accion"] != "aprobar" or ap["recibo_id"] != r["id"]:
        return "La aprobacion no corresponde a este recibo."
    if not ctx.firma_valida(ap):
        return "La firma de la aprobacion no es valida."
    if _t(ap["vence_en"]) < ctx.ahora:
        return "La aprobacion esta vencida."


def _c4(orden, r, ap, ctx):
    v, modo = r["veredicto"], r["modo_autonomia"]
    if v not in ("PAGAR", "ESCALAR"):
        return f"Un veredicto {v} no autoriza ningun pago."
    if modo not in ("autonomo", "sombra"):
        return "Modo de autonomia desconocido."
    return None if (v, modo) == ("PAGAR", "autonomo") else _aprobacion_invalida(r, ap, ctx)


def _c5(orden, r, ap, ctx):
    if r["mandato_version"] != ctx.mandato_vigente:
        return f"El mandato {r['mandato_version']} ya no es el vigente ({ctx.mandato_vigente})."
    if _t(r["vence_en"]) < ctx.ahora:
        return "El recibo esta vencido."


def _c6(orden, r, ap, ctx):
    return None if ctx.consumir_nonce(r["nonce"], r["id"]) else "El recibo ya se uso o su reserva de presupuesto se libero."


CHEQUEOS = (_c1, _c2, _c3, _c4, _c5, _c6)


def verificar(orden: dict, recibo: dict, aprobacion: dict | None, ctx: ContextoGuardian) -> dict:
    """Seis verificaciones en orden; tras la primera falla las demas quedan no_evaluada. El nonce se consume al final."""
    filas, motivo = [], None
    for n, (nombre, chequeo) in enumerate(zip(NOMBRES, CHEQUEOS), 1):
        falla = None
        if motivo is None:
            try:
                falla = chequeo(orden, recibo, aprobacion, ctx)
            except (KeyError, TypeError, ValueError) as e:
                falla = f"No se pudo evaluar: {e!r}"
        estado = "no_evaluada" if motivo is not None else "falla" if falla else "ok"
        filas.append({"n": n, "nombre": nombre, "estado": estado, "motivo": falla})
        motivo = motivo or falla
    return {"autorizada": motivo is None, "motivo": motivo, "verificaciones": filas}
