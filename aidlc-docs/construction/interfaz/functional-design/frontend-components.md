# Componentes de la interfaz: U3

HTML y JavaScript sin proceso de compilación, servido por el backend. Los endpoints son una propuesta que el contrato de U1 confirma o corrige.

## Jerarquía
```
App
├── Encabezado: ciclo, versión del mandato, SelectorDeRol (con "rol simulado"), BotónDemo, BotónReiniciar
├── BarraLateral: Marcador, Bandeja, Reglas, Guardián, Pentest y arena
├── Vistas
│   ├── Marcador
│   │   ├── NúmeroDominante (pagos fuera de reglas con su alcance)
│   │   ├── BandaDePendientes (enlace a la Bandeja)
│   │   ├── Métricas (aciertos, autonomía, escalada innecesaria, verificador independiente, costo de lecturas guardadas y de la sesión)
│   │   └── CierreDeCiclo (solo CFO, habilitado con todas las escaladas atendidas)
│   ├── Bandeja
│   │   ├── ListaDeDecisiones (filtros: pendientes, pagadas, frenadas, registradas, todas; las pendientes por riesgo)
│   │   ├── DetalleDeFactura: CamposOriginales, Recibo, AccionesPorRol, VistaPreviaDeAprobación
│   │   └── SelectorDeMuestras (simula la carga; etiqueta "lectura guardada")
│   ├── Reglas: MandatoVigente, ParámetrosEditables, PropuestaDeMandato, Contrafirma, ProveedoresYAutonomía (nivel y botón Promover, solo CFO)
│   ├── Guardián: SelectorDeFactura, ReciboYOrden, BotonesDeAtaque, SeisVerificaciones
│   └── PentestYArena: PentestPorCódigo, EstrategiasGrabadas, Arena, FlujoDeDosFirmas
├── Recibo (componente compartido): VistaLegible, Sello, ConmutadorTécnico, BotónVerificar
├── GuíaDeDemo (capa sobre la app): 5 pasos, teclado
└── Avisos: errores, estados de carga, etiquetas ("rol simulado", "firma de demo", "lectura guardada")
```

## Estado
| Estado | Dónde vive | Notas |
|---|---|---|
| Sesión (id, claves públicas) | Servidor, cookie de sesión | Copia del set y par de claves por visitante |
| Decisiones, recibos, mandato, reservas | Servidor | La interfaz no calcula decisiones |
| Rol actual | Navegador, enviado en cada acción | Se registra en el servidor; es simulado |
| Vista actual, factura abierta, conmutador técnico | Navegador | Se pierde al recargar sin problema |
| Paso de la guía | Navegador | Reiniciable |

## Endpoints que consume (propuesta)
| Acción | Endpoint |
|---|---|
| Estado del ciclo y marcador | `GET /api/marcador`, `GET /api/ciclo` |
| Lista y detalle de decisiones | `GET /api/decisiones`, `GET /api/decisiones/{id}` |
| Acciones sobre una escalada | `POST /api/decisiones/{id}/aprobar`, `/corregir`, `/rechazar`, `/escalar` |
| Vista previa de aprobar | `GET /api/decisiones/{id}/previa` |
| Mandato | `GET /api/mandato`, `POST /api/mandato/propuestas`, `POST /api/mandato/contrafirma` |
| Proveedores y autonomía | `GET /api/proveedores`, `POST /api/proveedores/{id}/promover` |
| Cierre del ciclo | `POST /api/ciclo/cerrar` (devuelve la conciliación para exportar) |
| Recibo y verificación | `GET /api/recibos/{id}`, `GET /api/clave-publica`, `POST /api/recibos/{id}/verificar` |
| Guardián | `POST /api/guardian/verificar` |
| Pentest y arena | `POST /api/pentest/ejecutar`, `POST /api/arena/ejecutar` |
| Muestras nuevas | `GET /api/muestras`, `POST /api/muestras/{id}/cargar` |
| Reinicio | `POST /api/sesion/reiniciar` |

## Reglas de implementación
- Todo texto de origen externo se inserta con `textContent`; ningún `innerHTML` con datos de facturas.
- Cada acción deshabilita su botón hasta recibir respuesta; las acciones llevan clave de idempotencia.
- El diseño parte de la maqueta `demo-front`, con la skill `frontend-design` para la identidad visual.
