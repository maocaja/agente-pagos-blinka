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

## Ola 6 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U4 Evaluación | Pentest de 6 estrategias (13 ataques por mandato) y arena con semilla (11 mutaciones) | 60 (8 nuevas; tope de la etapa) | verde | v1 paga 1 ataque indebido (tercera factura partida; hueco de política); v2: 0. Arena nivel 2, semilla 7: 3.200 ataques, 0 pagados indebidamente, 2 desvíos conservadores (f_14 ilegible: motor FRENAR, verificador ESCALAR). No probado: lectura del modelo, documentos originales, aprobaciones ni modo sombra |
| U2 Lectura | Selección de cliente por clave (`crear_cliente`), generador corregido (pdf-01 limpio, pdf-02 factura) | 40 (1 nueva) | verde | La señal `texto_dirigido_al_agente` la produce solo el modelo (prompt) o la lectura a mano: falta un detector determinista (Ola 7). Valores por defecto del cliente real en `TRANSPORTE`, no del mandato |
| U3 Interfaz | Explicación y qué hacer, panel del aprobador (CFO), vista previa de reglas, descargas de auditoría y pain.001 | 15 (5 nuevas) | verde | Falta el modo de lectura en `/api/sesion` (contrato). Contraste y foco sin revisar |
Pendientes (Ola 7): detector determinista de instrucciones en lectura, rutas de pentest y arena y modo de lectura en el núcleo, esperados de pdf-01, pdf-02 y eml-05, revisión de contraste y foco.
Consumo medido: unos 510.000 tokens de subagentes; acumulado cerca de 2,5 M.

## Ola 7 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U2 Lectura | Detector determinista de instrucciones (es, en, pt) integrado en todos los adaptadores y el extractor; la señal final es la mayor entre modelo y detector | 45 (5 nuevas) | verde | 5 positivos y 0 falsos positivos sobre 38 documentos (18 facturas y 20 documentos legibles; la foto no se analiza). Tope de lectura subido de 40 a 45 en `verify.budget.json` (total 182 de 200) |
| U1 Núcleo | Rutas de pentest y arena como datos, `lectura` en `/api/sesion`, contrato 1.1.0-rc2 | 62 (2 nuevas) | verde | El OpenAPI de pentest y arena difería de lo implementado; se alineó a `resultados.schema.json` |
| U4 Evaluación | Esperados ajustados (pdf-01 PAGAR, pdf-02 factura, eml-05 con R1) | 60 | verde | Hueco restante: calibrar falsos positivos de R8 con más documentos |
Hueco de integración detectado: `/api/muestras` y `/cargar` existen solo en el servidor simulado de la interfaz; la app real no los sirve. Tampoco se ha corrido el set multicanal de extremo a extremo contra los esperados.
Consumo medido: unos 330.000 tokens; acumulado cerca de 2,8 M.

## Olas 8 a 10 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | Ola 8: `/api/muestras` y `/cargar` en la app real. Ola 9: lista sin el adjunto (33 muestras) y títulos legibles | 65 | verde | Prueba de humo con `uvicorn nucleo.api.principal:app`: la trampa de instrucción da ESCALAR con motivo, la factura limpia paga y `/` sirve la interfaz |
| U3 Interfaz | Ataque con la forma real (E1 a E6, v1 contra v2), rótulo de lectura, "Cargar el set", revisión de contraste y foco | 16 | verde | Corregidos: `TypeError` en Reglas y bordes de tarjetas con contraste 1,25:1. La ventana de Chrome no se redimensionó: se auditó a 375 px en un iframe; consola solo desde la carga. Los nombres E1 a E6 están copiados en `paginas.js` |
| U2 Lectura | Ola 9: proveedor por alias. Ola 10: país del banco en las 3 trampas de instrucción | 45 | verde | Las 16 lecturas tienen proveedor. Las trampas ya disparan solo R8 |
| U4 Evaluación | Ola 8: corrida de extremo a extremo. Ola 10: la corrida salta el adjunto | 63 (tope 65) | verde | 13 de 15 documentos coinciden, 3 pagan (los esperados PAGAR) y ninguna imagen ni trampa paga. Quedan 2 diferencias de lista de reglas (foto-04 y pdf-03): el motor añade R1 por imagen, el esperado no |
Datos: alias cortos de Pixel, Logística Sur y Pampa en el registro maestro. Presupuesto de pruebas: 189 de 200.
Consumo medido: unos 650.000 tokens de subagentes en estas olas; acumulado cerca de 3,4 M.

## Olas 11 a 13 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U4 Evaluación | Ola 11: mutación del motor (17 mutantes) y corrida final con las 4 ocultas. Ola 13b: esperados de imágenes | 65 | verde | Mutación: 13 de 17 atrapados; los 4 sobrevivientes eran pruebas faltantes (falla cerrado ante excepción, límite de R9, guardián con FRENAR y con recibo vencido). Ocultas: 3 de 4 veredictos coinciden, 0 pagos indebidos; oc-a (nota de voz, DevNorte) escala por R4 porque la cuenta dictada termina en 8821 y el registro dice 3306: inconsistencia de datos, no se corrigió para no contaminar la prueba ciega |
| U1 Núcleo | Ola 11b: 4 pruebas contra los mutantes sobrevivientes | 69 | verde | Mutación 17 de 17 atrapados |
| U3 Interfaz | Ola 12: sesión persistente, Decisiones como pantalla principal, cabecera limpia. Ola 13: cifra honesta, set de demostración curado (12 muestras) | 18 | verde | Bug real: cada página creaba una sesión nueva y lo cargado se perdía. La banda decía "18 ataques" siendo 18 facturas. Cargar las 33 muestras juntas escalaba 20 por topes acumulados |
| Reglas | R1 incluye el formato imagen en el texto de las reglas del núcleo | n/a | aclarado | Corrida del set multicanal: 15 de 15 coinciden con sus esperados |
Puerta de calidad: `verify.py --gate` con dos corridas idénticas y mutación en OK. Presupuesto de pruebas: 197 de 200.
Consumo medido: unos 900.000 tokens de subagentes en estas olas; acumulado cerca de 4,3 M.
