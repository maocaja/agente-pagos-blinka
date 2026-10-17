# Graph Report - blinka  (2026-10-17)

## Corpus Check
- 119 files · ~55,437 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1428 nodes · 1505 edges · 151 communities (140 shown, 8 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `980fb01f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- sello
- properties
- enum
- properties
- null
- properties
- required
- properties
- required
- properties
- items
- items
- enum
- properties
- properties
- properties
- enum
- motor.js
- nivel_autonomia_defecto
- duplicado_probable
- enum
- enum
- fechas
- referencias
- properties
- properties
- required
- texto_dirigido_al_agente
- properties
- items
- required
- required
- required
- cuenta
- proveedor
- enum
- required
- redondeo
- Preguntas de verificación de requisitos: Agente de Pagos con Garantía (Reto Blinka)
- properties
- monto_menor
- enum
- tope_acumulado_proveedor
- enum
- Plan de código: U2 Lectura (Dev B, rama `lectura`)
- Reglas de negocio: U2 Lectura
- tope_gasto_corrida_microusd
- validar.py
- dias_proveedor_nuevo
- presupuesto_periodo_menor
- tolerancia_lineas_menor
- tope_pago_menor
- PRD: Agente de pagos con garantía (Reto Blinka)
- Reglas de la interfaz: U3
- monto_menor
- nonce
- verify.py
- items
- Reglas de negocio: U4 Evaluación
- moneda_base
- properties
- required
- enum
- Estado del arte: agente de IA para revisar facturas de proveedores (pagar, frenar, escalar)
- Requisitos no funcionales e infraestructura (nota fusionada)
- Reglas de negocio: U1 Núcleo
- Unidades de trabajo
- Requisitos: Agente de Pagos con Garantía (Reto Blinka)
- Agente de pagos con garantia: reglas del proyecto
- enum
- cuenta
- Estrategia de verificación
- required
- Modelo de lógica de negocio: U1 Núcleo
- Plan de ejecución
- enum
- null
- properties
- enum
- properties
- no_prueba
- Modelo de lógica de la interfaz: U3
- Preguntas de aclaración: Agente de Pagos con Garantía
- esperado_reglas
- enum
- Guion del video (criterio de "listo")
- Contrato compartido
- enum
- Modelo de lógica de la evaluación: U4
- enum
- esperado.schema.json
- factura-canonica.schema.json
- proveedor_asignado
- mandato.schema.json
- required
- resultados.schema.json
- Componentes de la interfaz: U3
- Modelo de lógica de la lectura: U2
- aprobacion.schema.json
- required
- required
- required
- type
- enum
- veredicto
- Plan de diseño funcional: U3 Interfaz
- Plan de diseño funcional: U1 Núcleo
- fallas_cubiertas
- rol
- items
- enum
- enum
- enum
- Set de datos sintetico
- Agente de pagos con garantia (Reto Blinka)
- Plan de diseño funcional: U4 Evaluación
- Plan de diseño funcional: U2 Lectura
- Dependencias entre unidades
- Plan de unidades de trabajo
- type
- fechas
- Entidades del dominio: U4 Evaluación
- Entidades del dominio: U2 Lectura
- Entidades del dominio: U1 Núcleo
- usuario_simulado
- vence_en
- sin_orden
- parametros
- umbral_senal_texto
- monto_base_menor
- aidlc-state.md
- tandas.md
- components.md
- dup_tolerancia_monto_pct
- Sistema de diseño de la interfaz (U3)
- .mcp.json
- properties
- conftest.py
- Plan de código: U1 Núcleo (Dev A, rama `nucleo`)
- costo_microusd
- Plan de código: U4 Evaluación (subagente, con revisión de una persona desarrolladora; rama `evaluacion`)
- Plan de código: U3 Interfaz (Dev B, rama `interfaz`)
- enum
- required
- items
- recibo.schema.json
- confianza
- suma_lineas_menor

## God Nodes (most connected - your core abstractions)
1. `required` - 23 edges
2. `Preguntas de verificación de requisitos: Agente de Pagos con Garantía (Reto Blinka)` - 21 edges
3. `Reglas de negocio: U2 Lectura` - 20 edges
4. `required` - 19 edges
5. `PRD: Agente de pagos con garantía (Reto Blinka)` - 18 edges
6. `enum` - 14 edges
7. `required` - 14 edges
8. `Reglas de la interfaz: U3` - 14 edges
9. `required` - 14 edges
10. `required` - 13 edges

## Surprising Connections (you probably didn't know these)
- `etapa_unidad()` --calls--> `revisar()`  [EXTRACTED]
  verify.py → calidad.py

## Import Cycles
- None detected.

## Communities (151 total, 8 thin omitted)

### Community 0 - "sello"
Cohesion: 0.15
Nodes (13): format, type, null, object, fecha, sello, sha256_archivo, sha256_esperado (+5 more)

### Community 1 - "properties"
Cohesion: 0.25
Nodes (8): type, type, additionalProperties, type, properties, archivo, caso, esperado_extremo_a_extremo

### Community 2 - "enum"
Cohesion: 0.17
Nodes (12): tipo_no_soportado, enum, formato_numerico_ambiguo, fuera_de_limites, http_4xx, json_invalido, moneda_ambigua, pdf_cifrado (+4 more)

### Community 3 - "properties"
Cohesion: 0.17
Nodes (12): type, format, type, type, type, type, properties, decision_id (+4 more)

### Community 4 - "null"
Cohesion: 0.19
Nodes (14): type, type, null, object, string, type, description, type (+6 more)

### Community 5 - "properties"
Cohesion: 0.15
Nodes (13): type, format, type, type, type, description, type, properties (+5 more)

### Community 6 - "required"
Cohesion: 0.09
Nodes (23): required, conf_min_dinero, conf_min_general, dias_proveedor_nuevo, dup_tolerancia_monto_pct, dup_ventana_dias, max_retries, moneda_base (+15 more)

### Community 7 - "properties"
Cohesion: 0.17
Nodes (12): format, type, type, null, type, properties, fecha, huella_codigo (+4 more)

### Community 8 - "required"
Cohesion: 0.15
Nodes (13): ciclo_id, confianza, cuenta, evidencia, fechas, required, documento, emisor (+5 more)

### Community 9 - "properties"
Cohesion: 0.22
Nodes (10): type, type, additionalProperties, type, additionalProperties, type, properties, ciclo_id (+2 more)

### Community 10 - "items"
Cohesion: 0.06
Nodes (33): format, type, type, description, items, type, additionalProperties, properties (+25 more)

### Community 11 - "items"
Cohesion: 0.09
Nodes (23): additionalProperties, properties, required, type, descripcion, lineas, moneda, items (+15 more)

### Community 12 - "enum"
Cohesion: 0.24
Nodes (10): enum, enum, chat, correo, csv, hoja, imagen, pdf (+2 more)

### Community 13 - "properties"
Cohesion: 0.05
Nodes (47): enum, type, items, type, enum, type, enum, type (+39 more)

### Community 14 - "properties"
Cohesion: 0.15
Nodes (13): type, properties, type, description, type, type, canal, formato (+5 more)

### Community 15 - "properties"
Cohesion: 0.15
Nodes (13): type, type, type, type, type, desvios_conservadores, frenadas_escalables, lanzadas (+5 more)

### Community 16 - "enum"
Cohesion: 0.05
Nodes (38): additionalProperties, type, description, $id, ciclo_id, factura, tipo, description (+30 more)

### Community 17 - "motor.js"
Cohesion: 0.13
Nodes (23): arena(), aUSD(), csvConciliacion(), emitirRecibo(), enc, escenarioPentest(), evaluar(), explicar() (+15 more)

### Community 18 - "nivel_autonomia_defecto"
Cohesion: 0.15
Nodes (15): enum, type, autonomo, sombra, additionalProperties, properties, required, type (+7 more)

### Community 19 - "duplicado_probable"
Cohesion: 0.10
Nodes (21): additionalProperties, properties, required, type, type, type, duplicado_probable, origen (+13 more)

### Community 20 - "enum"
Cohesion: 0.25
Nodes (8): anticipo, cuenta_de_cobro, desconocido, estado_de_cuenta, factura, nota_de_credito, proforma, enum

### Community 21 - "enum"
Cohesion: 0.14
Nodes (14): enum, cumple, falla, omitida, autorizada, con_recibo, denegada, evaluada (+6 more)

### Community 22 - "fechas"
Cohesion: 0.18
Nodes (11): type, additionalProperties, properties, required, type, emision, vencimiento, emision (+3 more)

### Community 23 - "referencias"
Cohesion: 0.13
Nodes (15): type, description, type, type, acuerdo_ref, numero, numero_normalizado, referencias (+7 more)

### Community 24 - "properties"
Cohesion: 0.11
Nodes (18): type, type, type, type, properties, conf_min_dinero, conf_min_general, dup_ventana_dias (+10 more)

### Community 25 - "properties"
Cohesion: 0.09
Nodes (23): type, type, type, format, type, type, type, type (+15 more)

### Community 26 - "required"
Cohesion: 0.17
Nodes (12): decision_id, firma, id, recibo_id, rol, vence_en, required, accion (+4 more)

### Community 27 - "texto_dirigido_al_agente"
Cohesion: 0.18
Nodes (11): type, type, cita, presente, texto_dirigido_al_agente, additionalProperties, properties, required (+3 more)

### Community 28 - "properties"
Cohesion: 0.24
Nodes (11): properties, properties, type, description, type, type, moneda, monto_total (+3 more)

### Community 29 - "items"
Cohesion: 0.18
Nodes (11): items, type, additionalProperties, required, type, estado, id, fallas_aprobadas (+3 more)

### Community 30 - "required"
Cohesion: 0.11
Nodes (18): decision_id, factura_id, firma, mandato_version, modo_autonomia, moneda, monto_menor, reglas (+10 more)

### Community 31 - "required"
Cohesion: 0.22
Nodes (9): fecha, mandato_version, tipo, required, casos, huella_codigo, no_prueba, recuentos (+1 more)

### Community 32 - "required"
Cohesion: 0.09
Nodes (23): additionalProperties, description, $id, required, ciclo_id, estado, evidencia, factura_id (+15 more)

### Community 33 - "cuenta"
Cohesion: 0.25
Nodes (8): additionalProperties, properties, type, type, cuenta, pais, ultimos4, type

### Community 34 - "proveedor"
Cohesion: 0.25
Nodes (8): type, type, id_fiscal, nombre, proveedor, additionalProperties, properties, type

### Community 35 - "enum"
Cohesion: 0.25
Nodes (8): OTRA, enum, ARS, BRL, COP, EUR, MXN, USD

### Community 36 - "required"
Cohesion: 0.13
Nodes (22): additionalProperties, required, description, required, $id, confianza, cuenta, evidencia (+14 more)

### Community 37 - "redondeo"
Cohesion: 0.29
Nodes (7): redondeo, description, enum, type, a_la_baja, al_alza, al_entero_mas_cercano

### Community 38 - "Preguntas de verificación de requisitos: Agente de Pagos con Garantía (Reto Blinka)"
Cohesion: 0.09
Nodes (21): Bloque 1. Tiempo y equipo, Bloque 2. Tecnología, Bloque 3. Alcance y diferenciación, Bloque 4. Reglas y aprobación, Bloque 5. Entrega, Preguntas de verificación de requisitos: Agente de Pagos con Garantía (Reto Blinka), Question 1, Question 10 (+13 more)

### Community 39 - "properties"
Cohesion: 0.20
Nodes (10): additionalProperties, description, type, properties, evidencia, referencia_acuerdo, suma_lineas, type (+2 more)

### Community 40 - "monto_menor"
Cohesion: 0.33
Nodes (6): type, pattern, type, activo, monto_menor, properties

### Community 41 - "enum"
Cohesion: 0.33
Nodes (6): enum, type, periodo, mes_calendario, semana_calendario, ventana_30_dias

### Community 42 - "tope_acumulado_proveedor"
Cohesion: 0.33
Nodes (6): monto_menor, tope_acumulado_proveedor, additionalProperties, required, type, activo

### Community 43 - "enum"
Cohesion: 0.22
Nodes (9): enum, type, type, properties, cumple, falla, omitida, estado (+1 more)

### Community 44 - "Plan de código: U2 Lectura (Dev B, rama `lectura`)"
Cohesion: 0.14
Nodes (13): Alcance y límites, Calendario de Dev B, Estructura, Generación del set simulado (subagente Sonnet, mandato aparte), Plan de código: U2 Lectura (Dev B, rama `lectura`), Riesgos y supuestos, T1. Extracciones a mano y adaptador de texto (sábado temprano, sin clave de API), T2. Extractor con Haiku (sábado 08:00 a 12:00; real cuando llegue la clave) (+5 more)

### Community 45 - "Reglas de negocio: U2 Lectura"
Cohesion: 0.10
Nodes (20): Adaptadores, Asignación del proveedor, Caché, Caché y umbral, Canales simulados (decisión del 2026-10-17), Cascada de modelos, Contador y tope de gasto, Correcciones humanas y la segunda lectura (+12 more)

### Community 46 - "tope_gasto_corrida_microusd"
Cohesion: 0.50
Nodes (4): tope_gasto_corrida_microusd, description, pattern, type

### Community 47 - "validar.py"
Cohesion: 0.67
Nodes (3): Validador minimo de JSON Schema para comprobar los ejemplos del contrato. Cubre…, tipo_ok(), validar()

### Community 48 - "dias_proveedor_nuevo"
Cohesion: 0.67
Nodes (3): description, type, dias_proveedor_nuevo

### Community 49 - "presupuesto_periodo_menor"
Cohesion: 0.67
Nodes (3): pattern, type, presupuesto_periodo_menor

### Community 50 - "tolerancia_lineas_menor"
Cohesion: 0.67
Nodes (3): tolerancia_lineas_menor, pattern, type

### Community 51 - "tope_pago_menor"
Cohesion: 0.67
Nodes (3): tope_pago_menor, pattern, type

### Community 52 - "PRD: Agente de pagos con garantía (Reto Blinka)"
Cohesion: 0.11
Nodes (18): 10. Métricas de éxito, 11. Plan de evaluación, 12. Riesgos y mitigaciones, 13. Plan de entrega (hackathon; supuesto 16-20 horas), 1. One-liner y JTBD, 2. Contexto y problema, 3. ICP, 4. Propuesta de valor y diferenciadores (+10 more)

### Community 53 - "Reglas de la interfaz: U3"
Cohesion: 0.13
Nodes (14): App pública, Bandeja del aprobador, Cierre del ciclo, Dirección y forma, Errores y estados, Guardián, Modo guiado (botón Demo), Pantalla inicial: Marcador (+6 more)

### Community 54 - "monto_menor"
Cohesion: 0.67
Nodes (3): pattern, type, monto_menor

### Community 55 - "nonce"
Cohesion: 0.67
Nodes (3): description, type, nonce

### Community 56 - "verify.py"
Cohesion: 0.22
Nodes (16): archivos(), complejidad(), duplicados(), exento(), lineas_utiles(), revisar(), revisar_archivo(), commit() (+8 more)

### Community 57 - "items"
Cohesion: 0.14
Nodes (14): type, additionalProperties, properties, required, type, descripcion, items, type (+6 more)

### Community 58 - "Reglas de negocio: U4 Evaluación"
Cohesion: 0.17
Nodes (11): Arena de ataques (dos niveles, sin llamar al modelo), Facturas ocultas: política, Otras pruebas a cargo de U4, Pentest por código, Principios, Pruebas de mutación del motor, Reglas de negocio: U4 Evaluación, Reporte (+3 more)

### Community 60 - "properties"
Cohesion: 0.17
Nodes (12): description, type, type, type, pattern, type, properties, aprobable (+4 more)

### Community 61 - "required"
Cohesion: 0.20
Nodes (10): additionalProperties, required, type, id, tipo_documento, documento, canal, formato (+2 more)

### Community 62 - "enum"
Cohesion: 0.11
Nodes (21): enum, type, type, properties, ESCALAR, FRENAR, otra, PAGAR (+13 more)

### Community 63 - "Estado del arte: agente de IA para revisar facturas de proveedores (pagar, frenar, escalar)"
Cohesion: 0.18
Nodes (10): 1. Productos actuales de cuentas por pagar con IA o agentes, 2. Fraude de facturas y cambio de datos bancarios, 3. Facturacion electronica: Mexico, Brasil, Colombia, Chile, Peru, Argentina, 4. Pagos transfronterizos a contratistas en LatAm y requisitos fiscales de EE. UU., 5. Blinka, 6. Protocolos de pagos con agentes, Estado del arte: agente de IA para revisar facturas de proveedores (pagar, frenar, escalar), Lo que no se pudo verificar (+2 more)

### Community 64 - "Requisitos no funcionales e infraestructura (nota fusionada)"
Cohesion: 0.20
Nodes (9): Calidad y pruebas, Datos y sesiones, Observabilidad (por defecto), Pila, Rendimiento y límites (por defecto), Requisitos no funcionales e infraestructura (nota fusionada), Riesgos de infraestructura, Seguridad (+1 more)

### Community 65 - "Reglas de negocio: U1 Núcleo"
Cohesion: 0.20
Nodes (9): Aprobación, Autonomía por proveedor, Catálogo de parámetros del mandato, Mandatos precargados, Política por tipo de documento, Principios, Reglas, Reglas de negocio: U1 Núcleo (+1 more)

### Community 66 - "Unidades de trabajo"
Cohesion: 0.20
Nodes (9): Contrato compartido (antes de empezar las unidades), Fuera de las unidades, Organización del código, Requisitos por unidad, U1 Núcleo (Dev A), U2 Lectura (Dev B), U3 Interfaz (Dev B), U4 Evaluación (subagente, con revisión de una persona desarrolladora) (+1 more)

### Community 67 - "Requisitos: Agente de Pagos con Garantía (Reto Blinka)"
Cohesion: 0.20
Nodes (9): 1. Análisis de la solicitud, 2. Decisiones tomadas, 3. Requisitos funcionales, 4. Requisitos no funcionales, 5. Riesgos y pendientes, 6. Ajustes por el diagnóstico de tres expertos (2026-10-16), Cómo se habla del proyecto, Recorte, en orden de lo primero que se corta (+1 more)

### Community 68 - "Agente de pagos con garantia: reglas del proyecto"
Cohesion: 0.17
Nodes (11): 1. Fuentes de verdad, 2. Orquestador y subagentes, 3. Economia de tokens, 4. Tanda de trabajo, 5. Reglas de codigo, 5b. Patrones de diseño, 5c. Calidad del codigo: SOLID y sin duplicacion (obligatorio), 6. Fuentes actualizadas (+3 more)

### Community 69 - "enum"
Cohesion: 0.20
Nodes (10): properties, type, ESCALAR, FRENAR, PAGAR, REGISTRAR, explicacion, veredicto (+2 more)

### Community 70 - "cuenta"
Cohesion: 0.18
Nodes (11): additionalProperties, description, properties, required, pais, ultimos4, type, cuenta (+3 more)

### Community 71 - "Estrategia de verificación"
Cohesion: 0.22
Nodes (8): Cuándo corre, Estrategia de verificación, Fuentes, Límites, Presupuesto de pruebas, Principio, Qué hace determinista a una prueba, Qué hace `verify.py`

### Community 72 - "required"
Cohesion: 0.20
Nodes (10): additionalProperties, required, type, lectura, costo_microusd, desde_cache, motivo_falla, reintentos (+2 more)

### Community 73 - "Modelo de lógica de negocio: U1 Núcleo"
Cohesion: 0.22
Nodes (8): 1. Evaluación de una factura, 2. Ciclo de vida de una decisión, 3. Mandato, 4. Reserva de presupuesto, 5. Recibo y guardián, 6. Ciclo de pagos, 7. Qué nunca ocurre, Modelo de lógica de negocio: U1 Núcleo

### Community 74 - "Plan de ejecución"
Cohesion: 0.22
Nodes (8): 1. Resumen de la evaluación, 2. Etapas por ejecutar, 3. Calendario por bloques, 4. Hitos y criterio de "listo", 5. Dependencias críticas, 6. Orden de recorte, 7. Riesgos y preguntas abiertas, Plan de ejecución

### Community 75 - "enum"
Cohesion: 0.25
Nodes (9): enum, ESCALAR, FRENAR, PAGAR, REGISTRAR, veredicto, description, enum (+1 more)

### Community 76 - "null"
Cohesion: 0.31
Nodes (9): type, type, null, string, accion_si_falla, recibo_id, reevaluacion_de, type (+1 more)

### Community 77 - "properties"
Cohesion: 0.18
Nodes (11): type, properties, type, desde_cache, modelo, reintentos, tokens_entrada, tokens_salida (+3 more)

### Community 78 - "enum"
Cohesion: 0.20
Nodes (11): required, id_fiscal, nombre, enum, type, metodo, conflicto, modelo (+3 more)

### Community 79 - "properties"
Cohesion: 0.22
Nodes (9): format, type, type, properties, creado_en, empresa_id, version, pattern (+1 more)

### Community 80 - "no_prueba"
Cohesion: 0.40
Nodes (5): type, description, items, type, no_prueba

### Community 81 - "Modelo de lógica de la interfaz: U3"
Cohesion: 0.25
Nodes (7): 1. Apertura de una sesión, 2. Escalada: de la bandeja a la decisión, 3. Verificar un recibo, 4. Mandato nuevo desde el pentest, 5. Cierre del ciclo, 6. Modo guiado, Modelo de lógica de la interfaz: U3

### Community 82 - "Preguntas de aclaración: Agente de Pagos con Garantía"
Cohesion: 0.25
Nodes (7): Clarification Question 1, Clarification Question 2, Clarification Question 3, Preguntas de aclaración: Agente de Pagos con Garantía, Tensión 1: app pública con URL (P15: B) frente a clave de API sin conseguir (P6: C) y control de costo, Tensión 2: dónde se despliega (P15: B) no está definido, Tensión 3: la clave de API (P6: C) bloquea la lectura con Claude

### Community 83 - "esperado_reglas"
Cohesion: 0.25
Nodes (8): additionalProperties, properties, type, type, esperado_reglas, reglas_que_fallan, items, type

### Community 84 - "enum"
Cohesion: 0.25
Nodes (8): sin_segunda_lectura, tipo_no_soportado, enum, type, lectura_esperada, difieren, dos_lecturas_coinciden, sin_texto_verificable

### Community 85 - "Guion del video (criterio de "listo")"
Cohesion: 0.18
Nodes (10): Encuadre con el reto (no desenfocar), Escenas (3:00), Fuentes de las revisiones (consultadas 2026-10-17; secundarias, no abiertas en su totalidad), Guion del video (criterio de "listo"), Línea de corte, Mensaje, Orden de construcción derivado, Personas a las que se le habla (inferidas, NO VERIFICADO con entrevistas) (+2 more)

### Community 86 - "Contrato compartido"
Cohesion: 0.25
Nodes (7): Archivos, Cambios, Contrato compartido, Convenciones, Ejemplos para el servidor simulado, Provisional, Pruebas del contrato

### Community 87 - "enum"
Cohesion: 0.25
Nodes (8): tipo, enum, type, arena, mutacion, ocultas, pentest, set

### Community 88 - "Modelo de lógica de la evaluación: U4"
Cohesion: 0.29
Nodes (6): Corrida de evaluación, Facturas ocultas, Modelo de lógica de la evaluación: U4, Mutación, Pentest, Qué nunca ocurre

### Community 89 - "enum"
Cohesion: 0.29
Nodes (7): enum, type, escalar, accion, aprobar, corregir, rechazar

### Community 90 - "esperado.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 91 - "factura-canonica.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 92 - "proveedor_asignado"
Cohesion: 0.29
Nodes (7): proveedor_asignado, additionalProperties, required, type, metodo, pista, proveedor_id

### Community 93 - "mandato.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 94 - "required"
Cohesion: 0.29
Nodes (7): estado, required, creado_en, empresa_id, firmas, parametros, version

### Community 95 - "resultados.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 96 - "Componentes de la interfaz: U3"
Cohesion: 0.33
Nodes (5): Componentes de la interfaz: U3, Endpoints que consume (propuesta), Estado, Jerarquía, Reglas de implementación

### Community 97 - "Modelo de lógica de la lectura: U2"
Cohesion: 0.33
Nodes (5): Fallas de la API en cualquier punto, Flujo de lectura de un documento, Modelo de lógica de la lectura: U2, Qué entrega U2 al núcleo, Qué nunca ocurre

### Community 98 - "aprobacion.schema.json"
Cohesion: 0.33
Nodes (5): additionalProperties, $id, $schema, title, type

### Community 99 - "required"
Cohesion: 0.40
Nodes (6): required, required, veredicto, explicacion, lectura_esperada, reglas_que_fallan

### Community 100 - "required"
Cohesion: 0.33
Nodes (6): required, archivo, caso, esperado_extremo_a_extremo, esperado_reglas, grupo

### Community 101 - "required"
Cohesion: 0.33
Nodes (6): required, id_fiscal, nombre, pais, ultimos4, required

### Community 102 - "type"
Cohesion: 0.29
Nodes (7): format, type, properties, emision, vencimiento, format, type

### Community 103 - "enum"
Cohesion: 0.33
Nodes (6): enum, type, estado, propuesto, reemplazado, vigente

### Community 104 - "veredicto"
Cohesion: 0.33
Nodes (6): ESCALAR, PAGAR, veredicto, description, enum, type

### Community 105 - "Plan de diseño funcional: U3 Interfaz"
Cohesion: 0.40
Nodes (4): Aclaraciones, Pasos, Plan de diseño funcional: U3 Interfaz, Preguntas

### Community 106 - "Plan de diseño funcional: U1 Núcleo"
Cohesion: 0.40
Nodes (4): Decisión previa, Pasos, Plan de diseño funcional: U1 Núcleo, Preguntas

### Community 107 - "fallas_cubiertas"
Cohesion: 0.40
Nodes (5): description, items, type, type, fallas_cubiertas

### Community 108 - "rol"
Cohesion: 0.40
Nodes (5): analista, cfo, rol, enum, type

### Community 109 - "items"
Cohesion: 0.40
Nodes (5): additionalProperties, type, reglas, items, type

### Community 110 - "enum"
Cohesion: 0.40
Nodes (5): autonomo, sombra, enum, type, modo_autonomia

### Community 111 - "enum"
Cohesion: 0.40
Nodes (5): enum, type, grupo, oculta, visible

### Community 112 - "enum"
Cohesion: 0.40
Nodes (5): autonomo, sombra, enum, type, modo_autonomia

### Community 113 - "Set de datos sintetico"
Cohesion: 0.33
Nodes (5): Brechas conocidas del motor, Como verificar, Parametros del esperado, Registro maestro, Set de datos sintetico

### Community 114 - "Agente de pagos con garantia (Reto Blinka)"
Cohesion: 0.40
Nodes (4): Agente de pagos con garantia (Reto Blinka), Carpetas y responsables, Equipo no tecnico, Reglas de trabajo

### Community 115 - "Plan de diseño funcional: U4 Evaluación"
Cohesion: 0.50
Nodes (3): Pasos, Plan de diseño funcional: U4 Evaluación, Preguntas

### Community 116 - "Plan de diseño funcional: U2 Lectura"
Cohesion: 0.50
Nodes (3): Pasos, Plan de diseño funcional: U2 Lectura, Preguntas

### Community 117 - "Dependencias entre unidades"
Cohesion: 0.50
Nodes (3): Dependencias entre unidades, Orden de integración, Riesgos de dependencia

### Community 118 - "Plan de unidades de trabajo"
Cohesion: 0.50
Nodes (3): Pasos, Plan de unidades de trabajo, Preguntas y respuestas

### Community 119 - "type"
Cohesion: 0.50
Nodes (4): null, string, recibo_id, type

### Community 120 - "fechas"
Cohesion: 0.33
Nodes (6): additionalProperties, required, type, emision, vencimiento, fechas

### Community 124 - "usuario_simulado"
Cohesion: 0.67
Nodes (3): usuario_simulado, description, type

### Community 125 - "vence_en"
Cohesion: 0.67
Nodes (3): vence_en, format, type

### Community 126 - "sin_orden"
Cohesion: 0.67
Nodes (3): sin_orden, description, type

### Community 127 - "parametros"
Cohesion: 0.67
Nodes (3): additionalProperties, type, parametros

### Community 128 - "umbral_senal_texto"
Cohesion: 0.67
Nodes (3): umbral_senal_texto, description, type

### Community 129 - "monto_base_menor"
Cohesion: 0.67
Nodes (3): pattern, type, monto_base_menor

### Community 134 - "Sistema de diseño de la interfaz (U3)"
Cohesion: 0.25
Nodes (7): Cómo se compila, Decisión de framework, Dirección visual, Inventario, Sistema de diseño de la interfaz (U3), Supuestos y avisos, Tokens (fuente única: `docs/design-system/tokens.css`; componentes en `componentes.css`)

### Community 138 - ".mcp.json"
Cohesion: 0.50
Nodes (3): npx, chrome-devtools, context7

### Community 139 - "properties"
Cohesion: 0.20
Nodes (10): additionalProperties, properties, type, type, type, type, emisor, id_fiscal (+2 more)

### Community 140 - "conftest.py"
Cohesion: 0.50
Nodes (4): ahora(), _determinismo(), Infraestructura comun de pruebas deterministas: sin red, reloj y semilla fijos., fixture

### Community 141 - "Plan de código: U1 Núcleo (Dev A, rama `nucleo`)"
Cohesion: 0.14
Nodes (13): Alcance y límites, Entrega a las otras unidades, Estructura, Para el subagente `ejecutor-de-unidad`, Plan de código: U1 Núcleo (Dev A, rama `nucleo`), Riesgos y supuestos, T1. Primer hito: decisión con recibo (sábado antes de las 18:00), T2. Guardián y registro (sábado por la tarde) (+5 more)

### Community 142 - "costo_microusd"
Cohesion: 0.50
Nodes (4): description, pattern, type, costo_microusd

### Community 143 - "Plan de código: U4 Evaluación (subagente, con revisión de una persona desarrolladora; rama `evaluacion`)"
Cohesion: 0.15
Nodes (12): Alcance y límites, Estructura, Plan de código: U4 Evaluación (subagente, con revisión de una persona desarrolladora; rama `evaluacion`), Qué corre dentro de `verify`, Riesgos y supuestos, T1. Esperados (sábado temprano, antes del verificador), T2. Verificador independiente (sábado 08:00 a 12:00), T3. Pentest y arena nivel 1 (sábado por la tarde) (+4 more)

### Community 144 - "Plan de código: U3 Interfaz (Dev B, rama `interfaz`)"
Cohesion: 0.15
Nodes (12): Alcance y límites, Dependencias, Estructura, Plan de código: U3 Interfaz (Dev B, rama `interfaz`), Riesgos y supuestos, T1. Pantalla de Decisiones con el recibo (sábado temprano), T2. Escena 3 del video: recibo alterable y guardián (sábado), T3. Pantalla de Reglas, la que pide el reto (sábado) (+4 more)

### Community 145 - "enum"
Cohesion: 0.20
Nodes (10): anticipo, cuenta_de_cobro, desconocido, estado_de_cuenta, factura, nota_de_credito, proforma, tipo_documento (+2 more)

### Community 146 - "required"
Cohesion: 0.20
Nodes (10): recuentos, additionalProperties, required, type, desvios_conservadores, frenadas_escalables, lanzadas, otras_diferencias (+2 more)

### Community 147 - "items"
Cohesion: 0.22
Nodes (9): items, type, additionalProperties, required, id, casos, clase, veredicto_motor (+1 more)

### Community 148 - "recibo.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 149 - "confianza"
Cohesion: 0.50
Nodes (4): additionalProperties, description, type, confianza

### Community 150 - "suma_lineas_menor"
Cohesion: 0.50
Nodes (4): suma_lineas_menor, description, pattern, type

## Knowledge Gaps
- **892 isolated node(s):** `Parametros del esperado`, `Como verificar`, `Brechas conocidas del motor`, `Registro maestro`, `format` (+887 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 940 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `properties` connect `properties` to `cuenta`, `required`, `properties`, `items`, `properties`, `properties`, `duplicado_probable`, `referencias`, `fechas`, `factura-canonica.schema.json`, `proveedor_asignado`, `required`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `properties` connect `properties` to `umbral_senal_texto`, `dup_tolerancia_monto_pct`, `redondeo`, `enum`, `items`, `tope_acumulado_proveedor`, `tope_gasto_corrida_microusd`, `dias_proveedor_nuevo`, `presupuesto_periodo_menor`, `nivel_autonomia_defecto`, `tolerancia_lineas_menor`, `tope_pago_menor`, `moneda_base`, `parametros`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `properties` connect `properties` to `cuenta`, `proveedor`, `required`, `confianza`, `fechas`, `items`, `texto_dirigido_al_agente`, `properties`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **What connects `Parametros del esperado`, `Como verificar`, `Brechas conocidas del motor` to the rest of the system?**
  _892 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `required` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._
- **Should `items` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._
- **Should `items` be split into smaller, more focused modules?**
  _Cohesion score 0.09486166007905138 - nodes in this community are weakly interconnected._