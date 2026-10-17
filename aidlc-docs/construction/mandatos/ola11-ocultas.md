# Mandato Ola 11: Evaluación, corrida final con las 4 facturas ocultas (rama `evaluacion`)

Objetivo: probar el sistema una sola vez con 4 documentos que nadie vio, y reportar el resultado tal cual. Esta es la prueba más honesta de la cifra del video. Código ligero: tope de diff 150 líneas. Máximo 2 pruebas nuevas.

REGLAS DE LA CORRIDA FINAL: no modifiques ningún archivo de `nucleo/`, `lectura/` (reglas, detector, adaptadores), `datos/registro-maestro.json` ni `datos/ocultas/esperado-ocultas.json`. Si algo falla, NO lo arregles: reporta. No repitas la corrida para "mejorar" el resultado.

Leer: `CLAUDE.md` (4, 5c), `datos/ocultas/` (los 4 documentos, `esperado-ocultas.json` y `SELLO.json`), `lectura/extracciones/` (formato de una lectura canónica a mano), `evaluacion/corrida_documentos.py`, `datos/registro-maestro.json`.
Escribir solo: `evaluacion/corrida_ocultas.py`, `evaluacion/ocultas_lecturas/` y `evaluacion/salida/ocultas.json`.

Hacer:
1. Verifica que los 4 archivos coinciden con los hashes de `SELLO.json`; si no coinciden, detente e informa.
2. Escribe a mano la lectura canónica de cada documento (marcada `manual-congelada`, como las 18) con `proveedor_asignado` por el mismo criterio de lectura (id fiscal o nombre o alias del registro; sin coincidencia, sin proveedor). Si un documento no se puede leer a canónica (nota de voz sin datos, correo sin datos), regístralo como "ilegible" y comprueba que el sistema lo escale, no que lo pague.
3. Cárgalas por la API del núcleo en sesiones limpias con el mandato v2 y compara con `esperado-ocultas.json`: veredicto de reglas y de extremo a extremo.
4. Escribe `evaluacion/salida/ocultas.json` con el resultado y cada diferencia, con la evidencia (qué regla, qué dato). No decidas quién tiene razón.
5. Hasta 2 pruebas: la salida valida contra el esquema; ninguna oculta da PAGAR si su esperado no es PAGAR.

Listo cuando: `python3 verify.py --etapa evaluacion` verde. Incluye la fila para `tandas.md` y el resultado en cifras (cuántas coinciden y cuáles no). Comentarios cortos, no commit ni push. Máximo 150 palabras.
