PRECEDENCIA = ("FRENAR", "ESCALAR")
MAXIMO_FRASES = 3
# Que hacer segun la regla que decide; una tabla, no una cadena de if.
QUE_HACER = {
    "R1": "Corregir la lectura o confirmarla contra el documento original.",
    "R2a": "No pagar: ya se recibio esta factura.",
    "R2b": "Confirmar con el proveedor que no es un cobro repetido.",
    "R3": "Verificar al proveedor y darlo de alta en el registro maestro antes de pagar.",
    "R4": "Confirmar con el proveedor antes de pagar.",
    "R5": "Revisar el acuerdo con el proveedor o pedir una factura corregida.",
    "R6": "Pedir la aprobacion de quien tenga el monto autorizado.",
    "R7": "Pedir la factura en una moneda permitida o ampliar el mandato.",
    "R8": "Ignorar las instrucciones del documento y revisar su origen.",
    "R9": "Esperar al siguiente periodo o ampliar el presupuesto.",
    "R10": "Revisar lo ya pagado al proveedor antes de aprobar.",
}
QUE_HACER_GENERICO = "Que una persona revise la decision."


def _fallas_por_precedencia(reglas) -> list:
    fallas = [r for r in reglas if r["estado"] == "falla"]
    return sorted(fallas, key=lambda r: PRECEDENCIA.index(r["accion_si_falla"]) if r["accion_si_falla"] in PRECEDENCIA else len(PRECEDENCIA))


def explicar(veredicto, motivo_corto, reglas) -> tuple:
    """Explicacion y que hacer, solo desde los resultados por regla; sin modelo."""
    fallas = _fallas_por_precedencia(reglas)
    if not fallas:
        return motivo_corto, None
    frases = [r["evidencia"] for r in fallas[:MAXIMO_FRASES]]
    que = QUE_HACER.get(fallas[0]["id"], QUE_HACER_GENERICO) if veredicto in PRECEDENCIA else None
    return " ".join(frases), que
