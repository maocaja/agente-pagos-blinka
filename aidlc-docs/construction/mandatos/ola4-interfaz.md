# Mandato Ola 4: Interfaz, reglas, marcador, bandeja y guion (rama `interfaz`, worktree `../wt-interfaz`)

Objetivo: lo que falta para las escenas 1 a 5 del video. Código ligero: tope de diff 900 líneas (sin CSS compilado). Páginas estáticas con Alpine sobre las de la Ola 2; sin SPA ni store.

Leer: `CLAUDE.md` (4, 5, 5c), `docs/design-system/`, `aidlc-docs/construction/interfaz/functional-design/`, `aidlc-docs/construction/plans/interfaz-code-generation-plan.md` (T3 a T5), `contrato/api.openapi.yaml` (`/api/mandato`, `/api/proveedores`, `/api/marcador`, `/api/muestras`, `/api/sesion/reiniciar`, `/api/pentest/ejecutar`, `/api/arena/ejecutar`), `contrato/ejemplos/`, `aidlc-docs/inception/demo-script.md`, `interfaz/` actual.
Escribir solo: `interfaz/` y `interfaz/tests/`. Si necesitas una ruta que el contrato no tiene, repórtalo; no la inventes.

Hacer:
1. Navegación entre páginas (Decisiones, Reglas, Marcador, Bandeja, Ataque).
2. Reglas (solo lectura): umbrales, límites, monedas, tope acumulado y versión del mandato desde `/api/mandato`; lista de proveedores desde `/api/proveedores`; autonomía por proveedor.
3. Marcador: el número dominante, aciertos de reglas y de extremo a extremo por separado, autonomía, escalada innecesaria, costo, y la nota "lo que esta cifra no prueba".
4. Ataque: vista dividida (estrategias a la izquierda; marcador y motivo del bloqueo a la derecha), mandato v1 contra v2 con el hueco señalado, con los resultados de `/api/pentest/ejecutar` y `/api/arena/ejecutar` (el servidor simulado los responde con `contrato/ejemplos/resultados.arena.json`).
5. Bandeja simulada con la etiqueta "simulada" visible: lista de `/api/muestras` (correo, chat, PDF, foto); abrir una muestra muestra el original junto a lo leído y su decisión. En esa vista, las tres trampas (instrucción oculta, autoridad falsa, cuenta cambiada) se ven con la regla que las detuvo.
6. Botón Demo: reinicia la sesión (`/api/sesion/reiniciar`) tras una confirmación dentro de la página y recorre las escenas del guion con flechas y Esc.
7. 4 a 6 pruebas de Python nuevas: ninguna página con `x-html`, las nuevas respuestas del servidor simulado validan contra el contrato, la navegación enlaza páginas existentes.
8. Revisa con Chrome (Claude in Chrome) la consola desde la carga inicial y el ancho de teléfono; si el navegador no responde, dilo.

Listo cuando: `python3 verify.py --etapa interfaz` verde y casillas del plan marcadas. En el informe incluye la fila para `tandas.md`. `x-text` siempre, `data-testid`, tokens de la guía, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
