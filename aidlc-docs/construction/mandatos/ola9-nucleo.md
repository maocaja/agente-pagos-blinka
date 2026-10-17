# Mandato Ola 9: Núcleo, la lista de muestras sin adjuntos y con títulos (rama `nucleo`)

Objetivo: cargar el set completo no produce un falso duplicado, y la bandeja muestra títulos legibles. Código ligero: tope de diff 60 líneas. Máximo 1 prueba nueva.

Leer: `CLAUDE.md` (4, 5c), `nucleo/api/rutas_muestras.py`, `datos/documentos/manifiesto.json`.
Escribir solo: `nucleo/` y `nucleo/tests/`.

Hacer:
1. Un adjunto de un correo (el adjunto PDF del `.eml` de DevNorte) es parte de ese correo, no una muestra aparte: sácalo de la lista de `/api/muestras` (se carga como parte del correo). Si el manifiesto no distingue adjuntos, usa su campo de canal o nota; si no hay forma fiable, repórtalo en vez de adivinar.
2. Título legible de cada muestra desde el manifiesto (nota o proveedor y canal) en vez del id con guiones; para las 18 facturas, el nombre del archivo en `datos/facturas/` sin prefijo.
3. 1 prueba: la lista no incluye el adjunto y cargar todas las muestras en una sola sesión no da FRENAR por duplicado entre el correo y su adjunto.

Listo cuando: `python3 verify.py --etapa nucleo` verde. Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 100 palabras.
