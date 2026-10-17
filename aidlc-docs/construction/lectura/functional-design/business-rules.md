# Reglas de negocio: U2 Lectura

Fecha: 2026-10-16. Fuente: 7 respuestas y una aclaración del diseño funcional, más `requirements.md` (RF1 a RF3, RF16, RF22) y el diseño del núcleo.

## Principios
1. La lectura **entrega datos y señales; no decide pagos**. Cualquier falla de lectura termina en ESCALAR con su motivo; ninguna puede producir PAGAR.
2. **Nada quemado:** modelos, límites de reintento, tope de gasto, umbrales de confianza y versión del esquema viven en configuración. La confianza mínima viene del mandato.
3. **Ningún camino paga sin acuerdo de dos lecturas independientes:** una del modelo y otra por reglas deterministas.
4. El tipo de documento **nunca relaja una regla**; solo la política por tipo del núcleo decide qué se hace con cada tipo.

## Extracción
El modelo **no convierte unidades**: devuelve los montos tal como están impresos (por ejemplo "1.200,50") y el código los convierte a unidades menores con reglas de separadores explícitas. El modelo devuelve, con salida estructurada, para cada factura: el **tipo de documento**, el proveedor, el número, las fechas, el monto, la moneda, la cuenta, las líneas, la confianza por campo y, para cada campo de dinero y para el tipo, una **cita de evidencia** (texto textual del documento). Sin `minimum` ni `maxLength` en el esquema (la salida estructurada no los admite).

## Verificaciones de la lectura
| Verificación | Cómo se hace | Si falla |
|---|---|---|
| Esquema | La respuesta valida contra el esquema | Sube a Sonnet |
| Campo de dinero presente | Monto, moneda, beneficiario y cuenta no vacíos | Sube a Sonnet |
| Suma de líneas | Las líneas suman el total | Sube a Sonnet |
| Cita de evidencia | La cita aparece en el texto local del documento (comparación normalizada; para los campos de dinero, el **número** coincide) | Sube a Sonnet |
| Tipo declarado | Si contradice palabras clave del texto | Sube a Sonnet |
| Confianza de dinero | Menor que el mínimo del mandato | **Puede provocar** la subida, **nunca impedirla** |
| Segunda lectura | Monto, moneda, número de factura y totales se extraen también con **reglas deterministas** y se comparan normalizados | Ver abajo |

**Segunda lectura**
- Si las dos lecturas difieren: **ESCALAR** con ambos valores y su origen.
- Si las reglas no encuentran el campo: cuenta como **"sin segunda lectura"**, no como coincidencia; también escala.
- En XML, las dos lecturas son el **parser estructurado** y una extracción por reglas sobre el texto del archivo; no se llama al modelo.

## Cascada de modelos
- Primera lectura con **Haiku 5.5**.
- Si alguna verificación marcada "Sube a Sonnet" falla, **una sola relectura con Sonnet 5.5 por factura**. Ese único reintento se comparte con el de truncado o JSON inválido.
- Si tras la relectura sigue fallando, ESCALAR con el motivo.

## Formatos numéricos, monedas e idiomas
- Los números se interpretan con reglas de separadores explícitas. Un número **ambiguo** ("1.200" puede ser 1200 o 1,2) no se adivina: cuenta como "sin segunda lectura" y escala.
- Una moneda sin código ($ suelto) es ambigua (puede ser USD, COP o MXN): sin segunda lectura.
- La segunda lectura por reglas soporta **español, inglés y portugués**. Otro idioma: sin segunda lectura.

## Segunda lectura del proveedor
Además de monto, moneda, número y totales, las reglas buscan en el texto el **identificador fiscal o el nombre normalizado de los proveedores del registro maestro**. Así un modelo que lea "DevNorte" en una factura de "Pixel Studio" no pasa solo porque el nombre aparezca en el documento. Si el proveedor que dice el modelo no coincide con el que encuentran las reglas, ESCALAR con ambos.

## Correcciones humanas y la segunda lectura
Una falla de lectura de R1 (lecturas que no coinciden, sin segunda lectura, cita no encontrada) **no se supera aprobando**: se resuelve con **Corregir**. La persona fija el valor viendo el original, esa corrección cuenta como la segunda lectura y la factura se reevalúa. Ver el cambio en el núcleo y la interfaz.

## Documentos sin texto verificable
- PDF cifrado o fuera de límites: **ESCALAR con motivo propio, sin llamar a la API**.
- **Imágenes, fotos y PDF escaneados (decisión del 2026-10-17):** se leen con Claude como imagen. No hay texto local, así que la cita no se puede verificar; la segunda lectura es una **segunda lectura independiente con otro modelo** (Haiku y luego Sonnet), y todos los campos críticos (proveedor, monto, moneda, cuenta, número, fecha) deben coincidir. Cualquier diferencia, confianza baja o campo ilegible: ESCALAR. Además, la factura de origen imagen **nunca llega a PAGAR sola**: si el motor diría PAGAR, la política por origen lo convierte en ESCALAR con el motivo "lectura de imagen: confirmar contra el original". FRENAR y ESCALAR sí son autónomos. Esto es política como dato en el mandato (SUPUESTO: se puede aflojar si el set mide un buen desempeño).

