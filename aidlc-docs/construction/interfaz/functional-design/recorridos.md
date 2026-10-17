# Recorridos de producto y criterios de aceptación

Fecha: 2026-10-17. La aplicación es una mesa de trabajo de cuentas por pagar: se recibe una factura, se revisa el documento y lo leído, se entiende la decisión, se resuelve una excepción según el rol y se consulta la evidencia. La demostración recorre esa misma mesa con datos simulados y un estado inicial reproducible (botón Demo). Personas en `inception/personas.md`.

## Vocabulario de estados (no mezclar)
| Estado | Significado en este producto |
|---|---|
| Decisión PAGAR, FRENAR, ESCALAR, REGISTRAR | Lo que decide el motor con las reglas del mandato |
| Autorizada | El guardián verificó el recibo y permite emitir la orden |
| Orden emitida (simulada) | Existe la orden de pago en formato bancario, marcada SIMULADA |
| Pago confirmado | **No existe**: el producto no mueve dinero. Nunca se rotula "pagado" |
El resumen de Decisiones usa "Autorizadas para pago", no "Pagadas".

## Contexto al abrir (Decisiones)
Empresa de demostración, periodo (ciclo), presupuesto reservado y disponible y actividad reciente (últimos eventos). Fuente: `GET /api/ciclo`.

## Recorrido 1: del documento a la resolución (analista y CFO)
- **Entrada:** Decisiones, fila de la factura con cuenta cambiada (Estudio Andino, foto) en estado Escalar y pendiente de aprobación.
- **El analista ve:** el documento original junto a lo leído; el dato que difiere ("cuenta 9021, la registrada termina en 4417") y el siguiente paso ("confirmar con el proveedor").
- **El CFO actúa:** Rechazar con nota (o Aprobar si fuera aprobable; aprobar siempre reevalúa).
- **Resultado:** la decisión cambia de estado, queda un **historial** visible (recibida, decidida por el motor, resuelta por el CFO con su nota y hora) y la actividad reciente lo refleja.
- **Errores:** rol sin permiso, falla no aprobable (409), nota faltante (422): cada uno con su motivo escrito.
- **Aceptación:** se completa sin perder sesión ni contexto, y en el navegador se ve el historial después de actuar.

## Recorrido 2: reconstruir y verificar (auditor)
- **Entrada:** el detalle de una decisión autorizada.
- **Ve:** la regla, la versión del mandato, la hora, quién resolvió y el recibo; el botón Verificar firma.
- **Verifica fuera de la aplicación:** un panel "Verificar sin esta aplicación" con el enlace al paquete de auditoría y el comando exacto del script (`python3 nucleo/auditoria/verificar_paquete.py <paquete>`), y qué resultado esperar.
- **Aceptación:** el auditor puede reconstruir la decisión con su historial y descargar lo necesario para verificarla por su cuenta.

## Reglas de coherencia
Proveedores, montos, fechas y estados coinciden entre Decisiones, Bandeja, detalle, Reglas y Marcador. Ninguna pantalla muestra un número que otra contradiga. Cargas, errores y listas vacías tienen respuestas claras; la sesión se conserva al navegar.

## Cierre de una tanda de interfaz
Se recorre cada recorrido en el navegador contra la app real (no contra el simulador) y se informa qué se vio. Las pruebas técnicas no sustituyen este paso.
