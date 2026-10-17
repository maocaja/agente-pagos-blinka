import json
from pathlib import Path

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

_COMANDOS = {"pentest.json": "python3 -m evaluacion.pentest", "pentest-v1.json": "python3 -m evaluacion.pentest",
             "arena.json": "python3 -m evaluacion.arena"}


def _servir(salida: Path, nombre: str):
    ruta = salida / nombre
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return JSONResponse({"codigo": "no_encontrado", "mensaje": f"Falta {nombre}; generalo con: {_COMANDOS[nombre]}",
                             "detalle": None}, status_code=404)


def rutas_evaluacion(salida: Path) -> APIRouter:
    """Sirve como datos lo que evaluacion ya produjo; no importa ni ejecuta su codigo."""
    r = APIRouter()

    @r.post("/api/pentest/ejecutar")
    def pentest(cuerpo: dict | None = Body(None)):
        v1 = (cuerpo or {}).get("mandato_base") == "v1"
        return _servir(salida, "pentest-v1.json" if v1 else "pentest.json")

    @r.post("/api/arena/ejecutar")
    def arena(cuerpo: dict | None = Body(None)):
        return _servir(salida, "arena.json")

    return r
