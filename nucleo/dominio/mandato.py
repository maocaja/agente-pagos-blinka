import json
from dataclasses import dataclass
from pathlib import Path

from .errores import FallaCerrada

RAIZ_CONTRATO = Path(__file__).resolve().parents[2] / "contrato"


@dataclass(frozen=True)
class Mandato:
    version: str
    estado: str
    p: dict
    doc: dict | None = None

    def tasa(self, moneda: str):
        from fractions import Fraction
        t = self.p["tasas_cambio"]["unidades_por_usd"].get(moneda)
        if t is None or moneda not in self.p["monedas_permitidas"]:
            raise FallaCerrada(f"moneda {moneda} sin tasa o no permitida en el mandato")
        return Fraction(t)


def cargar_mandato(ruta: Path) -> Mandato:
    d = json.loads(Path(ruta).read_text(encoding="utf-8"))
    return Mandato(d["version"], d["estado"], d["parametros"], d)


def ruta_ejemplo(version: str) -> Path:
    return RAIZ_CONTRATO / "ejemplos" / f"mandato.{version}.json"


def exponentes_moneda() -> dict:
    d = json.loads((RAIZ_CONTRATO / "monedas.json").read_text(encoding="utf-8"))
    return {k: v["exponente"] for k, v in d["monedas"].items()}
