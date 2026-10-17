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

### T1. Esperados (sábado temprano, antes del verificador)
- [x] 1.1 Reescribir `datos/esperado.json` de forma independiente desde el texto de las reglas: factura 07 escala, `tipo_documento`, factura 17 realista; **dos veredictos por factura** (de reglas y de extremo a extremo).
- [x] 1.2 Comprobar que el set cubre los casos trampa del reto: cobro duplicado, beneficiario nuevo, factura que no cuadra con lo acordado, monto sobre el límite y presupuesto insuficiente; si falta alguno, se pide una factura nueva a U2.
- [ ] 1.3 Sellar las 4 ocultas (hash) sin leerlas.
- Pruebas (≈ 18): una prueba parametrizada sobre las 18 facturas.

### T2. Verificador independiente (sábado 08:00 a 12:00)
- [ ] 2.1 Condición de pago escrita solo desde `contrato/reglas.registro.json` y el texto de las reglas, con estado propio; sin importar `nucleo/`.
- [ ] 2.2 Corrida del set contra la API de U1 (o su servidor simulado): coincidencia entre motor y verificador; toda discrepancia se muestra.
- [ ] 2.3 Resultados con `contrato/resultados.schema.json`: aciertos de reglas, de extremo a extremo, autonomía, escalada innecesaria.
- Pruebas (≈ 10): verificador por regla y por tipo.

### T3. Pentest y arena nivel 1 (sábado por la tarde)
Escena 4 del video.
- [x] 3.1 Las seis estrategias fijas del diseño (`evaluacion/functional-design/business-rules.md`), con su resultado esperado escrito antes de correrlas: partir en facturas bajo el umbral del mismo proveedor; una factura justo bajo el umbral; redondeo de moneda que cruza el umbral; número de factura reformateado (duplicado); proveedor nuevo con un pago pequeño y luego uno grande; cambio de cuenta después de una aprobación. La instrucción oculta se cubre con R8 y la arena, no con una estrategia aparte.
- [x] 3.2 Hallazgos con arreglo propuesto; el mandato v1 sin R10 debe dejar pasar el caso de facturas partidas y el v2 cerrarlo.
- [x] 3.3 **Qué es el hueco, sin maquillar:** el mandato v1 no tiene tope acumulado, así que deja pasar facturas partidas por **diseño del mandato**, no por un error del motor. Es un hueco de política que el pentest detecta y el v2 cierra. El video lo cuenta así ("un mandato sin tope acumulado deja pasar facturas partidas") y no como hallazgo sorpresa. Se comprueba que el motor con v2 lo bloquea y que ninguna otra estrategia pasa.
- [x] 3.4 Arena nivel 1: ≤ 500 variantes con semilla fija sobre el texto original de las facturas.
- Pruebas (≈ 8): pentest 6; arena acotada 2.

### T4. Arena nivel 2, fallas del extractor y carrera (sábado por la noche)
- [x] 4.1 Arena de la demo (3.200 variantes, fuera de `verify`), con semillas variables y el número final "X ataques, Y pagados indebidamente".
- [ ] 4.2 Fallas del extractor (salida truncada, rechazada, cita ausente) deben terminar en ESCALAR.
- [ ] 4.3 Carrera de presupuesto: dos pagos que juntos exceden el presupuesto; se simulan con una barrera o de forma secuencial, con reloj e identificadores inyectados, nunca con hilos reales.
- Pruebas (≈ 9): fallas del extractor 6; carrera 2; invariante por tipo 1.

### T5. Mutación y corrida final (domingo temprano)
- [ ] 5.1 14 mutantes (uno por regla, orden de agregación, falla cerrado y registro de solo adición), corridos por un agente distinto al del verificador.
- [ ] 5.2 Corrida final con las 4 ocultas y `python3 verify.py --gate`.
- [ ] 5.3 Registrar qué mutante no fue atrapado y qué se hizo.
- Sin pruebas nuevas dentro de `verify`: la mutación solo corre en la puerta de calidad.

## Qué corre dentro de `verify`
Las corridas contra la API de U1 (2.2, 3.x) usan el servidor simulado dentro de `verify`; contra el núcleo real corren solo en la puerta de calidad. Las pruebas de fallas del extractor de U4 comprueban el extremo a extremo hasta ESCALAR; las de U2 comprueban cada falla del cliente por separado.

## Total y control
≈ 45 pruebas (objetivo 45, máximo 60). Cierre de tanda según `CLAUDE.md` sección 4.

## Riesgos y supuestos
- U4 necesita el código de U1 para el pentest, la arena y la mutación: hasta entonces trabaja con el servidor simulado.
- Si la arena no encuentra el hueco por sí sola, el video no lo muestra como hallazgo sorpresa.
- La cifra "0 pagados indebidamente" es verdadera solo para este set y estas variantes; el cierre del video dice qué no se probó.
