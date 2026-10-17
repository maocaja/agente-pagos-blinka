# Plan de diseño funcional: U1 Núcleo

## Pasos
- [x] Analizar el contexto de la unidad (`unit-of-work.md`)
- [x] Responder las 13 preguntas de reglas de negocio (una por una)
- [x] Analizar las respuestas y resolver ambigüedades (4 supuestos quedaron marcados en `business-rules.md`)
- [x] Generar `nucleo/functional-design/business-rules.md`
- [x] Generar `nucleo/functional-design/business-logic-model.md`
- [x] Generar `nucleo/functional-design/domain-entities.md`
- [x] Aprobación (2026-10-16), incluidos los 7 supuestos de `business-rules.md`

## Decisión previa
Los identificadores de reglas son los de `demo-front/motor.js`: R1 lectura, R2 duplicado, R3 beneficiario, R4 cuenta, R5 acuerdo, R6 montos, R7 moneda, R8 texto dirigido al agente, R9 presupuesto, R10 tope acumulado. El PRD usaba otra numeración; la del motor prevalece y se registra en `contrato/`.

## Preguntas
| # | Tema | Respuesta |
|---|---|---|
| 1 | Duplicado difuso: acción y parámetros | A: ESCALAR, monto ±2%, ventana de 30 días |
| 2 | Normalización del número de factura | A: mayúsculas y sin símbolos, sin quitar ceros |
| 3 | Confianza mínima de lectura | A: 0,80 global y 0,90 en campos de dinero |
| 4 | Qué es "lo acordado" y qué pasa sin acuerdo | A: monto máximo por factura; sin acuerdo, ESCALAR |
| 5 | Perfil del mandato v1 | A: perfil Balanceado, con la condición de que todo esté parametrizado y no haya valores quemados |
| 6 | Periodo del presupuesto y del acumulado | A: mes calendario, configurable |
| 7 | Mandato del set frente al del pentest (R10) | A: dos mandatos precargados (v2 con R10 para el set; v1 sin R10 para el pentest) |
| 8 | Escalada aprobada cuando el presupuesto ya no alcanza | A: reevaluar y volver a ESCALAR con el motivo |
| 9 | Vigencia de la aprobación y del recibo | A: 24 horas, configurable |
| 10 | Cuenta nueva aprobada: ¿pasa a ser la registrada? | A: no, la aprobación vale solo para esa factura |
| 11 | Notas de crédito, estados de cuenta, proformas | A: nota de crédito como crédito a favor; estado de cuenta FRENAR; proforma ESCALAR |
| 12 | Quién edita el mandato | A: el CFO propone y el analista contrafirma |
| 13 | Nivel de autonomía por defecto de un proveedor | A: autónomo bajo reglas; el proveedor nuevo arranca en sombra |
