import re
import unicodedata

# Ordenes al agente en es, en y pt; cada patron se aplica sobre texto sin tildes y en minusculas.
_P = 0.9
_PATRONES = tuple(re.compile(p) for p in (
    r"(ignor\w*|ignore|disregard|olvid\w*|salt\w*|skip|bypass|desconsider\w*)\W+(\w+\W+){0,3}"
    r"(reglas?|regras?|rules?|instrucc\w+|instruc\w+|instructions?|politicas?|policy|policies)",
    r"(apru\w+|aprov\w+|approve|pag[ae]r?|pague|pay)\W+(\w+\W+){0,6}"
    r"(de inmediato|inmediatamente|immediately|right away|sin revis\w+|sem revis\w+|without review|"
    r"imediatamente|agora mesmo|hoy mismo)",
    r"(sin|no|sem|without|do not|don t|nao)\W+(\w+\W+){0,2}"
    r"(escal\w+|revis\w+|review\w*|verific\w+|check\w*|aprobacion|approval)",
    r"(autoriz\w+|autoris\w+|aprobad[oa]|approved|authori[sz]ed)\W+(por|by|pelo|pela)?\W*(\w+\W+){0,3}"
    r"(gerente|director|ceo|cfo|jefe|boss|manager|diretor|presidente)",
    r"(nota|mensaje|message|note)\W+(para|to|ao|a)\W+(\w+\W+){0,2}(sistema|agente|agent|system|ia|ai)",
    r"(you are|eres|usted es|voce e|ahora eres|act as|actua como)\W+(\w+\W+){0,3}"
    r"(payment|pagos?|pagamentos?)\W+(agent|agente)",
    r"\b(system|sistema)\s*:",
))


def _normalizar(texto):
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sin_tildes.lower())


def detectar(texto):
    """(p, cita) de la primera orden al agente que aparece en el texto; (0.0, '') si no hay."""
    plano = _normalizar(texto or "")
    for patron in _PATRONES:
        m = patron.search(plano)
        if m:
            return _P, m.group(0).strip()
    return 0.0, ""


def con_senal_local(factura, texto):
    """Sube la senal texto_dirigido_al_agente de la factura a la mayor entre el modelo y el detector."""
    p, cita = detectar(texto)
    previa = factura.get("senales", {}).get("texto_dirigido_al_agente")
    if p > (previa["p"] if previa else 0.0):
        origen = previa["origen"] if previa else cita
        factura.setdefault("senales", {})["texto_dirigido_al_agente"] = {"p": p, "origen": origen}
    return factura
