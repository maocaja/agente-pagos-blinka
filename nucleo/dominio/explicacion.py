PRECEDENCIA = ("FRENAR", "ESCALAR")
MAXIMO_FRASES = 3
# Que hacer segun la regla que decide; una tabla, no una cadena de if.
QUE_HACER = {
    "R1": "Confirmar contra el original.",
    "R2a": "No pagar: ya se recibio esta factura.",
    "R2b": "Confirmar con el proveedor que no es un cobro repetido.",
    "R3": "Verificar al proveedor y darlo de alta en el registro maestro antes de pagar.",
    "R4": "Confirmar la cuenta con el proveedor por un canal distinto al documento.",
    "R5": "Revisar el acuerdo con el proveedor o pedir una factura corregida.",
    "R6": "Pedir la aprobacion de quien tenga el monto autorizado.",
    "R7": "Pedir la factura en una moneda permitida o ampliar el mandato.",
    "R8": "No ejecutar la instrucción; revisar el documento original.",
    "R9": "Esperar al siguiente periodo o ampliar el presupuesto.",
    "R10": "Revisar lo ya pagado al proveedor antes de aprobar.",
}
# Relevancia para la persona: menor numero = razon principal. R1 (lectura) va al final.
PRIORIDAD = {r: i for i, r in enumerate(("R8", "R4", "R3", "R2a", "R2b", "R7", "R6", "R10", "R5", "R9", "R1"))}
QUE_HACER_GENERICO = "Que una persona revise la decision."


def fallas_por_precedencia(reglas) -> list:
    fallas = [r for r in reglas if r["estado"] == "falla"]
    return sorted(fallas, key=lambda r: (PRECEDENCIA.index(r["accion_si_falla"]) if r["accion_si_falla"] in PRECEDENCIA else len(PRECEDENCIA),
                                          PRIORIDAD.get(r["id"], len(PRIORIDAD))))


def explicar(veredicto, motivo_corto, reglas) -> tuple:
    """Explicacion y que hacer, solo desde los resultados por regla; sin modelo."""
    fallas = fallas_por_precedencia(reglas)
    if not fallas:
        return motivo_corto, None
    frases = [r["evidencia"] for r in fallas[:MAXIMO_FRASES]]
    que = QUE_HACER.get(fallas[0]["id"], QUE_HACER_GENERICO) if veredicto in PRECEDENCIA else None
    return " ".join(frases[:1] + [f"Además: {x}" for x in frases[1:]]), que
