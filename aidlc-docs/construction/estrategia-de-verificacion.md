# Estrategia de verificación

Fecha: 2026-10-17. Respuesta a: pocas pruebas, no miles, con un archivo `verify` que pruebe de forma determinista.

## Principio
Pocas pruebas, cada una atada a un riesgo del diseño, y **un solo comando** (`python3 verify.py`) que las corre igual todas las veces. Una prueba que a veces pasa y a veces no vale menos que ninguna.

## Presupuesto de pruebas
Tope duro: **200 en total**. `verify.py` marca "EXCEDE_PRESUPUESTO" si una unidad pasa de su máximo. Los límites viven en `verify.budget.json` y se cambian de común acuerdo.

| Unidad | Objetivo | Máximo | Qué cubre |
|---|---|---|---|
| U1 Núcleo | 67 | 80 | 11 reglas x 3 casos (cumple, falla, borde) = 33; precedencia y falla cerrado 5; tipos y REGISTRAR 4; recibo y firma 4; guardián 8; reserva y concurrencia 3; registro de solo adición 2; contrato de la API 8 |
| U2 Lectura | 30 | 40 | Cascada 5; verificaciones de lectura 6; segunda lectura 6; fallas simuladas de la API 6; proveedor 3; adaptadores y normalización 4 |
| U3 Interfaz | 12 | 20 | Escape de salida 3; permisos por rol 4; aprobar con reevaluación 2; modo público de solo lectura 2; la guía reinicia 1 |
| U4 Evaluación | 45 | 60 | Set de 18 casos (una prueba parametrizada) 18; verificador 10; pentest 6; arena acotada 2; fallas del extractor 6; carrera de presupuesto 2; invariante por tipo 1 |
| Mutación (aparte) | 14 mutantes | n/a | Un mutante por regla (11), más orden de agregación, fallo cerrado y registro de solo adición; solo en la puerta de calidad |

- **Proporción:** unas 70% pruebas de reglas y de unidad, 20% de integración (API, guardián, registro) y 10% de extremo a extremo.
- **La arena de la demo (3.200 variantes) no corre en `verify`.** Dentro de `verify` la arena se acota a 500 variantes con semilla fija (`VERIFY_ARENA_MAX`).
- **Propiedades con Hypothesis:** como máximo tres, con 100 ejemplos cada una, en el perfil `verify`.
- **No se prueba:** getters, estilos, capturas de pantalla, ni la lectura real del modelo.

## Qué hace determinista a una prueba
| Fuente de azar | Cómo se elimina |
|---|---|
| Semilla | `VERIFY_SEED=7` y `PYTHONHASHSEED=0`; el `conftest.py` raíz fija `random` en cada prueba |
| Orden | Sin plugin de orden aleatorio (`-p no:randomly`); se ejecutan en el orden del archivo |
| Reloj | El código recibe el reloj por inyección; la fixture `ahora` fija 2026-10-17T12:00:00Z; `TZ=UTC` |
| Red | El `conftest.py` bloquea toda conexión salvo localhost; `NO_NETWORK=1` |
| Modelos | `verify` quita `ANTHROPIC_API_KEY` y similares del entorno; las pruebas usan lecturas congeladas |
| Estado | Una base de datos temporal por prueba; nada compartido entre pruebas |
| Propiedades | Perfil `verify` de Hypothesis: `derandomize=True`, `database=None`, `max_examples=100`, `deadline=None` |
| Firmas y nonces | Clave y nonce se inyectan; Ed25519 no usa aleatoriedad al firmar (fuente secundaria) |

## Qué hace `verify.py`
- `python3 verify.py`: corre las etapas que existan (contrato, cuatro unidades), las pendientes se muestran como PENDIENTE sin fallar.
- `python3 verify.py --gate`: puerta de calidad. Todo es obligatorio, incluida la mutación; **corre dos veces y compara los resultados prueba por prueba**; una diferencia es "NO_DETERMINISTA". Cero pruebas omitidas.
- `python3 verify.py --etapa <nombre>`: una sola etapa.
- Comprueba el presupuesto de pruebas por unidad y en total, y un tope de tiempo (300 s en total).
- Escribe `verify-report.json` (commit, conteos, segundos, problemas) y sale con 0 o 1.

**Cómo se probó `verify.py` (en una copia temporal):** detecta una prueba que usa la red, una que supera el presupuesto, una que falla y una inestable.

## Límites
- **Dos corridas no atrapan toda inestabilidad:** en 8 intentos, una prueba con 50% de fallo pasó las dos corridas una vez. Lo que previene la inestabilidad son las reglas de la tabla; la doble corrida es una red de seguridad.
- `verify` no prueba la lectura real del modelo (decisión de diseño) ni el aspecto de la interfaz; eso se revisa a mano y con Chrome DevTools MCP.
- El presupuesto es una decisión nuestra, no una norma.
- Las pruebas de U3 requieren definirse en su plan de código; con solo Python, cubren la lógica y el escape, no el navegador.

## Cuándo corre
- Al cerrar cada tanda: `python3 verify.py --etapa <unidad>`.
- Antes del congelamiento (domingo 10:00): `python3 verify.py --gate`, en verde.
- No corre en la app pública.

## Fuentes
- Hypothesis, configuración: `derandomize`, `database`, `max_examples`, `deadline` y perfiles (leída el 2026-10-17; solo se leyeron los primeros 100.000 de 132.564 caracteres): https://hypothesis.readthedocs.io/en/latest/reference/api.html
- Pruebas deterministas (semilla registrada, reloj inyectado, red bloqueada, estado aislado): tutoriales y guías, no documentación oficial de pytest: https://archman.dev/docs/anti-patterns-and-pitfalls/flaky-tests-and-non-determinism
- Ed25519 determinista (RFC 8032): fuentes secundarias; **no verificado** en la documentación oficial de `cryptography`.
- **No encontré una recomendación formal de un "comando verify único".** El patrón lo armamos a partir de estas piezas.
