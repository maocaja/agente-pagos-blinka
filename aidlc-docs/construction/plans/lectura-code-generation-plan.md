# Plan de código: U2 Lectura (Dev B, rama `lectura`)

Fecha: 2026-10-17. Estado: PROPUESTO, sin aprobar. Diseño en `construction/lectura/functional-design/` (incluye el alcance multicanal del 2026-10-17).

## Alcance y límites
- Escribe solo en `lectura/` y `lectura/tests/`, y los documentos simulados en `datos/documentos/` (los genera un subagente con mandato escrito). No toca `contrato/` ni `nucleo/`.
- Modelos del producto: Haiku 5.5, luego Sonnet 5.5; ids y precios se leen de la documentación oficial al implementar (CLAUDE.md sección 6). **Ninguna prueba llama a un modelo ni a la red**: se usan lecturas congeladas.
- Todo adaptador entrega la factura canónica validada contra `contrato/factura-canonica.schema.json`; si no valida, ESCALAR. El texto de un documento es un dato, nunca una orden.
- Presupuesto de pruebas: objetivo 30, máximo 40.

## Estructura
```
lectura/
  adaptadores/   texto, pdf, imagen, correo_eml, chat, xml (si sobra tiempo)
  extractor/     cliente de modelo (puerto), cascada, verificaciones, caché, modo guardado
  normalizador/  montos en unidades menores, proveedor y número normalizados
  tests/
datos/documentos/   facturas simuladas (las genera el subagente)
```

## Tandas

### T1. Extracciones a mano y adaptador de texto (sábado temprano, sin clave de API)
Desbloquea a U1, U3 y U4.
- [x] 1.1 Extracciones escritas a mano de las 18 facturas del set, validadas contra el esquema; guardadas como lecturas congeladas.
- [x] 1.2 Normalizador (C4): unidades menores como texto, formatos numéricos, monedas, identificador fiscal o nombre normalizado.
- [x] 1.3 Registro de adaptadores (C1) con `soporta` y `a_canonica`; tipo desconocido escala.
- Pruebas (≈ 6): normalizador y formatos 3; adaptadores y tipo desconocido 3.

### T2. Extractor con Haiku (sábado 08:00 a 12:00; real cuando llegue la clave)
- [ ] 2.1 Puerto del cliente de modelo con una implementación real y otra de lectura congelada; la clave se lee del entorno, nunca del repositorio.
- [ ] 2.2 Extracción con esquema fijo, confianza por campo y cita de evidencia.
- [ ] 2.3 Contador de tokens y tope duro por corrida (C3b); costo en `_microusd`.
- [ ] 2.4 Verificaciones: cita encontrada en el texto, totales cuadran, moneda y formato.
- Pruebas (≈ 11): cascada 3; verificaciones 4; contador y tope 2; falla de API simulada (timeout, rechazo, salida truncada) 2 (la de extremo a extremo hasta ESCALAR la prueba U4).

### T3. Segunda lectura, cascada y caché (sábado de tarde)
- [ ] 3.1 Segunda lectura por reglas (monto, moneda, número, totales; proveedor contra el registro maestro; español, inglés y portugués).
- [ ] 3.2 Cascada: Haiku, relectura con Sonnet si las verificaciones fallan, luego ESCALAR con el motivo.
- [ ] 3.3 Caché por hash del archivo y modo guardado para la app pública.
- Pruebas (≈ 9): segunda lectura 5; cascada y escalamiento 2; caché 2.

### T4. Canales del set multicanal (sábado por la noche)
Prioridad por el guion: la foto con cambio de cuenta, el `.eml` con adjunto y el chat.
- [ ] 4.1 Adaptador PDF con texto (extracción local) y PDF cifrado o fuera de límites que escala sin llamar a la API.
- [ ] 4.2 Adaptador de imagen y PDF escaneado: lectura con Claude como imagen y **doble lectura independiente** (Haiku y Sonnet); campos críticos deben coincidir; origen imagen marcado en la factura para que R1 no deje pasar a PAGAR.
- [ ] 4.3 Adaptador de correo `.eml` con la biblioteca estándar: encabezados, `Reply-To`, cuerpo y adjunto PDF.
- [ ] 4.4 Adaptador de chat (exportación estilo WhatsApp).
- [ ] 4.5 Adaptador XML (UBL) con parser sin modelo, **solo si sobra tiempo**.
- Pruebas (≈ 6): imagen doble lectura 2; correo 2; chat 1; PDF cifrado 1.

### T5. Lecturas reales y muestras guardadas (domingo temprano)
- [ ] 5.1 Corrida local con la API real sobre el set multicanal; la lectura se congela sin retoques y se registra el costo real por documento.
- [ ] 5.2 Las cuatro muestras nuevas de la app pública (proforma, orden de compra enviada como factura, factura en portugués, cuenta de cobro por chat), con el veredicto esperado registrado **antes** de leer, **fijado por U4 desde el texto de las reglas** (U2 no decide sus propios esperados).
- [ ] 5.3 Medir tokens reales de un PDF y de una imagen y comprobar que cabe en el tope de costo del mandato.
- Sin pruebas nuevas: es una corrida y una medición (se anotan en `tandas.md`).

## Generación del set simulado (subagente Sonnet, mandato aparte)
Documentos sin datos reales en `datos/documentos/`: PDFs con layouts distintos, un PDF escaneado, una foto con perspectiva y poca luz (incluye la factura con cambio de cuenta del video), un `.eml` con `Reply-To` distinto y adjunto, un chat estilo WhatsApp y, si sobra tiempo, un XML UBL. Cubren los casos trampa del reto: cobro duplicado, beneficiario nuevo, factura que no cuadra con lo acordado, monto sobre el límite y presupuesto insuficiente. Los esperados los fija U4 desde el texto de las reglas, no el generador.

## Total y control
≈ 32 pruebas (objetivo 30, máximo 40). Cierre de tanda según `CLAUDE.md` sección 4.

## Calendario de Dev B
Dev B hace U2 y U3 a la vez: orden propuesto U2 T1, U3 T1, U2 T2, U3 T2 y T3; **U2 se congela tras T2** (lectura guardada). T3 y T4 se hacen solo con lo que sobre; dentro de T4 la prioridad es la foto con cambio de cuenta y el `.eml`. Si hay que cortar, se corta primero el XML, luego el chat.

## Riesgos y supuestos
- Sin clave de API el sábado a las 12:00, T2 y T4 avanzan con la lectura congelada y el video usa lecturas guardadas.
- La lectura de imágenes puede fallar con fotos borrosas o rotadas (documentación de visión, leída 2026-10-17): se prueba con la API real antes de grabar.
- La política "imagen no llega a PAGAR sola" es un supuesto de seguridad que se puede aflojar con evidencia del set.
