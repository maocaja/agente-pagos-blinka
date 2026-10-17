# Requisitos: Agente de Pagos con Garantía (Reto Blinka)

Salida de la etapa de análisis de requisitos, profundidad estándar. Fuentes: enunciado del reto, `PRD.md`, páginas publicadas, cuestionario y aclaraciones respondidos el 2026-10-16.

## 1. Análisis de la solicitud
- **Tipo:** proyecto nuevo. **Alcance:** sistema completo (lectura, reglas, firma, guardián, interfaz). **Complejidad:** alta para el tiempo disponible.
- **Entrega:** domingo 2026-10-18 a las 12:00; congelar a las 10:00. Más de 20 horas efectivas, dos desarrolladores y un subagente para datos e investigación.
- **Objetivo:** un agente que lee facturas y decide pagar, frenar o escalar según reglas por empresa, y que solo permite el pago si el punto de pago recibe un recibo firmado. No mueve dinero real.

## 2. Decisiones tomadas
| Tema | Decisión |
|---|---|
| Reparto | Dev A: núcleo (motor, firma, guardián, registro). Dev B: lectura e interfaz |
| Datos e investigación | Un subagente generó 18 facturas visibles y 4 ocultas, y la investigación con fuentes |
| Backend | Python, FastAPI, SQLite con tablas de solo inserción |
| Interfaz | HTML y JavaScript, con diseño llamativo y distinto (skill `frontend-design` al construirla) |
| Modelos | Claude Haiku 5.5, con subida a Sonnet 5.5 por señales verificables (suma que no cuadra, campo vacío, esquema inválido) y no por la confianza que declara el modelo. El clasificador es Haiku detrás de una interfaz; Jev solo si llega gratis |
| Clave de API | Una persona desarrolladora la consigue antes del sábado a las 12:00; mientras tanto, extracciones escritas a mano |
| Núcleo | Lectura con Claude, motor de reglas, recibo, guardián y marcador |
| Momento estrella | Pentest de reglas determinista por código, en vivo, y arena de ataques. El agente atacante genera las estrategias de antemano y se muestra grabado. Énfasis en el modelo canónico extensible |
| Extensibilidad | Adaptadores registrados, política por tipo de documento, reglas como funciones registradas con su configuración, validación contra el esquema |
| MCP | Extra, solo si sobra tiempo |
| Documentos del set | Texto, 3 o 4 PDF y un XML simulado |
| Aprobación | Dos roles con separación de funciones (analista prepara, CFO aprueba) |
| Firma | Par de claves; el guardián solo tiene la pública |
| Entrega | App desplegada en un servicio gratuito, repositorio y video |
| App pública | Modo guardado: usa extracciones ya hechas y no llama a la API |

## 3. Requisitos funcionales
1. **RF1 Ingesta.** Aceptar documentos por adaptador (texto, PDF, XML). Un tipo desconocido se escala, nunca se pierde.
2. **RF2 Factura canónica.** Todo adaptador entrega la factura canónica validada contra el esquema; si no valida, ESCALAR.
3. **RF3 Lectura.** Extracción con esquema fijo y confianza por campo; cascada Haiku, luego Sonnet, luego persona.
4. **RF4 Motor.** Reglas R1 a R10 por empresa; se evalúan todas, precedencia FRENAR, luego ESCALAR, luego PAGAR o REGISTRAR (cuarto veredicto, solo para una nota de crédito que pasa todas las reglas, sin orden de pago); el presupuesto va al final.
5. **RF5 Política por tipo.** Una tabla define qué reglas aplican a cada tipo (nota de crédito y estado de cuenta no se pagan).
6. **RF6 Recibo.** Cada decisión emite un recibo con evidencia por regla, hash de la factura, versión del mandato, probabilidades y modelo usado, firmado con la clave privada.
7. **RF7 Guardián.** Seis verificaciones; solo con la clave pública; rechaza con el motivo.
8. **RF8 Aprobación.** Acciones sobre una escalada: aprobar, corregir, rechazar, escalar. El analista prepara, el CFO aprueba; quien carga no aprueba. Una frenada no se aprueba.
9. **RF9 Registro.** Tablas de solo inserción; presupuesto derivado de las reservas; ciclo de pagos con estados y exportación de conciliación.
10. **RF10 Reglas editables** por empresa, con versión de mandato.
11. **RF11 Marcador.** Aciertos, autonomía, pagos fuera de reglas (verificador independiente), costo por factura y calibración del clasificador.
12. **RF12 Pentest y arena.** Pentest determinista por código sobre las reglas, en vivo. Las estrategias las propone un agente atacante de antemano y se muestran como resultado grabado. Arena con variantes generadas por código sobre el texto original de las facturas, con semillas variables; resultado visible.
13. **RF13 (extra)** Servidor MCP sin herramienta de aprobar. **RF14 (extra)** Verificación fuera de banda y máquina del tiempo.

