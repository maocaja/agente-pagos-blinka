# Modelo de lógica de la interfaz: U3

## 1. Apertura de una sesión
```mermaid
flowchart TD
  A[Visitante abre la app] --> B[El servidor crea una sesión]
  B --> C[Copia del set base inmutable y par de claves propio]
  C --> D[Pantalla Marcador con el set precargado]
  D --> E{¿Qué hace?}
  E -->|Navega| F[Bandeja, Reglas, Guardián, Pentest]
  E -->|Botón Demo| G[Modo guiado de 5 pasos]
  E -->|Reiniciar| H[Se vuelve a la copia original del set]
```

## 2. Escalada: de la bandeja a la decisión
```mermaid
flowchart TD
  P[Pendiente en la Bandeja] --> R{Rol}
  R -->|Analista| A1[Corregir un campo]
  R -->|Analista| A2[Escalar al CFO]
  R -->|CFO| C1[Aprobar con nota]
  R -->|CFO| C2[Rechazar con motivo]
  A1 --> V[El servidor reevalúa]
  C1 --> V
  V -->|Pasa| OK[Recibo nuevo y orden al guardián]
  V -->|Falla nueva o sin presupuesto| P
  V -->|Aparece una falla FRENAR| F[Frenada, sin acciones de aprobación]
  C2 --> X[Rechazada, queda en el registro]
```

## 3. Verificar un recibo
`Ver el recibo → conmutar a la vista técnica → pulsar Verificar → se recalcula la firma sobre el mismo JSON mostrado con la clave pública de la sesión → ✓ o ✗`. Si el JSON se altera, la verificación falla.

## 4. Mandato nuevo desde el pentest
`El pentest sobre v1 encuentra un hueco → arreglo propuesto → el CFO propone v2 → el analista contrafirma → v2 vigente → se repite el pentest`. Cada paso queda con el rol.

## 5. Cierre del ciclo
`Todas las escaladas con una acción humana → el CFO pulsa Cerrar ciclo → instantánea inmutable → se descarga la conciliación`. Si queda una escalada sin atender, el botón está deshabilitado y dice cuántas faltan.

## 6. Modo guiado
Los pasos están en `business-rules.md`. La guía solo mueve la pantalla, el rol y el estado; no tiene lógica propia: usa las mismas acciones que un usuario.
