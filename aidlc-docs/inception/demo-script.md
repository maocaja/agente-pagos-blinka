# Guion del video (criterio de "listo")

Fecha: 2026-10-17. El jurado ve el pitch y el video, no usa la aplicación. Por eso el wow es una secuencia guionizada, ensayada y grabada, no una interacción. Video de 3 minutos (dato del responsable). Los planes de código se ordenan por lo que este guion necesita.

## Mensaje único
"Un agente que lee facturas puede equivocarse. El nuestro no puede pagar mal: la decisión la toma un motor de reglas, queda en un recibo firmado, y el punto de pago se niega a pagar sin un recibo válido. Y lo atacamos nosotros primero."

## Escenas (3:00)
| Tiempo | Escena | Qué se ve | Qué se dice |
|---|---|---|---|
| 0:00 a 0:15 | Gancho: el recibo que se rompe | Primer plano: se cambia un dígito del monto en el recibo firmado, el sello se parte y el guardián rechaza con el motivo | "Esto es lo que pasa cuando alguien toca una decisión del agente." |
| 0:15 a 0:40 | El problema | Bandeja con facturas reales de prueba; una trae una instrucción oculta y el agente la frena | "Un agente que paga debe poder demostrar que no se equivoca. El texto de una factura es un dato, nunca una orden." |
| 0:40 a 1:50 | Centro: el agente que se ataca a sí mismo | Pantalla dividida: a la izquierda el atacante lanza estrategias (instrucción oculta, facturas partidas bajo el umbral, cuenta cambiada); a la derecha el marcador y el motivo de cada bloqueo. Con el mandato v1 aparece un hueco en rojo. Se cambia al v2 y el hueco se cierra | "Nos atacamos primero. Encontramos un hueco real, lo cerramos y lo volvemos a probar." |
| 1:50 a 2:20 | Una persona decide lo dudoso | Rol CFO aprueba una escalada; se emite un recibo nuevo y el guardián autoriza la orden | "Lo dudoso lo decide una persona, con la evidencia a la vista." |
| 2:20 a 3:00 | Cierre con honestidad | Marcador: 0 pagos fuera de reglas en N casos, verificado por un agente independiente; lista de lo que no probamos; siguiente paso (ruta de pago) | "Lo que no probamos lo decimos. Eso también es parte de la confianza." |

## Qué debe existir (unidad)
- Escena 1: recibo, firma, guardián y vista de recibo con campo alterable (U1, U3).
- Escena 2: lectura guardada con la factura de instrucción oculta, R1 y R3 (U1, U2).
- Escena 3: pentest, mandatos v1 y v2, R10 y arena, con la vista dividida (U1, U4, U3). Es el centro y la prioridad.
- Escena 4: roles simulados, bandeja y aprobación firmada (U1, U3).
- Escena 5: marcador, resultados del verificador independiente y texto fijo (U3, U4).

## Reglas de producción
- Set fijo y botón de guion que reinicia todo al mismo punto (el modo guiado de la interfaz sirve de claqueta).
- Todo lo que se graba funciona sin clave de API: la lectura se muestra desde extracciones guardadas, con la etiqueta "lectura guardada". La lectura en vivo es un extra, no un requisito.
- La grabación se rehace el domingo de 07:00 a 10:00 si el código cambió; el sábado se graba una versión de respaldo.
- Dos ensayos con cronómetro (sábado por la noche y domingo antes del congelamiento), anotando lo que falla. Nadie decide en el último minuto.

## Orden de construcción derivado
1. Motor con R2a, R3 y R6, recibo, firma y guardián. Sábado antes de las 18:00.
2. Vista de recibo alterable, marcador y bandeja con extracciones a mano.
3. Pentest, mandatos v1 y v2 y arena, con la vista dividida.
4. Lectura con modelo (si llega la clave) y el resto de las reglas.
5. Integración, despliegue y video.

## Línea de corte
Domingo 07:00 con la puerta de calidad en rojo: se corta primero la lectura en vivo, luego las reglas que el guion no usa, y el guion se queda como está. Nada nuevo después de las 10:00.
