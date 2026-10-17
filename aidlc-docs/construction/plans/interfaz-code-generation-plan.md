# Plan de código: U3 Interfaz (Dev B, rama `interfaz`)

Fecha: 2026-10-17. Estado: PROPUESTO, sin aprobar. Diseño en `construction/interfaz/functional-design/` (incluye `design-system.md` y `frontend-components.md`). Es lo que ve el jurado en el video.

## Alcance y límites
- Escribe solo en `interfaz/` y `interfaz/tests/`. Consume la API de U1; mientras no exista, usa el servidor simulado con los ejemplos del contrato.
- Tailwind v4.3.3 compilado con su CLI (sin Vite) + Alpine.js 3.17.4 con los tokens y componentes de `docs/design-system/` (`tokens.css`, `componentes.css`). No se inventan colores ni componentes sin pasar por la guía.
- `x-text`, nunca `x-html` con datos de facturas; `data-testid` estable en cada elemento interactivo; el servidor es la fuente de verdad y no hay interfaz optimista.
- Presupuesto de pruebas: objetivo 12, máximo 20.

## Estructura
```
interfaz/
  src/          entrada.css, páginas HTML, componentes Alpine, cliente de la API
  dist/         CSS compilado y Alpine copiado (sin CDN en la demo)
  tests/
```

## Tandas

### T1. Pantalla de Decisiones con el recibo (sábado temprano)
Primer hito: la factura con su decisión, el motivo escrito y el recibo.
- [ ] 1.1 Compilación de Tailwind con `tokens.css` y `componentes.css`; tema claro por defecto y oscuro; Alpine copiado a `dist/`.
- [ ] 1.2 Cliente de la API (sesión, rol, `Idempotency-Key`) y store de sesión y rol; mapa de capacidades por rol.
- [ ] 1.3 Lista de decisiones con chip de veredicto (ícono y palabra), razón en una frase y filtros.
- [ ] 1.4 **Recibo legible** como documento papel: factura, regla y versión del mandato, decisión, hora, firma; alternar a vista técnica.
- Pruebas (≈ 3): escape de salida 3.

### T2. Escena 3 del video: recibo alterable y guardián (sábado)
- [ ] 2.1 Campo del recibo editable con la etiqueta "alterar para la demo"; la interfaz altera una **copia** del recibo y la envía a `POST /api/guardian/verificar`; Verificar usa `POST /api/recibos/{id}/verificar` (sin rutas nuevas).
- [ ] 2.2 Sello que se estampa o se parte según el resultado; lista de las 6 verificaciones con motivo y "no evaluada" en las posteriores.
- [ ] 2.3 Verificación de la firma: en el navegador con la clave pública si el algoritmo es compatible; si no, con el endpoint del servidor (SUPUESTO sin verificar).
- Pruebas (≈ 3): permisos por rol y capacidades 2; rechazo mostrado con motivo 1.

### T3. Pantalla de Reglas, la que pide el reto (sábado)
- [ ] 3.1 La empresa define sus reglas: umbral de aprobación, límites por pago y por periodo, monedas y tope acumulado por proveedor (los beneficiarios permitidos no están en el mandato: salen del registro de proveedores y se ven en una lista de solo lectura desde `/api/proveedores`); edición como mandato nuevo con versión (CFO propone, analista contrafirma).
- [ ] 3.2 Vista previa "qué cambia si se aprueba" y autonomía visible por proveedor.
- [ ] 3.3 Bandeja del aprobador: razón en una frase, un botón por rol, aprobar siempre reevalúa.
- Pruebas (≈ 4): aprobar con reevaluación 2; mandato con dos firmas 1; modo público de solo lectura 1.

### T4. Marcador y escena del ataque (sábado por la noche)
- [ ] 4.1 Marcador: número dominante, aciertos de reglas y de extremo a extremo por separado, autonomía, escalada innecesaria y costo; nota "lo que esta cifra no prueba".
- [ ] 4.2 Vista dividida del ataque: a la izquierda las estrategias del atacante, a la derecha el marcador y el motivo de cada bloqueo; mandato v1 contra v2 con el hueco en rojo si la arena lo encontró.
- [ ] 4.3 Pantalla de Pentest y arena con resultados de U4 y semilla fija editable.
- Pruebas (≈ 1): reinicio de la guía.

### T5. Bandeja simulada, guion y pulido (sábado de madrugada a domingo)
- [ ] 5.1 **Bandeja simulada** de entrada con la etiqueta visible: llegan correo, chat, PDF y foto de la factura; abrir un mensaje muestra el original junto a lo leído.
- [ ] 5.2 Modo guiado (botón Demo) que reinicia la sesión con confirmación y recorre las escenas del guion; flechas y Esc.
- [ ] 5.3 Revisión con Chrome DevTools MCP: consola sin errores, contraste, foco por teclado, ancho de teléfono.
- [ ] 5.4 Versión para la app pública: modo guardado, etiqueta "lectura guardada", sin llamadas a la API de Claude.
- Pruebas (≈ 1): modo guiado reinicia.

## Dependencias
La pantalla de aprobar (T3) usa el stub hasta que U1 entregue aprobar y reevaluar (T4); la del ataque (T4) usa el servidor simulado hasta las rutas de pentest y arena (U1 5.6). Pruebas de la interfaz: solo Python, sobre el mapa de capacidades por rol servido como JSON y sobre la función de escape; no hay pruebas de navegador en `verify`.

## Total y control
≈ 12 pruebas (objetivo 12, máximo 20): cubren lógica y escape; el aspecto se revisa a mano y con Chrome DevTools MCP. Cierre de tanda según `CLAUDE.md` sección 4.

## Riesgos y supuestos
- U2 y U3 las hace la misma persona: si U2 se atrasa, la interfaz trabaja con extracciones a mano y el marcador muestra solo los aciertos de reglas.
- La interfaz depende de U1 (API), U4 (resultados) y U2 (contador de costo): hasta entonces usa el servidor simulado.
- El cambio de la guía del 2026-10-17 (alineada con blinka.co) no usa su logotipo, su nombre como marca ni sus ilustraciones.
