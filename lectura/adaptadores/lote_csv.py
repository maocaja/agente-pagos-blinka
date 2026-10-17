import csv
import io
from dataclasses import replace

from .base import Documento, Resultado, escalar
from .estructurado import Incompleto, a_resultado, extraccion

_OBLIGATORIAS = ("numero", "proveedor", "pais", "moneda", "monto", "concepto", "cuenta_ultimos4")
_OPCIONALES = ("id_fiscal", "emision", "vencimiento", "acuerdo_ref")


def _extraccion_de_fila(fila):
    v = {c: (fila.get(c) or "").strip() for c in (*_OBLIGATORIAS, *_OPCIONALES)}
    faltan = [c for c in _OBLIGATORIAS if not v[c]]
    if faltan:
        raise Incompleto(",".join(faltan))
    campos = {**v, "tipo_documento": "factura", "numero_factura": v["numero"], "monto_total": v["monto"],
              "ultimos4": v["cuenta_ultimos4"]}
    evidencia = {"tipo_documento": "factura", "numero_factura": v["numero"], "monto_total": v["monto"],
                 "moneda": v["moneda"], "proveedor": v["proveedor"], "cuenta": v["cuenta_ultimos4"]}
    return extraccion(campos, evidencia, [{"descripcion": v["concepto"], "total": v["monto"]}])


class AdaptadorCsvLote:
    """Cada fila es una factura candidata; una fila invalida escala sola y el resto sigue."""

    nombre = "csv_lote"

    def __init__(self, contexto):
        self._contexto = contexto

    def soporta(self, documento: Documento) -> bool:
        return documento.formato == "csv"

    def a_canonicas(self, documento: Documento) -> list:
        try:
            filas = list(csv.DictReader(io.StringIO(documento.contenido.decode("utf-8-sig"))))
        except (UnicodeDecodeError, csv.Error):
            return [escalar("csv_ilegible")]
        resultados = []
        for n, fila in enumerate(filas, start=1):
            hija = replace(documento, id=f"{documento.id}-fila{n}")
            try:
                resultados.append(a_resultado(_extraccion_de_fila(fila), hija, self._contexto, "hoja", "csv"))
            except Incompleto as falta:
                resultados.append(escalar("fila_invalida", [f"fila {n}", str(falta)]))
        return resultados or [escalar("csv_vacio")]

    def a_canonica(self, documento: Documento) -> Resultado:
        """Por el registro solo pasa un lote de una fila; uno mayor se lee con a_canonicas."""
        resultados = self.a_canonicas(documento)
        return resultados[0] if len(resultados) == 1 else escalar("lote_de_varias_filas", [str(len(resultados))])
