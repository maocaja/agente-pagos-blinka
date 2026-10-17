# Adaptación de la referencia "Biblioteca de facturas" a Decisiones

Fecha: 2026-10-17. Estado: **ADAPTACIÓN PROPUESTA; fase 1 (Decisiones y su detalle) para revisar antes de extender**. Referencia del equipo: `https://notification-four-spot-prominent.trycloudflare.com/prototipos/biblioteca.html` (recorrida en Chrome el 2026-10-17; es un prototipo con datos ficticios y sin conectores). Sustituye la estructura de `direccion-visual.md` (se conservan su diagnóstico y las tres escenas).

## 1. Qué es lo aprobado y qué es propuesta
| Fuente | Estado | Qué fija |
|---|---|---|
| `recorridos.md`, `personas.md` | Aprobado | Decisiones como entrada operativa; dos recorridos; vocabulario: decisión de pagar, autorizada por el guardián, orden emitida simulada; nunca "pagado" |
| `business-rules.md` y `frontend-components.md` (interfaz) | Aprobado | Barra lateral fija; encabezado con ciclo, mandato, selector de rol con la etiqueta "rol simulado" y botón Demo; permisos por rol (el analista no ve aprobar ni rechazar; una frenada no ofrece aprobación; R1 y R9 no ofrecen aprobar); orden por riesgo; etiquetas "firma de demo" y "lectura guardada" |
| `design-system.md`, `docs/design-system/` | Aprobado | Tokens, Inter y Geist Mono, escala (cuerpo 18 px, apoyo 15 px mínimo), formas (controles 10 px, paneles 18 px, botones en píldora), componentes de la guía |
| `contrato/` 1.1.0-rc5 | Aprobado | Datos y rutas disponibles; no se inventan campos |
| `direccion-visual.md`, `docs/propuesta-pantalla-principal.html` | Propuesta mía, reemplazada en estructura | |
| Referencia del equipo | Propuesta | Acabado, composición y relación campo a evidencia |

## 2. Matriz de adopción
| Elemento de la referencia | Decisión | Motivo |
|---|---|---|
| Barra lateral con tarjeta de empresa, secciones y ciclo activo | **Adoptar** (ya aprobada la barra) | Contexto de empresa, periodo y ciclo |
| Migas de pan y barra superior con periodo, tema y usuario | **Adoptar**, con el rol simulado | Encabezado aprobado |
| Marca "blinka" y su logotipo | **No adoptar** | La guía prohíbe usar su logotipo y su nombre como marca; se usa "Mesa de pagos" |
| Franja de cuatro cifras | **Reducir** a una línea de tres o cuatro cifras | Petición de simplificar; no repetir lo que muestra la lista |
| Búsqueda y filtro de estado | **Adoptar** como filtros principales | |
| Filtros de formato y procedencia | **Adaptar** como filtros adicionales plegados (formato y canal reales: correo, chat, PDF, imagen, XML, CSV) | |
| "Rutas de recepción": Portal, WhatsApp, Slack, SFTP, API | **No adoptar** | No existen en el contrato ni en el producto; no se presentan conectores |
| Lista de documentos a la izquierda con insignia de formato, proveedor, fecha, número, importe y estado | **Adoptar** | Biblioteca con selección de documentos |
| Cuatro o cinco etapas como pestañas (Documento, Extracción, Normalización, Validación, Decisión) | **Adaptar**: las pestañas siguen siendo Resumen, Documento, Recibo e Historial; las etapas pasan a una línea de proceso dentro de Documento | Se conserva el UX aprobado |
| Campos extraídos con clic que ubica el origen en el documento | **Adoptar donde los datos lo permiten** (campos con `evidencia` y cita en la factura canónica) | Relación campo y evidencia |
| "Aprobada simulada" y estados parecidos | **No adoptar** | Vocabulario: decisión de pagar, autorizada, orden simulada |
| "Corregir monto extraído", "Exportar biblioteca", "Añadir ejemplo" | **No adoptar** | Sin funciones nuevas |
| Etiqueta "Prototipo de hackathon, documentos ficticios, pagos simulados" | **Adoptar** como "Datos de demostración, lectura guardada, no se mueve dinero" | Etiquetas de simulación |
| Texto de 11 a 13 px | **No adoptar** | La escala aprobada exige 15 px mínimo para proyección |
| Radios y densidad | **Adaptar** a las formas y espacios del sistema de diseño | |
| Identificadores de reglas como R6b | **No adoptar** | Solo los ids del contrato; en pantalla, el motivo en lenguaje llano |

## 3. Estructura de Decisiones (fase 1)
- **Barra lateral fija** (Decisiones con el número de pendientes, Bandeja simulada, Reglas, Marcador, Ataque); abajo, tarjeta de empresa con periodo y ciclo abierto, y las etiquetas de simulación.
- **Encabezado:** migas (empresa, Decisiones), mandato, ciclo, selector de rol con "rol simulado", Demo y tema.
- **Área de trabajo:** título y una frase; una línea de cifras; búsqueda y filtro de estado; un enlace "Más filtros" (formato y canal); lista a la izquierda y detalle a la derecha, **sin bloques entre el encabezado y la lista**.
- **Detalle:** cabecera (proveedor, archivo y número, estado y motivo siempre visibles) y las pestañas **Resumen, Documento, Recibo, Historial**.
  - Resumen: decisión, siguiente paso, tres estados y acciones por rol, sin repetir lo de la lista.
  - Documento: línea de proceso (lectura, validación, reglas, decisión), original junto a los campos leídos con su evidencia, y las diferencias contra el registro.
  - Recibo e Historial: como están aprobados.
- Los cuatro estados de gestión se muestran con palabra e ícono: espera aprobación, decisión de pagar, frenada, rechazada por el CFO, autorizada por el guardián.

## 4. Fase 1 y fase 2
- **Fase 1 (esta):** Decisiones y su detalle conectados a los datos reales; capturas y comparación antes de seguir.
- **Fase 2 (tras la revisión):** extender los componentes compartidos (barra lateral, encabezado, tablas, controles) a Bandeja, Reglas, Marcador y Ataque, y las tres escenas de la demostración, sin añadir funciones.
- Cierre de cada fase: recorrer los dos recorridos en Chrome contra la app real y pasar la puerta de calidad.
