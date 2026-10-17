# Mandato Ola 16: Núcleo, autorizar por el guardián y textos coherentes (rama `nucleo`)

Problemas vistos en la app real: una decisión PAGAR aparece en la actividad como "Autorizada" cuando el guardián no la ha tocado; el nombre del proveedor sale con mayúsculas distintas (ESTUDIO ANDINO SAS contra Estudio Andino SAS); no hay forma simple de que la interfaz pida la autorización de una decisión PAGAR (la orden pain.001 da 409 hasta que el guardián autoriza); varios textos de reglas no llevan tildes ("aprobacion", "esta en"). Código ligero: tope de diff 200 líneas. Máximo 2 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/interfaz/functional-design/recorridos.md` (vocabulario de estados), `nucleo/dominio/servicio.py` (`verificar_orden`, `_cerrar_orden`), `nucleo/dominio/historial.py`, `nucleo/api/rutas_acciones.py`, textos en `nucleo/dominio/reglas.py`, `reglas_simples.py`, `explicacion.py`.
Escribir solo: `nucleo/`, `nucleo/tests/` y, como cambio ADITIVO, `contrato/` (ruta nueva; subir a 1.1.0-rc5 y anotarlo en `contrato/README.md`).

Hacer:
1. `POST /api/decisiones/{id}/autorizar` (rol analista o CFO, con `Idempotency-Key`): toma la decisión PAGAR (o escalada ya aprobada) con su recibo, arma la orden con los datos del propio recibo y llama al mismo `verificar_orden` del guardián. Devuelve el resultado del guardián (las 6 verificaciones). Si la decisión no es autorizable (FRENAR, ESCALAR sin aprobación, ya autorizada) responde 409 con el motivo. Tras autorizar, `estado_orden` pasa a "autorizada". Sin duplicar la lógica del guardián.
2. Actividad e historial: la palabra "Autorizada" solo cuando el guardián autorizó; una decisión PAGAR sin autorizar se anota "Decisión de pagar: ...". Añade el evento "autorizada" al historial cuando ocurre.
3. El nombre del proveedor en actividad y explicaciones sale siempre del registro maestro (una sola forma), nunca del texto leído.
4. Tildes y ortografía de los textos de reglas y explicaciones visibles al usuario (aprobación, está, umbral, etc.), sin cambiar su lógica.
5. Pruebas (máx. 2): autorizar una PAGAR deja `estado_orden` en "autorizada" y habilita el pain.001, y una FRENAR da 409; la actividad de una PAGAR sin autorizar no dice "Autorizada".

Listo cuando: `python3 verify.py --etapa nucleo` y `--etapa contrato` verdes. Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 120 palabras.
