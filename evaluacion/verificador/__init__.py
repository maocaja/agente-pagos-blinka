"""Verificador independiente de la condicion de pago, escrito solo desde el texto de las reglas."""
import json
import re
from pathlib import Path

from .dinero import a_base_menor
from .estado import Estado, Recibida
from .reglas import FINALES, REGLAS, Contexto, normalizar

RAIZ = Path(__file__).resolve().parents[2]
SEVERIDAD = {"PAGAR": 0, "REGISTRAR": 0, "ESCALAR": 1, "FRENAR": 2}
# tipo -> (se evaluan reglas, veredicto minimo, veredicto si todo pasa, motivo del piso)
POLITICA = {
    "factura": (True, None, "PAGAR", ""),
    "cuenta_de_cobro": (True, None, "PAGAR", ""),
    "nota_de_credito": (True, None, "REGISTRAR", ""),
    "estado_de_cuenta": (False, "FRENAR", "FRENAR", "no es una factura"),
    "proforma": (True, "ESCALAR", "ESCALAR", "proforma: requiere una persona"),
    "anticipo": (True, "ESCALAR", "ESCALAR", "anticipo: requiere una persona"),
}
SIN_POLITICA = (False, "ESCALAR", "ESCALAR", "tipo no soportado")


def _json(ruta):
    return json.loads((RAIZ / ruta).read_text(encoding="utf-8"))


def _digitos(texto):
    return re.sub(r"\D", "", texto or "")


class Verificador:
    def __init__(self, mandato, registro=None, monedas=None, reglas_registro=None):
        self.mandato = mandato
        self.registro = registro or _json("datos/registro-maestro.json")
        self.monedas = (monedas or _json("contrato/monedas.json"))["monedas"]
        tipos = (reglas_registro or _json("contrato/reglas.registro.json"))["reglas"]
        self.aplica = {r["id"]: set(r["tipos"]) for r in tipos}
        self.estado = Estado()

    def proveedor(self, f):
        emisor = f.get("emisor") or {}
        fiscal, nombre = _digitos(emisor.get("id_fiscal")), normalizar(emisor.get("nombre"))
        for p in self.registro["proveedores"]:
            alias = {normalizar(p["nombre"])} | {normalizar(a) for a in p.get("alias", [])}
            if (fiscal and fiscal == _digitos(p["id_fiscal"])) or (nombre and nombre in alias):
                return p
        return None

    def _evaluar_reglas(self, f, tipo):
        m = f["montos"]
        base = a_base_menor(m["total_menor"], m["moneda"], self.mandato, self.monedas) if m.get("total_menor") else None
        c = Contexto(f, self.mandato["parametros"], self.registro, self.monedas, self.estado, self.proveedor(f),
                     base, f["documento"]["recibido_en"][:7], {})
        orden = [i for i in REGLAS if i not in FINALES] + list(FINALES)
        for id_ in orden:
            if tipo in self.aplica.get(id_, ()):
                resultado = REGLAS[id_](c)
                if resultado:
                    c.fallas[id_] = {"accion": resultado[0], "evidencia": resultado[1]}
        return c

    def evaluar(self, f):
        """Veredicto y reglas que fallan para una extraccion; actualiza el estado propio."""
        tipo = (f.get("documento") or {}).get("tipo_documento")
        evalua, piso, exito, motivo = POLITICA.get(tipo, SIN_POLITICA)
        try:
            c = self._evaluar_reglas(f, tipo) if evalua else None
        except (KeyError, TypeError, ValueError) as e:
            return self._cerrar(f, tipo, "ESCALAR", {}, f"extraccion ilegible: {e!r}", None)
        fallas = c.fallas if c else {}
        acciones = [x["accion"] for x in fallas.values()] + ([piso] if piso else [])
        veredicto = max(acciones, key=SEVERIDAD.get) if acciones else exito
        return self._cerrar(f, tipo, veredicto, fallas, motivo, c)

    def _cerrar(self, f, tipo, veredicto, fallas, motivo, c):
        if c is not None:
            self.estado.registrar(Recibida(
                c.prov["id"] if c.prov else "", normalizar(f["referencias"].get("numero")), f["documento"].get("hash") or "",
                c.base or 0, f["documento"]["recibido_en"][:10], tipo, veredicto, c.periodo))
        return {"veredicto": veredicto, "reglas_que_fallan": sorted(fallas, key=orden_regla), "motivo": motivo,
                "detalle": fallas}


def orden_regla(id_):
    return int(re.sub(r"\D", "", id_)), id_
