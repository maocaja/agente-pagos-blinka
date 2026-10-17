# Mandato Ola 12: Interfaz, que se vea como un producto y no como un artefacto (rama `interfaz`)

Problema observado (capturas reales con la app real): (1) cada página crea una sesión nueva al cargar (`api.iniciar()` en `api.js`), así que lo cargado en la Bandeja desaparece al ir a Decisiones; (2) Decisiones abre vacía con "No hay decisiones con este veredicto"; (3) la cabecera mezcla demasiadas cosas sueltas (chip "rol simulado", Paquete de auditoría, Tema oscuro, selector de rol, Mandato v2); (4) la Bandeja es una lista de tarjetas con títulos pobres; (5) ninguna pantalla dice qué se ve ni por qué importa.
Objetivo: que la primera pantalla cuente la historia del producto en cinco segundos. Código ligero: tope de diff 700 líneas (sin CSS compilado). Máximo 3 pruebas nuevas (el presupuesto global casi se agotó).

Leer: `CLAUDE.md` (4, 5, 5c), `docs/design-system/` (tokens, componentes y guía: no se inventan colores ni componentes), `aidlc-docs/inception/demo-script.md` (las escenas que la interfaz debe sostener), `interfaz/dist/` y `interfaz/tests/`. Usa la skill frontend-design respetando la guía de estilo.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Hacer:
1. Sesión persistente: `api.iniciar()` reutiliza la sesión guardada en `sessionStorage` (con try/catch y respaldo en memoria); si el servidor la rechaza, crea otra. Nunca se pierde lo cargado al cambiar de página; "Demo" y "Reiniciar" sí la reinician.
2. Decisiones como pantalla principal: una banda de resumen arriba (cuántos documentos, cuántos pagados, frenados, escalados y pendientes de aprobación; y la frase "ningún pago salió de las reglas" solo si el marcador real lo respalda, si no, no la muestres); una lista con una fila por factura (proveedor, canal, monto, chip de veredicto con ícono y palabra, y la razón en una frase); al elegir una fila, el panel de detalle muestra la explicación, qué hacer y el recibo legible. Estado vacío diseñado con un botón "Cargar el set de ejemplo" que carga las muestras con progreso.
3. Cabecera limpia: navegación a la izquierda; a la derecha solo el rótulo de lectura (guardada o en vivo) y el botón Demo. Tema, paquete de auditoría y rol pasan a un menú "Opciones" (el selector de rol solo se muestra donde actúa: el panel del aprobador). Quita el chip "rol simulado".
4. Demo: el botón reinicia, carga el set y abre la primera escena; las flechas recorren las escenas del guion (`demo-script.md`).
5. Bandeja: títulos legibles (proveedor y canal), el canal como etiqueta, y al abrir una muestra se ve el original junto a lo leído y a la decisión.
6. Cada pantalla lleva bajo el título una frase que dice qué se ve y por qué importa (sin jerga).
7. Revisa tú mismo con Chrome (Claude in Chrome) a 1440 y a 375 px, con el set cargado: sin desborde, contraste y foco correctos. Si la ventana no se redimensiona, usa un iframe y dilo. No afirmes lo que no revisaste.

Listo cuando: `python3 verify.py --etapa interfaz` verde y el flujo Bandeja, Cargar el set, Decisiones, detalle con recibo funciona en la app real (`uvicorn nucleo.api.principal:app`), no solo en el simulador; di en el informe cómo lo comprobaste. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
