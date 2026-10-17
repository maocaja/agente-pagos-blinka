# Mandato Ola 14: Núcleo, contexto del ciclo e historial de cada decisión (rama `nucleo`)

Objetivo: la interfaz puede mostrar el contexto de la empresa y la traza de cada decisión. Código ligero: tope de diff 200 líneas. Máximo 3 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/interfaz/functional-design/recorridos.md`, `contrato/api.openapi.yaml` (`/api/ciclo` ya existe en el contrato), `nucleo/` actual (libro de reserva, sesión, aprobar y rechazar).
Escribir solo: `nucleo/`, `nucleo/tests/` y, como cambio ADITIVO, `contrato/` (subir a 1.1.0-rc3 y anotarlo en `contrato/README.md`).

Forma exacta de las respuestas (la interfaz se construye contra esto):
1. `GET /api/ciclo` devuelve `{ciclo_id, empresa, moneda, presupuesto_menor, reservado_menor, disponible_menor, actividad: [{hora, texto}]}`: `empresa` es el nombre de la empresa de demostración (del registro maestro o de una constante de datos, no de código de reglas); importes en unidades menores como texto; `actividad` son los últimos 5 eventos de la sesión (decisiones, aprobaciones, rechazos) en español, más reciente primero.
2. El detalle de decisión (`GET /api/decisiones/{id}`) añade `historial: [{hora, evento, actor, nota}]` en orden cronológico: `evento` en {recibida, decidida, aprobada, rechazada, reevaluada}; `actor` es "motor" o el rol; `nota` es null si no hay. Se deriva de lo que ya se registra; no inventes eventos.
3. Si el guardián autorizó, el detalle indica `estado_orden`: "autorizada" o "orden_simulada_emitida" (cuando se descargó o se pidió el pain.001) o null. Nunca un estado de pago confirmado.

Hacer: implementa lo anterior reutilizando el libro de reserva y el registro existentes (no dupliques lógica), con contrato aditivo, y 3 pruebas: ciclo coherente con las reservas tras cargar dos facturas, historial tras aprobar o rechazar, ningún estado "pagado".

Listo cuando: `python3 verify.py --etapa nucleo` y `--etapa contrato` verdes. Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 120 palabras.
