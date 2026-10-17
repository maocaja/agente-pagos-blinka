# Mandato Ola 19: Núcleo, notificaciones, salud y registros de operación (rama `nucleo`)

Objetivo: construir `construction/nucleo/functional-design/notificaciones.md` (manda) y añadir observabilidad mínima. Código ligero: tope de diff 450 líneas (sin pruebas). Máximo 4 pruebas nuevas (se sube el tope de núcleo a 85).

Leer: `CLAUDE.md` (4, 5c), `aidlc-docs/construction/nucleo/functional-design/notificaciones.md`, `aidlc-docs/inception/architecture-target-vs-mvp.md` (3e a 3g), `aidlc-docs/inception/personas.md`, `nucleo/` (servicio, historial, rutas de acciones, libro), `contrato/README.md`. Para Telegram, la documentación oficial ya está resumida en la especificación; no uses otra fuente.
Escribir solo: `nucleo/`, `nucleo/tests/` y, como cambio ADITIVO, `contrato/` (subir a 1.1.0-rc6 y anotarlo en `contrato/README.md`). Los destinos y el enrutamiento van en un archivo de datos de `nucleo/` (sin direcciones ni tokens).

Hacer:
1. Puerto `Notificador` (1 método) en el dominio, sin importar HTTP ni SMTP; adaptadores en `nucleo/infra/`: Telegram (`urllib`, `https://api.telegram.org/bot<token>/sendMessage`, JSON con `chat_id` y `text`, SIN `parse_mode`, tiempo de espera de 5 s), correo (`smtplib` con STARTTLS) y bandeja de salida. Configuración solo por las variables de entorno de la especificación; sin variables, el canal queda "simulado" y se anota en la bandeja.
2. Servicio de notificaciones: enrutamiento evento a canales por tabla de datos; plantillas fijas con datos del registro maestro, importe y regla en lenguaje llano; sin texto libre del documento ni cuentas; sin saltos ni caracteres de control; corte a 500 caracteres. Envío en segundo plano con espaciado de 1,1 s por chat, resumen si se acumulan más de 5 en 10 s, y reintento acotado (respeta 429). Un fallo nunca cambia ni bloquea una decisión.
3. Enganchar los eventos de la especificación (escalada pendiente, denegación del guardián, frenada, autorizada, resuelta) en el servicio existente, sin duplicar lógica.
4. `GET /api/notificaciones`, `POST /api/notificaciones/prueba` (analista o CFO; una por 10 s) y `GET /api/salud` con la forma de la especificación (`libro` verifica que la base responde).
5. Registros de operación: `logging` estándar con salida JSON por línea y un identificador de correlación (sesión, decisión, recibo) en las decisiones, autorizaciones, denegaciones y notificaciones; nunca tokens, cuentas ni texto del documento.
6. Pruebas (máx. 4, sin red, con transporte falso): la plantilla no contiene texto del documento ni números de cuenta; sin variables todo queda "simulado" y la decisión no cambia; un canal que falla deja "fallida" y la decisión intacta; `/api/salud` responde y no expone secretos.

Listo cuando: `python3 verify.py --etapa nucleo` y `--etapa contrato` verdes. Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
