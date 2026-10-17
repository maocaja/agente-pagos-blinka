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
- [x] 1.0 **Primero:** stub de API con los ejemplos del contrato (`POST /api/facturas`, `GET /api/decisiones`, `GET /api/decisiones/{id}`, `GET /api/mandato`) para desbloquear a U2, U3 y U4 desde la primera hora.
- [x] 1.1 Modelos del dominio desde los esquemas del contrato (factura canónica, mandato, decisión, recibo); validación con `contrato/validar.py` en pruebas.
- [x] 1.2 Mandato versionado: carga de `contrato/ejemplos/mandato.v1.json` y `v2.json`; sin valores quemados.
- [x] 1.3 Registro maestro mínimo (proveedores, cuentas registradas, acuerdos) sembrado desde datos de prueba.
- [x] 1.4 Motor: registro de reglas (estrategia), evaluación de todas sin cortocircuito, agregación por precedencia FRENAR, ESCALAR, PAGAR (REGISTRAR para nota de crédito), falla cerrado.
- [x] 1.5 Reglas del primer hito: **R2a** duplicado exacto, **R3** beneficiario permitido, **R4** cuenta registrada (escena 1: "la cuenta no es la registrada"), **R6** monto. Explicación determinista por regla, con evidencia citando el campo.
- [x] 1.6 Recibo: estructura, hash del documento, nonce y vigencia de 24 h inyectados; firma Ed25519 con clave inyectada; versión de clave.
- Pruebas (≈ 16): reglas R2a, R3, R4, R6 x3 casos (12); precedencia 2; recibo y firma 2.
- Listo cuando: `python3 verify.py --etapa nucleo` en verde y una factura de prueba produce decisión con recibo que valida contra el esquema.

### T2. Guardián y registro (sábado por la tarde)
Es la escena 3 del video: se altera un byte y el guardián rechaza.
- [x] 2.1 Guardián de 6 verificaciones con la clave pública, según `nucleo/functional-design/business-rules.md` (leer la lista oficial antes de escribirlo): firma y hash, monto y beneficiario del recibo, vigencia y versión de mandato vigente, nonce no usado, **modo sombra exige aprobación humana**, **aprobación vigente y ligada al recibo**, y **reevaluación del presupuesto antes de autorizar**. Rechazo con motivo en una frase y verificaciones posteriores marcadas "no evaluada".
- [ ] 2.2 Firmador como proceso aparte del servidor web (o, si el servicio gratuito no lo permite, módulo aislado con claves por sesión, declarado como SUPUESTO).
- [x] 2.3 Registro de solo adición (SQLite): decisiones, resultados por regla, recibos, eventos; sin UPDATE ni DELETE (prueba de que fallan).
- [x] 2.4 Reserva de presupuesto y consumo del nonce en una sola transacción; presupuesto derivado de las reservas; compensación al denegar o vencer.
- [x] 2.6 **Orden de pago y punto de pago:** un PAGAR emite una `OrdenDePago` desde el recibo; el guardián la marca Autorizada o Denegada; al denegar se libera la reserva con un movimiento compensatorio. Sin recibo válido no existe orden.
- [x] 2.7 **R10** tope acumulado por proveedor y mandatos v1 (sin R10) y v2 (con R10); el pentest de U4 los necesita el sábado por la tarde.
- [x] 2.8 `Idempotency-Key` en los comandos que crean recibos o reservas (decisión, aprobación, corrección), con una sola semántica para el nonce: se consume al emitir el recibo y el guardián comprueba que no se haya usado antes en una autorización.
- [x] 2.5 `POST /api/guardian/verificar` (orden y recibo en el cuerpo) y `POST /api/recibos/{id}/verificar`, ambos ya en el contrato, con la respuesta del ejemplo `guardian.rechazo.json`. **No se añade ruta nueva:** la interfaz altera una copia del recibo y la envía al guardián.
- Pruebas (≈ 18): guardián, una por verificación más motivos (10); orden sin recibo válido no existe y denegación libera la reserva 2; R10 y mandatos 2; reserva y carrera 2 (**simulada con una barrera o de forma secuencial, nunca con hilos reales**); registro de solo adición 1; contrato de la respuesta 1.
- Listo cuando: un recibo alterado en un byte es rechazado con motivo, y dos pagos que juntos exceden el presupuesto no pasan ambos.

