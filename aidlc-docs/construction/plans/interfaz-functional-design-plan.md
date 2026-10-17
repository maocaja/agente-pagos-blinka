# Plan de diseño funcional: U3 Interfaz

## Pasos
- [x] Analizar el contexto de la unidad (`unit-of-work.md`: pantallas, bandeja del aprobador, autonomía visible, contador de costo; parte de la maqueta `demo-front`)
- [x] Responder las preguntas de interfaz (una por una)
- [x] Analizar las respuestas y resolver ambigüedades (2 aclaraciones: app pública y carga de factura nueva)
- [x] Generar `interfaz/functional-design/business-logic-model.md` (flujos de la interfaz)
- [x] Generar `interfaz/functional-design/business-rules.md` (qué muestra y qué permite cada rol)
- [x] Generar `interfaz/functional-design/frontend-components.md` (componentes, estado, endpoints)
- [x] Aprobación (2026-10-16), incluidos los 7 supuestos de `business-rules.md`

## Preguntas
| # | Tema | Respuesta |
|---|---|---|
| 1 | Dirección visual | A: sala de control (oscura, el recibo como protagonista) |
| 2 | Navegación | A: barra lateral fija, solo con las secciones que aparecen en la demo; encabezado con ciclo, mandato y rol; alto contraste y tipografía grande |
| 3 | Pantalla inicial | A: Marcador, con 'pagos fuera de reglas' como número dominante, banda de escaladas y el set precargado |
| 4 | Cómo se muestran los dos roles | A: selector de rol en el encabezado, con la etiqueta 'rol simulado'; el analista no ve acciones de aprobación |
| 5 | Modo guiado para la demo de 3 minutos | A: guía opcional de 5 pasos, reiniciable, con teclado y rol CFO al final |
| 6 | Idioma | A: solo español |
| 7 | Presentación del recibo | A: documento legible con sello y vista técnica; botón Verificar; versión de reglas y rol; la llave no va en el repositorio |

## Aclaraciones
| Tema | Respuesta |
|---|---|
| App pública y demo guiada | Estado propio por visitante: copia del set base y par de claves por sesión; reiniciar vuelve al set original |
| Subir una factura nueva | Selector de muestras ya extraídas (lectura hecha en local con la API real y congelada), con un tipo no soportado que termina en ESCALAR; etiqueta 'lectura guardada' |
