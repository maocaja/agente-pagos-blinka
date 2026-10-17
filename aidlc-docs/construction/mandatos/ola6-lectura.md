# Mandato Ola 6: Lectura, selección por clave y generador (rama `lectura`)

Objetivo: configurar la clave basta para pasar de lectura guardada a lectura en vivo; y los documentos "limpios" del set pagan y los de trampa escalan por la razón correcta. Código ligero: tope de diff 250 líneas (sin pruebas). Máximo 5 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `lectura/extractor/` (cliente), `datos/documentos/generar.py` y `manifiesto.json`, `datos/registro-maestro.json`, `evaluacion/COBERTURA.md` (hallazgos sobre pdf-01 y pdf-02).
Escribir solo: `lectura/`, `lectura/tests/` y `datos/documentos/` (generador, manifiesto y archivos).

Hacer:
1. `lectura/extractor/seleccion.py`: una función `crear_cliente(entorno)` que devuelve el cliente real si `ANTHROPIC_API_KEY` está definida y el congelado si no, y un `modo` ("en_vivo" o "guardada") que el núcleo y la interfaz puedan mostrar. Sin clave nada llama a red. La clave nunca se imprime ni se guarda.
2. Corregir el generador: pdf-01 es el caso limpio (monto dentro del acuerdo del registro maestro, cuenta registrada) y debe poder pagar; pdf-02 deja de titularse RECIBO (usa un tipo que la política por tipo contemple). Regenera con semilla fija, actualiza `manifiesto.json` y las lecturas congeladas de `lectura/extracciones_multicanal/` afectadas. No toques `datos/esperado-documentos.json` (lo ajusta evaluación después); lista en el informe qué cambió en cada documento.
3. 3 a 5 pruebas: sin clave devuelve el congelado y modo "guardada"; con clave simulada devuelve el real sin llamar a red; el cliente real no imprime la clave.

Listo cuando: `python3 verify.py --etapa lectura` verde y `generar.py` reproduce igual dos veces. Incluye la fila para `tandas.md`. Sin secretos, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
