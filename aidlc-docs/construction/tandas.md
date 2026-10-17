# Registro de tandas

Una fila por tanda de trabajo entregada a un subagente. Se completa al cerrar cada tanda (ver `CLAUDE.md`, seccion 4).

| Fecha y hora | Unidad | Pasos del plan | Subagente y modelo | Pruebas | Hallazgos |
|---|---|---|---|---|---|

## Ola 1 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | T1 y T1b | 14 | verde | El motor podía devolver PAGAR con 4 de 11 reglas: ahora falla cerrado por regla no implementada (el fixture inyecta las 4 hasta T3). `crear_app` de 49 líneas dividido por calidad |
| U2 Lectura | T1 y T1b | 7 | verde | `_a_decimal` con complejidad 22 dividido. `proveedor_asignado` null: falta asignar proveedor desde el registro maestro. `suma_lineas` falla en fac-10, 14, 15, 16 y 18, pero el esperado no escala fac-16 por R1 |
| U4 Evaluación | T1 | 20 | verde | Esperados reescritos de forma independiente. Faltan casos: monto entre umbral y tope, proveedor bloqueado, proforma, anticipo y tipo desconocido |
| Datos | Registro maestro | n/a | cargado | `datos/registro-maestro.json` como fuente única (11 proveedores, presupuesto 900000). Los acuerdos de la maqueta no coinciden con los asumidos por núcleo y evaluación (Cloud 4.500 contra 2.000; núcleo sin 5 proveedores) |
Consumo medido: 47.000 a 100.000 tokens de subagente por tanda, unos 540.000 en la ola. Quedan para la Ola 2: núcleo lee `datos/registro-maestro.json`, evaluación revalida esperados contra él, lectura asigna `proveedor_id`.

## Ola 2 (2026-10-17)
| Unidad | Tanda | Pruebas | Resultado | Hallazgos |
|---|---|---|---|---|
| U1 Núcleo | 11 reglas, guardián (6 verificaciones), libro de reserva y nonce, mandatos v1 y v2, sesiones | 43 (29 nuevas) | verde | El registro maestro tenía a Nuevo Logos como proveedor activo: la factura 09 salía PAGAR. Corregido en `datos/` (ahora escala). Quedan diferencias con `esperado.json` en f_10, f_12, f_13, f_15 y f_16 |
| U2 Lectura | Asignación de proveedor desde el registro | 11 | verde | 17 de 18 asignadas; f_09 y f_12 quedan sin proveedor |
| U3 Interfaz | Decisiones, recibo legible, guardián con campo alterable | 5 | verde | `dist/` estaba ignorado por `.gitignore`: ahora se versiona. Sin store ni mapa de capacidades por rol |
Pendientes: las líneas de f_10, 14, 15, 16 y 18 no suman el total porque el IVA va aparte (lectura); `tandas.md` y `aidlc-state.md` al día; aprobar con reevaluación (núcleo T4).
Consumo medido: unos 320.000 tokens de subagentes en la ola.
