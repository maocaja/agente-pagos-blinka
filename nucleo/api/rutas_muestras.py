import json
import mimetypes
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse

_RAIZ = Path(__file__).resolve().parents[2]
_TEXTO = {".txt", ".eml"}


def _original(archivo: Path | None) -> str:
    if archivo is None:
        return "documento binario: no disponible"
    if archivo.suffix in _TEXTO:
        return archivo.read_text(encoding="utf-8", errors="replace")
    return f"documento binario: {archivo.name}"


def _titulos_multicanal(docs: Path) -> dict[str, tuple[str, bool]]:
    """Stem -> (titulo legible, es adjunto); el manifiesto marca el adjunto en `trampa`."""
    doc = json.loads((docs / "manifiesto.json").read_text(encoding="utf-8"))["documentos"]
    return {d["archivo"].rsplit(".", 1)[0]: (d["nota"] or f'{d["proveedor_id"].removeprefix("prov_")} ({d["canal"]})',
                                            d["trampa"].startswith("adjunto del")) for d in doc}


def _catalogo(raiz: Path) -> dict[str, dict]:
    """Muestras = lecturas congeladas (datos) con su documento original al lado."""
    docs, lect = raiz / "datos" / "documentos", raiz / "lectura"
    muestras, multicanal = {}, _titulos_multicanal(docs)
    for carpeta, originales in ((lect / "extracciones", (raiz / "datos" / "facturas").glob("*.txt")),
                                (lect / "extracciones_multicanal", docs.iterdir())):
        por_sello = {p.name.rsplit(".", 1)[0]: p for p in originales}
        for ruta in sorted(carpeta.glob("*.json")):
            clave = next((k for k in por_sello if k == ruta.stem or k.startswith(ruta.stem + "-")), None)
            titulo, adjunto = multicanal.get(ruta.stem, (None, False))
            if adjunto:
                continue
            if titulo is None:
                titulo = clave.split("-", 2)[2].replace("-", " ") if clave and clave.count("-") >= 2 else ruta.stem
            lectura = json.loads(ruta.read_text(encoding="utf-8"))
            muestras[ruta.stem] = {"lectura": lectura, "original": _original(por_sello.get(clave)), "titulo": titulo,
                                    "ruta": por_sello.get(clave)}
    return muestras


def rutas_muestras(dep, cargar_factura, raiz: Path = _RAIZ) -> APIRouter:
    r = APIRouter()
    catalogo = _catalogo(raiz)

    @r.get("/api/muestras")
    def listar():
        return [{"id": id_, "titulo": m["titulo"], "tipo": m["lectura"]["documento"]["canal"],
                 "lectura_guardada": True, "original": m["original"]} for id_, m in catalogo.items()]

    @r.post("/api/muestras/{id}/cargar", status_code=201)
    def cargar(id: str, servicio=Depends(dep)):
        m = catalogo.get(id)
        if m is None:
            return _no_encontrada()
        return cargar_factura(servicio, m["lectura"], None, None)

    @r.get("/api/muestras/{id}/archivo")
    def archivo(id: str):
        ruta = (catalogo.get(id) or {}).get("ruta")
        if ruta is None or not _dentro(ruta, raiz):
            return _no_encontrada()
        return FileResponse(ruta, media_type=mimetypes.guess_type(ruta.name)[0] or "application/octet-stream")

    return r


def _dentro(ruta: Path, raiz: Path) -> bool:
    """Solo se sirven archivos de datos/documentos y datos/facturas."""
    real = ruta.resolve()
    return any(real.is_relative_to((raiz / "datos" / c).resolve()) for c in ("documentos", "facturas"))


def _no_encontrada():
    return JSONResponse({"codigo": "no_encontrado", "mensaje": "La muestra no existe.", "detalle": None}, status_code=404)
