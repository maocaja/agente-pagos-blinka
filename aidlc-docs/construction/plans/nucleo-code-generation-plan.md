# Plan de código: U1 Núcleo (Dev A, rama `nucleo`)

Fecha: 2026-10-17. Estado: PROPUESTO, sin aprobar. Se ordena por el guion del video (`inception/demo-script.md`). Diseño en `construction/nucleo/functional-design/`; contrato en `contrato/` (manda).

## Alcance y límites
- Carpeta de escritura: `nucleo/` y `nucleo/tests/`. No se toca `contrato/`, `lectura/`, `interfaz/`, `evaluacion/` ni `datos/` (un cambio de contrato exige acuerdo de las dos personas y subir la versión).
- Python + FastAPI + SQLite (solo inserción). Dominio puro: sin FastAPI ni SQLite dentro de `nucleo/dominio/`; la API es una capa delgada.
- Inyección de reloj, identificadores, nonces, firmador y repositorios (lo que hace deterministas las pruebas).
- Nada quemado: todo valor de negocio sale del mandato. Falla cerrado. Dinero en enteros de unidades menores, como texto.
- Presupuesto de pruebas de U1: objetivo 67, máximo 80. Ninguna prueba llama a un modelo ni a la red.

## Estructura
```
nucleo/
  dominio/      entidades, mandato, reglas, motor, agregación, recibo, guardián (puro)
  infra/        repositorios SQLite (solo inserción), firmador, reloj, ids
  api/          FastAPI (rutas del contrato), sesión por visitante, modo público
  tests/
```

## Tandas

### T1. Primer hito: decisión con recibo (sábado antes de las 18:00)
Objetivo: un endpoint que reciba una factura canónica y devuelva decisión y recibo con 4 reglas. Es la base de las escenas 1 y 3 del video.
- [ ] 1.1 Modelos del dominio desde los esquemas del contrato (factura canónica, mandato, decisión, recibo); validación con `contrato/validar.py` en pruebas.
- [ ] 1.2 Mandato versionado: carga de `contrato/ejemplos/mandato.v1.json` y `v2.json`; sin valores quemados.
- [ ] 1.3 Registro maestro mínimo (proveedores, cuentas registradas, acuerdos) sembrado desde datos de prueba.
- [ ] 1.4 Motor: registro de reglas (estrategia), evaluación de todas sin cortocircuito, agregación por precedencia FRENAR, ESCALAR, PAGAR (REGISTRAR para nota de crédito), falla cerrado.
- [ ] 1.5 Reglas del primer hito: **R2a** duplicado exacto, **R3** beneficiario permitido, **R4** cuenta registrada (escena 1: "la cuenta no es la registrada"), **R6** monto. Explicación determinista por regla, con evidencia citando el campo.
- [ ] 1.6 Recibo: estructura, hash del documento, nonce y vigencia de 24 h inyectados; firma Ed25519 con clave inyectada; versión de clave.
- [ ] 1.7 Stub de API con los ejemplos del contrato (`POST /api/facturas`, `GET /api/decisiones`, `GET /api/decisiones/{id}`) para que U2, U3 y U4 avancen en paralelo.
- Pruebas (≈ 16): reglas R2a, R3, R4, R6 x3 casos (12); precedencia 2; recibo y firma 2.
- Listo cuando: `python3 verify.py --etapa nucleo` en verde y una factura de prueba produce decisión con recibo que valida contra el esquema.

### T2. Guardián y registro (sábado por la tarde)
Es la escena 3 del video: se altera un byte y el guardián rechaza.
- [ ] 2.1 Guardián de 6 verificaciones con la clave pública: firma, hash de la factura, monto y beneficiario, vigencia, nonce no usado, versión de mandato vigente. Rechazo con motivo en una frase y verificaciones posteriores marcadas "no evaluada".
- [ ] 2.2 Firmador como proceso aparte del servidor web (o, si el servicio gratuito no lo permite, módulo aislado con claves por sesión, declarado como SUPUESTO).
- [ ] 2.3 Registro de solo adición (SQLite): decisiones, resultados por regla, recibos, eventos; sin UPDATE ni DELETE (prueba de que fallan).
- [ ] 2.4 Reserva de presupuesto y consumo del nonce en una sola transacción; presupuesto derivado de las reservas; compensación al denegar o vencer.
- [ ] 2.5 `POST /api/guardian/verificar` (orden y recibo en el cuerpo) y `POST /api/recibos/{id}/verificar`, ambos ya en el contrato, con la respuesta del ejemplo `guardian.rechazo.json`. **No se añade ruta nueva:** la interfaz altera una copia del recibo y la envía al guardián.
- Pruebas (≈ 14): las 6 verificaciones x1 más casos de motivo (8); reserva y concurrencia 3; registro de solo adición 2; contrato de la respuesta 1.
- Listo cuando: un recibo alterado en un byte es rechazado con motivo, y dos pagos que juntos exceden el presupuesto no pasan ambos.

