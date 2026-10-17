# Mandato Ola 8: Núcleo, las muestras que usa la bandeja (rama `nucleo`)

Objetivo: la app real sirve `/api/muestras` y `/api/muestras/{id}/cargar`, hoy solo existentes en el simulador de la interfaz. Código ligero: tope de diff 200 líneas. Máximo 4 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `contrato/api.openapi.yaml` (`/api/muestras`, `/api/muestras/{id}/cargar`, campo `original`), `datos/documentos/manifiesto.json`, `datos/facturas/`, `lectura/extracciones/` y `lectura/extracciones_multicanal/` (se leen como datos; no importes código de `lectura/`), `interfaz/servidor_simulado.py` y `interfaz/rutas_ola4.py` (lo que la bandeja espera), `nucleo/api/` actual.
Escribir solo: `nucleo/` y `nucleo/tests/`.

Hacer:
1. `GET /api/muestras`: lista de las 18 facturas del set y los 16 documentos multicanal (id, título, tipo/canal, `lectura_guardada: true`, `original`: texto del documento si es texto, `.eml` o chat; para PDF o imagen, una nota "documento binario: <archivo>" sin inventar contenido).
2. `POST /api/muestras/{id}/cargar`: toma la lectura congelada de esa muestra (que ya es una factura canónica con su proveedor asignado) y la hace pasar por el mismo flujo que `POST /api/facturas`; devuelve la decisión. Id desconocido: 404. Sin `Idempotency-Key` nuevo requerido.
3. Que la app arranque con sesión limpia y sin muestras cargadas (se cargan por llamada).
4. Hasta 4 pruebas: lista incluye las 34 muestras, cargar una devuelve decisión con explicación, la trampa de instrucción sale ESCALAR por R8, id desconocido 404.

Listo cuando: `python3 verify.py --etapa nucleo` verde. Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 120 palabras.
