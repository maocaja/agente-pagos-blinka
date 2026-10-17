# Mandato Ola 10: Evaluación, la corrida no trata el adjunto como documento aparte (rama `evaluacion`)

Objetivo: `evaluacion/corrida_documentos.py` no carga el adjunto del correo de DevNorte como documento independiente (es parte de eml-05; en una sesión limpia por documento no debe dar R2a). Código ligero: tope de diff 20 líneas. Sin pruebas nuevas (la etapa está en 63 de 65).

Leer: `evaluacion/corrida_documentos.py`, `datos/documentos/manifiesto.json` (el adjunto lleva "adjunto del eml-05" en `trampa`), `datos/esperado-documentos.json`.
Escribir solo: `evaluacion/`. No cambies `datos/esperado-documentos.json`.

Hacer: salta el adjunto en la corrida (y deja en la salida cuántos documentos se corrieron y cuántos se saltaron y por qué). Explica en el informe si `d_04` (eml-05) pasa a coincidir con su esperado y con qué reglas.

Listo cuando: `python3 verify.py --etapa evaluacion` verde. Incluye la fila para `tandas.md`. Comentarios cortos, no commit ni push. Máximo 80 palabras.
