# Mandato Ola 7: Evaluación, ajuste de esperados del set multicanal (rama `evaluacion`)

Objetivo: los esperados reflejan los documentos corregidos y la señal de remitente. INDEPENDENCIA: NO leas `nucleo/` ni `datos/ocultas/`; lee solo `contrato/`, `aidlc-docs/construction/nucleo/functional-design/business-rules.md`, `datos/registro-maestro.json`, `datos/documentos/` (manifiesto y `generar.py`), `datos/esperado-documentos.json` y `evaluacion/COBERTURA.md`. Máximo 1 prueba nueva.
Escribir solo: `evaluacion/`, `evaluacion/tests/` y `datos/esperado-documentos.json`.

Hacer:
1. pdf-01: ahora total USD 1.428 con IVA bajo el acuerdo del proveedor y cuenta registrada: ajusta el esperado (puede ser PAGAR; verifica R1 a R10 con el texto de las reglas).
2. pdf-02: ahora es una factura (antes RECIBO): ajusta tipo y veredicto.
3. eml-05: el `Reply-To` falso ahora activa `senales.remitente_inconsistente` y R1 escala; ajusta reglas que fallan y explicación; quita ese hueco de `COBERTURA.md`.
4. Instrucción oculta y autoridad falsa: nota en `COBERTURA.md` de que ahora existe un detector determinista en lectura (R8 ya no depende solo del modelo); el hueco restante es calibrar falsos positivos.
5. La prueba de cobertura existente debe seguir verde.

Listo cuando: `python3 verify.py --etapa evaluacion` verde (ojo: tope de pruebas de la etapa). Incluye la fila para `tandas.md`. Comentarios cortos, no commit ni push. Máximo 100 palabras.
