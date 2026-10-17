# Componentes

Diseño ligero a partir de los diagramas C4 de la página de la propuesta. Cada componente pertenece a una unidad.

| # | Componente | Responsabilidad | Unidad |
|---|---|---|---|
| C1 | Registro de adaptadores | Cada formato es un adaptador con `soporta(documento)` y `a_canonica(documento)`; un formato nuevo no toca el núcleo | U2 |
| C2 | Clasificador de tipo de documento | Decide factura, cuenta de cobro, nota de crédito, estado de cuenta u otro; un tipo desconocido se escala | U2 |
| C3 | Extractor | Lectura con esquema fijo y confianza por campo; cascada Haiku, luego Sonnet, luego persona; caché por hash; modo guardado | U2 |
| C4 | Normalizador | Entrega la factura canónica validada contra el esquema (montos en unidades menores, número y proveedor normalizados) | U2 |
| C5 | Registro maestro | Proveedores, cuentas registradas, acuerdos y estado; el beneficiario y la cuenta salen de aquí | U1 |
| C6 | Motor de reglas | Reglas como funciones registradas con su configuración; política por tipo; todas las reglas se evalúan; precedencia FRENAR, ESCALAR, PAGAR | U1 |
| C7 | Mandato | Parámetros por empresa con versión; cambiarlo crea una versión nueva | U1 |
| C8 | Reserva de presupuesto | Reserva en la misma transacción que el identificador del recibo; presupuesto derivado de las reservas | U1 |
| C9 | Redactor de explicación | Plantilla determinista desde el resultado del motor; un modelo solo reescribe si se pide | U1 |
| C10 | Firmador | Proceso separado del servidor web; firma recibos con la clave privada; versión de clave en el recibo | U1 |
| C11 | Guardián | Seis verificaciones con la clave pública; reevalúa el presupuesto; rechaza con motivo | U1 |
| C12 | Registro de solo adición | SQLite con inserción únicamente; ciclo de pagos; exportación de conciliación | U1 |
| C13 | Aprobaciones y roles | Dos roles (analista y CFO); aprobación firmada por usuario autenticado, ligada a recibo y versión, con expiración | U1 |
| C14 | API | FastAPI: facturas, decisiones, aprobaciones, reglas, ciclo, guardián; vista previa de qué cambia si se aprueba; modo público de solo lectura | U1 |
| C15 | Pantallas | Decisiones, Reglas, Marcador, Guardián, Pentest y arena | U3 |
| C16 | Bandeja del aprobador | Razón en una frase, un botón, vista previa de qué cambia si aprueba | U3 |
| C17 | Autonomía visible y contador de costo (vista) | Interruptor por proveedor y monto; muestra el contador y el tope. La lógica del contador y del tope duro vive donde se llama a los modelos (C3 y C2) | U3 |
| C3b | Contador de tokens y tope duro | Cuenta tokens por corrida y corta al llegar al límite; lo consumen C3 y el clasificador | U2 |
| C18 | Set y esperado | Facturas con el veredicto esperado como intención; 4 ocultas | U4 |
| C19 | Verificador independiente | Condición de pago escrita a partir del texto de las reglas, con estado propio | U4 |
| C20 | Pentest por código | Intentos de evadir las reglas; hallazgos y arreglo propuesto | U4 |
| C21 | Arena | Variantes generadas por código sobre el texto original, con semillas variables | U4 |
| C22 | Pruebas de mutación y de falla del extractor | Romper una regla y ver que la prueba falla; salidas truncadas o rechazadas producen ESCALAR | U4 |
| X1 | Servidor MCP (extra) | Cinco herramientas, sin la de aprobar | U1 |
