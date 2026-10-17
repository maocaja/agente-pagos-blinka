"""Envio en segundo plano: espaciado por canal, resumen de rafagas y reintento acotado."""

import queue
import threading
import time

from ..dominio.errores import ErrorEntrega
from ..dominio.operacion import anotar


class Despachador:
    def __init__(self, p: dict, dormir=time.sleep, reloj=time.monotonic, hilo=True):
        self.p, self._dormir, self._reloj, self._hilo = p, dormir, reloj, hilo
        self._cola: queue.Queue = queue.Queue()
        self._ultimo: dict = {}
        self._arranque = threading.Lock()
        self._worker = None

    def __call__(self, trabajos) -> None:
        if not self._hilo:
            return self._procesar(trabajos)
        with self._arranque:
            if self._worker is None:
                self._worker = threading.Thread(target=self._bucle, daemon=True)
                self._worker.start()
        for t in trabajos:
            self._cola.put(t)

    def _bucle(self) -> None:
        while True:
            lote = [self._cola.get()]
            while not self._cola.empty():
                lote.append(self._cola.get_nowait())
            self._procesar(lote)

    def _procesar(self, lote) -> None:
        for items in self._por_canal(lote).values():
            if len(items) > self.p["rafaga_max"]:
                canal, _, _, ctx = items[0]
                self._entregar(canal, f"{len(items)} avisos nuevos; ver la bandeja de la aplicacion.",
                               [e for _, _, es, _ in items for e in es], ctx, "incluida en resumen")
            else:
                for canal, texto, entradas, ctx in items:
                    self._entregar(canal, texto, entradas, ctx)

    @staticmethod
    def _por_canal(lote) -> dict:
        por = {}
        for t in lote:
            por.setdefault(t[0].nombre, []).append(t)
        return por

    def _espaciar(self, canal) -> None:
        falta = canal.espaciado_s - (self._reloj() - self._ultimo.get(canal.nombre, -1e9))
        if falta > 0:
            self._dormir(falta)
        self._ultimo[canal.nombre] = self._reloj()

    def _entregar(self, canal, texto, entradas, ctx, nota=None) -> None:
        estado, motivo = "fallida", None
        for intento in range(self.p["reintentos"] + 1):
            self._espaciar(canal)
            try:
                canal.enviar(texto)
                estado, motivo = ("simulada", "simulada, sin configurar") if canal.simulado else ("enviada", nota)
                break
            except Exception as e:  # cualquier fallo se anota; nunca llega a la decision
                pedida = e.espera_s if isinstance(e, ErrorEntrega) else None
                motivo = e.motivo if isinstance(e, ErrorEntrega) else type(e).__name__
                if intento < self.p["reintentos"]:
                    self._dormir(min(pedida or self.p["espera_s"] * 2 ** intento, self.p["espera_max_s"]))
        for e in entradas:
            e.update(estado=estado, motivo=motivo)
        anotar("notificacion", canal=canal.nombre, estado=estado, **ctx)
