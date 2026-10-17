# Reglas de negocio: U1 Núcleo

Fecha: 2026-10-16. Fuente: 13 respuestas del diseño funcional más los requisitos RF4 a RF10, RF15 a RF25.

## Principios
1. **Nada está quemado en el código.** Todo valor (límites, tolerancias, ventanas, tasas, vigencias, niveles de confianza) vive en el **mandato** de la empresa, que es un dato versionado. Los perfiles (conservador, balanceado, ágil) solo siembran sus valores iniciales.
2. Se evalúan **todas** las reglas, sin cortar en la primera que falla, para que el recibo muestre cada falla.
3. Precedencia del veredicto: **FRENAR, luego ESCALAR, luego PAGAR o REGISTRAR**. **REGISTRAR** es el cuarto veredicto: solo para una nota de crédito que pasa todas las reglas, y **nunca lleva orden de pago**.
4. **Falla cerrado:** un error, una duda, un tipo o un dato desconocido producen ESCALAR (o FRENAR si la regla lo dice). Nunca PAGAR.
5. Dinero en enteros de unidades menores. Una moneda sin tasa en el mandato falla cerrado. **La conversión a la moneda base se redondea al alza** cuando se compara contra un tope o un umbral, para que un monto no pase por redondeo.
6. Las reglas son funciones registradas con su configuración. Una regla nueva es una función y una entrada de configuración.

## Reglas
| Id | Regla | Falla cuando | Acción | Parámetros del mandato |
|---|---|---|---|---|
| R1 | Lectura confiable | El documento es una imagen o un PDF escaneado (formato imagen: la cita no se puede verificar y nunca se paga sin una persona); un campo de dinero (monto, moneda, beneficiario, cuenta) tiene confianza menor que el mínimo de dinero; otro campo, menor que el mínimo general; falta un campo obligatorio; la suma de líneas no cuadra con el total; las dos lecturas no coinciden; no hay segunda lectura; la cita de evidencia no se encuentra en el documento | ESCALAR | `conf_min_dinero`, `conf_min_general`, `tolerancia_lineas` |
| R2a | Duplicado exacto | Mismo proveedor y mismo número normalizado (mayúsculas, sin símbolos, **sin quitar ceros**), o mismo hash de archivo | FRENAR | |
| R2b | Duplicado difuso | Mismo proveedor, número distinto, monto dentro de la tolerancia y dentro de la ventana | ESCALAR | `dup_tolerancia_monto_pct`, `dup_ventana_dias` |
| R3 | Beneficiario permitido | El proveedor no está en el registro maestro: ESCALAR. Está bloqueado: FRENAR | ESCALAR o FRENAR | estado del proveedor en el registro |
| R4 | Cuenta registrada | La factura trae una cuenta distinta de la registrada. Si no trae cuenta, no falla: el pago va a la registrada | ESCALAR | |
| R5 | Coincide con lo acordado | No hay acuerdo registrado, o el monto supera el acuerdo más la tolerancia | ESCALAR | `tolerancia_acuerdo_pct` |
| R6 | Monto | Supera el tope por pago: FRENAR. Supera el umbral de aprobación: ESCALAR | FRENAR o ESCALAR | `tope_pago`, `umbral_aprobacion`, tasas |
| R7 | Moneda | Moneda no permitida o sin tasa | FRENAR | `monedas_permitidas`, tasas y su fecha |
| R8 | Texto dirigido al agente | La señal de instrucciones dentro del documento no queda descartada | ESCALAR | `umbral_senal_texto` |
| R9 | Presupuesto | Se evalúa **al final y solo si ninguna otra regla falló**; el monto supera lo que queda del periodo | ESCALAR | `presupuesto_periodo` |
| R10 | Tope acumulado por proveedor | Lo pagado y reservado al proveedor en el periodo más esta factura supera el tope | ESCALAR | `tope_acumulado_proveedor`, activo o inactivo según la versión |

**Definiciones**
- **Acuerdo** = monto máximo por factura, por proveedor. Sin acuerdo, ESCALAR.
- **Periodo** = mes calendario; su longitud es un parámetro (`periodo`). Aplica a R9 y R10.
- **Duplicado difuso** compara contra las facturas recibidas del proveedor en la ventana que no fueron rechazadas (pagadas, pendientes o aprobadas).
- **Reserva:** un PAGAR reserva su monto en la misma transacción que emite el recibo; si el guardián deniega el pago, se libera con un movimiento compensatorio.

## Política por tipo de documento
| Tipo | Resultado |
|---|---|
| Factura, cuenta de cobro | Todas las reglas |
| Nota de crédito | Se evalúan las reglas aplicables; si pasan todas, veredicto **REGISTRAR**: crédito a favor del proveedor, sin orden de pago. Si alguna falla, ESCALAR o FRENAR como cualquier documento |
| Estado de cuenta | FRENAR con el motivo "no es una factura"; no se puede aprobar |
| Proforma o anticipo | ESCALAR |
| Tipo desconocido | ESCALAR con el motivo "tipo no soportado" |

