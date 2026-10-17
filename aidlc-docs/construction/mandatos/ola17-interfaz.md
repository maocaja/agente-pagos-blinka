# Mandato Ola 17: Interfaz, detalle compacto (rama `interfaz`)

Problema visto en la app real: el detalle de una decisión mide cuatro pantallas (el correo original completo, luego el historial, luego el recibo y al final el guardián); el recibo y el botón "Pedir autorización al guardián" quedan fuera de la vista. En un video de tres minutos no se alcanzan. Código ligero: tope de diff 250 líneas (sin CSS compilado). SIN pruebas nuevas (la etapa está en su tope); ajusta las existentes si cambian textos.

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/construction/interfaz/functional-design/recorridos.md`, `docs/design-system/`, `interfaz/dist/index.html`, `app.js`. Skill frontend-design con la guía de estilo.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Hacer:
1. El detalle se organiza en pestañas accesibles (teclado, `role=tablist`): **Resumen** (razón, siguiente paso, los tres estados y los botones de acción: aprobar o rechazar para el CFO, "Pedir autorización al guardián" y las descargas), **Documento** (original junto a lo leído y las reglas que difieren), **Recibo** (recibo, Verificar firma, vista técnica, alterar para la demo, guardián con las 6 verificaciones) e **Historial**. La pestaña por defecto es Resumen; al abrir desde una escena del modo Demo se abre la pestaña que la escena necesita (escena 1: Documento; escena 3: Recibo).
2. El texto original (correo o chat) tiene altura máxima (unas 16 líneas) con scroll interno; la imagen se limita a una altura razonable.
3. Mantén los `data-testid` existentes y `x-text` siempre.
4. Verifica en Chrome contra la app real (puerto libre, copia temporal de `dist`, restaura lo que toques): carga el set curado, abre una decisión PAGAR y comprueba que sin hacer scroll se ve el estado y el botón de autorización; pídelo, comprueba el sello, y descarga la orden. Abre la foto de Estudio Andino en la pestaña Documento. Describe lo que viste.

Listo cuando: `python3 verify.py --etapa interfaz` verde. Incluye la fila para `tandas.md`. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
