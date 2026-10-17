# Registro de tandas

Una fila por tanda de trabajo entregada a un subagente. Se completa al cerrar cada tanda (ver `CLAUDE.md`, seccion 4).

| Fecha y hora | Unidad | Pasos del plan | Subagente y modelo | Pruebas | Hallazgos |
|---|---|---|---|---|---|

## Ola 1 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | T1 y T1b | 14 | verde | El motor podía devolver PAGAR con 4 de 11 reglas: ahora falla cerrado por regla no implementada (el fixture inyecta las 4 hasta T3). `crear_app` de 49 líneas dividido por calidad |
| U2 Lectura | T1 y T1b | 7 | verde | `_a_decimal` con complejidad 22 dividido. `proveedor_asignado` null: falta asignar proveedor desde el registro maestro. `suma_lineas` falla en fac-10, 14, 15, 16 y 18, pero el esperado no escala fac-16 por R1 |
| U4 Evaluación | T1 | 20 | verde | Esperados reescritos de forma independiente. Faltan casos: monto entre umbral y tope, proveedor bloqueado, proforma, anticipo y tipo desconocido |
| Datos | Registro maestro | n/a | cargado | `datos/registro-maestro.json` como fuente única (11 proveedores, presupuesto 900000). Los acuerdos de la maqueta no coinciden con los asumidos por núcleo y evaluación (Cloud 4.500 contra 2.000; núcleo sin 5 proveedores) |
Consumo medido: 47.000 a 100.000 tokens de subagente por tanda, unos 540.000 en la ola. Quedan para la Ola 2: núcleo lee `datos/registro-maestro.json`, evaluación revalida esperados contra él, lectura asigna `proveedor_id`.

## Ola 2 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | 11 reglas, guardián (6 verificaciones), libro de reserva y nonce, mandatos v1 y v2, sesiones | 43 (29 nuevas) | verde | El registro maestro tenía a Nuevo Logos como proveedor activo: la factura 09 salía PAGAR. Corregido en `datos/` (ahora escala). Quedan diferencias con `esperado.json` en f_10, f_12, f_13, f_15 y f_16 |
| U2 Lectura | Asignación de proveedor desde el registro | 11 | verde | 17 de 18 asignadas; f_09 y f_12 quedan sin proveedor |
| U3 Interfaz | Decisiones, recibo legible, guardián con campo alterable | 5 | verde | `dist/` estaba ignorado por `.gitignore`: ahora se versiona. Sin store ni mapa de capacidades por rol |
Pendientes: las líneas de f_10, 14, 15, 16 y 18 no suman el total porque el IVA va aparte (lectura); `tandas.md` y `aidlc-state.md` al día; aprobar con reevaluación (núcleo T4).
Consumo medido: unos 320.000 tokens de subagentes en la ola.

## Ola 3 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U2 Lectura | IVA en líneas (f_14, 15, 16), extractor con prompt `extractor.v1` versionado y hash, cliente real y congelado, tope de gasto | 19 (8 nuevas) | verde | Cliente real sin probar (no hay clave). f_10 (documento incoherente) y f_18 (estado de cuenta) escalan por lectura. El cliente emite motivos de falla que el contrato no tiene: decisión de los dos desarrolladores |
| U4 Evaluación | Verificador independiente, corrida del set, `COBERTURA.md` | 35 (15 nuevas) | verde | Motor y verificador coinciden en las 18 (0 pagos indebidos en este set). Quedan 3 diferencias de lista de reglas con `esperado.json` (f_10, f_12, f_13), mismo veredicto: pendiente de revisión humana |
| Datos | Set multicanal simulado en `datos/documentos/`: 18 archivos (PDF, escaneado, foto, `.eml`, chat), instrucción oculta en 3 formatos y autoridad falsa | n/a | generado | Regenerable con semilla; dependencias `pillow` y `fpdf2` en el venv. Sin esperados todavía |
Pendientes: esperados del set multicanal (los fija evaluación), adaptadores PDF, `.eml`, foto y chat (lectura), pentest y arena, aprobar con reevaluación, marcador y pantallas restantes.
Consumo medido: unos 310.000 tokens de subagentes en la ola; acumulado cerca de 1,17 M.

## Ola 4 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | T4 parcial: aprobar y rechazar con reevaluación (solo CFO), marcador según contrato, servir `interfaz/dist` | 51 (8 nuevas) | verde | El agente había desviado el marcador del contrato; corregido. Rol del cargador "sistema" no bloquea. Pendiente de T4: mandato con dos firmas, escalar y corregir, vencimiento de 24 h |
| U2 Lectura | T4 4.1 a 4.4: adaptadores PDF, `.eml`, chat, imagen con doble lectura; 16 lecturas congeladas del set | 31 (12 nuevas) | verde | El manifiesto tiene 16 documentos, no 18. El `Reply-To` falso quedó en `evidencia.reply_to` y ninguna regla lo leía: se añadió `senales.remitente_inconsistente` al contrato (aditivo) y R1 lo usará en la Ola 5. Sin extractor real en los adaptadores de texto |
| U3 Interfaz | T3 (reglas solo lectura), T4 (marcador, ataque), T5 (bandeja simulada, botón Demo) | 10 (5 nuevas) | verde | Probada en Chrome sin errores de consola desde la carga en marcador y sin desborde a 375 px; contraste y foco por teclado sin revisar. Datos del simulador de pentest son inventados. `/api/muestras` ahora lleva `original` (contrato aditivo) |
Pendientes: Ola 5 (explicación, vista previa, auditoría, pain.001, XML y CSV, esperados multicanal) y Ola 6 (pentest y arena, aprobar y proponer mandato en la interfaz).
Consumo medido: unos 450.000 tokens de subagentes en la ola; acumulado cerca de 1,6 M.

## Ola 5 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | Explicación y qué hacer, vista previa de mandato, paquete de auditoría con script, orden pain.001 simulada, R1 por remitente inconsistente | 60 (9 nuevas) | verde | Contrato 1.1.0-rc1 aditivo. `/api/mandato/propuestas` no existía; se creó `/api/mandato/previa` |
| U2 Lectura | Adaptadores XML UBL (sin DOCTYPE, sin XXE) y CSV de lote; señal de `Reply-To` en `.eml` | 39 (8 nuevas) | verde | Un lote CSV de varias filas se lee con `a_canonicas`; por el registro escala. El flujo de lote falta en la orquestación |
| U4 Evaluación | Esperados de los 16 documentos del set multicanal | 53 (18 nuevas) | verde | 8 huecos en `COBERTURA.md`: autoridad falsa depende del umbral de R8; pdf-01 "limpio" escala y pdf-02 es RECIBO (errores del generador); el esperado de eml-05 no conoce la señal nueva |
Pendientes (Ola 6): pentest y arena, aprobar y proponer mandato en la interfaz, explicación y descarga de auditoría en la interfaz, selección automática de cliente por clave, corregir el generador, corrida del set multicanal contra los esperados, revisar contraste y foco.
Presupuesto de pruebas: 162 de 200.
Consumo medido: unos 390.000 tokens de subagentes; acumulado cerca de 2,0 M.
