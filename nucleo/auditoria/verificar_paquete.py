"""Verifica fuera de la app las firmas de un paquete de auditoria. Uso: python3 verificar_paquete.py paquete.json"""
import base64
import json
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def _bytes_firmados(recibo):
    sin = {k: v for k, v in recibo.items() if k != "firma"}
    return json.dumps(sin, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verificar(paquete):
    clave = Ed25519PublicKey.from_public_bytes(base64.b64decode(paquete["clave_publica"]))
    malos = []
    for r in paquete["recibos"]:
        try:
            clave.verify(base64.b64decode(r["firma"]), _bytes_firmados(r))
        except (InvalidSignature, KeyError, ValueError):
            malos.append(r.get("id"))
        if r.get("mandato_version") not in paquete["mandatos"]:
            malos.append(f"{r.get('id')}: mandato no incluido")
    return malos


if __name__ == "__main__":
    malos = verificar(json.load(open(sys.argv[1], encoding="utf-8")))
    print("PAQUETE VALIDO" if not malos else f"PAQUETE INVALIDO: {malos}")
    sys.exit(1 if malos else 0)
