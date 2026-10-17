# Contrato compartido

Version `1.1.0-rc6`. Es la ruta critica de las cuatro unidades. Se escribio antes que el codigo, a partir de los diseños funcionales aprobados en `aidlc-docs/construction/`.

## Archivos
| Archivo | Que define | Quien lo produce | Quien lo consume |
|---|---|---|---|
| `extraccion.schema.json` | Salida del modelo con salida estructurada | U2 | U2 |
| `factura-canonica.schema.json` | Factura canonica (entrada del motor) | U2 | U1, U3, U4 |
| `mandato.schema.json` y `ejemplos/mandato.v1.json`, `mandato.v2.json` | Parametros por empresa; v1 sin tope acumulado, v2 con el | U1 | Todas |
| `decision.schema.json` | Decision del motor, con cuatro veredictos | U1 | U3, U4 |
| `recibo.schema.json` | Recibo firmado | U1 (firmador) | U1 (guardian), U3, U4 |
| `aprobacion.schema.json` | Accion humana firmada | U1 | U1, U3 |
| `registro.schema.json` | Formato estable del registro de solo adicion | U1 | U4 (verificador) |
| `reglas.registro.json` | Identificadores de reglas y politica por tipo | U1 | Todas |
| `resultados.schema.json` | Resultado de una corrida de evaluacion (lo lee el Marcador) | U4 | U3 |
| `esperado.schema.json` | Los dos veredictos esperados de un caso y su sello | U4 | U4 |
| `monedas.json` | Exponente de unidades menores por moneda | U1 | Todas |
| `api.openapi.yaml` | Endpoints, errores y ejemplos para un servidor simulado | U1 | U2, U3, U4 |
| `validar.py` | Validador minimo de los ejemplos (sin dependencias) | U1 | Todas |

## Convenciones
- **Dinero:** enteros en unidades menores, como texto, con el exponente de `monedas.json`. Nunca decimales flotantes. **El modelo no convierte unidades:** extrae el monto tal como esta impreso y el codigo lo convierte; un formato ambiguo cuenta como "sin segunda lectura". La conversion a la moneda base se redondea al alza al comparar contra topes y umbrales.
- **Costo:** siempre en millonesimas de dolar (`*_microusd`), nunca en `_menor`, para no confundirlo con centavos.
- **Idempotencia:** toda accion que cambia estado lleva `Idempotency-Key`.
- **Documentos:** `POST /api/documentos` lee un archivo solo en local; en la app publica responde 403 y solo hay muestras con lectura guardada.
- **Fechas:** ISO 8601. **Identificadores de reglas:** R1, R2a, R2b, R3 a R10, solo los de `reglas.registro.json`.
- **Veredictos:** PAGAR, FRENAR, ESCALAR y REGISTRAR. Prioridad FRENAR > ESCALAR > PAGAR o REGISTRAR. REGISTRAR solo para una nota de credito que pasa todas las reglas y nunca lleva orden de pago.
- **Falla cerrado:** un cuerpo que no valida produce 422 y la factura queda ESCALADA con el motivo; nunca se pierde.
- **Sesion:** cada peticion lleva `X-Sesion-Id`; el rol simulado viaja en `X-Rol`.
- **Nada quemado:** todo valor vive en el mandato.

## Cambios
La version esta congelada. Un cambio requiere el acuerdo de las dos personas desarrolladoras, sube la version y actualiza los ejemplos del servidor simulado. Los cambios que rompen (renombrar o quitar campos) suben la version mayor.

## Ejemplos para el servidor simulado
| Endpoint | Ejemplo |
|---|---|
| `POST /api/facturas` (cuerpo) | `ejemplos/factura-canonica.f11.json` |
| `GET /api/decisiones/{id}` (decision) | `ejemplos/decision.f11.json` |
| `GET /api/recibos/{id}` | `ejemplos/recibo.pagar.json` |
| `POST /api/decisiones/{id}/aprobar` (aprobacion) | `ejemplos/aprobacion.ejemplo.json` |
| `POST /api/guardian/verificar` (respuesta) | `ejemplos/guardian.rechazo.json` |
| `GET /api/mandato` | `ejemplos/mandato.v1.json`, `ejemplos/mandato.v2.json` |
| Resultado de la arena | `ejemplos/resultados.arena.json` |
| Esperado de un caso | `ejemplos/esperado.f11.json` |

Faltan ejemplos para el resto de las rutas: se agregan al construir el servidor simulado.

## Pruebas del contrato
- `python3 validar.py` valida los ejemplos con un validador minimo (type, required, enum, pattern, additionalProperties, items). El test de contrato de U1 debe usar una libreria completa de JSON Schema.
- U1 corre un test de contrato contra su implementacion: cada respuesta, incluidos los caminos de fallo, valida contra la especificacion.
- U2 y U3 desarrollan contra un servidor simulado alimentado con los ejemplos de `api.openapi.yaml`.

## Provisional
Hay valores que se calibran despues: `umbral_senal_texto`, `dias_proveedor_nuevo` y `tope_gasto_corrida_menor`.

## Cambios de 1.1.0-rc1 (aditivos, Ola 5)
- `decision.schema.json`: campos opcionales `explicacion` y `que_hacer`.
- `api.openapi.yaml`: rutas nuevas `POST /api/mandato/previa`, `GET /api/auditoria/paquete` y `GET /api/ordenes/{id}/pain001`.

## Cambios de 1.1.0-rc2 (aditivos, Ola 7)
- `api.openapi.yaml`: campo opcional `lectura` (`en_vivo` o `guardada`) en la respuesta de `POST /api/sesion`.
- `factura-canonica.schema.json`: `senales.remitente_inconsistente` (remitente distinto del origen declarado, por ejemplo `Reply-To`; R1 escala). Añadido en la Ola 4.
- `api.openapi.yaml`: `GET /api/muestras` lleva el campo opcional `original`; `POST /api/pentest/ejecutar` y `POST /api/arena/ejecutar` devuelven la forma de `resultados.schema.json` (`recuentos`, `casos`, `no_prueba`), no la descrita antes (nunca implementada).

## Cambios de 1.1.0-rc3 (aditivos, Ola 14)
- `api.openapi.yaml`: `GET /api/ciclo` devuelve `ciclo_id`, `empresa`, `moneda`, importes `presupuesto_menor`, `reservado_menor` y `disponible_menor` (texto) y `actividad` (ultimos 5 eventos); `GET /api/decisiones/{id}` anade `historial` y `estado_orden`.

## Cambios de 1.1.0-rc4 (aditivos, Ola 15)
- `api.openapi.yaml`: ruta nueva `GET /api/muestras/{id}/archivo` (archivo original de la muestra; 404 si el id no existe).

## Cambios de 1.1.0-rc5 (aditivos, Ola 16)
- `api.openapi.yaml`: ruta nueva `POST /api/decisiones/{id}/autorizar` (analista o CFO): pide al guardian la orden de una decision con recibo y devuelve sus verificaciones; 409 si no es autorizable. El historial anade el evento `autorizada`.

## Cambios de 1.1.0-rc6 (aditivos, Ola 19)
- `api.openapi.yaml`: rutas nuevas `GET /api/notificaciones` (bandeja de salida de avisos), `POST /api/notificaciones/prueba` (analista o CFO; una cada 10 s, 429 si se excede) y `GET /api/salud`. Esquema nuevo `Aviso`.
