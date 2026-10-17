from .cliente import ClienteAnthropic, ClienteCongelado

# Parametros de transporte, no de negocio; quien llame puede sobreescribirlos.
TRANSPORTE = {"url": "https://api.anthropic.com/v1/messages", "max_tokens": 4096, "timeout_s": 60, "max_retries": 2}


def crear_cliente(entorno, transporte=TRANSPORTE):
    """Devuelve (cliente, modo): real si hay clave en el entorno, lectura guardada si no."""
    if (entorno.get("ANTHROPIC_API_KEY") or "").strip():
        return ClienteAnthropic(**transporte, entorno=entorno), "en_vivo"
    return ClienteCongelado(), "guardada"
