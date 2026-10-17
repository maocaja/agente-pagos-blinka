# Arquitectura objetivo y alcance del MVP

Fecha: 2026-10-17. Esta es la vista profesional del problema y la solución. Los diseños por unidad (`construction/*/functional-design/`) describen la arquitectura objetivo; el código del hackathon implementa una versión ligera de ella. La tabla de la sección 4 es el puente y se actualiza cuando el código cambie.

## 1. Problema
Un agente que lee facturas y paga por la empresa puede equivocarse o ser engañado: una cuenta cambiada por correo, una instrucción escondida en el documento, una factura partida bajo el umbral, un duplicado. Un solo pago indebido destruye la confianza. Pedirle al modelo que "tenga cuidado" no es un control.

## 2. Solución: separar quién lee de quién decide y de quién paga
- **El modelo lee, no decide.** Convierte cualquier documento en una factura canónica con confianza y evidencia por campo. El texto del documento es un dato, nunca una orden.
- **Un motor de reglas determinista decide.** Reglas versionadas en un mandato que fija la empresa; sin cortocircuito; precedencia FRENAR > ESCALAR > PAGAR. Ante duda o error, falla cerrado.
- **El recibo firmado prueba.** Cada decisión queda en un recibo legible con regla, versión del mandato, hora y firma Ed25519.
- **El guardián, en el punto de pago, se niega** a ejecutar sin un recibo válido, vigente y no reutilizado.
- **Se ataca primero.** Un verificador independiente, un pentest y una arena de variantes miden qué pasa y qué no.

## 3. Arquitectura objetivo (producción)
```
Canales (correo, chat, PDF, imagen, XML fiscal)
  -> Adaptadores -> Extractor (cascada de modelos, verificaciones)
  -> Factura canónica (contrato versionado)
  -> Motor de reglas (mandato versionado, R1..R10)
  -> Recibo firmado (llave en KMS o HSM)
  -> Guardián (6 verificaciones) -> Orden de pago -> ERP o banco
Transversal: registro de solo adición, aprobaciones con roles y doble firma,
             verificador independiente, pentest y arena continuos, observabilidad, multiempresa
```
Principios: dominio puro y puertos para lo que cambia (modelos, firmador, reloj, almacenamiento); la política es un dato; dinero en enteros; falla cerrado; el servidor es la fuente de verdad.

## 4. Objetivo frente a MVP del hackathon
| Componente | Objetivo en producción | MVP (lo que se construye) | Por qué el recorte es seguro |
|---|---|---|---|
| Entradas | Correo, chat, PDF, escaneado, foto, XML fiscal en vivo | Bandeja simulada con etiqueta visible; texto, PDF, `.eml` y chat de prueba; foto con doble lectura | Mismos adaptadores y la misma factura canónica; solo cambia la fuente |
| Lectura | Cascada de modelos con caché, cuotas y monitoreo | Lecturas congeladas; modelo real si llega la clave | La lectura nunca decide; lo que lee pasa por el mismo motor |
| Reglas | 11 reglas, registro extensible, auditoría de cambios | Reglas simples como filas del mandato; pocas con función propia | La precedencia y el falla cerrado no cambian |
| Mandato | Versionado, dos firmas (CFO propone, analista contrafirma) | Dos versiones fijas (v1 sin R10, v2 con R10); pantalla de solo lectura | Basta para mostrar el hueco de política y su cierre |
| Firma | Llave en KMS o HSM, rotación | Llave local de demo, Ed25519, nonce y vigencia | El algoritmo y la verificación son los mismos |
| Guardián | Servicio en la ruta de pago del ERP o banco | Servicio y función con las mismas 6 verificaciones | La verificación es idéntica; cambia dónde se aloja |
| Almacenamiento | Base transaccional con registro inmutable | SQLite de solo inserción | Mismo modelo de solo adición |
| Aprobaciones | Roles, doble firma, reevaluación al aprobar | Un camino mínimo de aprobar y reevaluar | Aprobar siempre reevalúa |
| Interfaz | Aplicación completa por rol | Decisiones, recibo, guardián, reglas (lectura), marcador, ataque | Es lo que pide el reto y lo que se ve |
| Evaluación | Pentest y arena continuos, mutación periódica | 6 estrategias, arena acotada con semilla, pocos mutantes en la puerta | La cifra se declara con su alcance |
| Despliegue | Multiempresa, alta disponibilidad, observabilidad | Una instancia gratuita | No cambia la lógica |
| Pago | Orden hacia banco o ERP | Orden de pago propuesta; **no se mueve dinero** | Frontera explícita del reto |

## 5. Qué el MVP no prueba
Lectura real a escala, concurrencia, llaves administradas, integración bancaria, multiempresa, XML fiscal real. El video lo dice.

## 6. Regla de mantenimiento
El código se escribe ligero (ver `CLAUDE.md` 5c). Si una decisión ligera se aparta del diseño, se anota en la tabla de la sección 4; los diseños funcionales no se reducen.
