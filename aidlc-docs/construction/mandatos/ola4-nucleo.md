# Mandato Ola 4: Núcleo, aprobar, marcador y servir la interfaz (rama `nucleo`, worktree `../wt-nucleo`)

Objetivo: una escalada se puede aprobar o rechazar con reevaluación, el marcador existe y la app sirve la interfaz. Código ligero: tope de diff 500 líneas (sin pruebas).

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/plans/nucleo-code-generation-plan.md` (T4), `aidlc-docs/construction/nucleo/functional-design/`, `contrato/api.openapi.yaml` y `contrato/aprobacion.schema.json`, `nucleo/` actual.
Escribir solo: `nucleo/` y `nucleo/tests/`.

Hacer:
1. `POST /api/decisiones/{id}/aprobar` y `/rechazar` según el contrato: aprobar siempre reevalúa (mismo motor); R9 no se supera aprobando; una escalada aprobada produce un recibo nuevo con las fallas aprobadas y la reserva, y la aprobación se liga a ese recibo; rol por la cabecera `X-Rol` y quien propone no contrafirma. `Idempotency-Key`.
2. `GET /api/marcador`: conteo de la sesión por veredicto y autonomía; si existe `evaluacion/salida/resultados-set.json`, lo incluye tal cual (se lee como dato, no se importa código de evaluación).
3. Montar `interfaz/dist` en `/` si la carpeta existe (sin romper las rutas `/api`), y comando de arranque documentado en `nucleo/LEEME.md` para el despliegue de Dev A.
4. Pruebas (máx. 12): aprobar reevalúa, R9 no se supera, escalada aprobada da recibo nuevo y el guardián lo acepta, rechazar, rol incorrecto, idempotencia, marcador.

Listo cuando: `python3 verify.py --etapa nucleo` verde y marcadas las casillas del plan. En el informe incluye la fila para `tandas.md` (CLAUDE.md, control del avance). Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
