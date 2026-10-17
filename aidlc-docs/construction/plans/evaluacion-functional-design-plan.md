# Plan de diseño funcional: U4 Evaluación

## Pasos
- [x] Analizar el contexto de la unidad (set y esperado, verificador independiente, pentest, arena, pruebas de mutación y de falla del extractor)
- [x] Responder las 6 preguntas (una por una)
- [x] Analizar las respuestas y resolver ambigüedades (semilla fija frente a variable; 4 ocultas en lugar de 3)
- [x] Generar `evaluacion/functional-design/business-rules.md`
- [x] Generar `evaluacion/functional-design/business-logic-model.md`
- [x] Generar `evaluacion/functional-design/domain-entities.md`
- [x] Aprobación (2026-10-16), incluidos los supuestos de `business-rules.md`

## Preguntas
| # | Tema | Respuesta |
|---|---|---|
| 1 | Cómo se definen los dos veredictos esperados | A: dos esperados escritos a mano antes de generar las lecturas, por quien lee solo el texto de las reglas; ninguno sale del motor; las ocultas se sellan con huella |
| 2 | Alcance del verificador independiente | A: recalcula todo el veredicto con un módulo independiente, con estado reconstruido desde el registro; separa pagos indebidos de desvíos conservadores |
| 3 | Niveles de la arena | A: dos niveles sin llamar al modelo (campos de la factura canónica y texto contra lecturas guardadas), semilla fija y visible |
| 4 | Estrategias del pentest | A: seis estrategias fijas con su esperado escrito antes; el hueco se corrige o se documenta; antes y después con la misma semilla |
| 5 | Pruebas de mutación | A: un mutante manual por regla, más orden de agregación, fallo cerrado y registro de solo adición; cada uno debe hacer fallar una prueba |
| 6 | Qué pasa si fallan las facturas ocultas | A: se reportan tal cual; política y huellas fijadas antes; cada fallo se diagnostica; si hay corrección se reportan ambas corridas |
