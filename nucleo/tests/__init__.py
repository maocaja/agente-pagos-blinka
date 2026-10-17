import os
from pathlib import Path

REGISTRO = Path(__file__).resolve().parents[2] / "datos" / "registro-maestro.json"

# Ninguna prueba debe enviar avisos reales aunque el entorno tenga credenciales.
for _v in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "SMTP_HOST", "NOTIFY_EMAIL_TO", "APP_BASE_URL"):
    os.environ.pop(_v, None)
