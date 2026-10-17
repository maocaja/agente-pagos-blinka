# Graph Report - blinka  (2026-10-17)

## Corpus Check
- 66 files · ~41,072 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1348 nodes · 1424 edges · 143 communities (132 shown, 8 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `28e102e9`
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
- enum
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
- confianza
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
- cuenta
- enum
- Estado del arte: agente de IA para revisar facturas de proveedores (pagar, frenar, escalar)
- Requisitos no funcionales e infraestructura (nota fusionada)
- Reglas de negocio: U1 Núcleo
- Unidades de trabajo
- Requisitos: Agente de Pagos con Garantía (Reto Blinka)
- Agente de pagos con garantia: reglas del proyecto
- enum
- properties
- Estrategia de verificación
- required
- Modelo de lógica de negocio: U1 Núcleo
- Plan de ejecución
- enum
- null
- properties
- enum
- properties
- items
- Modelo de lógica de la interfaz: U3
- Preguntas de aclaración: Agente de Pagos con Garantía
- esperado_reglas
- enum
- metodo
- Contrato compartido
- enum
- Modelo de lógica de la evaluación: U4
- enum
- esperado.schema.json
- type
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
- fechas
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
- costo_microusd
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
- factura-canonica.schema.json
- recibo.schema.json
- conftest.py
- properties
- suma_lineas_menor

## God Nodes (most connected - your core abstractions)
1. `required` - 23 edges
2. `Preguntas de verificación de requisitos: Agente de Pagos con Garantía (Reto Blinka)` - 21 edges
3. `required` - 19 edges
4. `Reglas de negocio: U2 Lectura` - 19 edges
5. `PRD: Agente de pagos con garantía (Reto Blinka)` - 18 edges
6. `enum` - 14 edges
7. `required` - 14 edges
8. `Reglas de la interfaz: U3` - 14 edges
9. `required` - 14 edges
10. `required` - 13 edges

## Surprising Connections (you probably didn't know these)
- `required` --extends--> `id`  [EXTRACTED]
  contrato/recibo.schema.json → contrato/recibo.schema.json  _Bridges community 29 → community 30_
- `type` --extends--> `null`  [EXTRACTED]
  contrato/factura-canonica.schema.json → contrato/factura-canonica.schema.json  _Bridges community 61 → community 4_
- `type` --extends--> `null`  [EXTRACTED]
  contrato/factura-canonica.schema.json → contrato/factura-canonica.schema.json  _Bridges community 142 → community 4_
- `type` --extends--> `null`  [EXTRACTED]
  contrato/factura-canonica.schema.json → contrato/factura-canonica.schema.json  _Bridges community 4 → community 91_
- `type` --extends--> `null`  [EXTRACTED]
  contrato/factura-canonica.schema.json → contrato/factura-canonica.schema.json  _Bridges community 4 → community 85_

## Import Cycles
- None detected.

## Communities (143 total, 8 thin omitted)

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
Cohesion: 0.31
Nodes (9): type, null, string, type, type, description, type, motivo_falla (+1 more)

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
Cohesion: 0.10
Nodes (20): required, ciclo_id, confianza, cuenta, evidencia, fechas, id, tipo_documento (+12 more)

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
Cohesion: 0.27
Nodes (10): ESCALAR, FRENAR, PAGAR, REGISTRAR, veredicto_motor, veredicto_verificador, enum, type (+2 more)

### Community 13 - "properties"
Cohesion: 0.05
Nodes (47): enum, type, items, type, enum, type, enum, type (+39 more)

### Community 14 - "enum"
Cohesion: 0.06
Nodes (36): enum, type, additionalProperties, properties, type, enum, type, description (+28 more)

### Community 15 - "properties"
Cohesion: 0.09
Nodes (23): type, type, type, type, type, desvios_conservadores, frenadas_escalables, lanzadas (+15 more)

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
Nodes (22): additionalProperties, properties, required, type, type, type, con, duplicado_probable (+14 more)

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
Cohesion: 0.14
Nodes (14): required, fecha, id, mandato_version, tipo, required, casos, clase (+6 more)

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

### Community 44 - "confianza"
Cohesion: 0.50
Nodes (4): additionalProperties, description, type, confianza

### Community 45 - "Reglas de negocio: U2 Lectura"
Cohesion: 0.10
Nodes (19): Adaptadores, Asignación del proveedor, Caché, Caché y umbral, Cascada de modelos, Contador y tope de gasto, Correcciones humanas y la segunda lectura, Documentos sin texto verificable (+11 more)

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
Cohesion: 0.42
Nodes (9): commit(), correr(), entorno(), etapa_contrato(), etapa_mutacion(), etapa_unidad(), leer_junit(), main() (+1 more)

### Community 57 - "items"
Cohesion: 0.14
Nodes (14): type, additionalProperties, properties, required, type, descripcion, items, type (+6 more)

### Community 58 - "Reglas de negocio: U4 Evaluación"
Cohesion: 0.17
Nodes (11): Arena de ataques (dos niveles, sin llamar al modelo), Facturas ocultas: política, Otras pruebas a cargo de U4, Pentest por código, Principios, Pruebas de mutación del motor, Reglas de negocio: U4 Evaluación, Reporte (+3 more)

### Community 60 - "properties"
Cohesion: 0.17
Nodes (12): description, type, type, type, pattern, type, properties, aprobable (+4 more)

### Community 61 - "cuenta"
Cohesion: 0.25
Nodes (8): additionalProperties, description, required, type, object, pais, ultimos4, cuenta

### Community 62 - "enum"
Cohesion: 0.18
Nodes (11): enum, type, type, properties, otra, clase, id, desvio_conservador (+3 more)

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
Cohesion: 0.18
Nodes (10): 1. Fuentes de verdad, 2. Orquestador y subagentes, 3. Economia de tokens, 4. Tanda de trabajo, 5. Reglas de codigo, 5b. Patrones de diseño, 6. Fuentes actualizadas, 7. MCP y herramientas aprobadas (+2 more)

### Community 69 - "enum"
Cohesion: 0.20
Nodes (10): properties, type, ESCALAR, FRENAR, PAGAR, REGISTRAR, explicacion, veredicto (+2 more)

### Community 70 - "properties"
Cohesion: 0.20
Nodes (10): additionalProperties, properties, type, type, type, type, emisor, id_fiscal (+2 more)

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
Cohesion: 0.20
Nodes (10): type, properties, desde_cache, modelo, reintentos, tokens_entrada, tokens_salida, type (+2 more)

### Community 78 - "enum"
Cohesion: 0.25
Nodes (9): required, id_fiscal, nombre, enum, conflicto, modelo, ninguno, nombre_normalizado (+1 more)

### Community 79 - "properties"
Cohesion: 0.22
Nodes (9): format, type, type, properties, creado_en, empresa_id, version, pattern (+1 more)

### Community 80 - "items"
Cohesion: 0.22
Nodes (9): items, type, additionalProperties, type, description, items, type, casos (+1 more)

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

### Community 85 - "metodo"
Cohesion: 0.40
Nodes (5): type, metodo, proveedor_id, properties, type

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

### Community 91 - "type"
Cohesion: 0.29
Nodes (7): format, type, properties, emision, vencimiento, format, type

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

### Community 102 - "fechas"
Cohesion: 0.33
Nodes (6): additionalProperties, required, type, emision, vencimiento, fechas

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
Cohesion: 0.40
Nodes (4): Brechas conocidas del motor, Como verificar, Parametros del esperado, Set de datos sintetico

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

### Community 120 - "costo_microusd"
Cohesion: 0.50
Nodes (4): description, pattern, type, costo_microusd

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
Nodes (7): Cómo se compila, Decisión de framework, Dirección visual, Inventario, Sistema de diseño de la interfaz (U3), Supuestos y avisos, Tokens (en `docs/design-system/tokens.css`)

### Community 138 - "factura-canonica.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 139 - "recibo.schema.json"
Cohesion: 0.29
Nodes (6): additionalProperties, description, $id, $schema, title, type

### Community 140 - "conftest.py"
Cohesion: 0.50
Nodes (4): ahora(), _determinismo(), Infraestructura comun de pruebas deterministas: sin red, reloj y semilla fijos., fixture

### Community 141 - "properties"
Cohesion: 0.40
Nodes (5): properties, type, pais, ultimos4, type

### Community 142 - "suma_lineas_menor"
Cohesion: 0.50
Nodes (4): suma_lineas_menor, description, pattern, type

## Knowledge Gaps
- **836 isolated node(s):** `1. Fuentes de verdad`, `2. Orquestador y subagentes`, `3. Economia de tokens`, `4. Tanda de trabajo`, `5. Reglas de codigo` (+831 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 879 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `properties` connect `properties` to `properties`, `fechas`, `required`, `factura-canonica.schema.json`, `items`, `properties`, `enum`, `duplicado_probable`, `referencias`, `proveedor_asignado`, `cuenta`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `properties` connect `properties` to `umbral_senal_texto`, `dup_tolerancia_monto_pct`, `redondeo`, `enum`, `items`, `tope_acumulado_proveedor`, `tope_gasto_corrida_microusd`, `dias_proveedor_nuevo`, `presupuesto_periodo_menor`, `nivel_autonomia_defecto`, `tolerancia_lineas_menor`, `tope_pago_menor`, `moneda_base`, `parametros`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `verificaciones` connect `properties` to `properties`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **What connects `1. Fuentes de verdad`, `2. Orquestador y subagentes`, `3. Economia de tokens` to the rest of the system?**
  _836 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `required` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._
- **Should `required` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `items` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._