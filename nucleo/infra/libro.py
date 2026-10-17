import sqlite3
import threading
from contextlib import contextmanager

from ..dominio.errores import FallaCerrada

_ESQUEMA = """
CREATE TABLE movimientos (id INTEGER PRIMARY KEY, recibo_id TEXT NOT NULL, nonce TEXT NOT NULL,
  proveedor_id TEXT NOT NULL, periodo TEXT NOT NULL, monto INTEGER NOT NULL, tipo TEXT NOT NULL);
CREATE UNIQUE INDEX un_nonce_reserva ON movimientos(nonce) WHERE tipo = 'reserva';
CREATE UNIQUE INDEX un_movimiento ON movimientos(recibo_id, tipo);
CREATE TABLE usos (nonce TEXT PRIMARY KEY, recibo_id TEXT NOT NULL);
CREATE TRIGGER sin_update_mov BEFORE UPDATE ON movimientos BEGIN SELECT RAISE(ABORT, 'solo adicion'); END;
CREATE TRIGGER sin_delete_mov BEFORE DELETE ON movimientos BEGIN SELECT RAISE(ABORT, 'solo adicion'); END;
CREATE TRIGGER sin_update_uso BEFORE UPDATE ON usos BEGIN SELECT RAISE(ABORT, 'solo adicion'); END;
CREATE TRIGGER sin_delete_uso BEFORE DELETE ON usos BEGIN SELECT RAISE(ABORT, 'solo adicion'); END;
"""


class LibroSqlite:
    """Registro de solo adicion; el presupuesto restante se deriva de la suma de movimientos."""

    def __init__(self, ruta: str = ":memory:"):
        self._c = sqlite3.connect(ruta, check_same_thread=False, isolation_level=None)
        self._c.executescript(_ESQUEMA)
        self._cerrojo = threading.Lock()

    @contextmanager
    def _transaccion(self):
        with self._cerrojo:
            self._c.execute("BEGIN IMMEDIATE")
            try:
                yield
                self._c.execute("COMMIT")
            except BaseException:
                self._c.execute("ROLLBACK")
                raise

    def _suma(self, periodo, proveedor_id=None) -> int:
        sql, args = "SELECT COALESCE(SUM(monto), 0) FROM movimientos WHERE periodo = ?", [periodo]
        if proveedor_id is not None:
            sql, args = sql + " AND proveedor_id = ?", args + [proveedor_id]
        return self._c.execute(sql, args).fetchone()[0]

    def acumulado(self, periodo, proveedor_id=None) -> int:
        with self._cerrojo:
            return self._suma(periodo, proveedor_id)

    def reservar(self, recibo_id, nonce, proveedor_id, periodo, monto, tope) -> None:
        with self._transaccion():
            if self._suma(periodo) + monto > tope:
                raise FallaCerrada("El presupuesto del periodo ya no alcanza para reservar este pago.")
            try:
                self._c.execute("INSERT INTO movimientos (recibo_id, nonce, proveedor_id, periodo, monto, tipo) VALUES (?,?,?,?,?,'reserva')",
                                (recibo_id, nonce, proveedor_id, periodo, monto))
            except sqlite3.IntegrityError as e:
                raise FallaCerrada("El nonce o el recibo ya tienen una reserva.") from e

    def liberar(self, recibo_id) -> bool:
        """Movimiento compensatorio; no libera un recibo ya autorizado ni uno ya liberado."""
        with self._transaccion():
            fila = self._c.execute("SELECT nonce, proveedor_id, periodo, monto FROM movimientos WHERE recibo_id = ? AND tipo = 'reserva'", (recibo_id,)).fetchone()
            if fila is None or self._c.execute("SELECT 1 FROM usos WHERE recibo_id = ?", (recibo_id,)).fetchone():
                return False
            try:
                self._c.execute("INSERT INTO movimientos (recibo_id, nonce, proveedor_id, periodo, monto, tipo) VALUES (?,?,?,?,?,'liberacion')",
                                (recibo_id, fila[0], fila[1], fila[2], -fila[3]))
            except sqlite3.IntegrityError:
                return False
            return True

    def consumir_nonce(self, nonce, recibo_id) -> bool:
        """Autoriza una sola vez y solo si la reserva sigue viva (reevaluacion del presupuesto)."""
        with self._transaccion():
            viva = self._c.execute("SELECT COALESCE(SUM(monto), 0) FROM movimientos WHERE recibo_id = ? AND nonce = ?", (recibo_id, nonce)).fetchone()[0]
            if viva <= 0:
                return False
            try:
                self._c.execute("INSERT INTO usos (nonce, recibo_id) VALUES (?, ?)", (nonce, recibo_id))
            except sqlite3.IntegrityError:
                return False
            return True
