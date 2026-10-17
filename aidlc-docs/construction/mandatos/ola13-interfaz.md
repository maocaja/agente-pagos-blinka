# Mandato Ola 13: Interfaz, una cifra honesta y un set de demostración curado (rama `interfaz`)

Problemas vistos en la app real (capturas): (1) la banda verde dice "0 pagos indebidos en 18 ataques probados", pero 18 son las FACTURAS del set (`casos` del marcador), no ataques; la arena es otra cifra (3.200 variantes). Una cifra mal rotulada es un error grave. (2) "Cargar el set de ejemplo" carga las 33 muestras en una sola sesión y da 6 pagadas, 6 frenadas y 20 escaladas por topes acumulados y repeticiones entre muestras: el producto parece escalar casi todo. Código ligero: tope de diff 250 líneas. Máximo 1 prueba nueva o ajustada (queda poco presupuesto global).

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/inception/demo-script.md` (escenas y trampas), `datos/documentos/manifiesto.json`, `evaluacion/salida/documentos.json` y `evaluacion/COBERTURA.md` (qué da cada documento en sesión limpia), `contrato/api.openapi.yaml` (`/api/marcador`), `interfaz/dist/`.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Hacer:
1. Cifra honesta: la banda verde usa SOLO campos reales del marcador y los rotula como lo que son, por ejemplo "N facturas del set verificadas, M pagos indebidos" (verde solo si M es 0 y N mayor que 0). La arena se muestra en la página Ataque con su propio rótulo ("N variantes, M pagos indebidos") y su `no_prueba`. Nunca mezcles ambas cifras ni llames "ataques" a facturas.
2. Set de demostración curado: `interfaz/dist/demo-set.json` con 10 a 12 ids de muestra EN ORDEN, elegidos para que, cargadas en una sola sesión limpia, den el resultado que cuenta la historia: al menos 4 PAGAR (limpias), la cuenta cambiada (foto), tres trampas de instrucción (texto, chat, autoridad falsa), el `Reply-To` falso, un duplicado, un monto sobre el límite y un proveedor bloqueado o nuevo. Comprueba cargando en una sesión nueva contra la app real que cada una da el veredicto y la regla que se espera (usa `evaluacion/salida/documentos.json` y `esperado*.json` como referencia); si una acumulación cambia el resultado, reordena o cámbiala. Informa la tabla final: id, veredicto y regla.
3. "Cargar el set de ejemplo" y el botón Demo cargan SOLO ese set curado. En la Bandeja queda un botón secundario "Cargar todas las muestras" con la nota de que acumulan topes y repeticiones.
4. Verifica con Chrome en la app real (`uvicorn nucleo.api.principal:app --port 8770`, ciérrala al terminar) y describe lo que viste: la banda de resumen y al menos tres filas. No afirmes lo que no revisaste.

Listo cuando: `python3 verify.py --etapa interfaz` verde. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, tokens de la guía, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
