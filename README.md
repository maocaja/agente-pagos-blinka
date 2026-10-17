# Agente de pagos con garantía (Reto Blinka)

Un agente lee facturas (PDF, escaneado, foto, correo, chat, XML fiscal, CSV) y un motor de reglas determinista decide PAGAR, FRENAR, ESCALAR o REGISTRAR. Cada decisión queda en un recibo firmado y verificable, y un guardián en el punto de pago se niega sin un recibo válido. No se mueve dinero real.

Entrega: domingo 2026-10-18, 12:00 (se congela a las 10:00).

## Dónde mirar
- Arquitectura y alcance: `docs/arquitectura.html` y `aidlc-docs/inception/architecture-target-vs-mvp.md`.
- Guion del video: `aidlc-docs/inception/demo-script.md` y paso a paso en `aidlc-docs/inception/demo-operativo.md`.
- Estado del desarrollo: `aidlc-docs/aidlc-state.md` y `aidlc-docs/construction/tandas.md`.
- Reglas del proyecto: `CLAUDE.md`. Contrato de la API: `contrato/` (versión 1.1.0-rc5).

## Carpetas
| Carpeta | Contenido |
|---|---|
| `nucleo/` | Motor de reglas, recibo y firma, guardián, libro de reserva y nonce, API |
| `lectura/` | Adaptadores por formato, extractor con prompt versionado, detector de instrucciones, lecturas guardadas |
| `interfaz/` | Pantallas (Tailwind compilado y Alpine) y servidor simulado |
| `evaluacion/` | Verificador independiente, pentest, arena, corrida del set |
| `datos/` | Registro maestro, facturas de prueba, documentos multicanal simulados, esperados |
| `contrato/` | Esquemas y OpenAPI; manda sobre cualquier otro documento |
| `docs/` | Páginas públicas (guía de estilo, arquitectura, modelo canónico) |
| `aidlc-docs/` | Requisitos, diseños, planes y registro de avance |

## Ejecutar
```
source .venv/bin/activate
python3 verify.py                 # pruebas y calidad
uvicorn nucleo.api.principal:app  # API y interfaz en http://localhost:8000
```
Sin `ANTHROPIC_API_KEY` la app usa lecturas guardadas (etiquetadas en la interfaz). Con la variable definida pasa a lectura en vivo. Ninguna prueba usa red ni modelos.

## Alcance
El set de pruebas es sintético. Las cifras (por ejemplo "0 pagos indebidos" en la arena) valen para las entradas probadas; no se probó la lectura real del modelo ni los documentos originales mutados.
