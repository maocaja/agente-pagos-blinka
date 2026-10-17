# Reparto de los desarrolladores (después de la Ola 2)

Fecha: 2026-10-17. Código ligero (`CLAUDE.md` 5c): se construye lo que sale en el video; el diseño completo queda documentado en `inception/architecture-target-vs-mvp.md`. Cada quien trabaja con su orquestador y sus ramas; los mandatos de ejemplo están en `construction/mandatos/`.

## Dev A: núcleo y despliegue (ramas `nucleo`, `evaluacion`)
Orden:
1. Revisar y mezclar la Ola 2 de núcleo (reglas, guardián, mandatos v1 y v2). Criterio: las 18 facturas coinciden con `datos/esperado.json`.
2. **Clave de API** de Anthropic en el entorno (nunca en el repositorio) y cuenta de despliegue gratuito. Antes del sábado 12:00.
3. Montar `interfaz/dist` desde la API del núcleo y desplegar una sola instancia.
4. Rutas restantes del video: `/api/marcador`, `/api/pentest/ejecutar`, `/api/arena/ejecutar`, `/api/mandato/propuestas`.
5. Evaluación (Ola 3): verificador independiente (otro agente, sin leer `nucleo/`), 6 estrategias de pentest, arena acotada con semilla, 5 mutantes solo en la puerta.

## Dev B: lectura e interfaz (ramas `lectura`, `interfaz`)
Orden:
1. Mezclar la Ola 2 de lectura (proveedor asignado) e interfaz (Decisiones y recibo con guardián).
2. **Set multicanal simulado** en `datos/documentos/`: un subagente Sonnet genera PDF con texto, PDF escaneado, foto con el cambio de cuenta del video, `.eml` con `Reply-To` distinto y adjunto, y chat. Los esperados los fija evaluación, no el generador.
3. Adaptadores en este orden de prioridad: PDF con texto, `.eml`, foto con doble lectura (Haiku y Sonnet), chat. Un archivo por adaptador, registrado en el registro de adaptadores. XML solo si sobra.
4. Extractor con el cliente de modelo (real y congelado), contador y tope de gasto. Prompts en archivos versionados (`lectura/prompts/extractor.vN.md`); cada extracción guarda versión, hash del prompt, modelo y costo. Con la clave de Dev A se congelan las lecturas reales.
5. Interfaz: pantalla de Reglas (solo lectura), marcador y escena del ataque, bandeja simulada con etiqueta visible, botón de guion que reinicia.

## Equipo no técnico
Pitch y video según `inception/demo-script.md` v3. Dos ensayos con cronómetro y versión de respaldo el sábado.

## Reglas comunes
Control del avance obligatorio (`CLAUDE.md`, seccion 4): al cerrar cada tanda, casillas del plan, fila en `tandas.md` y `aidlc-state.md` al dia, antes del commit y el merge; `python3 control.py` lo comprueba.
Cada uno mezcla `main` en su rama al empezar y al cerrar; el contrato (`contrato/`) solo cambia con acuerdo de los dos. Antes de congelar (domingo 10:00): `python3 verify.py --gate`.
