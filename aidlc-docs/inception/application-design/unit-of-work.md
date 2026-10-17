# Unidades de trabajo

## U1 Núcleo (Dev A)
- **Contiene:** C5 a C14, y X1 si hay tiempo.
- **Entrega:** API estable, motor con identificadores de regla únicos, recibos firmados, guardián y registro.
- **Sesión por visitante (RF27):** la app pública crea una copia del set y un par de claves por sesión, y permite reiniciar.
- **Incluye el despliegue** en un servicio gratuito, con SQLite sembrada al arrancar, al final del núcleo.
- **Primer hito (sábado, antes de las 18:00):** endpoints que acepten una factura canónica y devuelvan decisión y recibo con 3 reglas.
- **Prioridad dentro de U1 (es la unidad más cargada, 10 componentes):** P0: C5, C6, C7, C8, C10, C11, C12 y un C14 mínimo. P1: C13 completo y C9 (plantilla simple). Extra: X1. Si la lectura de U2 termina temprano, Dev B apoya a Dev A en U1.

## U2 Lectura (Dev B)
- **Contiene:** C1 a C4 y C3b (contador y tope duro).
- **Entrega:** factura canónica validada a partir de texto, PDF y un XML simulado; extracciones guardadas para la demo pública.
- **Primer hito:** extracciones escritas a mano de las 18 facturas, mientras llega la clave de la API.

## U3 Interfaz (Dev B)
- **Contiene:** C15 a C17.
- **Entrega:** HTML y JavaScript con diseño llamativo (skill `frontend-design`), consumiendo la API de U1. Toda salida se escapa; la app pública no escribe.
- **Punto de partida:** la maqueta `demo-front/index.html` y su motor de referencia, no una página en blanco.
- **Primer hito:** pantalla de Decisiones con el recibo de una factura.
- **Depende también de U4** (resultados del verificador y de la arena para el marcador) **y de U2** (contador de costo).

## U4 Evaluación (subagente, con revisión de una persona desarrolladora)
- **Contiene:** C18 a C22.
- **Regla de independencia (solo para el verificador, C19):** se escribe desde el texto de las reglas, sin acceso al código del motor ni a `motor.js`, y en una sesión que no escriba el pentest ni la arena. Pentest y arena (C20 y C21) sí pueden ver el motor. Las pruebas de mutación (C22) las ejecuta una persona o un agente distinto al que escribió el verificador.
- **Primer hito:** esperado corregido a la intención (factura 07 escala, `tipo_documento`, factura 17 realista).
- **Prioridad dentro de U4:** P0, esperados reescritos, verificador y corrida del set. P1, pentest y arena de nivel 1. P2, arena de nivel 2, mutación, fallas del extractor y carrera de presupuesto. Las pruebas de mutación y la arena de nivel 2 necesitan el código de U1, así que son de la noche del sábado.

## Contrato compartido (antes de empezar las unidades)
Lo escriben juntas las dos personas desarrolladoras en la primera hora: esquema de la factura canónica con `tipo_documento`, esquema de decisión y recibo, registro único de identificadores de reglas y los endpoints entre U1 y las demás.

## Organización del código
Un repositorio, una carpeta y una rama por unidad. Nadie edita carpetas ajenas.

```
contrato/      compartido (esquemas, registro de reglas, endpoints)
nucleo/        U1   (rama nucleo)      reemplaza la carpeta vacía motor/
lectura/       U2   (rama lectura)     reemplaza la carpeta vacía extraccion/
interfaz/      U3   (rama interfaz)    reemplaza la carpeta vacía ui/
evaluacion/    U4   (rama evaluacion)
datos/         set de facturas y esperado (U4)
demo-front/    maqueta de referencia, no es el producto
```

## Requisitos por unidad
| Requisito | Unidad |
|---|---|
| RF1, RF2, RF3 (ingesta, canónica, lectura), RF16 | U2 |
| RF4, RF5, RF6, RF7, RF9, RF10, RF15, RF17, RF18, RF19, RF22 | U1 |
| RF8 (pantalla de aprobación), RF11 (marcador), RF23 (escapar salida), RF24 y RF25 (parte visual) | U3, con la API de U1 |
| RF23 (modo público de solo lectura), RF24 (parámetros de autonomía), RF25 (vista previa de qué cambia si se aprueba) | U1: el servidor ofrece lo que la interfaz muestra |
| RF12, RF20, RF21, pruebas de falla del extractor | U4 |
| RF13 (MCP), RF14 (extras) | U1, solo si sobra tiempo |
| RF26 (diapositiva de posicionamiento) | Equipo no técnico |

## Fuera de las unidades
- Pitch, guion de la demo, video de respaldo y diapositiva de posicionamiento: equipo no técnico.
- **Despliegue en un servicio gratuito y modo guardado:** Dev A, al final del núcleo (decisión del 2026-10-16); el mismo backend sirve la interfaz estática. Dos riesgos: muchos servicios gratuitos tienen disco temporal, así que SQLite se reinicia y hay que sembrarla al arrancar; y el firmador separado (RF17) puede no caber como segundo proceso en un servicio gratuito.
