# Reglas de negocio: U4 Evaluación

Fecha: 2026-10-16. Fuente: 6 respuestas del diseño funcional, el diagnóstico de los tres expertos, `requirements.md` (RF12, RF20, RF21) y los diseños aprobados de núcleo, lectura e interfaz.

## Principios
1. **Independencia:** nada de lo que evalúa se calcula con el código evaluado. Los esperados y el verificador salen del texto de las reglas.
2. **Honestidad del reporte:** cada cifra lleva su alcance y lo que no prueba. Un fallo se muestra como fallo.
3. **Reproducibilidad:** toda corrida registra semilla, versión del mandato y huella del código evaluado.
4. Ninguna cifra dice "garantía". Se dice "0 en N entradas verificadas".

## Set y veredictos esperados
- Cada factura lleva **dos esperados**: el **de reglas** (con la factura canónica correcta) y el **de extremo a extremo** (con las limitaciones de lectura según el canal).
- Ambos se escriben **a mano, antes de generar las lecturas**, por quien lee **solo el texto de las reglas** (sin acceso al motor ni a `motor.js`). Ninguno sale del motor.
- Los esperados actuales de `datos/esperado.json` se **reescriben**: el subagente que los creó los verificó ejecutando el motor, y en la factura 17 acomodó la confianza para que escalara. Las diferencias entre el esperado reescrito y el actual se revisan a mano, una por una.
- **Facturas ocultas:** las 4 existentes se **sellan con una huella** (SHA-256 de cada archivo y del esperado) antes de la primera corrida. El marcador muestra ambas cifras: aciertos de reglas y de extremo a extremo.

## Verificador independiente
- Módulo propio que **no importa el motor** y se escribe desde el texto de las reglas y de los mandatos v1 y v2.
- **Reconstruye el estado desde el registro** (decisiones y reservas), no desde la memoria del motor, **y además lo rederiva repitiendo la secuencia de entradas con sus propios veredictos**. Si su estado y el del registro difieren, es un hallazgo. Usar solo el registro heredaría los errores del motor.
- **Recalcula todo el veredicto** de cada entrada. Aplica al set y a las variantes de la arena.
- Clasifica cada diferencia con el motor:
  | Clase | Definición | Debe ser |
  |---|---|---|
  | **Pago indebido** | El motor dice PAGAR y el verificador no | 0 |
  | **Frenada escalable** | El motor dice ESCALAR y el verificador dice FRENAR (una persona podría aprobar lo que debía bloquearse) | 0 |
  | **Desvío conservador** | El motor es más estricto que el verificador (orden de severidad: PAGAR o REGISTRAR, ESCALAR, FRENAR) | Se cuenta, no es una falla de seguridad |
  | **Otra diferencia** | Cualquier otra | Se investiga |
- El Marcador muestra el **recuento de entradas verificadas**.

## Arena de ataques (dos niveles, sin llamar al modelo)
- **Nivel 1:** mutaciones de campos de la factura canónica, aleatorias y dirigidas a los bordes (umbral menos una unidad menor, tolerancias, ventanas, moneda sin tasa, redondeos).
- **Nivel 2:** mutaciones del **texto original** contra las **lecturas guardadas**, pasando por la cita de evidencia y la segunda lectura determinista (cambiar dígitos, cambiar separadores, intercambiar el nombre del proveedor, insertar texto con instrucciones, quitar un campo, usar otro idioma).
- **Semilla fija y visible por defecto**, con un control para probar otra. El recuento es visible.
- El oráculo es el **verificador independiente**. En el nivel 2 comprueba además que todo PAGAR tenga su monto, moneda, número y proveedor respaldados en el texto mutado según su propia lectura; si no, es un pago indebido.
- **Pentest y arena corren sobre una copia temporal** del estado de la sesión: parten de él, pero no modifican su registro ni los números del Marcador.
- La pantalla indica **qué no prueba**: la lectura real del modelo, PDFs reales, la concurrencia y el comportamiento del servidor.

