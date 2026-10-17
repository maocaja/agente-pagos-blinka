# Dependencias entre unidades

| Unidad | Depende de | Qué necesita |
|---|---|---|
| Contrato | nada | Lo escriben las dos personas desarrolladoras en la primera hora |
| U1 Núcleo | Contrato | Esquemas y registro de reglas |
| U2 Lectura | Contrato, API de U1 | Entrega facturas canónicas a la API de U1 |
| U3 Interfaz | Contrato, API de U1, U4 y U2 | Decisiones, recibos y aprobaciones de U1; resultados del verificador y de la arena de U4 para el marcador; contador de costo de U2 |
| U4 Evaluación | Texto de las reglas, API de U1 | El verificador usa solo el texto; el pentest y la arena llaman a la API de U1; las pruebas de mutación modifican el código de U1 en una copia |

## Orden de integración
1. Contrato firmado por las dos personas.
2. U1 publica endpoints con respuestas fijas (stubs) para que U2 y U3 trabajen en paralelo.
3. Extremo a extremo con 3 reglas antes del sábado a las 18:00.
4. El resto de las reglas, el pentest y la arena el sábado por la noche.
5. Congelamiento el domingo a las 10:00.

## Riesgos de dependencia
- **U2 y U3 las hace la misma persona:** si la lectura se atrasa, la interfaz también. La interfaz trabaja con extracciones escritas a mano.
- **U4 la hace un subagente:** necesita las reglas escritas en texto antes de arrancar (diseño funcional del núcleo).
- **El contrato es el cuello de botella:** si no se cierra en la primera hora, se bloquea todo.
- **U1 es la unidad más cargada** y todas dependen de su API: por eso el sábado a las 18:00 debe existir un extremo a extremo mínimo, y los endpoints con respuestas fijas salen primero.
- **El marcador (U3) depende de tres unidades.** Si U4 se atrasa, el marcador muestra primero solo los aciertos contra el esperado.
