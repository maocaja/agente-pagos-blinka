# Mandato Ola 17: Núcleo, el titular usa la razón principal (rama `nucleo`)

Problema visto en la app real: en la foto de Estudio Andino la explicación y el siguiente paso empiezan por la cuenta cambiada (R4), pero el titular de la fila y del detalle (`motivo_corto`) sigue siendo "Lectura no confiable: lectura de imagen: confirmar contra el original" (R1). Código ligero: tope de diff 40 líneas. Sin pruebas nuevas (ajusta la existente si cambia un texto, o amplía una aserción de `test_ola15.py`).

Leer: `nucleo/dominio/explicacion.py` (tabla `PRIORIDAD`), donde se arma `motivo_corto`, `nucleo/tests/test_ola15.py`.
Escribir solo: `nucleo/` y `nucleo/tests/`.

Hacer: `motivo_corto` es la razón principal según la misma `PRIORIDAD` (una sola fuente, sin duplicar el orden); para la foto de Estudio Andino debe ser la de la cuenta (R4). Comprueba con la app real o un TestClient y ajusta una aserción existente.

Listo cuando: `python3 verify.py --etapa nucleo` verde. Incluye la fila para `tandas.md`. Comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 80 palabras.
