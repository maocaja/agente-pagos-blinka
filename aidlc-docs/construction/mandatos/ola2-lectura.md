# Mandato Ola 2: Lectura, asignación de proveedor (rama `lectura`, worktree `../wt-lectura`)

Objetivo: cada extracción lleva `proveedor_id` del registro maestro. Tope de diff 150 líneas (sin pruebas). Es corta: el núcleo la espera.

Leer: `CLAUDE.md` (5c), `aidlc-docs/construction/plans/lectura-code-generation-plan.md`, `datos/registro-maestro.json`, `lectura/` actual.
Escribir solo: `lectura/` y `lectura/tests/`.

Hacer:
1. Función única `asignar_proveedor(factura, registro)`: coincidencia por identificador fiscal normalizado, luego por nombre normalizado; sin coincidencia deja `proveedor_asignado` null (R3 decide, no esta función). No inventa.
2. Reescribir `lectura/extracciones/fac-01..18.json` con el `proveedor_asignado` resultante (script de una vez; no se editan montos ni textos). Validar contra el esquema.
3. Si `suma_lineas` falla en fac-10, 14, 15, 16 y 18, listar cuáles y por qué en el informe sin cambiar los datos.
4. 3 a 4 pruebas: coincidencia por id fiscal, por nombre, sin coincidencia, las 18 validan.

Listo cuando: `python3 verify.py --etapa lectura` verde. Recordatorio: sin red ni modelos en pruebas, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
