import json
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

_RAIZ = Path(__file__).resolve().parents[2]
_TEXTO = {".txt", ".eml"}


def _original(archivo: Path | None) -> str:
    if archivo is None:
        return "documento binario: no disponible"
    if archivo.suffix in _TEXTO:
        return archivo.read_text(encoding="utf-8", errors="replace")
    return f"documento binario: {archivo.name}"


def _catalogo(raiz: Path) -> dict[str, dict]:
    """Muestras = lecturas congeladas (datos) con su documento original al lado."""
    docs, lect = raiz / "datos" / "documentos", raiz / "lectura"
    muestras = {}
    for carpeta, originales in ((lect / "extracciones", (raiz / "datos" / "facturas").glob("*.txt")),
                                (lect / "extracciones_multicanal", docs.iterdir())):
        por_sello = {p.name.rsplit(".", 1)[0]: p for p in originales}
        for ruta in sorted(carpeta.glob("*.json")):
            clave = next((k for k in por_sello if k == ruta.stem or k.startswith(ruta.stem + "-")), None)
            lectura = json.loads(ruta.read_text(encoding="utf-8"))
            muestras[ruta.stem] = {"lectura": lectura, "original": _original(por_sello.get(clave))}
    return muestras


def rutas_muestras(dep, cargar_factura, raiz: Path = _RAIZ) -> APIRouter:
    r = APIRouter()
    catalogo = _catalogo(raiz)

    @r.get("/api/muestras")
    def listar():
        return [{"id": id_, "titulo": id_.replace("-", " "), "tipo": m["lectura"]["documento"]["canal"],
                 "lectura_guardada": True, "original": m["original"]} for id_, m in catalogo.items()]

    @r.post("/api/muestras/{id}/cargar", status_code=201)
    def cargar(id: str, servicio=Depends(dep)):
        m = catalogo.get(id)
        if m is None:
            return _no_encontrada()
        return cargar_factura(servicio, m["lectura"], None, None)

    return r


def _no_encontrada():
    return JSONResponse({"codigo": "no_encontrado", "mensaje": "La muestra no existe.", "detalle": None}, status_code=404)
