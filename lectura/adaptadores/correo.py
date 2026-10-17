from email import policy
from email.parser import BytesParser
from email.utils import parseaddr

from .congelada import AdaptadorDeTexto, Ilegible
from .pdf import leer_pdf


def leer_correo(contenido):
    """Encabezados, cuerpo (con pie) y texto de los adjuntos PDF. El Reply-To se conserva aparte."""
    msg = BytesParser(policy=policy.default).parsebytes(contenido)
    cuerpo = msg.get_body(preferencelist=("plain",))
    adjuntos = []
    for parte in msg.iter_attachments():
        if parte.get_content_type() == "application/pdf":
            estado, texto = leer_pdf(parte.get_content())
            adjuntos.append((parte.get_filename() or "", estado, texto))
    return {
        "de": str(msg["From"] or ""), "reply_to": str(msg["Reply-To"] or ""),
        "asunto": str(msg["Subject"] or ""), "cuerpo": cuerpo.get_content() if cuerpo else "",
        "adjuntos": adjuntos,
    }


class AdaptadorCorreo(AdaptadorDeTexto):
    nombre = "correo"
    formato = "eml"

    def texto(self, documento):
        c = leer_correo(documento.contenido)
        if any(estado != "ok" for _, estado, _ in c["adjuntos"]):
            raise Ilegible("sin_texto")
        partes = [f"From: {c['de']}"]
        if c["reply_to"]:
            partes.append(f"Reply-To: {c['reply_to']}")
        partes += [f"Subject: {c['asunto']}", "", c["cuerpo"]]
        partes += [f"[Adjunto {n}]\n{t}" for n, _, t in c["adjuntos"]]
        return "\n".join(partes)

    def a_canonica(self, documento):
        resultado = super().a_canonica(documento)
        motivo = _motivo_remitente(leer_correo(documento.contenido))
        if resultado.factura is not None and motivo:
            resultado.factura.setdefault("senales", {})["remitente_inconsistente"] = {"motivo": motivo}
        return resultado


def _dominio(direccion):
    return parseaddr(direccion)[1].rpartition("@")[2].lower()


def _motivo_remitente(correo):
    """Reply-To en otro dominio que el remitente: las respuestas irian a un tercero."""
    destino = _dominio(correo["reply_to"])
    if destino and destino != _dominio(correo["de"]):
        return f"Reply-To en el dominio {destino}, distinto del remitente {_dominio(correo['de'])}"
    return None
