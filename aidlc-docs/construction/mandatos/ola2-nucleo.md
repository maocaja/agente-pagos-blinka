# Mandato Ola 2: Núcleo (rama `nucleo`, worktree `../wt-nucleo`)

Objetivo: el núcleo decide las 18 facturas con las 11 reglas, firma el recibo y el guardián se niega sin recibo válido. Código ligero: tope de diff 900 líneas añadidas en total (sin pruebas).

Leer: `CLAUDE.md` (5c), `aidlc-docs/inception/architecture-target-vs-mvp.md`, `aidlc-docs/construction/plans/nucleo-code-generation-plan.md` (T2, T3 y partes de T5), `aidlc-docs/construction/nucleo/functional-design/`, `contrato/` (manda), `datos/registro-maestro.json`, `datos/esperado.json`, `nucleo/` actual.
Escribir solo: `nucleo/` y `nucleo/tests/`. No tocar `contrato/`, `lectura/`, `evaluacion/`, `interfaz/`, `datos/`.

Hacer, en este orden:
1. Cargar `datos/registro-maestro.json` como único registro; borrar `nucleo/datos_prueba/`.
2. Reglas simples (R3, R4, R5, R6, R7) como filas del mandato leídas por un evaluador genérico; funciones propias solo para R1, R2a, R2b, R8, R9, R10. Quitar el fixture que inyecta 4 reglas: el motor debe tener las 11.
3. Mandatos `contrato/ejemplos/mandato.v1.json` (sin R10) y `v2.json` (con R10), seleccionables por la sesión.
4. Guardián con las 6 verificaciones del diseño, `POST /api/guardian/verificar` y orden de pago Autorizada o Denegada (no mueve dinero). Reserva de presupuesto y nonce en una transacción SQLite, idempotencia por clave.
5. Rutas mínimas del contrato para el video: `/api/sesion`, `/api/sesion/reiniciar`, `/api/decisiones` (+ detalle), `/api/recibos/{id}` y `/verificar`, `/api/clave-publica`, `/api/mandato`, `/api/proveedores`, `/api/guardian/verificar`. Aprobar con reevaluación solo si cabe en el tope.
6. Prueba parametrizada sobre `lectura/extracciones/fac-*.json` contra `datos/esperado.json` (veredicto de reglas). Al llegar a este paso ejecuta `git merge lectura` en tu worktree para tener `proveedor_id` asignado. Más 10 a 15 pruebas: firma alterada, guardián (6 verificaciones), nonce reutilizado, v1 contra v2 con facturas partidas, falla cerrado ante tipo desconocido.

Listo cuando: `python3 verify.py --etapa nucleo` verde (incluye calidad); las 18 facturas coinciden con `esperado.json` o cada discrepancia queda listada con motivo (no se edita `esperado.json`); máximo 30 pruebas nuevas.
Recordatorio: falla cerrado, dinero en enteros como texto, sin secretos, comentarios cortos sin emojis, `graphify query` antes de grep, no commit ni push. Responde en máximo 150 palabras: hechos, rutas:línea, discrepancias.
