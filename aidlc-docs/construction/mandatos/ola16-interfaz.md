# Mandato Ola 16: Interfaz, los estados dicen la verdad y el Recorrido 2 se completa (rama `interfaz`)

Problemas vistos en la app real: el resumen cuenta como "Autorizadas para pago" las decisiones PAGAR, pero su detalle dice "Autorizada: No" porque el guardián no las ha tocado; no hay en la interfaz un paso para pedir la autorización, así que la orden pain.001 (409) nunca se puede descargar; los eventos del historial llegan en minúscula. Código ligero: tope de diff 250 líneas (sin CSS compilado). Máximo 1 prueba nueva.

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/construction/interfaz/functional-design/recorridos.md` (manda; Recorrido 2), `interfaz/dist/` y el simulador. Skill frontend-design con la guía de estilo.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Nueva ruta del núcleo (en paralelo; el simulador debe imitarla): `POST /api/decisiones/{id}/autorizar` devuelve el resultado del guardián (`autorizada`, `verificaciones` con su motivo) o 409 con el motivo; después el detalle trae `estado_orden: "autorizada"`.

Hacer:
1. El resumen dice "Con decisión de pagar" (no "Autorizadas para pago"). Los estados del detalle (Decisión, Autorizada, Orden emitida simulada) reflejan solo lo que el guardián hizo.
2. En el detalle de una decisión PAGAR: botón "Pedir autorización al guardián". Muestra el sello y las 6 verificaciones con su motivo; al autorizar, el estado cambia a Autorizada y se habilita "Descargar la orden de pago simulada (pain.001)". Errores (409) con su motivo.
3. Historial con los eventos en mayúscula inicial y en español ("Recibida · sistema", "Decidida · motor", "Rechazada · CFO"), sin cambiar los datos.
4. Recorrido 2 completo contra la app real (puerto libre, copia temporal de `dist`, restaura lo que toques): cargar el set curado, abrir una decisión PAGAR, pedir la autorización, descargar la orden y el paquete de auditoría, y EJECUTAR el script `python3 nucleo/auditoria/verificar_paquete.py <paquete>` sobre el paquete descargado; informa la salida exacta (debe decir que el paquete es válido). Si la ruta `/autorizar` del núcleo no existe aún en main, valida contra el simulador y dilo.
5. Una prueba: la página no usa "Autorizadas para pago" y el simulador responde a `/autorizar` con la forma del contrato.

Listo cuando: `python3 verify.py --etapa interfaz` verde y el Recorrido 2 descrito. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
