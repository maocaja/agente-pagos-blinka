# Sistema de diseño de la interfaz (U3)

Fecha: 2026-10-17. Es la definición de colores, controles y componentes que usa el producto. La "página de controles" es `docs/design-system/guia-de-estilo.html`: una página viva con los controles y los componentes funcionando.

## Decisión de framework
**Tailwind CSS v4.3.3 compilado con su CLI, más Alpine.js 3.17.4.** Elegido entre cuatro opciones (CSS propio, daisyUI, React con Vite y shadcn, y esta).
- Tailwind da clases utilitarias para ir rápido; se compila **una vez** a un solo archivo CSS que se versiona; no hay Vite ni proceso de compilación en el servidor.
- El Play CDN de Tailwind es solo para desarrollo según su documentación (leída el 2026-10-17), por eso se compila.
- Alpine aporta la interactividad con directivas en el HTML; la versión se fija y el archivo se copia al repositorio para no depender de un CDN durante la demo.
- Los componentes se estilan con tokens propios, así que no se parece a una biblioteca genérica.

## Dirección visual
Sala de control oscura, casi monocromática (tinta azulada y texto hueso). El color queda para dos cosas: los cuatro veredictos y el sello del recibo. El recibo es **papel claro sobre la sala oscura**: es el protagonista. Un solo movimiento: el sello que se estampa al pulsar Verificar.

## Tokens (en `docs/design-system/tokens.css`)
| Grupo | Valores |
|---|---|
| Superficies | lienzo `#0D1520`, panel `#131F2E`, elevado `#1A293B`, línea `#2C3F55` (solo separadores), línea fuerte `#5B7694` (bordes de controles) |
| Texto | principal `#EAF0F7`, secundario `#A9B8CC`, terciario `#8497B0` |
| Veredictos | pagar `#3DDBA8`, frenar `#FF7A6B`, escalar `#FFB84D`, registrar `#94AEFF` |
| Papel y sello | papel `#EEF2F5`, texto `#14202E`, secundario `#4A5A6C`, línea `#C6D0DA`, sello `#7D5F18`, latón `#C9A24A` |
| Tipografía | Hanken Grotesk (interfaz), Source Serif 4 (solo el recibo), JetBrains Mono (solo la vista técnica) |
| Escala | cuerpo 18 px, apoyo 15 px (mínimo), subtítulo 22, sección 28, título 40, dominante 96 |
| Forma | radios 6 px (controles), 14 px (paneles), 2 px (papel) |

Los contrastes están calculados (fórmula de luminancia relativa de WCAG 2.x) y listados en la guía. La línea decorativa (1,7:1) no es nunca el único indicador de un límite; los bordes de controles usan la línea fuerte (3,1 a 3,9:1).

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
