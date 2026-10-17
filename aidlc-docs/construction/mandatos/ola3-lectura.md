# Mandato Ola 3: Lectura, IVA y extractor (rama `lectura`, worktree `../wt-lectura`)

Objetivo: las líneas de cada factura suman su total, y existe el extractor con prompt versionado, cliente de modelo real y congelado, y tope de gasto. Código ligero: tope de diff 450 líneas (sin pruebas).

Leer: `CLAUDE.md` (5c), `aidlc-docs/construction/plans/lectura-code-generation-plan.md` (T2), `aidlc-docs/construction/lectura/functional-design/`, `contrato/extraccion.schema.json`, `contrato/factura-canonica.schema.json`, `datos/facturas/`, `lectura/` actual.
Escribir solo: `lectura/` y `lectura/tests/`.

Hacer:
1. IVA: en las extracciones donde el documento trae impuestos aparte (fac-10, 14, 15, 16; revisar 18) añadir una línea "IVA" o "Impuestos" con su monto para que `suma_lineas_menor` iguale `total_menor`, leyendo el texto de `datos/facturas/`. No cambiar montos del documento. Si una no cuadra por otra razón (p. ej. fac-18 o fac-10), no forzarla: listar el motivo en el informe.
2. Puerto del cliente de modelo (máx. 5 métodos) con dos implementaciones: real (Anthropic; clave solo del entorno; ids y precios de la documentación oficial leída en vivo, con URL y fecha en el informe) y de lectura congelada (lee `lectura/extracciones/`). Ninguna prueba usa red.
3. Prompt del extractor en `lectura/prompts/extractor.v1.md`; cada extracción guarda `prompt_version`, `prompt_hash` (sha256), modelo y `costo_microusd`. El prompt no contiene reglas de negocio y trata el texto del documento como dato.
4. Contador de tokens y tope duro por corrida (valor del mandato, no quemado); superarlo o una falla del cliente (timeout, rechazo, salida truncada) termina en ESCALAR con motivo.
5. Verificaciones del extractor: la cita existe en el texto, los totales cuadran, la moneda es válida.
6. 8 a 12 pruebas: IVA cuadra en las facturas corregidas, hash del prompt guardado, tope, cada falla del cliente, cita ausente.

Listo cuando: `python3 verify.py --etapa lectura` verde. Recordatorio: falla cerrado, dinero en enteros como texto, sin secretos, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
