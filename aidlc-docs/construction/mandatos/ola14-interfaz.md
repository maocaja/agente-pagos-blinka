# Mandato Ola 14: Interfaz, los dos recorridos de producto (rama `interfaz`)

Objetivo: que la aplicación se sienta como una mesa de trabajo de cuentas por pagar y que los DOS recorridos de `aidlc-docs/construction/interfaz/functional-design/recorridos.md` se completen sin perder sesión ni contexto. Código ligero: tope de diff 600 líneas (sin CSS compilado). Máximo 2 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/construction/interfaz/functional-design/recorridos.md` (manda), `aidlc-docs/inception/personas.md`, `aidlc-docs/inception/demo-operativo.md`, `docs/design-system/` (sin colores ni componentes nuevos), `interfaz/dist/` y el simulador. Skill frontend-design con la guía de estilo.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Formas de respuesta del núcleo (se construyen en paralelo; el simulador debe devolver lo mismo):
- `GET /api/ciclo` devuelve `{ciclo_id, empresa, moneda, presupuesto_menor, reservado_menor, disponible_menor, actividad: [{hora, texto}]}`.
- `GET /api/decisiones/{id}` añade `historial: [{hora, evento, actor, nota}]` y `estado_orden` ("autorizada", "orden_simulada_emitida" o null).

Hacer:
1. Vocabulario: el resumen dice "Autorizadas para pago", nunca "Pagadas"; en el detalle se ven separados Decisión, Autorizada, Orden emitida (simulada) y se aclara que no hay "pago confirmado" porque no se mueve dinero.
2. Contexto al abrir Decisiones: empresa, periodo, presupuesto reservado y disponible (con barra simple) y la actividad reciente.
3. Recorrido 1: desde la fila de la cuenta cambiada, el detalle muestra el documento original junto a lo leído, el dato que difiere y el siguiente paso; el CFO rechaza con nota o aprueba; después se ve el historial y la actividad reciente actualizada. Errores con su motivo.
4. Recorrido 2: en el detalle, el panel "Verificar sin esta aplicación" con el enlace al paquete de auditoría, el comando exacto del script y el resultado esperado; y el historial completo de la decisión.
5. Actualiza `ESCENAS` del modo Demo para que sigan esos recorridos (escena 1: cuenta cambiada y resolución del CFO con su historial; escena 3: recibo, Verificar y el panel del auditor), con los textos del guion.
6. Verifica en Chrome contra la app real (`uvicorn nucleo.api.principal:app` en un puerto libre; restaura cualquier carpeta que toques) los DOS recorridos completos con el set curado y describe lo que viste paso a paso. Si el núcleo aún no sirve `/api/ciclo` o el `historial`, dilo y valida contra el simulador sin afirmar más.

Listo cuando: `python3 verify.py --etapa interfaz` verde y los dos recorridos descritos. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
