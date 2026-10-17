# Mandato Ola 5: Lectura, XML fiscal y CSV de lote (rama `lectura`)

Objetivo: dos canales deterministas más, sin modelo: XML de factura electrónica (UBL) y CSV de lote. Se agregan registrándolos. Código ligero: tope de diff 350 líneas (sin pruebas).

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/lectura/functional-design/`, `contrato/factura-canonica.schema.json`, `lectura/` actual (registro de adaptadores y los adaptadores de la Ola 4).
Escribir solo: `lectura/` y `lectura/tests/`, y ejemplos en `datos/documentos/xml/` y `datos/documentos/csv/` (3 XML y 2 CSV inventados, uno con una factura partida en varias filas del mismo proveedor bajo el umbral).

Hacer:
1. Adaptador XML UBL con `xml.etree` de la biblioteca estándar y defensa contra XXE y entidades (no resolver entidades externas); campos a la factura canónica; montos en unidades menores como texto; XML mal formado o con totales incoherentes escala.
2. Adaptador CSV de lote con el módulo `csv`: cada fila es una factura candidata; una fila inválida escala sola sin tumbar el lote.
3. Registrar ambos sin editar el registro. Sin modelo, sin red.
4. 6 a 8 pruebas: UBL válido, XML con entidad externa rechazado, totales incoherentes escalan, CSV con fila inválida, lote con facturas partidas produce las filas esperadas.

5. `Reply-To` distinto del remitente: el adaptador `.eml` llena `senales.remitente_inconsistente` con el motivo (campo aditivo ya añadido al esquema canónico); actualiza las lecturas congeladas del `.eml` afectado y una prueba.

Listo cuando: `python3 verify.py --etapa lectura` verde. Incluye la fila para `tandas.md`. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