## Fallas de la API
| Falla | Qué ocurre |
|---|---|
| Conexión, 408, 409, 429, 5xx | El SDK reintenta 2 veces por defecto; `max_retries` se fija explícitamente en la configuración |
| Salida truncada o JSON inválido | Un único reintento con Sonnet por factura (compartido con la cascada) |
| Rechazo del modelo (`refusal`) | ESCALAR sin reintento |
| Otros 4xx (400, 401, 403, 404, 422) | ESCALAR sin reintento |
| Tope de gasto alcanzado | ESCALAR sin reintento |

Todo termina en ESCALAR con el motivo en el recibo.

## Asignación del proveedor
- Por **identificador fiscal** cuando exista; si no, por **nombre normalizado** (mayúsculas y sin símbolos).
- Si ambos conflictúan, o no hay coincidencia: **ESCALAR por R3** (proveedor no registrado).
- La coincidencia aproximada solo aparece como **pista** en el recibo y nunca decide.

## Caché
- Clave: hash del archivo, versión del esquema y modelo. Una factura ya leída no se vuelve a leer.
- En la app pública no se llama a la API: solo se sirven lecturas guardadas.

## Contador y tope de gasto
- Cuenta tokens y costo por corrida; al llegar al tope (`tope_gasto_corrida`, configurable), las lecturas siguientes escalan con ese motivo.
- Guarda el costo de cada lectura, que luego se muestra como "costo de lecturas guardadas".

## Adaptadores
- Cada formato es un adaptador con `soporta(documento)` y `a_canonica(documento)`; uno nuevo no toca el núcleo.
- Todo adaptador entrega la factura canónica **validada contra el esquema**; si no valida, ESCALAR.
- Un tipo desconocido o dudoso se escala como "tipo no soportado".

## Dos veredictos esperados por factura
El set debe llevar **dos esperados**: el de reglas (con una factura canónica correcta) y el de extremo a extremo (con las limitaciones de lectura: canales informales, imágenes, segunda lectura). El marcador no puede mezclarlos: la autonomía y los aciertos de extremo a extremo se calculan con el segundo. Lo implementa U4.

## Caché y umbral
El caché guarda la lectura final con sus verificaciones. La subida por confianza usa el umbral del mandato vigente al leer; R1 del núcleo recalcula con el umbral actual.

## Muestras nuevas de la app pública
Cuatro muestras: una **proforma**, una **orden de compra enviada como factura** (tipo no soportado), una **factura en portugués** y una **cuenta de cobro por chat** cuyas dos lecturas difieren de forma natural. La lectura se hace en local con la API real y se congela **sin retoques**; el veredicto esperado de cada muestra se registra **antes** de generar la lectura.

## Impacto en el núcleo
La regla R1 del núcleo debe incluir, como causas de ESCALAR: "las dos lecturas no coinciden", "sin segunda lectura" y "cita de evidencia no encontrada". Ya está reflejado en `nucleo/functional-design/business-rules.md`.

## Supuestos a confirmar
1. **Imágenes, fotos y PDF escaneados sí se leen (cambio del 2026-10-17):** con doble lectura de modelos y sin PAGAR autónomo; ver "Documentos sin texto verificable". Riesgo: un modelo puede equivocarse con imágenes borrosas, rotadas o pequeñas (documentación de visión, leída 2026-10-17), por eso se prueba el set con la API real el sábado.
2. **XML sin modelo:** las dos lecturas son parser y reglas; el modelo no interviene.
3. **Menor autonomía en canales informales:** los mensajes de chat y correos con datos poco estructurados escalarán más por "sin segunda lectura". Se mide en el marcador.
4. **Fallas de lectura no aprobables:** R1 por lectura se resuelve con Corregir y no con Aprobar. Es un cambio sobre lo aprobado del núcleo y de la interfaz, ya reflejado allí.
5. **Fallas por formato numérico y moneda ambigua** escalan sin adivinar. Aumenta las escaladas de facturas con "$" sin código.
6. **Costo de leer un PDF:** la estimación de 2.000 tokens por factura no está medida para PDFs; hay que medir un PDF real.
7. **El SDK reintenta 408, 409 y 429** (verificado en la documentación del SDK de Python el 2026-10-16), aunque son 4xx; se mantiene, y los demás 4xx no se reintentan.

## Canales simulados (decisión del 2026-10-17)
Todo el set es simulado, sin datos reales, y la app muestra una **bandeja simulada** con la etiqueta visible; nunca se conecta a un buzón.
| Canal | Cómo se simula | Lectura |
|---|---|---|
| PDF con texto | Layouts distintos: proveedor local e internacional, portugués, tablas, varias páginas | Texto local + Claude |
| PDF escaneado | El mismo PDF convertido a imagen, con ruido e inclinación leve | Claude como imagen, doble lectura |
| Foto de factura | PNG o JPEG con perspectiva y poca luz; incluye la factura con cambio de cuenta del video | Claude como imagen, doble lectura |
| Correo | `.eml` real: encabezados, `Reply-To` distinto y adjunto PDF; se leen con la biblioteca estándar de Python | Cuerpo y adjunto, doble lectura |
| Chat | Exportación con formato de WhatsApp | Texto + Claude |
| XML fiscal | Estructura real (UBL) con parser sin modelo | Solo si sobra tiempo |
La hoja de cálculo queda fuera. El texto de un correo o un chat es un dato, nunca una orden.
