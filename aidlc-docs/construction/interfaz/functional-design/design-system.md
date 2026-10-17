# Sistema de diseño de la interfaz (U3)

Fecha: 2026-10-17. Es la definición de colores, controles y componentes que usa el producto. La "página de controles" es `docs/design-system/guia-de-estilo.html`: una página viva (generada por `construir_guia.py`) con los controles y los componentes funcionando.

## Decisión de framework
**Tailwind CSS v4.3.3 compilado con su CLI, más Alpine.js 3.17.4.** Elegido entre cuatro opciones (CSS propio, daisyUI, React con Vite y shadcn, y esta).
- Tailwind da clases utilitarias para ir rápido; se compila **una vez** a un solo archivo CSS que se versiona; no hay Vite ni proceso de compilación en el servidor.
- El Play CDN de Tailwind es solo para desarrollo según su documentación (leída el 2026-10-17), por eso se compila.
- Alpine aporta la interactividad con directivas en el HTML; la versión se fija y el archivo se copia al repositorio para no depender de un CDN durante la demo.
- Los componentes se estilan con tokens propios, así que no se parece a una biblioteca genérica.

## Dirección visual
Alineada con el lenguaje visual público de blinka.co (CSS leído el 2026-10-17; no hay guía de marca oficial leída, no verificado como "marca"). Tema claro por defecto: papel cálido, tinta azulada, azul de acción, botones en píldora, cifras con centavos en gris, tipografía Inter. Tema oscuro "sala de control" para proyectar. El color propio queda para los cuatro veredictos y el sello. El recibo es papel blanco en ambos temas y es el protagonista. Un solo movimiento: el sello que se estampa al pulsar Verificar. No se usa el logotipo, el nombre como marca, la Inter propia de Blinka ni sus ilustraciones. Vocabulario de Blinka en componentes: cuenta en USD, rutas de pago (ACH, wire, SWIFT, Pix y TED; calcular la ruta es mejora posterior al MVP), back office.

## Tokens (fuente única: `docs/design-system/tokens.css`; componentes en `componentes.css`)
| Grupo | Claro | Oscuro |
|---|---|---|
| Superficies | lienzo `#F7F7F4`, panel `#FFFFFF`, elevado `#F0F2F4`, línea `#DEDFDC`, línea fuerte `#7C879A` | lienzo `#111720`, panel `#18202C`, elevado `#1F2A3A`, línea `#2A3547`, línea fuerte `#6580A0` |
| Texto | `#1C253A`, `#555B6A`, `#626977` | `#E9EDF1`, `#B2BBC7`, `#8E9AAD` |
| Acento | `#2A4BD0` (texto blanco) | `#B9C8FF` (texto `#111720`) |
| Veredictos | pagar `#0B7A55`, frenar `#B8321E`, escalar `#8F5700`, registrar `#5B3FC4` | `#3DDBA8`, `#FF7A6B`, `#FFB84D`, `#94AEFF` |
| Sello | `#8A6A1F` | `#C9A24A` |
| Papel (constante) | papel `#FFFFFF`, texto `#1C253A`, secundario `#555B6A`, sello `#8A6A1F` | igual |
| Tipografía | Inter (interfaz y recibo), Geist Mono (solo vista técnica) | igual |
| Escala | cuerpo 18 px, apoyo 15 px (mínimo), subtítulo 22, sección 28, título 42, dominante 96 | igual |
| Forma | controles 10 px, paneles 18 px, botones en píldora | igual |

`docs/design-system/construir_guia.py` calcula los contrastes (WCAG 2.x) al generar la guía y se niega a generarla si un texto baja de 4,5:1 o un borde de control de 3:1. La línea decorativa nunca es el único indicador de un límite.

## Inventario
| Controles | Componentes |
|---|---|
| Botón primario, secundario, de peligro y fantasma, con estados deshabilitado y cargando | Encabezado del ciclo; chip de veredicto (y modo sombra) |
| Selector de rol, con la etiqueta "rol simulado" | Número dominante del marcador; cifras y costo |
| Filtros de la bandeja | Fila de la bandeja; fila de regla |
| Campos de número con unidad, selección, interruptor, casillas, texto con error | Recibo con sello y vista técnica; verificaciones del guardián |
| Semilla de la arena | Resultado del pentest; proveedor y autonomía |
| | Aviso, cajón de detalle, confirmación y guía de la demo |
| Estados: vacío, cargando, error, sin permiso, vencido y "lectura guardada" | |

Cada componente de la guía corresponde a uno del árbol de `frontend-components.md`.

## Cómo se compila
```
npm install tailwindcss@4.3.3 @tailwindcss/cli@4.3.3
npx @tailwindcss/cli -i entrada.css -o guia.css --minify
```
`entrada.css` importa Tailwind y `tokens.css`. El resultado (22,6 KB) se versiona. La opción `--minify` existe en la CLI de la versión instalada (verificada con `--help`).

## Supuestos y avisos
- **"Página de controles":** se interpretó como una guía de estilo con los controles y componentes funcionando. Si te referías a otra cosa (por ejemplo, la pantalla Reglas del producto), dímelo.
- **Fuentes:** vienen de Google Fonts, con una familia de reserva. Si la demo se hace sin red, se ven con la de reserva; habría que copiarlas al repositorio.
- **Aviso de `npm audit`:** la CLI de Tailwind arrastra una vulnerabilidad de denegación de servicio en `braces`, solo al compilar con patrones de archivo maliciosos. Solo se compilan archivos propios y `node_modules` no se despliega.
- **La guía es una definición de diseño, no código de U3.** U3 copia los tokens y los componentes cuando se apruebe su plan de código.

## Componentes propuestos (2026-10-17, pendientes de aprobación)
Ver `direccion-visual.md` y el prototipo `docs/propuesta-pantalla-principal.html`: lateral corto con una acción primaria, banda de tres zonas separadas por líneas punteadas, barra segmentada, tabla de atención de dos líneas, panel comparativo registrado frente a recibido y línea de estado de tres pasos. Sin colores nuevos: se usan los tokens de la guía; el rojo se reserva para la diferencia que importa. Inter debe cargarse (hoy cae a la fuente del sistema).
