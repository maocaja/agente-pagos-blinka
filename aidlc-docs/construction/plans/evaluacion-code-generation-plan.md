# Plan de código: U4 Evaluación (subagente, con revisión de una persona desarrolladora; rama `evaluacion`)

Fecha: 2026-10-17. Estado: PROPUESTO, sin aprobar. Diseño en `construction/evaluacion/functional-design/`. Es lo que sostiene la cifra "X ataques, 0 pagados indebidamente" del video.

## Alcance y límites
- Escribe solo en `evaluacion/` y `evaluacion/tests/`, y los esperados en `datos/` (`esperado.json`). No toca `contrato/` ni `nucleo/`. Las 4 facturas de `datos/ocultas/` no se leen hasta la corrida final.
- **Independencia (CLAUDE.md sección 2):** el agente que escribe el verificador (C19) no lee `nucleo/` ni `demo-front/motor.js`; los esperados los escribe quien lee solo el texto de las reglas; la mutación la corre un agente distinto al del verificador (decisión del 2026-10-17). El pentest y la arena (C20, C21) sí pueden ver el motor.
- Ninguna prueba llama a un modelo ni a la red. Presupuesto: objetivo 45, máximo 60.

## Estructura
```
evaluacion/
  verificador/   condición de pago escrita desde el texto de las reglas, con estado propio
  pentest/       6 estrategias por código
  arena/         variantes generadas sobre el texto original, con semilla
  mutacion/      14 mutantes
  corrida/       corrida del set y resultados según contrato/resultados.schema.json
  tests/
```

## Tandas

### T1. Esperados (viernes noche, antes del verificador)
- [ ] 1.1 Reescribir `datos/esperado.json` de forma independiente desde el texto de las reglas: factura 07 escala, `tipo_documento`, factura 17 realista; **dos veredictos por factura** (de reglas y de extremo a extremo).
- [ ] 1.2 Comprobar que el set cubre los casos trampa del reto: cobro duplicado, beneficiario nuevo, factura que no cuadra con lo acordado, monto sobre el límite y presupuesto insuficiente; si falta alguno, se pide una factura nueva a U2.
- [ ] 1.3 Sellar las 4 ocultas (hash) sin leerlas.
- Pruebas (≈ 18): una prueba parametrizada sobre las 18 facturas.

### T2. Verificador independiente (sábado 08:00 a 12:00)
- [ ] 2.1 Condición de pago escrita solo desde `contrato/reglas.registro.json` y el texto de las reglas, con estado propio; sin importar `nucleo/`.
- [ ] 2.2 Corrida del set contra la API de U1 (o su servidor simulado): coincidencia entre motor y verificador; toda discrepancia se muestra.
- [ ] 2.3 Resultados con `contrato/resultados.schema.json`: aciertos de reglas, de extremo a extremo, autonomía, escalada innecesaria.
- Pruebas (≈ 10): verificador por regla y por tipo.

### T3. Pentest y arena nivel 1 (sábado por la tarde)
Escena 4 del video.
- [ ] 3.1 Seis estrategias: partir en facturas bajo el umbral, una factura justo bajo el umbral, texto dirigido al agente, cuenta cambiada, duplicado con número alterado, moneda no permitida.
- [ ] 3.2 Hallazgos con arreglo propuesto; el mandato v1 sin R10 debe dejar pasar el caso de facturas partidas y el v2 cerrarlo.
- [ ] 3.3 **El hueco debe ser genuino:** se comprueba que el motor sin R10 lo deja pasar por diseño del mandato, no por un error sembrado; si no se puede sostener así, la escena se omite.
- [ ] 3.4 Arena nivel 1: ≤ 500 variantes con semilla fija sobre el texto original de las facturas.
- Pruebas (≈ 8): pentest 6; arena acotada 2.

### T4. Arena nivel 2, fallas del extractor y carrera (sábado por la noche)
- [ ] 4.1 Arena de la demo (3.200 variantes, fuera de `verify`), con semillas variables y el número final "X ataques, Y pagados indebidamente".
- [ ] 4.2 Fallas del extractor (salida truncada, rechazada, cita ausente) deben terminar en ESCALAR.
- [ ] 4.3 Carrera de presupuesto: dos pagos concurrentes no exceden el presupuesto.
- Pruebas (≈ 8): fallas del extractor 6; carrera 2; invariante por tipo 1.

### T5. Mutación y corrida final (domingo temprano)
- [ ] 5.1 14 mutantes (uno por regla, orden de agregación, falla cerrado y registro de solo adición), corridos por un agente distinto al del verificador.
- [ ] 5.2 Corrida final con las 4 ocultas y `python3 verify.py --gate`.
- [ ] 5.3 Registrar qué mutante no fue atrapado y qué se hizo.
- Sin pruebas nuevas dentro de `verify`: la mutación solo corre en la puerta de calidad.

## Total y control
≈ 45 pruebas (objetivo 45, máximo 60). Cierre de tanda según `CLAUDE.md` sección 4.

## Riesgos y supuestos
- U4 necesita el código de U1 para el pentest, la arena y la mutación: hasta entonces trabaja con el servidor simulado.
- Si la arena no encuentra el hueco por sí sola, el video no lo muestra como hallazgo sorpresa.
- La cifra "0 pagados indebidamente" es verdadera solo para este set y estas variantes; el cierre del video dice qué no se probó.
