import re

from .congelada import AdaptadorDeTexto, Ilegible

_MENSAJE = re.compile(r"^([^:\[\]]{1,60}): (.+)$")


def leer_chat(contenido):
    """(remitentes, mensajes) de una exportacion estilo WhatsApp; los avisos entre corchetes se ignoran."""
    mensajes = []
    for linea in contenido.decode("utf-8", errors="replace").splitlines():
        m = _MENSAJE.match(linea.strip())
        if m:
            mensajes.append((m.group(1).strip(), m.group(2).strip()))
    return sorted({r for r, _ in mensajes}), mensajes


class AdaptadorChat(AdaptadorDeTexto):
    nombre = "chat"
    formato = "chat"

    def texto(self, documento):
        _, mensajes = leer_chat(documento.contenido)
        if not mensajes:
            raise Ilegible("sin_texto")
        return "\n".join(f"{r}: {m}" for r, m in mensajes)
