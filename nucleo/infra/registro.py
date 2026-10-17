import json
import logging
from datetime import datetime, timezone

# Lista cerrada: lo que no esta aqui (tokens, cuentas, texto del documento) nunca se escribe.
PERMITIDOS = ("sesion", "decision", "recibo", "veredicto", "estado", "canal", "evento_aviso", "autorizada")


class FormatoJson(logging.Formatter):
    def format(self, record) -> str:
        campos = {k: str(v)[:80] for k, v in getattr(record, "campos", {}).items() if k in PERMITIDOS and v is not None}
        return json.dumps({"hora": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": record.getMessage(),
                           **campos}, ensure_ascii=False)


def configurar_registros() -> None:
    log = logging.getLogger("nucleo.operacion")
    if not log.handlers:
        h = logging.StreamHandler()
        h.setFormatter(FormatoJson())
        log.addHandler(h)
        log.setLevel(logging.INFO)
        log.propagate = False
