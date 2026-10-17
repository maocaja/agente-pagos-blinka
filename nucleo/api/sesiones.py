class Sesiones:
    """Una sesion por visitante: servicio propio, claves propias. Sin cabecera se usa la sesion por defecto."""

    def __init__(self, fabrica, ids):
        self._fabrica, self._ids = fabrica, ids
        self._por_id: dict = {}
        self.defecto = self._nuevo("v2", "defecto")

    def _nuevo(self, version, sid):
        s = self._fabrica(version)
        s.asignar_sesion(sid)
        return s

    def crear(self, version: str = "v2") -> str:
        sid = self._ids("s")
        self._por_id[sid] = self._nuevo(version, sid)
        return sid

    def obtener(self, sid):
        return self.defecto if sid is None else self._por_id.get(sid)

    def reiniciar(self, sid) -> bool:
        servicio = self.obtener(sid)
        if servicio is None:
            return False
        nuevo = self._nuevo(servicio.m.version, sid or "defecto")
        if sid is None:
            self.defecto = nuevo
        else:
            self._por_id[sid] = nuevo
        return True
