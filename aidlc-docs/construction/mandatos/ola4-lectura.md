# Mandato Ola 4: Lectura, adaptadores del set multicanal (rama `lectura`, worktree `../wt-lectura`)

Objetivo: PDF con texto, correo `.eml`, chat y foto o PDF escaneado entran por el registro de adaptadores y producen la factura canónica. Código ligero: tope de diff 600 líneas (sin pruebas ni JSON congelados).

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/plans/lectura-code-generation-plan.md` (T3 y T4), `aidlc-docs/construction/lectura/functional-design/`, `contrato/extraccion.schema.json` y `factura-canonica.schema.json`, `datos/documentos/manifiesto.json`, `datos/documentos/generar.py` (contenido real de cada documento) y `lectura/` actual (adaptadores, extractor, cliente).
Escribir solo: `lectura/` y `lectura/tests/`. Los documentos de `datos/documentos/` no se editan.

Hacer, un archivo por adaptador, registrados en el registro existente (no se edita el registro):
1. PDF con texto: extracción local del texto (usa una librería ya instalada o instala `pypdf` en el venv y anótalo en `lectura/LEEME.md`); PDF cifrado o ilegible escala sin llamar a la API. El texto oculto de `pdf-07` debe llegar al extractor (para que R8 lo vea).
2. `.eml` con la biblioteca estándar: encabezados, `Reply-To` distinto del remitente (se guarda como señal en el campo que permita el contrato; si no hay dónde, repórtalo sin inventar), cuerpo, pie y adjunto PDF.
3. Chat estilo WhatsApp: mensajes y remitente.
4. Imagen y PDF escaneado: lectura con el cliente de modelo como imagen y doble lectura independiente (Haiku y Sonnet); los campos críticos (monto, moneda, cuenta, número) deben coincidir o escala; el formato queda marcado como imagen para que R1 no deje pasar a PAGAR autónomo.
5. Lecturas congeladas de los 18 documentos del set, escritas a mano desde `generar.py` y marcadas `manual-congelada`, para que las pruebas no usen red ni modelos.
6. 10 a 14 pruebas: un caso por adaptador, `Reply-To`, instrucción oculta llega al texto, PDF cifrado escala, doble lectura que no coincide escala, tipo desconocido escala.

Listo cuando: `python3 verify.py --etapa lectura` verde. En el informe incluye la fila para `tandas.md`. Sin red en pruebas, sin secretos, falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
