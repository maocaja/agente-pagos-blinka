# Entidades del dominio: U4 Evaluación

| Entidad | Atributos principales | Notas |
|---|---|---|
| **Caso** | id, archivo, canal, grupo (visible u oculta) | Una factura del set |
| **EsperadoDeReglas** | caso, veredicto, reglas que fallan, explicación | Escrito a mano antes de las lecturas |
| **EsperadoExtremoAExtremo** | caso, veredicto, lectura esperada según el canal | Ídem |
| **Sello** | archivos, huellas SHA-256, fecha, política | Se registra antes de la primera corrida |
| **CorridaDeEvaluacion** | id, semilla, versión del mandato, huella del código, fecha, tipo (set, arena, pentest, ocultas, mutación) | Produce `resultados.json` |
| **ResultadoPorCaso** | corrida, caso o variante, veredicto del motor, veredicto del verificador, clase (verificada, pago indebido, frenada escalable, desvío conservador, otra) | Alimenta el recuento del Marcador |
| **Variante** | caso base, nivel (1 campos o 2 texto), mutación aplicada, semilla | Reproducible con la semilla |
| **EstrategiaDePentest** | nombre, esperado en v1, esperado en v2, resultado real | Esperado escrito antes de correr |
| **Hallazgo** | origen, descripción, estado (abierto, corregido, documentado), fecha | Del pentest, la mutación o las ocultas |
| **Mutante** | regla o componente, tipo (quitar, invertir), pruebas que fallan, estado (muerto, sobreviviente, equivalente) | Sobre una copia temporal |
| **PruebaDeFalla** | falla simulada (rechazo, truncado, JSON inválido, tiempo, 4xx, tope), resultado esperado ESCALAR | Fallas del extractor |
| **EstrategiaGrabada** | texto, fecha, origen (agente atacante), revisada por una persona | Solo se muestra |

## Relaciones
`Caso 1—1 EsperadoDeReglas`, `Caso 1—1 EsperadoExtremoAExtremo`, `Sello 1—n Caso`, `CorridaDeEvaluacion 1—n ResultadoPorCaso`, `Caso 1—n Variante`, `CorridaDeEvaluacion 1—n Hallazgo`, `Mutante n—1 CorridaDeEvaluacion`.
