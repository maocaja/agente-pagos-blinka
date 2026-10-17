# Modelo de lógica de negocio: U1 Núcleo

## 1. Evaluación de una factura
```mermaid
flowchart TD
  A[Factura canónica] --> B{¿Tipo conocido?}
  B -->|No| E1[ESCALAR: tipo no soportado]
  B -->|Sí| C[Política por tipo]
  C -->|Estado de cuenta| E2[FRENAR: no es una factura]
  C -->|Nota de crédito| E3[Registrar crédito, sin orden]
  C -->|Proforma o anticipo| E4[ESCALAR: la decide una persona]
  C -->|Factura o cuenta de cobro| D[Evaluar R1 a R8 y R10 sin cortar]
  D --> F{¿Falló alguna?}
  F -->|Sí| G[Veredicto: FRENAR si alguna frena, si no ESCALAR]
  F -->|No| H[Evaluar R9 presupuesto]
  H -->|Falla| G
  H -->|Pasa| I[PAGAR: reservar presupuesto y emitir recibo]
  G --> J[Registrar decisión con el resultado por regla]
  I --> J
```

## 2. Ciclo de vida de una decisión
```mermaid
stateDiagram-v2
  [*] --> Evaluada
  Evaluada --> Frenada: FRENAR
  Evaluada --> Pendiente: ESCALAR
  Evaluada --> ConRecibo: PAGAR
  Pendiente --> Reevaluada: aprobar o corregir
  Pendiente --> Rechazada: rechazar con motivo
  Pendiente --> Pendiente: escalar a otro rol
  Pendiente --> Vencida: pasan 24 horas
  Reevaluada --> ConRecibo: sigue cumpliendo
  Reevaluada --> Pendiente: falla nueva o sin presupuesto, con motivo
  Reevaluada --> Frenada: aparece una falla FRENAR
  ConRecibo --> Autorizada: el guardián valida
  ConRecibo --> Denegada: el guardián rechaza
  Denegada --> [*]: se libera la reserva
  Frenada --> [*]
  Rechazada --> [*]
  Vencida --> [*]
  Autorizada --> [*]
```

## 3. Mandato
`Propuesto por el CFO → Contrafirmado por el analista → Vigente (versión n)`. Una versión nueva no cambia las decisiones ya tomadas: cada recibo lleva la versión con la que se emitió. El guardián rechaza recibos de una versión que ya no es la vigente.

## 4. Reserva de presupuesto
Se hace en la misma transacción que registra la decisión y consume el identificador del recibo. El presupuesto restante es la suma de las reservas del periodo, no un número editable. Una denegación del guardián, un vencimiento o un rechazo generan un movimiento compensatorio.

## 5. Recibo y guardián
El recibo contiene: factura, hash del documento, beneficiario, monto, veredicto, modo de autonomía (autónomo o sombra), resultado por regla, fallas aprobadas si las hay, versión del mandato, identificador aleatorio, vigencia y versión de la clave. El firmador (proceso aparte) lo firma. El guardián ejecuta las seis verificaciones y reevalúa el presupuesto antes de autorizar (ver `components.md`, C10 y C11). La verificación 4 queda así: PAGAR en modo autónomo; o ESCALAR con una aprobación firmada y vigente; o PAGAR en modo sombra con una aprobación firmada; nunca FRENAR. Esta verificación hay que reflejarla en el contrato.

## 6. Ciclo de pagos
`Abierto → En proceso → En revisión → Aprobado → Cerrado`. Se cierra cuando todas las escaladas tienen una acción humana; el cierre guarda una instantánea inmutable y exporta la conciliación.

## 7. Qué nunca ocurre
- Un PAGAR sin que todas las reglas apliquen y pasen, y con reserva hecha.
- Una orden autorizada para una factura frenada.
- Una aprobación sin reevaluación, o vencida.
- Un cambio del mandato con una sola firma.
