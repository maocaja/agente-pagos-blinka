#!/usr/bin/env python3
"""Revision mecanica de calidad de una unidad: tamano, complejidad, capas y duplicacion.

Uso: python3 calidad.py <carpeta> [<carpeta> ...]
Una funcion puede quedar fuera con un comentario `# calidad-ok: <motivo>` en la linea del def.
"""
import ast
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

MAX_LINEAS_FUNCION = 60
MAX_COMPLEJIDAD = 12
MAX_LINEAS_ARCHIVO = 400
MAX_METODOS_PUERTO = 5
VENTANA_DUPLICADO = 6
PROHIBIDOS_EN_DOMINIO = {"fastapi", "starlette", "sqlite3", "sqlalchemy", "anthropic", "httpx", "requests", "uvicorn"}
EXCLUIDOS = {"tests", "__pycache__", "node_modules", "dist"}
# El verificador es independiente a proposito: no se compara con el resto.
SIN_COMPARAR = ("evaluacion/verificador",)
RAMAS = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.With, ast.AsyncWith,
         ast.IfExp, ast.comprehension, ast.Assert)


def archivos(carpeta):
    for p in sorted(Path(carpeta).rglob("*.py")):
        if not (set(p.parts) & EXCLUIDOS):
            yield p


def complejidad(nodo):
    n = 1
    for h in ast.walk(nodo):
        if isinstance(h, RAMAS):
            n += 1
        elif isinstance(h, ast.BoolOp):
            n += len(h.values) - 1
    return n


def exento(lineas, nodo):
    return "calidad-ok" in lineas[nodo.lineno - 1]


def revisar_archivo(p):
    texto = p.read_text()
    lineas = texto.splitlines()
    hallazgos = []
    if len(lineas) > MAX_LINEAS_ARCHIVO:
        hallazgos.append(f"{p}: {len(lineas)} lineas; el maximo es {MAX_LINEAS_ARCHIVO}. Dividir por responsabilidad")
    try:
        arbol = ast.parse(texto)
    except SyntaxError as e:
        return [f"{p}: no se puede analizar ({e.msg})"]
    en_dominio = "dominio" in p.parts
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and not exento(lineas, nodo):
            largo = nodo.end_lineno - nodo.lineno + 1
            if largo > MAX_LINEAS_FUNCION:
                hallazgos.append(f"{p}:{nodo.lineno} {nodo.name} tiene {largo} lineas; el maximo es {MAX_LINEAS_FUNCION}")
            c = complejidad(nodo)
            if c > MAX_COMPLEJIDAD:
                hallazgos.append(f"{p}:{nodo.lineno} {nodo.name} tiene complejidad {c}; el maximo es {MAX_COMPLEJIDAD}")
        if isinstance(nodo, ast.ClassDef) and any(
                (getattr(b, "id", None) or getattr(b, "attr", None)) == "Protocol" for b in nodo.bases):
            metodos = [m for m in nodo.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if len(metodos) > MAX_METODOS_PUERTO:
                hallazgos.append(f"{p}:{nodo.lineno} puerto {nodo.name} con {len(metodos)} metodos; el maximo es {MAX_METODOS_PUERTO}")
        if en_dominio and isinstance(nodo, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in nodo.names] if isinstance(nodo, ast.Import) else [nodo.module or ""]
            for m in mods:
                if m.split(".")[0] in PROHIBIDOS_EN_DOMINIO:
                    hallazgos.append(f"{p}:{nodo.lineno} el dominio no puede importar {m}; se inyecta detras de un puerto")
    return hallazgos


def lineas_utiles(p):
    salida = []
    for i, linea in enumerate(p.read_text().splitlines(), 1):
        s = linea.strip()
        if len(s) < 20 or s.startswith(("#", "import ", "from ", "@", '"""', ")", "]", "}")):
            continue
        salida.append((i, s))
    return salida


def duplicados(rutas):
    vistos = defaultdict(list)
    for p in rutas:
        if any(x in p.as_posix() for x in SIN_COMPARAR):
            continue
        u = lineas_utiles(p)
        for k in range(len(u) - VENTANA_DUPLICADO + 1):
            bloque = "\n".join(s for _, s in u[k:k + VENTANA_DUPLICADO])
            vistos[hashlib.sha1(bloque.encode()).hexdigest()].append((p, u[k][0]))
    hallazgos, ya = [], set()
    for sitios in vistos.values():
        distintos = {(p, l) for p, l in sitios}
        if len(distintos) > 1:
            clave = tuple(sorted(f"{p}:{l}" for p, l in distintos))
            if not any(c in ya for c in clave):
                ya.update(clave)
                hallazgos.append("bloque duplicado (>= %d lineas) en %s. Extraer a una sola funcion" % (VENTANA_DUPLICADO, ", ".join(clave[:4])))
    return hallazgos


def revisar(carpetas):
    rutas = [p for c in carpetas for p in archivos(c)]
    hallazgos = []
    for p in rutas:
        hallazgos += revisar_archivo(p)
    return hallazgos + duplicados(rutas)


if __name__ == "__main__":
    h = revisar(sys.argv[1:] or ["."])
    for x in h:
        print("CALIDAD:", x)
    print(f"calidad: {len(h)} hallazgos")
    sys.exit(1 if h else 0)
