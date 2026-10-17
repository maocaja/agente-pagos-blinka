# Mandato Ola 7: Lectura, detector determinista de instrucciones (rama `lectura`)

Objetivo: R8 no depende solo de que el modelo marque la instrucción oculta. Defensa en profundidad: un detector local, sin modelo, sobre el texto del documento. Código ligero: tope de diff 150 líneas. Máximo 5 pruebas nuevas.

Leer: `CLAUDE.md` (4, 5c), `lectura/adaptadores/canonica.py`, `lectura/extractor/` (donde se arma la señal `texto_dirigido_al_agente`), `contrato/factura-canonica.schema.json` (`senales`), `datos/documentos/` (los textos con instrucción: pdf-07, eml-08, eml-10, chat-09) y `datos/facturas/fac-11-*.txt`.
Escribir solo: `lectura/` y `lectura/tests/`.

Hacer:
1. `lectura/seguridad/instrucciones.py`: detector con una tabla de patrones (español, inglés, portugués) de órdenes al agente: ignorar o saltarse reglas o instrucciones previas, aprobar o pagar de inmediato, no escalar ni revisar, invocar autoridad ("lo autorizó el gerente", "approved by the CEO"), cambiar el rol del modelo. Devuelve `p` y la cita encontrada. Los patrones son datos (tabla), no ramas `if`.
2. Integrarlo donde se arma la señal: la señal final es la mayor entre la del modelo y la del detector; cita del detector si el modelo no marcó. Una sola función compartida por todos los adaptadores y el extractor.
3. Falsos positivos: córrelo sobre las 18 facturas de `datos/facturas/` y los documentos limpios de `datos/documentos/`; solo deben disparar las trampas. Informa el resultado en cifras.
4. Hasta 5 pruebas: español, inglés, portugués, autoridad falsa, texto benigno que no dispara.

Listo cuando: `python3 verify.py --etapa lectura` verde. Incluye la fila para `tandas.md` y las cifras de falsos positivos y positivos. Sin red ni modelos, comentarios cortos, `graphify query` antes de grep, no commit ni push. Máximo 150 palabras.
