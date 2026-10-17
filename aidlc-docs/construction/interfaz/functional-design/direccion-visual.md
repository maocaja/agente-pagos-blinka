# Dirección visual: mesa de revisión de cuentas por pagar

Fecha: 2026-10-17. Estado: **ESTRUCTURA REEMPLAZADA por `adaptacion-biblioteca.md` (referencia del equipo); se conservan el diagnóstico (sección 1) y las tres escenas (sección 4)**. Texto original: propuesta pendiente de aprobación. Prototipo: `docs/propuesta-pantalla-principal.html` (datos reales del set curado de 12 muestras). Personas en `inception/personas.md`; recorridos en `recorridos.md`.

## 1. Diagnóstico (app real, revisada en Chrome)
Qué impide entender el valor en 10 segundos:
1. **Composición:** navegación de enlaces subrayados sin identidad; la lista ocupa un tercio del ancho y el resto queda vacío hasta que se elige una fila. No hay un punto focal.
2. **Jerarquía:** cinco contadores del mismo peso (12, 4, 3, 5, 5) y ninguna cifra de dinero. El jurado no ve cuánto dinero está en juego.
3. **Datos y textos:** casi todas las filas dicen "Cumple las reglas evaluadas"; la diferencia del producto (frenar con motivo) queda en filas sueltas. Los motivos usan ids de reglas (R1, R4, R10) que una persona de finanzas no sabe leer.
4. **Recorrido:** la evidencia está repartida en pestañas (Documento, Recibo, Historial); para entender una decisión hay que abrir tres.
5. **Mensaje:** una línea verde ("Verificación independiente de las 18 facturas…") compite con el resto y se pierde; no cuenta la garantía.
6. **Tipografía:** la guía define Inter, pero la aplicación nunca la carga y cae a la fuente del sistema.
7. **Redundancia:** estados idénticos repetidos en cada fila (todo "Escalar") consumen ancho que necesitan los motivos.

## 2. Referencia: Dribbble "Banking Dashboard UI" (Abron Studio, marca Finexa)
Observado en la imagen publicada (no se pudo abrir el archivo en alta resolución):
- **Un número protagonista** (saldo) con su matiz al lado ("disponible para gastar"), y el resto de la pantalla lo respalda.
- **Tres zonas** separadas por líneas punteadas verticales, no por tarjetas pesadas.
- **Lateral con navegación corta** y una sola acción primaria (Send Money).
- **Lista de movimientos** de dos líneas (nombre; categoría y hora), importe alineado a la derecha y chips verdes para lo positivo; enlace "See All" en cada bloque.
- **Un indicador único** (puntaje 74/100) acompañado de consejos concretos.
- Paleta suave y jerarquía tipográfica marcada; un gráfico por bloque, solo si explica.
Principios que adoptamos: número protagonista con contexto; zonas separadas por líneas punteadas; lateral corto; filas de dos líneas con el importe a la derecha; un indicador que explica y no decora; sin gráficos de adorno. **No adoptamos** la paleta crema y pastel: seguimos con la guía de estilo (papel frío, tinta azul, color fuerte solo en veredictos).

## 3. Propuesta de la pantalla principal ("Revisión de hoy")
Comunica de inmediato:
- **Qué empresa y cuánto dinero está en revisión:** lateral con empresa, periodo y mandato; primera zona "En revisión: USD 11.070" con una barra segmentada por motivo (cuenta distinta, instrucción dentro del documento, remitente y monto).
- **Qué necesita atención y por qué:** tabla "Necesita atención" ordenada por riesgo; cada fila: documento (canal, proveedor, importe), por qué en una frase y qué hacer. Sin ids de reglas visibles.
- **Qué documento respalda la decisión:** panel de detalle con la foto original y la comparación contra lo registrado; la diferencia ("cuenta terminada en 9021; registrada 4417") es el único elemento rojo.
- **Qué acción y qué ocurre después:** decisión, siguiente paso, línea de estado (recibida, motor, espera al CFO) y qué pasa al rechazar y al aprobar.
- **La garantía:** zona "Pagos fuera de las reglas: 0" con su alcance (18 facturas, 3.200 ataques, 17 de 17 fallos detectados) y un enlace a "lo que no probamos". Debajo, "con decisión de pagar" y "frenados" como listas compactas.
Cada elemento tiene una función; el único gráfico de composición es la barra segmentada y la del presupuesto.

## 4. Tres momentos de la demostración (flujo real, sin buscar entre pestañas)
1. **Cuenta cambiada:** la pantalla principal con la fila seleccionada; foto original y cuenta registrada comparadas, diferencia destacada, decisión y siguiente paso (prototipo hecho).
2. **Recibo manipulado:** vista dividida "recibo firmado" frente a "copia alterada" con el campo modificado resaltado (valor original y alterado), y debajo el resultado del guardián como una fila de seis pasos con el que falla marcado y su motivo en una frase ("la firma no corresponde al contenido"); los demás, "no evaluados".
3. **Facturas partidas:** tres facturas del mismo proveedor, cada una bajo el umbral, apiladas contra una línea de tope acumulado; con el mandato v1 el acumulado cruza el tope sin que nadie lo detenga (el hueco), con el v2 la tercera se frena y se ve el motivo. Importes de la estrategia E1 de `evaluacion/salida/pentest.json`.
Las tres usan las rutas reales (decisiones, guardián, pentest); el botón Demo las recorre en ese orden.

## 5. Encargos derivados (NO lanzados; esperan aprobación de esta dirección)
| Encargo | Contenido | Datos |
|---|---|---|
| E1. Estructura y cifras | Lateral, cabecera con rol, banda de tres zonas (en revisión por moneda, presupuesto, garantía), Inter autoalojada | `/api/ciclo`, decisiones, `/api/marcador` |
| E2. Revisión | Tabla de atención por riesgo con motivo y siguiente paso en lenguaje llano (los ids de reglas pasan a un detalle secundario), panel de detalle con comparación y línea de estado, acciones del CFO | decisiones, `historial`, `/archivo` |
| E3. Recibo manipulado | Vista dividida original frente a alterado y resultado del guardián en seis pasos | recibo, guardián |
| E4. Facturas partidas | Apilado contra el tope acumulado, v1 contra v2 | `pentest.json`, `pentest-v1.json` |
| E5. Guion | `demo-operativo.md` y `ESCENAS` alineados con las tres escenas | |
Cada encargo cierra con el recorrido en Chrome contra la app real (regla de `CLAUDE.md`).

## 6. Preguntas abiertas para quien evalúa
- ¿Se aprueba la estructura (lateral y tres zonas) y el orden "en revisión, presupuesto, garantía"?
- ¿Los importes en monedas distintas se muestran separados por moneda (propuesta) o convertidos a USD con el tipo de cambio del mandato?
- ¿"Evidencia" y "Ataque" quedan como secciones del lateral o se fusionan en una sola?
