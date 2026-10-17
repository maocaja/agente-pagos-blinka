# Mandato Ola 10: Lectura y datos, el país de la cuenta en las trampas de instrucción (rama `lectura`)

Objetivo: chat-09 (Pixel), eml-08 (Logística Sur) y eml-10 (Pampa) dicen el país del banco como lo haría un documento real (Brasil, Chile y Argentina, según el registro maestro), para que R4 no falle por país vacío y la trampa dispare solo R8. Código ligero: tope de diff 40 líneas. Sin pruebas nuevas (lectura está en su tope).

Leer: `CLAUDE.md` (4, 5c), `datos/documentos/generar.py`, `datos/registro-maestro.json`, `lectura/extracciones_multicanal/` de esos tres documentos.
Escribir solo: `lectura/` y `datos/documentos/`.

Hacer:
1. En `generar.py`, añade a esos tres documentos el país del banco en una línea natural (por ejemplo "Banco ... , Brasil, cuenta terminada en 8830"), manteniendo la instrucción oculta tal cual. Regenera con semilla fija; deben cambiar solo esos tres archivos y el manifiesto si hace falta.
2. Actualiza las lecturas congeladas de esos tres documentos: `cuenta.pais` (BR, CL, AR), hash y cita del texto cambiado. No toques montos.
3. Informa si algún otro documento tiene `cuenta.pais` vacío.

Listo cuando: `python3 verify.py --etapa lectura` verde y `generar.py` reproduce igual dos veces. Incluye la fila para `tandas.md`. Comentarios cortos, no commit ni push. Máximo 100 palabras.