## Mandatos precargados
- **v1:** perfil Balanceado, **sin** el tope acumulado. Es el punto de partida del pentest.
- **v2:** perfil Balanceado **con** el tope acumulado. Es con el que corre el set de facturas.
- Valores iniciales del perfil Balanceado: umbral USD 3.000, tolerancia del acuerdo 5%, tope por pago USD 10.000, confianza 0,80 general y 0,90 en dinero, duplicado difuso ±2% en 30 días, vigencia 24 horas. El presupuesto del periodo y las tasas salen del set de datos.
- Cambiar el mandato: el CFO propone, el analista contrafirma y nace una versión nueva.

## Aprobación
- Dos roles: **analista** (prepara, carga, corrige) y **CFO** (aprueba). Quien carga la factura no la aprueba.
- Acciones sobre una escalada: **aprobar, corregir, rechazar, escalar a otro rol**. El rechazo exige un motivo.
- Una **frenada no se aprueba** ni se paga.
- **Qué cubre una aprobación:** las fallas de tipo ESCALAR que la persona vio al aprobar; quedan listadas en la aprobación. No cubre una falla FRENAR ni una falla nueva.
- **Aprobar reevalúa:** genera una decisión nueva y un recibo nuevo, con la lista de fallas aprobadas y la reserva de presupuesto. Si aparece una falla FRENAR, una falla ESCALAR distinta de las aprobadas, o el presupuesto ya no alcanza, vuelve a ESCALAR con el motivo.
- **R9 (presupuesto) no se supera aprobando.** Se resuelve con un mandato nuevo que suba el presupuesto (lo propone el CFO y lo contrafirma el analista), rechazando, o esperando al periodo siguiente.
- **Las fallas de lectura de R1** (lecturas que no coinciden, sin segunda lectura, cita no encontrada) **tampoco se superan aprobando.** Se resuelven con **Corregir**: la persona fija el valor viendo el original, esa corrección cuenta como segunda lectura y la factura se reevalúa.
- **Corregir** un campo reevalúa la factura completa; nunca salta las reglas.
- La aprobación y el recibo **vencen a las 24 horas** (`vigencia_aprobacion`, `vigencia_recibo`).
- La **cuenta nueva aprobada no cambia la cuenta registrada.** La aprobación vale solo para esa factura; el registro maestro cambia por un trámite aparte con firma.

## Autonomía por proveedor
- **Autónomo bajo reglas:** si cumple todas, se paga sin persona.
- **Sombra:** el agente decide y deja el registro, pero la orden la autoriza una persona.
- Por defecto, un proveedor conocido es autónomo y uno nuevo arranca en sombra hasta que el CFO lo promueva.
- En sombra, el recibo lleva `modo: sombra` y el guardián exige una aprobación humana aunque el veredicto sea PAGAR.

## Catálogo de parámetros del mandato
| Parámetro | Valor inicial (perfil Balanceado) | Lo usa |
|---|---|---|
| `tope_pago` | USD 10.000 | R6 |
| `umbral_aprobacion` | USD 3.000 | R6 |
| `tolerancia_acuerdo_pct` | 5 | R5 |
| `conf_min_dinero` | 0,90 | R1 |
| `conf_min_general` | 0,80 | R1 |
| `tolerancia_lineas` | 0 (exacta) | R1 |
| `dup_tolerancia_monto_pct` | 2 | R2b |
| `dup_ventana_dias` | 30 | R2b |
| `periodo` | mes calendario | R9, R10 |
| `presupuesto_periodo` | del set de datos | R9 |
| `tope_acumulado_proveedor` | USD 3.000, activo solo en v2 | R10 |
| `monedas_permitidas` | USD, COP, BRL, MXN | R7 |
| `tasas_cambio` y su fecha | del set de datos (la maqueta usa 1 USD = 4000 COP, 5 BRL, 17 MXN) | R6, R7, R9, R10 |
| `umbral_senal_texto` | por calibrar con el set | R8 |
| `vigencia_recibo_h`, `vigencia_aprobacion_h` | 24 | guardián, aprobación |
| `dias_proveedor_nuevo` | sin decidir | autonomía |
| `nivel_autonomia_defecto` | conocido: autónomo; nuevo: sombra | autonomía |

## Supuestos a confirmar
1. **"Proveedor nuevo"** (sombra) se entiende como un proveedor que ya está en el registro maestro pero tiene menos de `dias_proveedor_nuevo` días (valor por defecto sin decidir). Un proveedor que no está en el registro es R3.
2. **Nota de crédito (resuelto):** cuarto veredicto **REGISTRAR**, decidido al escribir el contrato. El crédito se registra y se muestra en la interfaz; en la demo no altera el presupuesto ni el tope acumulado.
3. Proveedor **bloqueado** como FRENAR en R3 sale del catálogo de parámetros, no de una pregunta tuya.
4. El valor de `umbral_senal_texto` se calibra con el set de facturas.
5. **R9 no se supera aprobando** (deriva de tu respuesta 8, que pedía reevaluar). Una factura escalada por presupuesto insuficiente solo avanza con un mandato nuevo, o se rechaza.
6. **Firma de la aprobación:** en la demo el servidor firma en nombre del usuario autenticado; que cada usuario tenga su par de claves en el navegador queda como mejora.
7. **Una escalada aprobada** produce un recibo nuevo (con las fallas aprobadas y la reserva), y la aprobación se liga a ese recibo.
8. **Redondeo al alza** en la conversión de moneda al comparar contra topes y umbrales (nuevo, lo exige el pentest y el verificador independiente; el mandato lleva el modo de redondeo como parámetro).
