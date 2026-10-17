# Requisitos no funcionales e infraestructura (nota fusionada)

Fecha: 2026-10-16. Resume lo decidido en los diseños de las cuatro unidades y fija valores por defecto donde no hubo una pregunta. Lo marcado "por defecto" se puede cambiar.

## Pila
| Tema | Decisión | Origen |
|---|---|---|
| Backend | Python, FastAPI, SQLite | Pregunta 4 de requisitos |
| Interfaz | HTML y JavaScript sin proceso de compilación, servida por el backend; skill `frontend-design` | Pregunta 5 |
| Modelos | Haiku 5.5, relectura con Sonnet 5.5; clasificador Haiku detrás de una interfaz, Jev si llega gratis | Preguntas 6 y 7; diseño de la lectura |
| Firma | Par de claves; el guardián solo tiene la pública | Pregunta 14 |
| Despliegue | Servicio gratuito de hospedaje, un backend que sirve la interfaz; Dev A | Aclaraciones 1 y 2; unidades |
| Repositorio | Uno, con carpeta y rama por unidad | Plan de unidades |

## Rendimiento y límites (por defecto)
- La arena de nivel 1 (3.200 facturas) corre en pocos segundos; en la maqueta tardó cerca de 1 segundo. Si en el backend tarda más de 30 segundos, se reduce el recuento por defecto.
- Un visitante no puede lanzar más de una arena a la vez; las acciones se limitan por sesión.
- SQLite en modo WAL, una escritura a la vez, con reserva de presupuesto en una transacción.

## Seguridad
- **Secretos:** la clave de la API de Claude y las claves de firma viven en variables de entorno o archivos fuera del repositorio. El `.gitignore` los excluye. No hay llave en el repositorio.
- **Claves de firma:** un par por sesión en la app pública; el par de la instancia local lo genera el firmador al arrancar.
- **Salida:** todo texto de origen externo se escapa; sin `innerHTML` con datos de facturas.
- **App pública:** sin llamadas a la API de Claude, sin escritura compartida, límite de tasa por IP y por sesión. Sin autenticación real: roles simulados, declarado en pantalla.
- **MCP (extra):** si se construye, con token de acceso, límites de tasa y sin herramienta de aprobar.
- **Datos:** todo es sintético; sin datos reales de empresas ni de personas.

## Datos y sesiones
- La SQLite base del set es de solo lectura y se siembra al arrancar (el disco de un servicio gratuito suele ser temporal).
- Cada sesión de visitante trabaja sobre una copia; se elimina tras un periodo de inactividad (por defecto 60 minutos).
- El registro de decisiones solo admite inserción (disparadores que bloquean UPDATE y DELETE).

## Observabilidad (por defecto)
- Registro en JSON con identificador de solicitud, sesión, regla, veredicto, modelo, tokens y costo. Sin datos de las facturas en los registros.
- Para el costo: contador por corrida y tope duro configurable.

## Calidad y pruebas
- **Puerta de calidad antes de congelar** (domingo 10:00): pasan las pruebas del invariante, las del guardián, la carrera de presupuesto, las fallas del extractor, la corrida del set sin pagos indebidos ni frenadas escalables, y la mutación sin sobrevivientes sin explicar.
- Las pruebas corren en local con `pytest`; no hay integración continua.
- **Plan B de la demo:** lecturas guardadas, video de respaldo y modo guardado en la app pública.

## Riesgos de infraestructura
| Riesgo | Mitigación |
|---|---|
| Disco temporal del servicio gratuito | Sembrar SQLite al arrancar |
| Firmador separado imposible en un servicio gratuito | Claves de sesión en el mismo proceso; se declara; el firmador separado se muestra en local y en el video |
| Sin clave de la API todavía | Una persona desarrolladora la consigue antes del sábado a las 12:00; mientras tanto, lecturas escritas a mano |
| El servicio gratuito se duerme o tarda en arrancar | Despertar la app antes de la presentación; video de respaldo |
| Gasto de la API | Tope duro por corrida; la app pública no llama a la API |

## Valores por defecto a confirmar
1. Inactividad de sesión: 60 minutos.
2. Pruebas solo en local, sin integración continua.
3. Registro en JSON sin datos de facturas.
4. Si la arena tarda más de 30 segundos en el servicio gratuito, se reduce el recuento.
