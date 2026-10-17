def armar_paquete(s, clave: dict, generado_en: str) -> dict:
    """Todo lo que un auditor necesita para verificar las firmas sin la app."""
    recibos = list(s.recibos.values())
    versiones = {r["mandato_version"] for r in recibos}
    return {"formato": "paquete-auditoria/1", "generado_en": generado_en, **clave, "recibos": recibos,
            "mandatos": {s.m.version: s.m.doc} if s.m.version in versiones else {}}
