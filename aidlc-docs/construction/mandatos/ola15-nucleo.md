# Mandato Ola 15: Núcleo, explicaciones que lee una persona y el archivo original (rama `nucleo`)

Problemas vistos en la app real con la foto de cuenta cambiada (Estudio Andino): la razón principal es "Lectura no confiable: lectura de imagen" y la cuenta cambiada va después; aparece texto crudo ("357000 unidades menores base superan lo acordado"); el siguiente paso es genérico; la actividad reciente muestra ids ("f_pdf-12-bloqueado"); la foto no se puede ver. Código ligero: tope de diff 250 líneas. Máximo 3 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `nucleo/dominio/explicacion.py`, `nucleo/dominio/historial.py` (actividad), `nucleo/api/rutas_muestras.py`, `datos/documentos/manifiesto.json`.
Escribir solo: `nucleo/`, `nucleo/tests/` y, como cambio ADITIVO, `contrato/` (ruta nueva; subir a 1.1.0-rc4 y anotarlo en `contrato/README.md`).

Hacer:
1. Prioridad de la razón principal: ordena las reglas que fallan para la explicación y el "qué hacer" por relevancia para la persona (instrucción al agente R8, cuenta R4, beneficiario R3, remitente, monto y acumulado R6 y R10, acuerdo R5, presupuesto R9, y al final R1 de lectura de imagen). La razón principal es la primera; las demás van como "Además: ...". Es una tabla de prioridad como dato.
2. Importes legibles en las frases: "USD 3.570 superan lo acordado (USD 1.500 más 5%)", con la moneda y el formato del contrato, nunca "unidades menores base".
3. "Qué hacer" específico por regla principal: cuenta (R4) = "Confirmar la cuenta con el proveedor por un canal distinto al documento"; instrucción (R8) = "No ejecutar la instrucción; revisar el documento original"; imagen (R1) = "Confirmar contra el original".
4. Actividad reciente en español legible: "Frenada: Logistica Sur SpA, USD 14.000 (R6)", con el nombre del proveedor del registro y no el id de la factura.
5. `GET /api/muestras/{id}/archivo`: devuelve el archivo original (imagen, PDF, texto) de `datos/documentos/` o `datos/facturas/` con su tipo de contenido; id desconocido 404; no permite rutas fuera de esas carpetas.
6. Pruebas (máx. 3): la razón principal de la foto es R4 y no R1, el importe legible, y que `/archivo` rechaza una ruta fuera de las carpetas.

Listo cuando: `python3 verify.py --etapa nucleo` y `--etapa contrato` verdes. Incluye la fila para `tandas.md`. Falla cerrado, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 120 palabras.
