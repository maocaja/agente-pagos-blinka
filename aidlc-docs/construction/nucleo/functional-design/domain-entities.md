# Entidades del dominio: U1 Núcleo

| Entidad | Atributos principales | Relaciones | Notas |
|---|---|---|---|
| **Empresa** | id, nombre, moneda base | tiene mandatos, proveedores, ciclos | Multiempresa desde el esquema |
| **Mandato** | empresa, versión, parámetros, estado, firmas (CFO y analista), fecha | pertenece a Empresa | Inmutable por versión; v1 sin R10, v2 con R10 |
| **Usuario** | id, nombre, rol (analista o CFO), clave pública | firma aprobaciones y mandatos | Autenticado; el rol limita las acciones |
| **Proveedor** | id canónico, nombre, estado (activo, bloqueado), fecha de alta, nivel de autonomía | tiene cuentas y acuerdos | Registro maestro |
| **CuentaRegistrada** | proveedor, país, moneda, últimos 4, titular | pertenece a Proveedor | Solo cambia por trámite aparte con firma |
| **Acuerdo** | proveedor, monto máximo por factura, moneda, vigencia | pertenece a Proveedor | Sin acuerdo, ESCALAR |
| **Documento** | id, hash del archivo, canal, tipo, recibido en | origina una Factura canónica | El crudo es inmutable |
| **FacturaCanónica** | documento, emisor, número y número normalizado, fechas, montos en unidades menores, moneda, cuenta, líneas, señales, confianza por campo | cita Documento | Validada contra el esquema |
| **Decisión** | factura, mandato (versión), veredicto, resultado por regla, motivo, fecha | genera Reserva y Recibo | **Solo inserción**; las correcciones y aprobaciones son filas nuevas |
| **ResultadoRegla** | decisión, id de regla, estado (cumple, falla, omitida), acción, evidencia | pertenece a Decisión | La evidencia cita el campo de la factura |
| **Reserva** | decisión, periodo, proveedor, monto, tipo (reserva o compensación) | pertenece a Decisión | El presupuesto restante se deriva de aquí |
| **Recibo** | decisión, hash del documento, beneficiario, monto, veredicto, versión del mandato, identificador aleatorio, vigencia, versión de clave, firma | pertenece a Decisión | El identificador se consume una sola vez, con UNIQUE |
| **Aprobación** | decisión, usuario, rol, acción (aprobar, corregir, rechazar, escalar), nota, vigencia, firma | ligada a un Recibo y su versión | Quien cargó la factura no aprueba |
| **OrdenDePago** | recibo, beneficiario, monto, moneda, ruta propuesta, estado | la verifica el Guardián | Formato propio; no hay integración real |
| **CicloDePagos** | empresa, periodo, estado, instantánea | agrupa decisiones | Cierra con exportación de la conciliación |
| **Evento** | actor, acción, entidad, antes, después, fecha | | Registro de auditoría de solo adición |

## Relaciones clave
`Empresa 1—n Mandato`, `Empresa 1—n Proveedor 1—n CuentaRegistrada`, `Proveedor 1—n Acuerdo`, `Documento 1—1 FacturaCanónica`, `FacturaCanónica 1—n Decisión` (cada reevaluación es otra decisión), `Decisión 1—n ResultadoRegla`, `Decisión 1—n Reserva`, `Decisión 1—0..1 Recibo`, `Recibo 1—0..1 OrdenDePago`, `CicloDePagos 1—n Decisión`.
