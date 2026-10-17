# Mandato Ola 7: Núcleo, rutas de pentest y arena, y modo de lectura (rama `nucleo`)

Objetivo: la interfaz puede pedir el pentest y la arena, y mostrar si la lectura es guardada o en vivo. Código ligero: tope de diff 200 líneas. Máximo 3 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `contrato/api.openapi.yaml` (`/api/pentest/ejecutar`, `/api/arena/ejecutar`, `/api/sesion`), `contrato/resultados.schema.json`, `nucleo/api/` actual (cómo el marcador lee `evaluacion/salida/resultados-set.json`).
Escribir solo: `nucleo/`, `nucleo/tests/` y, como cambio ADITIVO, `contrato/` (campo opcional `lectura` en la respuesta de `/api/sesion`; subir a 1.1.0-rc2 y anotarlo en `contrato/README.md`).

Hacer:
1. `POST /api/pentest/ejecutar` y `/api/arena/ejecutar` devuelven, como datos, el contenido de `evaluacion/salida/pentest.json` (o `pentest-v1.json` si el cuerpo pide mandato v1) y `arena.json`; no importan código de evaluación ni lo ejecutan. Si el archivo no existe, error claro 404 con el comando para generarlo.
2. `/api/sesion` incluye `lectura`: "en_vivo" si `ANTHROPIC_API_KEY` está definida y no vacía, "guardada" si no (solo lee la variable; nunca la imprime).
3. 3 pruebas: ambas rutas devuelven resultados que validan contra el esquema, 404 si falta el archivo, el modo cambia con la variable sin exponerla.

Listo cuando: `python3 verify.py --etapa nucleo` y `--etapa contrato` verdes. Incluye la fila para `tandas.md`. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 120 palabras.
