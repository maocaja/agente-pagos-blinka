# Mandato Ola 2: Interfaz, pantalla de Decisiones y recibo (rama `interfaz`, worktree `../wt-interfaz`)

Objetivo: lo que se ve en las escenas 1 a 3 del video. Código ligero: tope de diff 700 líneas (sin CSS compilado). Páginas HTML estáticas con Alpine, sin SPA, sin store, sin componentes separados: la página pide JSON y lo pinta.

Leer: `CLAUDE.md` (5, 5c), `docs/design-system/{tokens.css,componentes.css,entrada.css,construir_guia.py}`, `aidlc-docs/construction/interfaz/functional-design/`, `aidlc-docs/construction/plans/interfaz-code-generation-plan.md` (T1 y T2), `contrato/api.openapi.yaml` y `contrato/ejemplos/`.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Hacer:
1. Tailwind v4.3.3 con su CLI sobre `entrada.css` y los tokens: `interfaz/dist/app.css` compilado y Alpine 3.17.4 copiado a `dist/` (sin CDN). Tema claro y oscuro.
2. `interfaz/dist/index.html`: lista de decisiones con chip de veredicto (ícono y palabra), razón en una frase y filtro por veredicto. Cliente de la API en un solo archivo JS con `Idempotency-Key`.
3. Recibo legible como documento (factura, regla y versión del mandato, decisión, hora, firma) con vista técnica; campo editable "alterar para la demo" que altera una copia y la envía a `POST /api/guardian/verificar`; sello que se estampa o se parte y lista de las 6 verificaciones con motivo.
4. `interfaz/servidor_simulado.py`: FastAPI mínimo que sirve `dist/` y responde con los ejemplos del contrato, para trabajar y probar sin el núcleo. En el despliegue, el núcleo monta `interfaz/dist` (lo hace Dev A).
5. `x-text` siempre, nunca `x-html`; `data-testid` en cada elemento interactivo. 4 a 6 pruebas de Python: función de escape, que ningún HTML use `x-html`, que el servidor simulado devuelva ejemplos que validan contra el contrato.

Listo cuando: `python3 verify.py --etapa interfaz` verde; la página abre contra el servidor simulado sin errores de consola (revisar con Chrome DevTools MCP o, si no responde, decirlo). Verificación de la firma en el navegador: solo por el endpoint del servidor.
Recordatorio: skill `frontend-design` con la guía de estilo, sin colores nuevos, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
