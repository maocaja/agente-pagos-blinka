# Mandato Ola 19: Interfaz, notificaciones y salud (rama `interfaz`)

Objetivo: mostrar que el sistema está vivo. Código ligero: tope de diff 250 líneas (sin CSS compilado). Máximo 1 prueba nueva (tope de interfaz 22).

Leer: `CLAUDE.md` (4, 5, 5c), `aidlc-docs/construction/nucleo/functional-design/notificaciones.md`, `aidlc-docs/construction/interfaz/functional-design/adaptacion-biblioteca.md` y `recorridos.md`, `docs/design-system/`, `interfaz/dist/` y el simulador. Skill frontend-design con la guía de estilo.
Escribir solo: `interfaz/` y `interfaz/tests/`.

Formas del núcleo (se construye en paralelo; el simulador debe imitarlas): `GET /api/notificaciones` devuelve una lista de `{hora, evento, canal, destino, estado, texto}` con `estado` en {enviada, simulada, fallida}; `POST /api/notificaciones/prueba` devuelve esa misma entrada; `GET /api/salud` devuelve `{estado, version, mandato, lectura, libro, notificaciones: {telegram, correo}}` con cada canal en {configurado, simulado}.

Hacer:
1. Sección "Notificaciones" en la barra lateral compartida (con el número de avisos), y la página con la bandeja de salida: hora, evento, canal, destino enmascarado, estado con palabra e ícono y el texto; etiqueta clara "simulada, sin configurar" cuando el canal no tiene token; filtro por estado.
2. Botón "Enviar notificación de prueba" (analista o CFO), con confirmación dentro de la página y el resultado visible; deshabilitado mientras responde.
3. En la barra lateral, un indicador de salud ("Sistema operativo") tomado de `/api/salud`, con la etiqueta de qué canales están configurados o simulados.
4. Vocabulario aprobado; la bandeja nunca presenta un aviso simulado como enviado.
5. Verifica en Chrome contra la app real (puerto libre, copia temporal de `dist`; restaura lo que toques): cargar el set, ver los avisos generados (escaladas, frenadas), enviar la prueba y ver el estado "simulada". Si el núcleo aún no sirve las rutas en main, valida contra el simulador y dilo.

Listo cuando: `python3 verify.py --etapa interfaz` verde. Incluye la fila para `tandas.md`. `x-text`, `data-testid`, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
