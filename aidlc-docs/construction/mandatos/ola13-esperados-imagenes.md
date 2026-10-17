# Mandato Ola 13b: Evaluación, esperados de las dos imágenes (rama `evaluacion`)

Objetivo: los esperados de reglas de `foto-04-andino-cambio-cuenta` (d_07) y `pdf-03-pixel-escaneado` (d_10) deben reflejar lo que dicen las reglas de lectura para imágenes. INDEPENDENCIA: NO leas `nucleo/` ni `evaluacion/salida/` ni `datos/ocultas/`; deriva solo del texto: `aidlc-docs/construction/lectura/functional-design/business-rules.md` (imágenes: doble lectura, "nunca PAGAR autónomo", formato imagen marcado para R1), `aidlc-docs/construction/nucleo/functional-design/business-rules.md` (R1), `datos/documentos/manifiesto.json` y `generar.py`. Sin pruebas nuevas.
Escribir solo: `datos/esperado-documentos.json` y `evaluacion/COBERTURA.md`.

Hacer: decide, solo desde el texto de las reglas, si R1 debe figurar entre las reglas que fallan para los documentos de formato imagen (y por qué); ajusta d_07 y d_10 (reglas y explicación; los veredictos solo si el texto lo exige) y anótalo en `COBERTURA.md`. Si el texto de las reglas es ambiguo, dilo y deja el esperado como estaba.

Listo cuando: `python3 verify.py --etapa evaluacion` verde. Incluye la fila para `tandas.md`. Máximo 80 palabras.
