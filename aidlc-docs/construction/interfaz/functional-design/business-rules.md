# Reglas de la interfaz: U3

Fecha: 2026-10-16. Fuente: 7 respuestas del diseño funcional y 2 aclaraciones, más `requirements.md` (RF8, RF11, RF23 a RF26) y el diseño funcional del núcleo.

## Dirección y forma
- **Lenguaje visual alineado con blinka.co:** tema claro por defecto y tema oscuro "sala de control", **alto contraste y tipografía grande** pensados para proyectar (ver `design-system.md`). Se construye con la skill `frontend-design`; parte de la maqueta `demo-front`.
- **Barra lateral fija** con solo las secciones que aparecen en la demo: Marcador, Bandeja, Reglas, Guardián y Pentest y arena. El recibo se abre desde la Bandeja y el Marcador, no tiene sección propia.
- **Encabezado siempre visible:** ciclo de pagos, versión del mandato, selector de rol y botón Demo.
- **Solo español.**
- Ninguna señal depende solo del color: cada estado lleva texto o ícono (pagar, frenar, escalar).

## Pantalla inicial: Marcador
- Número dominante: **pagos fuera de reglas según el verificador independiente**, con su alcance: "0 en 18 casos" y, cuando la arena ya corrió, "y N variantes". Nunca un "0" suelto ni la palabra "garantía".
- Si el verificador independiente (U4) aún no está disponible, no se muestra un 0: se muestra el conteo del motor con la etiqueta "según el motor, sin verificador independiente".
- Una banda de **escaladas pendientes** que lleva a la Bandeja.
- El set de 18 facturas visibles viene precargado.
- También se muestran: **dos cifras de aciertos** (de reglas y de extremo a extremo), autonomía, tasa de escalada innecesaria, desvíos conservadores y el **recuento de entradas verificadas**.
- **Costo, con dos números:** el costo de las lecturas guardadas (registrado al leerlas en local) y el costo de esta sesión, que en la app pública es USD 0 porque no llama a la API.

## Roles
Un selector de rol en el encabezado, con la etiqueta fija **"rol simulado"**. El rol queda en cada registro.

| Acción | Analista | CFO |
|---|---|---|
| Ver todo | Sí | Sí |
| Elegir una factura de muestra | Sí | Sí |
| Corregir un campo y reevaluar | Sí | No |
| Escalar al CFO | Sí | No (no hay otro rol) |
| Aprobar una escalada | **No** | Sí |
| Rechazar (con motivo) | No | Sí |
| Proponer un mandato nuevo | No | Sí |
| Contrafirmar un mandato | Sí | No |
| Promover un proveedor de sombra a autónomo | No | Sí |
| Aprobar una factura **frenada** | Nadie | Nadie |

El analista no ve los botones de aprobar y rechazar. Una factura frenada no muestra ninguna acción de aprobación para ningún rol.

## Bandeja del aprobador
- **Filtros:** Pendientes, Pagadas, Frenadas, Registradas (notas de crédito) y Todas, para poder abrir el recibo de cualquier decisión. Las pendientes van ordenadas por riesgo.
- Cada pendiente muestra la **razón en una frase** y **un botón principal** según el rol (CFO: Aprobar; analista: Corregir).
- Orden por riesgo: señales de fraude (R4, R8, R2b), luego monto (R6, R10), luego acuerdo (R5), luego lectura (R1), luego presupuesto (R9).
- **Vista previa de "qué cambia si apruebo":** presupuesto restante antes y después, acumulado del proveedor en el periodo y la lista de fallas que se aprobarían.
- Una escalada por presupuesto insuficiente (R9) **no ofrece aprobar**; ofrece rechazar o proponer un mandato.
- Una escalada por **falla de lectura** (R1: lecturas que no coinciden, sin segunda lectura o cita no encontrada) **no ofrece aprobar**; ofrece Corregir (analista) o rechazar (CFO).
- Aprobar y rechazar piden una nota; rechazar la exige.
- Se muestran los **campos originales de la factura**, no solo el resumen del modelo.

## Recibo
- Por defecto, un documento legible: una línea por regla con su evidencia, un sello de firma, la **versión del mandato** y el **rol**.
- Un conmutador abre la vista técnica. **El JSON mostrado es el mismo que se firmó.**
- Un botón **Verificar** recalcula la firma con la clave pública de la sesión y muestra el resultado.
- La llave de demo no va en el repositorio; la sesión genera la suya.
- Etiquetas visibles: "firma de demo" y, en la app pública, "lectura guardada".

