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
- Los modelos del producto (Haiku 5.5, Sonnet 5.5) los gobierna el mandato (contador y tope de gasto). **Ninguna prueba de `verify` llama a un modelo ni usa la red.**
- Pocas pruebas y que cubran riesgo: maximo 200 en total; una prueba nueva que supere el presupuesto de su unidad se discute antes de escribirla.

## 4. Tanda de trabajo
Una tanda es un conjunto de pasos de un plan de codigo entregados a un subagente. Al terminar **cada tanda**, en este orden:
1. `python3 verify.py --etapa <unidad>`: no se cierra con pruebas en rojo ni sobre el presupuesto. Antes del congelamiento: `python3 verify.py --gate`. Reglas en `aidlc-docs/construction/estrategia-de-verificacion.md`.
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
- Interfaz: Tailwind compilado + Alpine.js, con los tokens y componentes de `docs/design-system/` (no se inventan colores ni componentes nuevos sin pasar por la guía); skill `frontend-design`; `data-testid` estable en cada elemento interactivo; `x-text`, nunca `x-html` con datos de facturas.

## 5b. Patrones de diseño
Se usan pocos y solo si resuelven un riesgo o un requisito de los diseños; un patron "por si acaso" no entra.
- **Back:** adaptadores y puertos (formatos de entrada, rutas de salida y clientes de modelos detras de una interfaz); reglas como funciones registradas (estrategia y registro) con una politica por tipo como tabla de datos; evaluacion en pipeline sin cortocircuito y con agregacion por precedencia; politica como dato (mandato versionado inyectado); maquinas de estado explicitas para la decision y el ciclo de pagos; registro de solo adicion con estado derivado; inyeccion de dependencias para reloj, identificadores, nonces, firmador y modelos (lo que hace deterministas las pruebas); clave de idempotencia y una transaccion para reserva y nonce; dominio puro (sin FastAPI ni SQLite) con la API como capa delgada y los repositorios detras de una interfaz; falla cerrado como manejo de errores.
- **Front:** el servidor es la fuente de verdad y los datos fluyen en un solo sentido; componentes de presentacion con estado local minimo (Alpine) y un store para sesion y rol; mapa de capacidades por rol que decide que se pinta (el servidor igual lo valida); acciones como comandos con clave de idempotencia y **nunca interfaz optimista**; maquinas de estado para la guia de la demo y para la verificacion del recibo; tokens de diseno como unica fuente de color y tipografia.
- **No se usan:** microservicios, CQRS ni event sourcing completo, fabricas abstractas, herencia profunda, bibliotecas de estado global, SPA con enrutador, ni una abstraccion que no tenga hoy dos usos reales.

## 5c. Calidad del codigo: SOLID y sin duplicacion (obligatorio)
Se cumple siempre; `python3 verify.py` lo comprueba con `calidad.py` y una unidad con hallazgos no cierra la tanda. Una excepcion puntual se marca con `# calidad-ok: <motivo>` en la linea del `def` y la revisa el orquestador.
- **S, una razon de cambio:** funcion de maximo 40 lineas y complejidad 10; archivo de maximo 400 lineas; una clase o modulo hace una cosa. Si crece, se divide.
- **O, abierto a extension:** una regla, un adaptador o una estrategia nueva se agrega registrandola; no se edita el motor, el registro de adaptadores ni la agregacion. Prohibido encadenar `if tipo == ...` para elegir comportamiento: se usa una tabla o un registro.
- **L e I, sustituibles y pequenos:** los puertos (Protocol) tienen como maximo 5 metodos y toda implementacion (real, simulada, de lectura congelada) cumple el mismo contrato.
- **D, depender de abstracciones:** `dominio/` no importa fastapi, sqlite3, anthropic, httpx ni requests; reloj, ids, nonces, firmador, repositorios y modelos entran por inyeccion.
- **Sin duplicacion (DRY):** una regla de negocio vive en un solo lugar. Antes de escribir una funcion se busca con `graphify query` si ya existe; se reutiliza o se extrae, no se copia. Ningun bloque de 6 o mas lineas se repite. Una unidad no copia la logica de otra: la consume por la API o por el contrato (`contrato/` se cambia solo con acuerdo de ambos desarrolladores). Unica excepcion deliberada: `evaluacion/verificador/`, que se escribe aparte a proposito para ser independiente.
- **Nombres y comentarios:** el nombre dice que hace; si hace falta un comentario largo, el codigo esta mal dividido.

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
