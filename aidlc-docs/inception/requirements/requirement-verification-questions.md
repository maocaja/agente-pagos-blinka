# Preguntas de verificación de requisitos: Agente de Pagos con Garantía (Reto Blinka)

**Fase:** Inception, Análisis de requisitos (profundidad estándar). **Fecha:** 2026-10-16.

**Qué ya está definido** (no se pregunta de nuevo): el enunciado del reto y su rúbrica, el `PRD.md` con su actualización v2, la página de la propuesta, la página del modelo canónico y los diagramas C4. Estas preguntas cierran lo que falta para poder diseñar y construir.

**Restricción fija:** todo el set de datos es sintético. No se usan datos reales de clientes ni de empresas.

**Cómo responder:** escribe la letra después de `[Answer]:`. Si ninguna opción encaja, elige la última (Otra) y descríbela ahí. Las opciones marcadas "(recomendada)" son una sugerencia, no una decisión. Avisa cuando termines.

---

## Bloque 1. Tiempo y equipo

## Question 1
¿Cuántas horas efectivas de trabajo hay hasta el congelamiento del domingo a las 10:00?

A) Menos de 12 horas
B) Entre 12 y 20 horas
C) Más de 20 horas
D) Other (please describe after [Answer]: tag below)

[Answer]: C (más de 20 horas)

## Question 2
¿Cómo se reparten las dos personas desarrolladoras?

A) Una hace el núcleo (motor, firma, guardián, registro) y la otra la lectura y la interfaz (recomendada)
B) Una hace núcleo y lectura, la otra interfaz y servidor MCP
C) Trabajan en pareja en el núcleo primero y luego se separan
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
¿Qué hace el equipo no técnico?

A) Facturas del set con su veredicto esperado, investigación con fuentes, pitch y video de respaldo (recomendada)
B) Solo pitch y video; las facturas las genera el equipo técnico
C) Solo investigación; el resto lo hace el equipo técnico
D) Other (please describe after [Answer]: tag below)

[Answer]: A, con ajuste: un subagente de IA genera las facturas del set y hace la investigación; el equipo no técnico no las produce

---

## Bloque 2. Tecnología

## Question 4
¿Qué stack para el backend?

A) Python con FastAPI y SQLite (recomendada: es lo que traen el PRD y la guía de salidas estructuradas)
B) TypeScript (Node) con SQLite
C) Lo decide quien construya el núcleo
D) Other (please describe after [Answer]: tag below)

[Answer]: A (Python con FastAPI y SQLite)

## Question 5
¿Cómo se construye la interfaz?

A) Web simple en HTML y JavaScript, servida por el backend, sin proceso de compilación (recomendada por velocidad)
B) React o Next.js
C) Una herramienta rápida de Python tipo Streamlit
D) Other (please describe after [Answer]: tag below)

[Answer]: A, con ajuste: HTML y JS, pero con un diseño llamativo y distinto; se usará la skill frontend-design al construir la interfaz

## Question 6
¿Hay acceso a la API de Claude y con qué tope de gasto?

A) Hay clave y un tope definido (indica el monto después de [Answer]:)
B) Hay clave pero sin tope definido
C) Todavía no hay clave
D) Other (please describe after [Answer]: tag below)

[Answer]: C (todavía no hay clave de la API de Claude)

## Question 7
¿Qué se hace con Jev (el clasificador de TypeSafe AI)?

A) Ya hay acceso: se usa Jev para las cuatro preguntas de señales
B) Se pide acceso y, si no llega a tiempo, se usa Haiku 5.5 como reemplazo detrás de la misma interfaz (recomendada)
C) No se usa Jev; solo Haiku 5.5
D) Other (please describe after [Answer]: tag below)

[Answer]: B (se pide acceso a Jev; si no llega, Haiku 5.5 detrás de la misma interfaz)

## Question 8
¿Dónde se guarda el registro de decisiones?

A) SQLite, con tablas de solo inserción (recomendada)
B) Archivos JSON o CSV
C) Postgres
D) Other (please describe after [Answer]: tag below)

[Answer]: A (SQLite, tablas de solo inserción)

---

## Bloque 3. Alcance y diferenciación

## Question 9
El PRD pone en el núcleo: lectura con Claude, motor con las reglas, recibo, guardián y marcador. ¿Se confirma?

A) Se confirma tal cual (recomendada)
B) El guardián y la firma pasan a ser extra; el núcleo es solo lectura, motor, registro y marcador
C) Se agrega algo más al núcleo (describir)
D) Other (please describe after [Answer]: tag below)

[Answer]: A (se confirma el núcleo tal cual)

## Question 10
¿Cuál es el momento estrella de la demo?

A) Pentest de reglas y arena de ataques (recomendada)
B) Verificación fuera de banda ante un cambio de cuenta
C) Máquina del tiempo sobre el historial
D) Solo el guardián y el recibo, sin pentest
E) Other (please describe after [Answer]: tag below)

[Answer]: A (pentest de reglas y arena), con énfasis adicional en el modelo canónico extensible: los tipos o formatos nuevos se manejan sin romper el núcleo. Pregunta 10b: reglas como funciones registradas, adaptadores y política por tipo (respuesta A)

## Question 11
¿Dónde queda el servidor MCP para conectar otros agentes (Claude, ChatGPT)?

A) Extra, solo si sobra tiempo (recomendada)
B) Dentro del núcleo
C) Fuera del alcance de la hackathon
D) Other (please describe after [Answer]: tag below)

[Answer]: A (extra, solo si sobra tiempo)

## Question 12
¿Qué tipos de documento tiene el set de facturas?

A) Texto y 3 o 4 PDF, más un XML fiscal simulado (recomendada)
B) Solo texto
C) PDF e imágenes reales, más XML fiscal
D) Other (please describe after [Answer]: tag below)

[Answer]: A (texto, 3 o 4 PDF y un XML simulado)

---

## Bloque 4. Reglas y aprobación

## Question 13
¿Quién aprueba las escaladas en la demo?

A) Un solo rol (CFO), con su firma
B) Dos roles: el analista prepara y el CFO aprueba, con separación de funciones (recomendada si cabe en el tiempo)
C) Una matriz por monto con varios aprobadores
D) Other (please describe after [Answer]: tag below)

[Answer]: A (dos roles con separación de funciones)

## Question 14
¿Qué firma tienen los recibos?

A) Clave compartida (HMAC): simple y rápida, como en la maqueta; quien verifica podría falsificar
B) Par de claves: el sistema firma con la privada y el guardián solo tiene la pública, así un tercero puede verificar sin poder falsificar (recomendada si el tiempo alcanza)
C) Sin firma real: solo hash encadenado
D) Other (please describe after [Answer]: tag below)

[Answer]: A (par de claves; el guardián solo tiene la pública)

---

## Bloque 5. Entrega

## Question 15
¿Qué se sube el domingo antes de las 12:00?

A) Repositorio y video de la demo
B) Aplicación desplegada con URL, repositorio y video
C) Solo presentación en vivo
D) Other (please describe after [Answer]: tag below)

[Answer]: B (app desplegada con URL, repositorio y video)