## Pentest por código
- **Seis estrategias fijas**, cada una con su resultado esperado escrito **antes** de correrla:
  1. Partir en facturas bajo el umbral del mismo proveedor.
  2. Una factura justo bajo el umbral.
  3. Redondeo de moneda que cruza el umbral.
  4. Número de factura reformateado (duplicado).
  5. Proveedor nuevo con un pago pequeño y luego uno grande.
  6. Cambio de cuenta después de una aprobación.
- Se ejecutan sobre el **estado de la sesión** y se comparan con el verificador independiente.
- Un hueco encontrado **se corrige o se documenta**. El antes y el después se muestran **con la misma semilla**.
- Se parte del mandato v1 (sin el tope acumulado); la estrategia 1 debe encontrar el hueco y v2 debe cerrarlo.
- Las estrategias que propuso un agente atacante de antemano se guardan con fecha, se **revisan por una persona** antes de incluirlas y se muestran como grabadas. Ninguna se ejecuta en vivo.

## Pruebas de mutación del motor
- **Un mutante manual por regla** (R1 a R10, condición quitada o invertida), más mutantes de: orden de agregación, fallo cerrado y registro de solo adición.
- Se aplican sobre una **copia temporal** del código.
- Cada mutante debe **hacer fallar al menos una prueba**, y se registra cuál.
- Un mutante que sobrevive es un **hallazgo**: se corrige o se documenta como equivalente. El recuento se muestra y se puede repetir.

## Otras pruebas a cargo de U4
- **Fallas del extractor:** rechazo del modelo, salida truncada, JSON inválido, tiempo agotado, 4xx y tope de gasto; en todas, el resultado esperado es ESCALAR con motivo.
- **Carrera de presupuesto:** varias solicitudes concurrentes contra el mismo presupuesto; nunca se excede.
- **Invariante por tipo de documento**, incluido que un veredicto **REGISTRAR** nunca lleva orden de pago. Lo cubren una prueba del invariante, un mutante (permitir una orden para REGISTRAR) y una mutación de la arena.

## Facturas ocultas: política
- La política se fija **antes** de correr, y las huellas de las facturas y del esperado se registran antes.
- Se corren **una vez, al final**, y se reportan **tal cual**.
- Cada fallo se diagnostica: **defecto, regla ambigua, limitación de lectura o esperado erróneo**.
- Si se corrige algo, se reportan **ambas corridas** con fecha y versión, y se avisa de que la segunda ya no es ciega.
- Un pago indebido en la primera corrida se muestra como tal.

## Reporte
Cada corrida escribe un `resultados.json` con semilla, versión del mandato, huella del código, recuentos y la clasificación por caso. El Marcador lo lee.

## Supuestos a confirmar
1. **Hay 4 ocultas, no 3.** Se sellan las cuatro y las cuatro son la evaluación ciega.
2. **Semilla fija por defecto**, y una semilla variable solo como control opcional (la interfaz decía "variable"; ya está ajustada).
3. **Quién reescribe los esperados:** un subagente distinto al que generó las facturas, con acceso solo al texto de las reglas y a las facturas, nunca al motor ni al código.
4. **La reconstrucción del estado desde el registro** exige que el formato del registro de U1 sea estable: se fija en el contrato.
5. **El nivel 2 de la arena** depende de las lecturas guardadas de U2 (caché y muestras).
6. **El verificador no prueba la lectura del modelo:** eso queda fuera y se dice en pantalla.
7. **La ciega es respecto a quienes afinan el motor.** Las facturas ocultas las generó un subagente que conocía las reglas de la maqueta, así que no son una muestra independiente del diseño. Se reporta así.
8. **Redondeo:** la estrategia 3 del pentest y el verificador necesitan una regla explícita de redondeo en la conversión a la moneda base. Se añadió al núcleo (redondeo al alza al comparar contra un tope o un umbral).
9. **Prioridad dentro de U4:** P0, esperados reescritos, verificador y corrida del set. P1, pentest y arena de nivel 1. P2, arena de nivel 2, mutación, fallas del extractor y carrera de presupuesto.
