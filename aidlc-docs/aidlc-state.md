# Estado de AI-DLC: Agente de Pagos con Garantía

Versión reducida para hackathon. Entrega: domingo 2026-10-18, 12:00 (se congela a las 10:00). Actualizado: 2026-10-17, tras la Ola 5. Lo actualiza el orquestador al cerrar cada ola (`CLAUDE.md`, sección 4).

## Etapas
| Etapa | Estado |
|---|---|
| Requisitos, diseño de aplicación, unidades, diseños funcionales, contrato (1.0.0-rc1), plan de ejecución | Aprobados |
| Reglas del proyecto, subagentes, graphify, sistema de diseño, estrategia de verificación | Instalados |
| Planes de código por unidad (x4) | Aprobados; ejecución con código ligero (`CLAUDE.md` 5c) |
| Arquitectura objetivo frente a MVP | `inception/architecture-target-vs-mvp.md` y `docs/arquitectura.html` |
| Guion del video | v3; escena 2 ampliada a tres trampas seguidas |

## Construcción por unidad (registro detallado en `construction/tandas.md`)
| Unidad | Hecho | Pendiente |
|---|---|---|
| U1 Núcleo | Ola 2 y 4: 11 reglas, guardián de 6 verificaciones, libro de reserva y nonce, mandatos v1 y v2, sesiones, aprobar y rechazar con reevaluación, marcador. 51 pruebas | Ola 5 hecha (60 pruebas): explicación, vista previa, auditoría, pain.001, R1 con remitente inconsistente. Pendiente: rutas de pentest y arena, mandato con dos firmas, despliegue; diferencias con `esperado.json` de lista de reglas (mismo veredicto) en f_10, f_12 y f_13 |
| U2 Lectura | T1, T1b y asignación de proveedor. 11 pruebas (19 tras la Ola 3) | Ola 3 hecha: IVA en líneas, extractor con prompt versionado y tope de gasto (19 pruebas). Ola 4 hecha: adaptadores PDF, `.eml`, chat e imagen (31 pruebas). Ola 5 hecha (39 pruebas): XML fiscal, CSV de lote, señal de `Reply-To`. Pendiente: orquestación de lotes; lecturas reales con la clave de API |
| U3 Interfaz | Decisiones, recibo, guardián, reglas (solo lectura), marcador, ataque, bandeja simulada y botón Demo. 10 pruebas | Reglas editables con vista previa, bandeja del aprobador, explicación; revisar contraste y foco; datos reales de pentest (Ola 6) |
| U4 Evaluación | Esperados de las 18 facturas. 20 pruebas | Ola 3 hecha: verificador independiente y corrida (35 pruebas; motor y verificador coinciden en las 18). Esperados del set multicanal hechos (53 pruebas). Ola 6 hecha: pentest de 6 estrategias (v1 deja pasar las partidas, v2 las frena con R10) y arena (500 en verify, 3.200 por script; 60 pruebas). Pendiente: mutantes y ocultas |
| Datos | Registro maestro corregido (Nuevo Logos fuera del registro) | Set multicanal simulado generado en `datos/documentos/` (18 archivos); esperados hechos; generador por corregir (pdf-01, pdf-02) |

`verify.py` global: VERDE, 162 pruebas (máximo 200).

## Decisiones recientes
- 2026-10-17: Ola 5 incluye explicación en lenguaje claro, reglas editables con vista previa (sin lenguaje natural), paquete de auditoría verificable fuera de la app, orden de pago simulada (pain.001), y los canales XML fiscal y CSV de lote. Voz y lenguaje natural quedan como arquitectura objetivo.

## Pendientes de personas
Clave de API de Anthropic (Dev A, antes del sábado 12:00); cuenta de despliegue gratuito; video de respaldo el sábado y regrabación el domingo de 07:00 a 10:00; dos ensayos con cronómetro.