### T3. Resto de reglas y tipos (sábado por la noche)
- [x] 3.1 **R1** lectura confiable (confianza y causas de ESCALAR: lecturas distintas, sin segunda lectura, cita no encontrada; origen imagen nunca llega a PAGAR, ver `lectura/business-rules.md`).
- [x] 3.2 **R2b** duplicado difuso, **R5** coincide con lo acordado, **R7** moneda, **R8** texto dirigido al agente, **R9** presupuesto del periodo (siempre al final); R10 se entregó en T2.
- [x] 3.3 Política por tipo como tabla de datos: nota de crédito REGISTRAR sin orden; estado de cuenta FRENAR; proforma y anticipo ESCALAR; tipo desconocido ESCALAR.
- [x] 3.4 R9 y fallas de lectura de R1 no aprobables.
- Pruebas (≈ 21): 6 reglas x3 casos (18; R10 ya está en T2); tipos y REGISTRAR 3.
- Listo cuando: las 11 reglas del registro corren y `contrato/reglas.registro.json` coincide con las reglas registradas en el código (prueba).

### T4. Aprobaciones, roles y ciclo (sábado de madrugada)
- [x] 4.1 Dos roles simulados (analista y CFO) con encabezado `X-Rol`; mapa de capacidades por rol; quien cargó no aprueba.
- [x] 4.2 Aprobar siempre reevalúa y emite un recibo nuevo; vigencia de 24 h; falla de lectura de R1 no se aprueba, se corrige.
- [ ] 4.3 Mandato propuesto por el CFO y contrafirmado por el analista; versión nueva.
- [ ] 4.4 Ciclo de pagos y exportación de la conciliación.
- [ ] 4.5 Vista previa "qué cambia si se aprueba".
- Pruebas (≈ 9): permisos por rol 3; aprobar con reevaluación 2; vencimiento 1; mandato con dos firmas 2; vista previa 1.

### T5. API completa, sesión y despliegue (sábado 23:00 a domingo)
- [ ] 5.1 Las rutas de `contrato/api.openapi.yaml` que dependen solo de U1, `X-Sesion-Id` y errores con el formato del contrato.
- [ ] 5.6 **Integración con U2 y U4 (Dev A con Dev B y el subagente):** `/api/pentest/ejecutar`, `/api/arena/ejecutar`, `/api/marcador`, `/api/costo`, `/api/muestras` y `/api/documentos` dependen de código de otras carpetas. U1 define los puertos (interfaces) y monta las rutas; U2 y U4 aportan funciones en sus carpetas, registradas por configuración. U1 expone `copiar_estado_sesion()` para que la arena y el pentest corran sobre una copia de la sesión sin tocar la original.
- [ ] 5.2 Sesión por visitante: copia del set base y par de claves por sesión; reinicio.
- [ ] 5.3 Modo público: solo lectura salvo la sesión propia; sin llamadas a modelos.
- [ ] 5.4 Despliegue en un servicio gratuito: SQLite sembrada al arrancar; despertar antes del pitch (riesgos 5 y 6 del plan de ejecución).
- [ ] 5.5 Exportar `/openapi.json` y comprobarlo contra `api.openapi.yaml` (prueba de contrato).
- Pruebas (≈ 4): contrato de rutas 1; sesión aislada 1; modo público 1; integración de un puerto con una función de prueba 1.

## Total y control
≈ 69 pruebas (el objetivo es 67; el máximo, 80). Cada tanda cierra con el procedimiento de `CLAUDE.md` sección 4: `verify.py --etapa nucleo`, `graphify update .`, marcar este plan, anotar en `tandas.md`, commit local.

## Entrega a las otras unidades
Orden en que U1 desbloquea a los demás: (1) stub de API en la primera hora; (2) R10 y mandatos v1 y v2 en T2, para el pentest; (3) aprobar y reevaluar en T4: hasta entonces la interfaz usa el stub; (4) rutas de pentest y arena en 5.6. Sin esas entregas, las otras unidades trabajan con el servidor simulado.

## Riesgos y supuestos
- U1 es la unidad más cargada y las demás dependen de ella: los stubs de T1.7 existen para desbloquear a U2, U3 y U4 el sábado temprano.
- La regla R4 se añade al primer hito respecto del plan anterior (R2a, R3, R6) porque es la escena 1 del video.
- El firmador separado puede no ser posible en el servicio gratuito (SUPUESTO declarado).
- El reloj de la demo y los identificadores son inyectados; el video usa un set y una semilla fijos.

## Para el subagente `ejecutor-de-unidad`
Cada tanda se entrega con un mandato mínimo (CLAUDE.md sección 2): objetivo, archivos a leer, rutas que puede escribir (`nucleo/`), criterio de listo medible, pruebas a ejecutar y respuesta de máximo 150 palabras. Comentarios cortos, solo el porqué. Si el código no avanza, no se reabre el diseño: se anota el hallazgo.
