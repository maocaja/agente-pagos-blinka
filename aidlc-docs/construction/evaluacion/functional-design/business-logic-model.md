# Modelo de lógica de la evaluación: U4

## Corrida de evaluación
```mermaid
flowchart TD
  A[Corrida: semilla, mandato, huella del código] --> B[Set y variantes de la arena]
  B --> C[El motor decide]
  B --> D[El verificador independiente recalcula, con estado propio desde el registro]
  C --> E{Comparar}
  D --> E
  E -->|Igual| F[Entrada verificada]
  E -->|Motor PAGAR, verificador no| G[Pago indebido: debe ser 0]
  E -->|Motor ESCALAR, verificador FRENAR| H[Frenada escalable: debe ser 0]
  E -->|Motor más estricto| I[Desvío conservador: se cuenta]
  E -->|Otra diferencia| J[Se investiga]
  F --> K[resultados.json]
  G --> K
  H --> K
  I --> K
  J --> K
  K --> L[Marcador: recuento de entradas verificadas y alcance]
```

## Facturas ocultas
`Sellar huellas y política → correr una vez al final → reportar tal cual → diagnosticar cada fallo → si hay corrección, segunda corrida con fecha y versión y aviso de que ya no es ciega`.

## Pentest
`Mandato v1 → seis estrategias con esperado escrito antes → comparar con el verificador → hueco: corregir o documentar → mandato v2 → repetir con la misma semilla → mostrar antes y después`.

## Mutación
`Copia temporal → aplicar un mutante → correr las pruebas → registrar cuál falla → si ninguna falla, hallazgo → restaurar la copia`.

## Qué nunca ocurre
- Un esperado calculado con el motor.
- Un mutante que sobrevive sin quedar anotado.
- Un cambio al motor para pasar las ocultas que no se reporte.
- Una cifra de "0" sin su alcance.
