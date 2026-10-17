#!/usr/bin/env python3
"""Control del avance: el estado y el registro de tandas no pueden quedar detras del codigo."""
import subprocess
import sys

CODIGO = ["nucleo", "lectura", "interfaz", "evaluacion", "contrato", "datos"]
CONTROL = ["aidlc-docs/aidlc-state.md", "aidlc-docs/construction/tandas.md"]


def ultimo_cambio(rutas):
    salida = subprocess.run(["git", "log", "-1", "--format=%ct", "--", *rutas],
                            capture_output=True, text=True).stdout.strip()
    return int(salida) if salida else 0


def revisar():
    codigo = ultimo_cambio(CODIGO)
    return [f"{c} esta detras del ultimo cambio de codigo; actualizar antes de cerrar la tanda"
            for c in CONTROL if ultimo_cambio([c]) < codigo]


if __name__ == "__main__":
    h = revisar()
    for x in h:
        print("CONTROL:", x)
    print(f"control: {len(h)} hallazgos")
    sys.exit(1 if h else 0)
