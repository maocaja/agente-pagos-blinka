# Referencia: QuickBooks, "Introduce y gestiona facturas de proveedor y pagos"

Fuente: `https://quickbooks.intuit.com/learn-support/es-global/help-article/pay-bills/introduce-gestiona-facturas-pagos-de-facturas-en/L1e9Ce5J7_ROW_es`, leída el 2026-10-17. Es una página de ayuda **breve**: describe lo básico y no cubre estados, aprobaciones, duplicados, créditos, pagos parciales ni conciliación (se comprobó que no los mencionan).

## Qué describe
- **Dos formas de entrada:** cargar archivos (PDF, JPEG, JPG, GIF o PNG) con extracción automática de datos, o alta manual con proveedor, condiciones, fechas, número, categoría, artículos, importe e impuestos.
- **Pago desde el mismo producto** y una pestaña **"Sin pagar"** para ver el flujo de caja pendiente y su efecto en el informe de beneficios y pérdidas.

## Qué nos sirve (y qué no)
| Idea de QuickBooks | Aplicación a nuestro producto | Decisión |
|---|---|---|
| Doble entrada: archivo o manual | Ya tenemos canales (correo, chat, PDF, imagen, XML, CSV) y la bandeja simulada | Sin cambio |
| La factura y el pago son objetos distintos | Coincide con nuestro vocabulario: decisión de pagar, autorización del guardián, orden simulada | Refuerza lo aprobado |
| Vista "Sin pagar" | Equivale a nuestras pendientes y al presupuesto reservado y disponible | Ya cubierto en Decisiones y la barra lateral |
| Campos: condiciones de pago, categoría, artículos | La factura canónica no lleva condiciones de pago ni categoría contable | Idea para después; no se añade ahora |
| Fecha de vencimiento | La factura canónica trae `fechas.vencimiento`, pero ninguna regla ni pantalla la usa | Idea para después: indicador "por vencer"; sin ampliar funciones hoy |
| Pagos parciales, créditos de proveedor, aprobaciones, lotes | La página no los describe; las notas de crédito ya se registran con REGISTRAR | No aplica |

**Conclusión:** sirve como validación del enfoque (separar factura y pago, ver lo pendiente) pero aporta poco como especificación. No cambia el contrato ni el alcance.
