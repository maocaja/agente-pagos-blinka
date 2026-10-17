# Mandato Ola 8: Evaluación, corrida del set multicanal de extremo a extremo (rama `evaluacion`)

Objetivo: comprobar que los 16 documentos, pasando por la lectura congelada y el motor, dan lo que fijan los esperados. Es una corrida de integración (puedes importar la app del núcleo solo para arrancarla, como `evaluacion/corrida/`). No cambies los esperados: toda diferencia se reporta. Código ligero: tope de diff 150 líneas. Máximo 3 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `evaluacion/corrida/`, `datos/esperado-documentos.json`, `datos/documentos/manifiesto.json`, `lectura/extracciones_multicanal/` (lecturas congeladas) y `evaluacion/COBERTURA.md`.
Escribir solo: `evaluacion/` y `evaluacion/tests/`.

Hacer:
1. `python -m evaluacion.corrida_documentos`: para cada documento, sesión limpia con mandato v2, carga la lectura congelada por la API del núcleo, compara veredicto y reglas que fallan con el esperado (de reglas y de extremo a extremo) y escribe `evaluacion/salida/documentos.json` con el conteo de coincidencias y la lista de discrepancias con su motivo.
2. Informa en cifras: cuántos coinciden, cuáles no y por qué (¿esperado equivocado, motor equivocado o dato del documento?). No decidas cuál tiene razón: lista la evidencia.
3. Hasta 3 pruebas: el script corre sobre un subconjunto pequeño sin red, la salida valida contra el esquema, ningún documento de imagen o trampa da PAGAR.

Listo cuando: `python3 verify.py --etapa evaluacion` verde. Incluye la fila para `tandas.md` y las discrepancias. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
