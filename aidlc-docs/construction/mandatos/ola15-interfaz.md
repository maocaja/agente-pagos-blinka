# Mandato Ola 15: Interfaz, pulido de lo que se ve en el video (rama `interfaz`)

Problemas vistos en la app real: la foto original no se ve ("documento binario: ..."); "Autonomo bajo reglas" aparece en decisiones Escalar (contradictorio y sin tilde); el contexto y la actividad no se refrescan al cargar el set; la actividad muestra la hora como ISO; el enlace al paquete de auditoría no envía la sesión y puede dar 401. Código ligero: tope de diff 300 líneas (sin CSS compilado). Máximo 1 prueba nueva.

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/construction/interfaz/functional-design/recorridos.md`, `interfaz/dist/` y el simulador. Skill frontend-design con la guía de estilo.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Nueva ruta del núcleo (en paralelo; el simulador debe imitarla): `GET /api/muestras/{id}/archivo` devuelve el archivo original con su tipo de contenido. Pedirlo con la sesión no hace falta.

Hacer:
1. En el detalle, "Documento original": si la muestra es una imagen, mostrarla en una `<img>` con texto alternativo (carga desde `/api/muestras/{id}/archivo`); si es PDF, un enlace "Abrir el documento" y el texto leído; si es texto, el texto como hoy. Nada de `x-html` ni `innerHTML` con datos.
2. Etiqueta de autonomía: "Autónomo bajo reglas" solo para PAGAR; para ESCALAR "Requiere una persona"; para FRENAR "Frenada por las reglas". Con tilde.
3. Tras "Cargar el set" o una acción (aprobar, rechazar), refrescar el contexto (presupuesto y actividad) sin recargar la página.
4. La hora de la actividad en formato corto local (HH:MM).
5. Descargas (paquete de auditoría y orden simulada): con `fetch` enviando la sesión y descarga por blob, con mensaje de error legible si falla.
6. Revisa tildes en los textos visibles que encuentres sin acentos.
7. Verifica en Chrome contra la app real (puerto libre, copia temporal de `dist`, restaura lo que toques) el Recorrido 1 completo con el set curado: abrir la foto de Estudio Andino, ver la imagen, la razón principal y el siguiente paso, rechazar como CFO con nota, ver el historial y la actividad; y la descarga del paquete. Describe lo que viste.

Listo cuando: `python3 verify.py --etapa interfaz` verde. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
