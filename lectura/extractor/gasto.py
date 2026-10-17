import json
from pathlib import Path

_MODELOS = Path(__file__).resolve().parents[1] / "modelos.json"
_MILLON = 1_000_000


def cargar_modelos(ruta=_MODELOS):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))["modelos"]


class ContadorGasto:
    """Tokens y costo por corrida; el tope viene del mandato (tope_gasto_corrida_microusd)."""

    def __init__(self, tope_microusd, modelos):
        self.tope = int(tope_microusd)
        self._modelos = modelos
        self.gastado = 0
        self.tokens_entrada = 0
        self.tokens_salida = 0

    def costo(self, clave, tokens_entrada, tokens_salida):
        m = self._modelos[clave]
        bruto = tokens_entrada * m["entrada_microusd_mtok"] + tokens_salida * m["salida_microusd_mtok"]
        return -(-bruto // _MILLON)

    def registrar(self, clave, tokens_entrada, tokens_salida):
        c = self.costo(clave, tokens_entrada, tokens_salida)
        self.gastado += c
        self.tokens_entrada += tokens_entrada
        self.tokens_salida += tokens_salida
        return c

    @property
    def agotado(self):
        return self.gastado >= self.tope