## 4. Requisitos no funcionales
- **Seguridad:** falla cerrado (error, duda, tipo desconocido o respuesta inválida producen ESCALAR); ningún modelo decide un pago; sin datos reales.
- **Costo:** código primero, caché por hash, cascada de modelos; un contador y un tope duro por corrida (a USD 0,0004 por factura con Haiku, el costo es de centavos). Medir los tokens reales de un PDF. La app pública no llama a la API.
- **Explicabilidad:** cada decisión legible sin abrir el código.
- **Extensibilidad:** un formato nuevo es un adaptador nuevo; una regla nueva es una función y una entrada de configuración.
- **Pruebas:** invariante con un verificador independiente, fuzzing, carrera de presupuesto y fallas simuladas del extractor.

## 5. Riesgos y pendientes
| Pendiente | Efecto |
|---|---|
| Sin clave de API todavía | Bloquea la lectura en vivo; plan B con extracciones escritas a mano |
| Acceso a Jev sin confirmar | Reemplazo con Haiku |
| El motor de la maqueta paga un duplicado difuso; el PRD pide ESCALAR | Hay que definir la regla en el diseño funcional |
| Falta `tipo_documento` en el contrato | Necesario para nota de crédito y estado de cuenta; se agrega al esquema |
| El set depende de tener R10 activo | Definir los parámetros iniciales del mandato |
| AP2 sí define límites, presupuesto y beneficiarios | Corregido en el relato: llevamos esa idea a cuentas por pagar |
| Varias fuentes de la investigación marcadas NO VERIFICADO | Ver `investigacion/estado-del-arte.md` |

## 6. Ajustes por el diagnóstico de tres expertos (2026-10-16)
Tres revisiones independientes (seguridad de agentes, arquitectura y evaluación, producto y mercado) coincidieron en varios puntos. Se aplican estos requisitos adicionales.

| # | Requisito | Origen |
|---|---|---|
| RF15 | **Registro maestro** de proveedores y cuentas. El beneficiario y la cuenta salen del registro; la factura solo se coteja. Evita que una extracción plausible pero falsa se firme | Seguridad |
| RF16 | **Lectura doble independiente** cuando haya campos estructurados (XML, regex) y comparación con el modelo. El aprobador ve los campos originales de la factura, no solo el resumen del modelo | Seguridad |
| RF17 | **Firmador separado** del proceso web, con versión de clave en el recibo. Se declara el supuesto: con un servidor único, quien lo comprometa puede firmar | Seguridad, arquitectura |
| RF18 | **Identificador de recibo aleatorio** con consumo atómico en SQLite (UNIQUE), caducidad del recibo, y reevaluación del presupuesto por el guardián en la misma transacción | Seguridad, arquitectura |
| RF19 | **Aprobación firmada** por un usuario autenticado, ligada al recibo y a la versión, con expiración. La separación de funciones se aplica en código | Seguridad |
| RF20 | **Verificador independiente** con estado propio, escrito por la otra persona desarrolladora a partir del texto de las reglas, más pruebas de mutación. Sin él no se reporta "0 pagos indebidos" | Los tres |
| RF21 | **El esperado del set es la intención.** Factura 07 espera ESCALAR, se agrega `tipo_documento` y la factura 17 se modela con confianza real. Un solo registro de identificadores de regla en el contrato, validado | Arquitectura |
| RF22 | Dinero en enteros o Decimal. Una moneda sin tasa falla cerrado | Seguridad, arquitectura |
| RF23 | Escapar toda salida en la interfaz. La app pública no acepta escritura | Seguridad |
| RF24 | **Autonomía graduada visible:** un interruptor por proveedor y monto (modo sombra, aprueba solo bajo X, autónomo) | Producto |
| RF25 | **Bandeja del aprobador:** la razón en una frase, un botón y una vista previa de qué cambia si aprueba | Producto |
| RF26 | **Posicionamiento:** una diapositiva frente a Ramp, BILL y Meow con la diferencia concreta | Producto |
| RF27 | **Sesión por visitante** en la app pública: copia del set base inmutable, par de claves de firma propio y reinicio; sin escritura compartida ni llamadas a la API | Diseño de la interfaz |

### Cómo se habla del proyecto
- No decir "garantía" ni "cero pagos indebidos" a secas. Decir "0 en 22 casos más N variantes", con la tasa de escalada innecesaria visible.
- No decir "ninguna plataforma lo hace". Decir "no encontramos". Ramp ya decide solo dentro de política y Meow ya envía pagos con topes; la diferencia es el recibo verificable por un tercero, el guardián y el pentest de reglas.
- La inyección en facturas se presenta como riesgo plausible. La investigación no encontró casos reales documentados, solo un escenario académico.
- La calibración de Jev sobre 22 facturas no tiene valor estadístico: se reportan conteos, no una curva.
- La integración con Blinka es una propuesta: no hay API pública y la orden de pago es un formato propio.

### Recorte, en orden de lo primero que se corta
1. Servidor MCP. 2. Verificación fuera de banda y máquina del tiempo. 3. Grabación del agente atacante (queda el pentest por código). 4. Jev (queda Haiku). 5. Adaptador XML (el XML del set queda escrito a mano) y pesos de prioridad. 6. Cadena de hashes y modo sombra. **Núcleo intocable:** lectura con esquema y caché, motor con identificadores únicos, recibo firmado, guardián, verificador independiente, registro de solo adición y una interfaz mínima.
