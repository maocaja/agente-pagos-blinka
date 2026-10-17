from lectura.extractor.verificaciones import totales_cuadran
from lectura.normalizador.normalizador import normalizar_clave, normalizar_monto
from lectura.proveedor import asignar_proveedor
from lectura.seguridad.instrucciones import con_senal_local


def _o_nulo(texto):
    return texto or None


def desde_extraccion(ext, documento, contexto, lectura, canal="imagen", formato="imagen"):
    """Extraccion del modelo -> factura canonica. `contexto` trae ciclo_id, recibido_en y el registro maestro."""
    moneda = ext["moneda"]
    prov = ext["proveedor"]
    cuenta = ext["cuenta"]
    factura = {
        "id": f"f_{documento.id}", "ciclo_id": contexto["ciclo_id"],
        "documento": {"id": f"d_{documento.id}", "hash": documento.hash, "canal": canal, "formato": formato,
                      "tipo_documento": ext["tipo_documento"], "recibido_en": contexto["recibido_en"]},
        "emisor": {"nombre": prov["nombre"], "nombre_normalizado": normalizar_clave(prov["nombre"]),
                   "id_fiscal": prov["id_fiscal"], "pais": prov["pais"]},
        "referencias": {"numero": ext["numero_factura"],
                        "numero_normalizado": normalizar_clave(ext["numero_factura"]),
                        "acuerdo_ref": ext["referencia_acuerdo"]},
        "fechas": {"emision": _o_nulo(ext["fechas"]["emision"]), "vencimiento": _o_nulo(ext["fechas"]["vencimiento"])},
        "montos": {"moneda": moneda, "total_menor": normalizar_monto(ext["monto_total"], moneda),
                   "suma_lineas_menor": normalizar_monto(ext["suma_lineas"], moneda) if ext["suma_lineas"] else None,
                   "lineas": [{"descripcion": x["descripcion"], "total_menor": normalizar_monto(x["total"], moneda)}
                              for x in ext["lineas"]]},
        "cuenta": {"pais": cuenta["pais"], "ultimos4": cuenta["ultimos4"]} if cuenta["ultimos4"] else None,
        "evidencia": ext["evidencia"], "confianza": ext["confianza"],
        "verificaciones": {"esquema": "ok", "dinero_presente": "ok", "suma_lineas": totales_cuadran(ext),
                           "cita_evidencia": "no_verificable", "tipo": "ok",
                           "segunda_lectura": {"estado": "coincide", "detalle": []}},
        "lectura": lectura,
    }
    factura["proveedor_asignado"] = asignar_proveedor(factura, contexto["registro"])
    if ext["texto_dirigido_al_agente"]["presente"]:
        factura["senales"] = {"texto_dirigido_al_agente": {"p": 1.0, "origen": ext["texto_dirigido_al_agente"]["cita"]}}
    return con_senal_local(factura, documento.contenido.decode("utf-8", errors="ignore"))
