# Mandato Ola 5: Núcleo, explicación, vista previa, paquete de auditoría y orden de pago (rama `nucleo`)

Objetivo: cada decisión se explica en lenguaje claro; la empresa ve qué cambia antes de aprobar un mandato; un auditor verifica todo sin la app; la orden de pago sale en formato bancario simulado. Código ligero: tope de diff 600 líneas (sin pruebas).

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/inception/architecture-target-vs-mvp.md`, `contrato/` (README, `api.openapi.yaml` rutas `/api/decisiones/{id}/previa`, `/api/mandato/propuestas`, `/api/mandato/contrafirma`; `decision.schema.json`, `recibo.schema.json`), `nucleo/` actual.
Escribir solo: `nucleo/` y `nucleo/tests/`; y, como cambio ADITIVO, `contrato/` (campos o rutas nuevas opcionales; subir a 1.1.0-rc1 y anotarlo en `contrato/README.md`). No quitar ni cambiar nada existente.

Hacer:
1. Explicación: cada decisión trae `explicacion` (una a tres frases en español, determinista, construida solo desde los resultados por regla y su motivo; sin modelo) y "qué hacer" cuando es ESCALAR o FRENAR. Ejemplo: "La cuenta termina en 9021 y la registrada termina en 4417. Confirmar con el proveedor antes de pagar."
2. Vista previa del mandato: dado un mandato propuesto (o cambios sobre el vigente), reevalúa las facturas de la sesión (o las 18 del set) y devuelve cuántas cambian de veredicto y cuáles, sin guardar nada. Si ya existe `/api/mandato/propuestas` o `/previa` con ese fin, úsalas.
3. Paquete de auditoría: `GET /api/auditoria/paquete` entrega un JSON con los recibos de la sesión, la clave pública y el mandato citado en cada recibo, más `verificar_paquete.py` en `nucleo/auditoria/` (≤ 40 líneas, solo `cryptography` y biblioteca estándar, sin importar el resto del núcleo) que verifica todas las firmas fuera de la app.
4. Orden de pago simulada: cuando el guardián autoriza, la orden se puede descargar como XML tipo pain.001 mínimo (sin enviar nada, con la etiqueta SIMULADA). Ruta: `GET /api/ordenes/{id}/pain001`.
5. Pruebas (máx. 12): explicación por regla (R4, R8, R10), vista previa v1 contra v2 cambia lo esperado, el script verifica un paquete bueno y rechaza uno alterado, el XML bien formado.

Listo cuando: `python3 verify.py --etapa nucleo` verde y `contrato` valida. En el informe incluye la fila para `tandas.md` y los cambios del contrato. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
