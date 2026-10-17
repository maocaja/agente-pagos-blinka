# Mandato Ola 11: Evaluación, mutación del motor (rama `evaluacion`)

Objetivo: demostrar que las pruebas atrapan un motor roto a propósito. Eres un agente DISTINTO del que escribió el verificador y del que escribió el pentest; puedes leer `nucleo/`. Código ligero: tope de diff 200 líneas. Máximo 1 prueba nueva.

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/plans/evaluacion-code-generation-plan.md` (T5), `aidlc-docs/construction/estrategia-de-verificacion.md`, `verify.py` (`etapa_mutacion`: llama a `evaluacion/mutacion.py --semilla N` con un máximo de segundos en `verify.budget.json`), `nucleo/` y `nucleo/tests/`.
Escribir solo: `evaluacion/mutacion.py`, `evaluacion/mutacion/` y `evaluacion/salida/mutacion.json`.

Hacer:
1. `evaluacion/mutacion.py --semilla N`: copia `nucleo/` a una carpeta temporal (NUNCA modifica el original), aplica un mutante por vez con reemplazo de texto y corre las pruebas de `nucleo/tests/` contra la copia; un mutante está atrapado si alguna prueba falla. Sale con código 0 solo si todos quedan atrapados; si sobrevive alguno, código 1 y lo lista.
2. Cinco mutantes de más impacto, escritos como datos (archivo, texto original, texto mutado, qué rompe): por ejemplo precedencia de veredictos invertida, falla cerrado (tipo desconocido o regla ausente da PAGAR), R10 con comparación al límite desplazada, el guardián que no revisa el nonce usado, y una regla que devuelve cumple sin evaluar. Elige los más relevantes tras leer el motor.
3. Sin modelo ni red; debe terminar dentro del límite de segundos del presupuesto.
4. Escribe `evaluacion/salida/mutacion.json` con cada mutante, si fue atrapado y por qué prueba. Si un mutante sobrevive NO lo arregles: repórtalo (qué prueba faltó) para decidir.

Listo cuando: `python3 evaluacion/mutacion.py --semilla 7` termina y `python3 verify.py --etapa evaluacion` sigue verde. Incluye la fila para `tandas.md` y los mutantes sobrevivientes si los hay. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