### T3. Resto de reglas y tipos (sábado por la noche)
- [ ] 3.1 **R1** lectura confiable (confianza y causas de ESCALAR: lecturas distintas, sin segunda lectura, cita no encontrada; origen imagen nunca llega a PAGAR, ver `lectura/business-rules.md`).
- [ ] 3.2 **R2b** duplicado difuso, **R5** coincide con lo acordado, **R7** moneda, **R8** texto dirigido al agente, **R9** presupuesto del periodo (siempre al final), **R10** tope acumulado por proveedor (solo mandato v2).
- [ ] 3.3 Política por tipo como tabla de datos: nota de crédito REGISTRAR sin orden; estado de cuenta FRENAR; proforma y anticipo ESCALAR; tipo desconocido ESCALAR.
- [ ] 3.4 R9 y fallas de lectura de R1 no aprobables.
- Pruebas (≈ 24): 7 reglas x3 casos (21); tipos y REGISTRAR 3.
- Listo cuando: las 11 reglas del registro corren y `contrato/reglas.registro.json` coincide con las reglas registradas en el código (prueba).

### T4. Aprobaciones, roles y ciclo (sábado de madrugada)
- [ ] 4.1 Dos roles simulados (analista y CFO) con encabezado `X-Rol`; mapa de capacidades por rol; quien cargó no aprueba.
- [ ] 4.2 Aprobar siempre reevalúa y emite un recibo nuevo; vigencia de 24 h; falla de lectura de R1 no se aprueba, se corrige.
- [ ] 4.3 Mandato propuesto por el CFO y contrafirmado por el analista; versión nueva.
- [ ] 4.4 Ciclo de pagos y exportación de la conciliación.
- [ ] 4.5 Vista previa "qué cambia si se aprueba".
- Pruebas (≈ 9): permisos por rol 3; aprobar con reevaluación 2; vencimiento 1; mandato con dos firmas 2; vista previa 1.

### T5. API completa, sesión y despliegue (sábado 23:00 a domingo)
- [ ] 5.1 Las 28 rutas de `contrato/api.openapi.yaml`, `Idempotency-Key`, `X-Sesion-Id`, errores con el formato del contrato.
- [ ] 5.2 Sesión por visitante: copia del set base y par de claves por sesión; reinicio.
- [ ] 5.3 Modo público: solo lectura salvo la sesión propia; sin llamadas a modelos.
- [ ] 5.4 Despliegue en un servicio gratuito: SQLite sembrada al arrancar; despertar antes del pitch (riesgos 5 y 6 del plan de ejecución).
- [ ] 5.5 Exportar `/openapi.json` y comprobarlo contra `api.openapi.yaml` (prueba de contrato).
- Pruebas (≈ 4): contrato de rutas 1; sesión aislada 1; modo público 1; idempotencia 1.

## Total y control
≈ 67 pruebas (objetivo del presupuesto). Cada tanda cierra con el procedimiento de `CLAUDE.md` sección 4: `verify.py --etapa nucleo`, `graphify update .`, marcar este plan, anotar en `tandas.md`, commit local.

## Riesgos y supuestos
- U1 es la unidad más cargada y las demás dependen de ella: los stubs de T1.7 existen para desbloquear a U2, U3 y U4 el sábado temprano.
- La regla R4 se añade al primer hito respecto del plan anterior (R2a, R3, R6) porque es la escena 1 del video.
- El firmador separado puede no ser posible en el servicio gratuito (SUPUESTO declarado).
- El reloj de la demo y los identificadores son inyectados; el video usa un set y una semilla fijos.

## Para el subagente `ejecutor-de-unidad`
Cada tanda se entrega con un mandato mínimo (CLAUDE.md sección 2): objetivo, archivos a leer, rutas que puede escribir (`nucleo/`), criterio de listo medible, pruebas a ejecutar y respuesta de máximo 150 palabras. Comentarios cortos, solo el porqué. Si el código no avanza, no se reabre el diseño: se anota el hallazgo.
