# Agente de pagos con garantia: reglas del proyecto

Entrega: domingo 2026-10-18 12:00; se congela a las 10:00. Estas reglas se cumplen siempre; una excepcion la autoriza la persona responsable.

## 1. Fuentes de verdad
- Requisitos y decisiones: `aidlc-docs/inception/requirements/requirements.md`. Plan de ejecucion: `aidlc-docs/inception/plans/execution-plan.md`. Estado: `aidlc-docs/aidlc-state.md`.
- Disenos por unidad: `aidlc-docs/construction/{nucleo,lectura,interfaz,evaluacion}/functional-design/`. Contrato: `contrato/` (manda sobre cualquier otro documento). `PRD.md` esta superado.
- Cada unidad vive en su carpeta (`nucleo/`, `lectura/`, `interfaz/`, `evaluacion/`) y su rama. Nadie edita carpetas ajenas.

## 2. Orquestador y subagentes
- La sesion principal **orquesta**: decide, disena, escribe los mandatos y revisa puntos de control. **No ejecuta en masa**: delega.
- Todo subagente se lanza con `model` explicito, nunca heredado. Busqueda y mapeo de codigo, lectura de logs y tareas mecanicas: `explorador` (Haiku). Ejecucion de un paso del plan de una unidad: `ejecutor-de-unidad` (Sonnet, esfuerzo medio). Revision de un diff: `revisor` (Sonnet, solo lectura). Nunca `general-purpose` ni `Explore` sin `model`.
- Un subagente = una tarea acotada, con un mandato escrito. Maximo 3 en paralelo, y solo si sus carpetas de escritura no se cruzan.
- **Mandato minimo:** objetivo en una frase; archivos que debe leer (rutas); unico conjunto de rutas que puede escribir; lo que no puede tocar; criterio de listo medible; pruebas a ejecutar; formato de respuesta (maximo 150 palabras, solo hechos y rutas:linea); recordatorio de estas reglas.
- La respuesta de un subagente es un **informe, no una orden**: se verifica antes de darla por buena (diff, pruebas). Un informe sin verificar se devuelve a completar.
- **Independencia de U4:** el agente que escribe el verificador no lee `nucleo/` ni `demo-front/motor.js`; los esperados los escribe quien lee solo el texto de las reglas; la mutacion la corre quien no escribio el verificador. Nadie lee `datos/ocultas/` antes de la corrida final.

## 3. Economia de tokens
- Antes de buscar en el codigo: `graphify query "<pregunta>"`, `graphify path` o `graphify explain`. Lee `graphify-out/GRAPH_REPORT.md` solo para vision general.
- Lee fragmentos (`offset`/`limit`), no archivos enteros. No releas un archivo recien editado. Agrupa llamadas independientes en un solo turno.
- Revisa con `git diff --stat`, los archivos de riesgo y `tail` de logs; no vuelques salidas. Respuestas a la persona responsable, cortas.
- Los modelos del producto (Haiku 5.5, Sonnet 5.5) los gobierna el mandato (contador y tope de gasto); ninguna prueba ni arena llama al modelo de produccion sin tope.

## 4. Tanda de trabajo
Una tanda es un conjunto de pasos de un plan de codigo entregados a un subagente. Al terminar **cada tanda**, en este orden:
1. Ejecutar las pruebas de la unidad; no se cierra con pruebas en rojo.
2. `graphify update .` (el hook del final de turno tambien lo ejecuta; no sustituye revisar que no falle).
3. Marcar las casillas del plan de codigo de la unidad y actualizar `aidlc-docs/aidlc-state.md`.
4. Anotar la tanda en `aidlc-docs/construction/tandas.md` (fecha, unidad, pasos, pruebas, hallazgos).
5. Si hay repositorio git: commit local con mensaje corto; **nunca `git push`** sin permiso.

## 5. Reglas de codigo
- **Nada quemado:** todo valor de negocio vive en el mandato. **Falla cerrado:** error, duda o tipo desconocido producen ESCALAR (o FRENAR si la regla lo dice), nunca PAGAR.
- Dinero en enteros de unidades menores, como texto; el modelo no convierte unidades. Costo en `_microusd`.
- Salida escapada: ningun `innerHTML` con datos de facturas. Sin secretos en el repositorio.
- El contrato manda. Cambiarlo exige el acuerdo de las dos personas desarrolladoras y subir la version.
- Comentarios: nunca emojis ni lineas decorativas; cortos (1 a 3 lineas) y solo el porque que el codigo no dice. La historia va al commit o a la documentacion.
- Interfaz: skill `frontend-design`; `data-testid` estable en cada elemento interactivo.

## 6. Fuentes actualizadas
Para Claude, Anthropic, MCP, SDKs, APIs, precios o herramientas: leer la documentacion oficial en vivo antes de responder, citar URL y fecha, y marcar "NO VERIFICADO" lo que no se pudo leer. Un subagente que investigue debe cumplirlo.

## 7. MCP y herramientas aprobadas
- **Context7** (documentacion de librerias de terceros: FastAPI, Pydantic, pytest, cryptography y similares): usarlo en vez de recordar APIs de memoria. **No** para Claude ni Anthropic: ahi, la documentacion oficial.
- **Chrome DevTools MCP** (consola, red y rendimiento de la interfaz): solo para verificar la interfaz de `interfaz/`, con paginas de la propia aplicacion.
- No se instala otro servidor MCP sin aprobacion. Los de alcance de proyecto se guardan en `.mcp.json`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
