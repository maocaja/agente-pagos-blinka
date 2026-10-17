# Mandato Ola 3: Evaluación, verificador independiente (rama `evaluacion`, worktree `../wt-evaluacion`)

Objetivo: un verificador de la condición de pago escrito solo desde el texto de las reglas, que corre las 18 facturas contra la API del núcleo y muestra toda discrepancia. Código ligero: tope de diff 500 líneas (sin pruebas).

INDEPENDENCIA (obligatoria): NO leas `nucleo/`, `demo-front/motor.js` ni `datos/ocultas/`. Lee solo: `contrato/` (reglas.registro.json, esquemas, ejemplos, api.openapi.yaml), `aidlc-docs/construction/evaluacion/functional-design/`, el texto de las reglas en `aidlc-docs/construction/nucleo/functional-design/business-rules.md`, `datos/registro-maestro.json`, `datos/esperado.json`, `lectura/extracciones/` y `evaluacion/` actual.
Escribir solo: `evaluacion/` y `evaluacion/tests/`.

Hacer:
1. `evaluacion/verificador/`: condición de pago por tipo de documento, con estado propio (duplicados, acumulado por proveedor, presupuesto), sin importar `nucleo`. Entrada: la extracción; salida: veredicto y reglas que fallan.
2. `evaluacion/corrida/`: corre las 18 extracciones contra el servidor de la API del núcleo con el mandato elegido (la app se arranca en pruebas con TestClient desde `nucleo.api` solo para la corrida de integración, marcada para la puerta de calidad, no para `verify` normal) y contra el verificador; escribe resultados con `contrato/resultados.schema.json`: aciertos de reglas, de extremo a extremo, autonomía, escalada innecesaria, y lista de discrepancias motor contra verificador.
3. Revalidar `datos/esperado.json` contra `datos/registro-maestro.json` (por ejemplo la factura 09: Nuevo Logos NO está en el registro) y listar en `evaluacion/COBERTURA.md` qué casos trampa del reto siguen sin factura: monto entre umbral y tope, proveedor bloqueado, proforma, anticipo, tipo desconocido (los documentos los genera otro agente; sus esperados se fijan después).
4. 8 a 12 pruebas sobre el verificador por regla y por tipo de documento.

Listo cuando: `python3 verify.py --etapa evaluacion` verde y la corrida produce un resultado válido contra el esquema. Recordatorio: comentarios cortos, `graphify query` antes de grep (solo en carpetas permitidas), no commit ni push. Máximo 150 palabras, incluye las discrepancias encontradas.
