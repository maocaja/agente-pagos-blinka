# Mandato Ola 11b: Núcleo, pruebas que matan los 4 mutantes sobrevivientes (rama `nucleo`)

Objetivo: cada mutante que sobrevivió debe ser atrapado por una prueba del núcleo. NO cambies código de producción salvo que una prueba destape un error real (en ese caso, repórtalo antes de arreglar). Máximo 4 pruebas nuevas (una por mutante), pequeñas y que cubran riesgo.

Leer: `CLAUDE.md` (4, 5c), `evaluacion/mutacion/mutantes.json` (M04, M07, M14, M15: archivo, texto original, texto mutado), `evaluacion/salida/mutacion.json`, `nucleo/dominio/motor.py`, `nucleo/dominio/reglas.py`, `nucleo/dominio/guardian.py`, `nucleo/tests/`.
Escribir solo: `nucleo/tests/` (y `nucleo/` solo si una prueba destapa un error real).

Hacer:
1. M04: una regla que lanza una excepción produce ESCALAR (o el veredicto cerrado que el diseño dice), nunca PAGAR ni cumple.
2. M07: R9 en el límite exacto del presupuesto (justo igual, y uno por encima).
3. M14: el guardián deniega un recibo FRENAR aunque traiga una aprobación válida.
4. M15: el guardián deniega un recibo vencido (`vence_en` pasado, con el reloj inyectado).
5. Comprueba que cada prueba FALLA con su mutante: aplica el mutante a mano en una copia temporal (o con `python3 evaluacion/mutacion.py --semilla 7` si ya lo corres sobre tu worktree) y que pasa sin él.

Listo cuando: `python3 verify.py --etapa nucleo` verde y `python3 evaluacion/mutacion.py --semilla 7` termina con código 0 (17 de 17 atrapados). Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 120 palabras.
