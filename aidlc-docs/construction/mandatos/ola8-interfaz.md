# Mandato Ola 8: Interfaz, adaptar el ataque a lo real, modo de lectura, cargar set y revisión en Chrome (rama `interfaz`)

Objetivo: la interfaz funciona igual contra la app real que contra el simulador. Código ligero: tope de diff 350 líneas. Máximo 3 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5, 5c), `contrato/api.openapi.yaml` (pentest y arena ahora devuelven la forma de `resultados.schema.json`: `recuentos`, `casos`, `no_prueba`; el id de un caso empieza por la estrategia, p. ej. `E1-v2-1`; `/api/sesion` trae `lectura`), `evaluacion/salida/pentest.json`, `pentest-v1.json` y `arena.json` (ejemplos reales), `interfaz/` actual.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Hacer:
1. Página Ataque: adaptarla a la forma real. Agrupa `casos` por estrategia (prefijo del id), muestra v1 contra v2 (`pentest-v1.json` contra `pentest.json`: pagos indebidos y la clase de cada caso), y el hueco de v1 señalado. Arena: `recuentos` y `no_prueba`. Actualiza el servidor simulado para devolver estos archivos reales.
2. Rótulo "Lectura guardada" o "Lectura en vivo" en la barra, tomado de `/api/sesion.lectura`.
3. Botón "Cargar el set" en la Bandeja: llama a `POST /api/muestras/{id}/cargar` por cada muestra, en orden, y refresca la lista; muestra progreso y errores con su motivo.
4. Revisión en Chrome (Claude in Chrome): consola sin errores desde la carga, contraste (texto 4,5:1, bordes 3:1) y foco visible por teclado en las 5 páginas, ancho 375 px. Corrige lo que falle. Si el navegador no responde, dilo y no afirmes que se revisó.
5. Hasta 3 pruebas: el ataque agrupa por estrategia con los archivos reales, el simulador devuelve respuestas que validan, ninguna página con `x-html`.

Listo cuando: `python3 verify.py --etapa interfaz` verde. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, tokens de la guía, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