## Reglas y autonomía por proveedor
- La sección Reglas muestra el mandato vigente y sus parámetros, y una **lista de proveedores con su nivel de autonomía** (autónomo bajo reglas o sombra).
- Solo el CFO puede promover un proveedor de sombra a autónomo.

## Cierre del ciclo
- En el Marcador, el botón **Cerrar ciclo y exportar la conciliación** está habilitado solo cuando todas las escaladas tienen una acción humana, y solo para el CFO.

## Guardián
- Seis verificaciones en orden, con el motivo del rechazo y las siguientes marcadas "no evaluada".
- Ataques disponibles: alterar el recibo, pedir un monto mayor, enviar sin aprobación humana, modificar la factura original, usar un recibo de un mandato anterior y reenviar un recibo ya usado.

## Pentest y arena
- Pentest **determinista por código**, en vivo, desde el mandato v1. Si encuentra un hueco, ofrece el arreglo y el flujo de dos firmas (el CFO propone, el analista contrafirma); luego se vuelve a probar con v2.
- Los intentos que propuso un agente atacante de antemano se muestran etiquetados "estrategias grabadas".
- La arena muestra lanzadas, pagos fuera de reglas según el verificador independiente, y el tiempo. Semilla fija y visible por defecto, con un control para probar otra; la pantalla indica qué no prueba. Nunca dice "garantía".

## App pública
- **Estado propio por visitante:** cada sesión parte de una copia del set base inmutable, con su propio par de claves. Aprobar, corregir y reiniciar no tocan nada compartido.
- **Reiniciar** vuelve al set original.
- No se llama a la API de Claude. "Subir una factura nueva" es un selector que simula la carga con **muestras nuevas ya extraídas** (la lectura se hizo en local con la API real y se congeló), incluido un tipo no soportado que termina en ESCALAR. Etiqueta visible: "lectura guardada". La lectura en vivo existe solo en local y en el video.

## Modo guiado (botón Demo)
Cinco pasos, con la flecha derecha para avanzar, la izquierda para retroceder y Esc para salir en cualquier momento. El estado es reiniciable, e **iniciar la guía reinicia la sesión** (con confirmación) para que el guion parta siempre del mismo punto.
1. **Marcador:** el set corre y se ve el "0 en N casos".
2. **Recibo de la factura con instrucción oculta:** se lee como lo haría un gerente.
3. **Guardián:** se altera un recibo y se rechaza.
4. **Pentest y arena:** el hueco de las facturas partidas, el mandato v2 y el reintento.
5. **Rol CFO:** aprueba una escalada y el guardián autoriza la orden. El cierre del ciclo no es parte de la guía, porque exige que todas las escaladas tengan una acción humana.

## Errores y estados
- Si el servidor no responde, la pantalla lo dice. Nunca se muestra un éxito que no ocurrió.
- Los botones se deshabilitan mientras la acción está en curso, para evitar dobles envíos.
- **Toda salida se escapa:** los textos que vienen de facturas se insertan como texto, nunca como HTML.

## Supuestos a confirmar
1. **Rechazar es del CFO**, y "escalar" es una acción del analista hacia el CFO. Antes el diseño del núcleo dejaba esas acciones sin dueño por rol.
2. **Contrafirma en la demo guiada:** el paso 4 exige dos roles. Si no cabe en el tiempo, la propuesta del CFO llega precargada y solo se muestra la contrafirma del analista.
3. **Verificar la firma en el navegador** con la clave pública depende de que el navegador sostenga el algoritmo elegido. Está sin verificar; si no, se verifica con un endpoint del servidor.
4. **Sesión por visitante:** es un requisito nuevo para U1 (copia del set y par de claves por sesión, y reinicio). Ver RF27 en `requirements.md`.
5. **Roles simulados, no autenticación real.** RF19 pedía una aprobación firmada por un usuario autenticado; en la demo el "usuario" es la sesión más el rol elegido. Se declara en la interfaz y en el pitch: la separación de funciones se demuestra con roles simulados.
6. **Firmador separado frente a claves por sesión.** RF17 pide un firmador fuera del servidor web; RF27 pide un par de claves por sesión. En el servicio gratuito de la app pública, las claves de sesión viven en el mismo proceso, y se declara como limitación. El firmador separado se muestra en local y en el video.
7. **Tiempo del paso 4 de la guía** (pentest, arena y dos firmas): puede no caber en los tres minutos. Si no cabe, la arena pasa a ser opcional y se muestra su resultado ya calculado.
