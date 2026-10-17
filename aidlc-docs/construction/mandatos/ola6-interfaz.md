# Mandato Ola 6: Interfaz, aprobar, proponer mandato, explicación y auditoría (rama `interfaz`)

Objetivo: cerrar lo que falta de las escenas 1 a 5 y de las ideas aprobadas. Código ligero: tope de diff 700 líneas (sin CSS compilado). Máximo 5 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5, 5c), `docs/design-system/`, `aidlc-docs/construction/plans/interfaz-code-generation-plan.md` (3.1 a 3.3, 1.2, 5.3), `contrato/api.openapi.yaml` (aprobar, rechazar, `/api/mandato/previa`, `/api/auditoria/paquete`, `/api/ordenes/{id}/pain001`, campos `explicacion` y `que_hacer` de la decisión), `interfaz/` actual y `interfaz/servidor_simulado.py`.
Escribir solo: `interfaz/` y `interfaz/tests/`. Si necesitas algo que el contrato no tiene, repórtalo; no lo inventes.

Hacer:
1. Decisiones y recibo: mostrar `explicacion` y `que_hacer` en una frase clara, bien visible.
2. Bandeja del aprobador: razón en una frase, botones aprobar y rechazar (solo el rol CFO; el servidor igual lo valida); aprobar siempre reevalúa y muestra el recibo nuevo; errores del servidor (409) con su motivo, sin apología.
3. Reglas editables con vista previa: el usuario cambia un umbral o límite, pulsa Vista previa y ve cuántas facturas cambian de veredicto y cuáles (`POST /api/mandato/previa`); nada se guarda en la vista previa.
4. Auditoría: botón que descarga el paquete (`/api/auditoria/paquete`) y, en una decisión autorizada, la orden de pago simulada (pain.001) con su etiqueta SIMULADA. Descargas con enlaces `<a href>` normales a la API, no con scripts.
5. Rótulo de modo de lectura ("lectura guardada" o "lectura en vivo") tomado de `/api/sesion` si el contrato lo trae; si no, repórtalo sin inventar.
6. Revisión: contraste (texto 4,5:1, bordes 3:1) y foco visible por teclado en todas las páginas, con Chrome si responde. Corrige lo que falle y anota lo que no pudiste revisar.
7. El servidor simulado devuelve respuestas que validan contra el contrato para todo lo nuevo. Pruebas: ninguna página con `x-html`, las respuestas nuevas validan, la vista previa no persiste.

Listo cuando: `python3 verify.py --etapa interfaz` verde y casillas marcadas. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, tokens de la guía, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
