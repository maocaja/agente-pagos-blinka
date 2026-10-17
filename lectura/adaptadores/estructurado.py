from .base import Resultado, escalar, validar_canonica
from .canonica import desde_extraccion
from lectura.extractor.verificaciones import totales_cuadran

LECTURA_PARSER = {"metodo": "parser", "modelo": None, "reintentos": 0, "tokens_entrada": 0, "tokens_salida": 0,
                  "desde_cache": False, "motivo_falla": None, "costo_microusd": "0"}
_CAMPOS = ("tipo_documento", "numero_factura", "monto_total", "moneda", "proveedor", "cuenta")


class Incompleto(Exception):
    """Falta un dato obligatorio del documento estructurado."""


def extraccion(campos, evidencia, lineas):
    """Arma la extraccion de formato fijo; `campos` ya trae los textos tal como vienen del archivo."""
    return {
        "tipo_documento": campos["tipo_documento"], "numero_factura": campos["numero_factura"],
        "proveedor": {"nombre": campos["proveedor"], "id_fiscal": campos["id_fiscal"], "pais": campos["pais"]},
        "fechas": {"emision": campos["emision"], "vencimiento": campos["vencimiento"]},
        "moneda": campos["moneda"], "monto_total": campos["monto_total"],
        "cuenta": {"pais": campos["pais"], "ultimos4": campos["ultimos4"]},
        "lineas": lineas, "suma_lineas": None, "referencia_acuerdo": campos["acuerdo_ref"],
        "evidencia": {c: evidencia[c] for c in _CAMPOS}, "confianza": {c: 1.0 for c in _CAMPOS},
        "texto_dirigido_al_agente": {"presente": False, "cita": ""},
    }


def a_resultado(ext, documento, contexto, canal, formato):
    """Extraccion -> Resultado validado; totales que no cuadran, montos ilegibles o esquema roto escalan."""
    if totales_cuadran(ext) == "falla":
        return escalar("totales_incoherentes", [documento.id])
    try:
        factura = desde_extraccion(ext, documento, contexto, dict(LECTURA_PARSER), canal, formato)
    except ValueError as exc:
        return escalar("monto_ilegible", [str(exc)])
    errores = validar_canonica(factura)
    return escalar("esquema_invalido", errores) if errores else Resultado(factura)
