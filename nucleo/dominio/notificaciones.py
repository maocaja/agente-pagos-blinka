"""Avisos por plantilla fija con datos del registro; nunca texto libre del documento ni cuentas."""

import json
import unicodedata
from collections import defaultdict
from pathlib import Path

from .dinero import base_de, importe
from .errores import ErrorAccion, FallaCerrada
from .explicacion import QUE_HACER, fallas_por_precedencia
from .operacion import anotar

DATOS = Path(__file__).resolve().parents[1] / "notificaciones.json"


def cargar_datos() -> dict:
    return json.loads(DATOS.read_text(encoding="utf-8"))


def limpiar(texto, corte: int) -> str:
    """Sin saltos ni caracteres de control, espacios colapsados y cortado."""
    plano = "".join(" " if unicodedata.category(c).startswith("C") else c for c in str(texto))
    return " ".join(plano.split())[:corte]


def datos_de(s, d) -> dict:
    """Solo valores del registro maestro, del mandato y de reglas; el documento no aporta texto."""
    if d is None:
        return {"proveedor": "orden no reconocida", "importe": "", "que_hacer": "", "decision": ""}
    f = s.facturas.get(d["factura_id"]) or {}
    prov = s.reg.proveedor((f.get("proveedor_asignado") or {}).get("proveedor_id"))
    try:
        monto = importe(base_de(f, s.m), s.m)
    except (KeyError, FallaCerrada):
        monto = "importe no disponible"
    fallas = fallas_por_precedencia(d["reglas"])
    return {"proveedor": (prov or {}).get("nombre", "proveedor no registrado"), "importe": monto,
            "que_hacer": QUE_HACER.get(fallas[0]["id"], "") if fallas else "", "decision": d["id"]}


class Notificaciones:
    """Enruta eventos a canales y deja cada intento en la bandeja de la sesion. Nunca lanza hacia la decision."""

    def __init__(self, canales, datos, reloj, despachar, sesion_id="defecto", enlace_base=""):
        self.canales, self.rutas, self.plantillas = canales, datos["rutas"], datos["plantillas"]
        self.p, self.reloj, self.despachar = datos["entrega"], reloj, despachar
        self.sesion_id, self.enlace_base = sesion_id, enlace_base
        self.bandeja: list = []
        self._ultima_prueba = None

    def estado_canales(self) -> dict:
        return {n: "simulado" if c.simulado else "configurado" for n, c in self.canales.items()}

    def avisar(self, evento, servicio, d, **extra) -> None:
        try:
            datos = {**datos_de(servicio, d), **extra}
            self._encolar(evento, datos, {"sesion": self.sesion_id, "decision": datos.get("decision"),
                                          "recibo": (d or {}).get("recibo_id")})
        except Exception as e:  # un aviso fallido no puede tocar la decision
            anotar("notificacion_no_encolada", evento_aviso=evento, estado=type(e).__name__)

    def prueba(self) -> list:
        ahora = self.reloj()
        if self._ultima_prueba and (ahora - self._ultima_prueba).total_seconds() < self.p["prueba_cada_s"]:
            raise ErrorAccion(429, "demasiadas_peticiones", "Solo se permite una prueba cada pocos segundos.")
        self._ultima_prueba = ahora
        return self._encolar("prueba", {}, {"sesion": self.sesion_id})

    def _encolar(self, evento, datos, contexto) -> list:
        base = self.enlace_base.rstrip("/")
        datos = defaultdict(str, {**datos, "enlace": f"{base}/?decision={datos['decision']}" if base and datos.get("decision") else ""})
        texto = limpiar(self.plantillas[evento].format_map(datos), self.p["corte"])
        trabajos, entradas = [], []
        for nombre in self.rutas[evento]:
            canal = self.canales.get(nombre)
            if canal is None:
                continue
            e = {"hora": self.reloj().strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": evento, "canal": nombre,
                 "destino": canal.destino, "estado": "en_cola", "texto": texto, "motivo": None}
            self.bandeja.append(e)
            entradas.append(e)
            trabajos.append((canal, texto, [e], {**contexto, "evento_aviso": evento}))
        self.despachar(trabajos)
        return entradas
