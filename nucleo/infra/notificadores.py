"""Canales de aviso. Los secretos entran por el entorno y nunca salen en destino, motivo ni registros."""

import json
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage

from ..dominio.errores import ErrorEntrega

TIEMPO_ESPERA_S = 5


def enmascarar(valor: str) -> str:
    return "..." + str(valor)[-3:]


class Simulado:
    """Bandeja de salida sin envio real: el aviso queda anotado como simulado."""

    simulado, espaciado_s, destino = True, 0.0, "sin configurar"

    def __init__(self, nombre: str):
        self.nombre = nombre

    def enviar(self, texto: str) -> None:
        return None


def _espera_pedida(e: urllib.error.HTTPError):
    try:
        return float(json.loads(e.read())["parameters"]["retry_after"])
    except (ValueError, KeyError, TypeError, OSError):
        return None


class Telegram:
    nombre, simulado = "telegram", False

    def __init__(self, token, chat_id, espaciado_s=1.1, abrir=urllib.request.urlopen):
        self._token, self._chat, self._abrir = token, chat_id, abrir
        self.destino, self.espaciado_s = enmascarar(chat_id), espaciado_s

    def enviar(self, texto: str) -> None:
        # Texto plano: sin parse_mode.
        req = urllib.request.Request(f"https://api.telegram.org/bot{self._token}/sendMessage", method="POST",
                                     data=json.dumps({"chat_id": self._chat, "text": texto}).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        try:
            with self._abrir(req, timeout=TIEMPO_ESPERA_S) as r:
                r.read()
        except urllib.error.HTTPError as e:
            raise ErrorEntrega(f"HTTP {e.code}", _espera_pedida(e) if e.code == 429 else None) from None
        except (urllib.error.URLError, OSError) as e:
            raise ErrorEntrega(type(e).__name__) from None


class Correo:
    nombre, simulado, espaciado_s = "correo", False, 0.0

    def __init__(self, env: dict, abrir=smtplib.SMTP):
        self._env, self._abrir = env, abrir
        self.destino = enmascarar(env["NOTIFY_EMAIL_TO"])

    def enviar(self, texto: str) -> None:
        msg = EmailMessage()
        msg["Subject"], msg["From"], msg["To"] = "Aviso del agente de pagos", self._env["SMTP_FROM"], self._env["NOTIFY_EMAIL_TO"]
        msg.set_content(texto)
        try:
            with self._abrir(self._env["SMTP_HOST"], int(self._env.get("SMTP_PORT") or 587), timeout=TIEMPO_ESPERA_S) as smtp:
                smtp.starttls()
                if self._env.get("SMTP_USER"):
                    smtp.login(self._env["SMTP_USER"], self._env.get("SMTP_PASSWORD", ""))
                smtp.send_message(msg)
        except (smtplib.SMTPException, OSError, ValueError) as e:
            raise ErrorEntrega(type(e).__name__) from None


def canales_desde_entorno(env) -> dict:
    """Sin variables el canal queda simulado; con ellas el mismo codigo envia de verdad."""
    tg = (Telegram(env["TELEGRAM_BOT_TOKEN"], env["TELEGRAM_CHAT_ID"])
          if env.get("TELEGRAM_BOT_TOKEN") and env.get("TELEGRAM_CHAT_ID") else Simulado("telegram"))
    correo = Correo(env) if all(env.get(k) for k in ("SMTP_HOST", "SMTP_FROM", "NOTIFY_EMAIL_TO")) else Simulado("correo")
    return {"telegram": tg, "correo": correo}
