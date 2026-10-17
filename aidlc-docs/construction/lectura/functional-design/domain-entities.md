# Entidades del dominio: U2 Lectura

| Entidad | Atributos principales | Notas |
|---|---|---|
| **Documento** | id, hash del archivo, canal, formato, texto local (si existe), recibido en | El archivo crudo es inmutable |
| **AdaptadorDeEntrada** | nombre, formatos que soporta | Se registra; uno nuevo no toca el núcleo |
| **LecturaDelModelo** | documento, modelo, tipo de documento, campos, cita de evidencia por campo, confianza por campo, tokens, reintentos | Salida estructurada validada contra el esquema |
| **SegundaLectura** | documento, monto, moneda, número, totales, origen (parser o regla) | Determinista; puede quedar "sin segunda lectura" |
| **ResultadoDeVerificacion** | documento, esquema, dinero presente, suma de líneas, cita de evidencia, tipo, concordancia entre lecturas | Cada una con estado y evidencia |
| **EventoDeLectura** | documento, modelo, tokens, costo, reintentos, motivo de falla, hora | Alimenta el contador y el recibo |
| **EntradaDeCache** | hash, versión del esquema, modelo, lectura, costo registrado | La lectura guardada se sirve sin llamar a la API |
| **ProveedorAsignado** | documento, proveedor del registro maestro o ninguno, método (id fiscal o nombre), pista aproximada | La pista nunca decide |
| **FacturaCanonica** | ver contrato | Producto final de U2, validado contra el esquema |
| **MuestraNueva** | tipo, lectura congelada, veredicto esperado registrado antes de generarla | Solo para la app pública |
| **ConfiguracionDeLectura** | modelos, `max_retries`, `tope_gasto_corrida`, versión del esquema | Nada quemado en el código |

## Relaciones
`Documento 1—0..1 LecturaDelModelo`, `Documento 1—0..1 SegundaLectura`, `Documento 1—1 ResultadoDeVerificacion`, `Documento 1—n EventoDeLectura`, `Documento 1—0..1 EntradaDeCache`, `Documento 1—0..1 ProveedorAsignado`, `Documento 1—0..1 FacturaCanonica`.
