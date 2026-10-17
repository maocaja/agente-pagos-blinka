# Plan de diseño funcional: U2 Lectura

## Pasos
- [x] Analizar el contexto de la unidad (adaptadores, clasificador de tipo, extractor con cascada y caché, normalizador, contador y tope)
- [x] Responder las 7 preguntas (una por una)
- [x] Analizar las respuestas y resolver ambigüedades (1 aclaración sobre los tipos de documento)
- [x] Generar `lectura/functional-design/business-rules.md`
- [x] Generar `lectura/functional-design/business-logic-model.md`
- [x] Generar `lectura/functional-design/domain-entities.md`
- [x] Aprobación (2026-10-16), incluidos los supuestos de `business-rules.md`

## Preguntas
| # | Tema | Respuesta |
|---|---|---|
| 1 | Cuándo sube la lectura de Haiku a Sonnet | A: ante cualquier señal verificable (esquema, falta de dinero, suma, cita de evidencia); la confianza baja puede provocar la subida y nunca impedirla |
| 2 | Cómo se determina el tipo de documento | A: el tipo va en el esquema de extracción con cita; la política por tipo está en el núcleo; 'tipo no soportado' solo para desconocido o dudoso |
| 3 | Lectura de PDF | A: texto local para verificar las citas y PDF a Claude para el diseño; sin texto, cifrado o fuera de límites, ESCALAR sin llamar a la API |
| 4 | Lectura doble independiente (campos de dinero) | A: monto, moneda, número y totales con reglas deterministas; si difieren o no hay segunda lectura, ESCALAR; ningún camino paga sin acuerdo de las dos lecturas |
| 5 | Cómo se asigna el proveedor al registro maestro | A: identificador fiscal si existe, nombre normalizado si no; conflicto o sin coincidencia, ESCALAR por R3; la coincidencia aproximada es solo una pista |
| 6 | Fallas de la API y reintentos | A: dos reintentos del SDK; un único reintento con Sonnet para truncado y JSON inválido, compartido con la subida; refusal, 4xx y tope de gasto escalan sin reintento |
| 7 | Muestras nuevas de la app pública | A: cuatro muestras (proforma, orden de compra como factura, factura en portugués, cuenta de cobro por chat con lecturas que difieren); lectura real en local, congelada sin retoques, esperado registrado antes |
