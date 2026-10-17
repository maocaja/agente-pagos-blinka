# Mandato Ola 9: Lectura, reasignar proveedor de los documentos multicanal (rama `lectura`)

Objetivo: los documentos con nombre corto (Pixel Studio, Logistica Sur, Taller Pampa) se asignan a su proveedor del registro, que ahora tiene esos alias en `datos/registro-maestro.json`. Código ligero: tope de diff 60 líneas. Máximo 1 prueba nueva.

Leer: `CLAUDE.md` (4, 5c), `lectura/proveedor.py`, `lectura/extracciones_multicanal/` (en especial chat-09, eml-08, eml-10, pdf-03, foto-04), `datos/registro-maestro.json`.
Escribir solo: `lectura/` y `lectura/tests/`.

Hacer:
1. Reasigna `proveedor_asignado` en las lecturas congeladas de `lectura/extracciones_multicanal/` con `asignar_proveedor` (script de una vez; no se tocan montos, textos ni hashes). Valida contra el esquema.
2. Informa cuáles documentos quedan sin proveedor y por qué (nombre, id fiscal); no inventes coincidencias. Una coincidencia ambigua debe quedar sin asignar.
3. 1 prueba: los tres nombres cortos se asignan al proveedor correcto y un nombre parecido no registrado no se asigna.

Listo cuando: `python3 verify.py --etapa lectura` verde. Incluye la fila para `tandas.md`. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 100 palabras.
