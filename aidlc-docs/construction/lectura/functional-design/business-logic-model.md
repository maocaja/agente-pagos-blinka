# Modelo de lógica de la lectura: U2

## Flujo de lectura de un documento
```mermaid
flowchart TD
  A[Documento recibido] --> B[Hash del archivo]
  B --> C{¿Ya está en caché?}
  C -->|Sí| Z[Usar la lectura guardada]
  C -->|No| D{¿Tiene texto verificable?}
  D -->|No: cifrado o fuera de límites| E1[ESCALAR sin llamar a la API]
  D -->|Imagen o PDF escaneado| I[Doble lectura Haiku y Sonnet; campos críticos deben coincidir; nunca PAGAR autónomo]
  D -->|Sí, XML| X[Parser estructurado y reglas sobre el texto]
  D -->|Sí, texto o PDF| H[Lectura con Haiku 5.5, con cita de evidencia]
  H --> V{¿Verificaciones?}
  V -->|Fallan| S[Una relectura con Sonnet 5.5]
  S --> V2{¿Verificaciones?}
  V2 -->|Fallan| E2[ESCALAR con el motivo]
  V -->|Pasan| R2
  V2 -->|Pasan| R2
  X --> R2[Segunda lectura por reglas deterministas]
  R2 --> K{¿Coinciden las dos lecturas?}
  K -->|No o sin segunda lectura| E3[ESCALAR con ambos valores]
  K -->|Sí| N[Normalizar a la factura canónica]
  N --> P[Asignar proveedor: id fiscal, luego nombre]
  P --> Q{¿Valida contra el esquema?}
  Q -->|No| E4[ESCALAR]
  Q -->|Sí| G[Guardar en caché y entregar al núcleo]
  Z --> G
```

## Fallas de la API en cualquier punto
Una falla de la API se resuelve según la tabla de `business-rules.md`. En todos los casos el resultado es una factura canónica **incompleta con el motivo**, que el núcleo convierte en ESCALAR.

## Qué entrega U2 al núcleo
La factura canónica, la confianza por campo, el resultado de cada verificación (esquema, dinero, suma, cita, tipo, segunda lectura), el modelo y los tokens usados, los reintentos, el costo y, si hubo, el motivo de la falla.

## Qué nunca ocurre
- Una lectura que decide un pago.
- Un campo de dinero sin segunda lectura que llegue como confiable.
- Una subida de modelo evitada por una confianza alta del propio modelo.
- Un documento sin texto verificable enviado a la API.
