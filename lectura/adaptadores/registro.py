from .base import Documento, Resultado, escalar, validar_canonica


class Registro:
    def __init__(self, adaptadores=()):
        self._adaptadores = list(adaptadores)

    def registrar(self, adaptador):
        self._adaptadores.append(adaptador)

    def convertir(self, documento: Documento) -> Resultado:
        """Primer adaptador que soporta el documento; sin ninguno, o ante cualquier falla, escala."""
        for adaptador in self._adaptadores:
            try:
                if not adaptador.soporta(documento):
                    continue
                resultado = adaptador.a_canonica(documento)
                if resultado.factura is not None:
                    errores = validar_canonica(resultado.factura)
                    if errores:
                        return escalar("esquema_invalido", errores)
                return resultado
            except Exception as exc:
                return escalar("error_de_adaptador", [f"{adaptador.nombre}: {type(exc).__name__}"])
        return escalar("tipo_no_soportado", [documento.formato])


def registro_por_defecto():
    from .texto import AdaptadorTexto
    return Registro([AdaptadorTexto()])
