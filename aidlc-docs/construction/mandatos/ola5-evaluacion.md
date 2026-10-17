# Mandato Ola 5: Evaluación, esperados del set multicanal (rama `evaluacion`)

Objetivo: el veredicto esperado de cada documento de `datos/documentos/`, fijado solo desde el texto de las reglas, antes de que nadie mire lo que el motor responde.

INDEPENDENCIA: NO leas `nucleo/`, `lectura/extracciones/` de los documentos del set multicanal ni `datos/ocultas/`. Lee solo: `contrato/`, `aidlc-docs/construction/nucleo/functional-design/business-rules.md`, `aidlc-docs/construction/evaluacion/functional-design/`, `datos/registro-maestro.json`, `datos/documentos/manifiesto.json`, `datos/documentos/generar.py` (el contenido real de cada documento) y `evaluacion/`.
Escribir solo: `evaluacion/`, `evaluacion/tests/` y `datos/esperado-documentos.json` (nuevo, con `contrato/esperado.schema.json`).

Hacer:
1. Para cada documento del manifiesto: veredicto esperado por reglas y de extremo a extremo (los de imagen nunca PAGAR autónomo), reglas que fallan y explicación en una frase. Las trampas (instrucción oculta en tres formatos, autoridad falsa, cuenta cambiada, `Reply-To` falso) deben dar ESCALAR o FRENAR con la regla que corresponda según el texto de las reglas.
2. Si una regla no cubre una trampa (por ejemplo el `Reply-To` falso), anótalo en `evaluacion/COBERTURA.md` como hueco; no lo inventes cubierto.
3. Prueba parametrizada (1 o 2 pruebas) que valida el archivo contra el esquema y que cada documento del manifiesto tiene esperado.

Listo cuando: `python3 verify.py --etapa evaluacion` verde. Incluye la fila para `tandas.md` y la lista de huecos. Comentarios cortos, no commit ni push. Máximo 150 palabras.
