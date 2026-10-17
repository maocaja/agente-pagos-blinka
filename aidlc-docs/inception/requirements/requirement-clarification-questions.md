# Preguntas de aclaración: Agente de Pagos con Garantía

Se detectaron tensiones entre respuestas del cuestionario de requisitos. No son contradicciones lógicas, pero cada una afecta el diseño y conviene cerrarla antes de pasar a las unidades de trabajo.

## Tensión 1: app pública con URL (P15: B) frente a clave de API sin conseguir (P6: C) y control de costo
Una app desplegada con URL pública que llame a la API de Claude permite que cualquiera con el enlace gaste el presupuesto. Además todavía no hay clave.

### Clarification Question 1
¿Cómo funciona la app desplegada para el jurado?

A) Modo guardado: usa las extracciones ya hechas del set y no llama a la API; la lectura en vivo se muestra solo en el video
B) Modo mixto: el set usa extracciones guardadas y una factura nueva llama a la API, protegido con un código de acceso y un tope de gasto
C) Modo en vivo: todo llama a la API, protegido con un código de acceso y un tope de gasto
D) Other (please describe after [Answer]: tag below)

[Answer]: A (modo guardado: usa las extracciones ya hechas del set y no llama a la API; la lectura en vivo se muestra en el video)

## Tensión 2: dónde se despliega (P15: B) no está definido

### Clarification Question 2
¿Dónde se despliega la app?

A) En un servicio gratuito de hospedaje de aplicaciones (el equipo elige cuál según lo que ya use)
B) En una máquina propia expuesta con un túnel temporal
C) En la nube de la cuenta que ya tenga el equipo técnico
D) Other (please describe after [Answer]: tag below)

[Answer]: A (servicio gratuito de hospedaje; el equipo técnico elige cuál)

## Tensión 3: la clave de API (P6: C) bloquea la lectura con Claude

### Clarification Question 3
¿Quién consigue la clave y para cuándo?

A) Una de las dos personas desarrolladoras, antes del sábado a las 12:00; mientras tanto se trabaja con extracciones escritas a mano
B) Alguien del equipo no técnico, antes del sábado a las 12:00
C) Si no hay clave el sábado, se construye todo con extracciones guardadas y la lectura en vivo queda fuera del alcance
D) Other (please describe after [Answer]: tag below)

[Answer]: A (una de las dos personas desarrolladoras, antes del sábado a las 12:00; mientras tanto, extracciones escritas a mano)
