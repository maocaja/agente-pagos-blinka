# Agente de pagos con garantia (Reto Blinka)

Entrega: domingo 2026-10-18, 12:00. Meta interna: congelar y subir a las 10:00.

Documento base: `PRD.md`. Demo rapida de planteamiento: abrir `demo-front/index.html` en el navegador (sin instalar nada).

## Carpetas y responsables
| Carpeta | Contenido | Responsable |
|---|---|---|
| `contrato/` | JSON de extraccion y de decision. Se cambia solo de comun acuerdo | Los dos devs |
| `motor/` | Reglas, registro de solo adicion, tests del invariante | Dev A |
| `extraccion/` | Llamada a Claude con esquema, cache, manejo de refusal y truncado | Dev B |
| `ui/` | Pantallas Decisiones, Reglas, Marcador, bandeja de aprobacion | Dev B |
| `datos/facturas/` | Facturas simuladas (texto y 3 o 4 PDF) | Equipo no tecnico |
| `datos/esperado.json` | Veredicto esperado por factura; 3 facturas se guardan sin mirar hasta el final | Equipo no tecnico |
| `demo-front/` | Maqueta de planteamiento con 16 facturas simuladas y motor en JavaScript | Referencia |

## Reglas de trabajo
- Una rama por dev (`motor`, `ui-extraccion`). Nadie edita carpetas ajenas.
- El modelo extrae y redacta; nunca decide. Ante error, refusal o JSON invalido: ESCALAR.
- Solo se aprueban escaladas; una frenada no se aprueba.
- Sin datos reales ni llaves en el repositorio.
- Lo que no aparece en la demo baja de prioridad.

## Equipo no tecnico
1. Facturas simuladas con respuesta esperada (ver los 16 casos de `demo-front/motor.js` como guia).
2. Investigacion: como se pagan hoy las facturas internacionales y donde fallan las herramientas existentes. Cada dato con fuente y fecha; lo no verificado se marca asi.
3. Pitch, guion y video de respaldo de la demo.
