# Set de datos sintetico

Todo es inventado: nombres, cuentas, NIT y correos (dominios .example).

- `facturas/`: 18 textos que simulan como llega cada factura (correo, chat, PDF, XML UBL, nota de credito, estado de cuenta).
- `esperado.json`: veredicto esperado por archivo, en el campo `orden` (importa: presupuesto, duplicados y acumulado dependen de las facturas previas).

## Parametros del esperado

Los de `PARAMS_INICIALES` de `demo-front/motor.js` (tope 10.000, umbral 3.000, presupuesto 9.000, tolerancia 5%, confianza 0,8) con el tope acumulado por proveedor ACTIVO en USD 3.000 (R10). Con R10 inactivo cambian fac-08, fac-10 y fac-13 (fac-08 pasaria a PAGAR).

## Como verificar

1. Extraer cada texto a los campos del contrato (`contrato/extraccion.schema.json`) y pasarlos a `evaluar()` en el orden indicado.
2. Comparar el veredicto con `esperado.json`. Las reglas que fallan se listan en `reglas_que_fallan`.

## Brechas conocidas del motor

- fac-07 (duplicado difuso): el motor paga; `veredicto_ideal` es ESCALAR segun el PRD.
- fac-17 (nota de credito): el motor no tiene tipo de documento; se escala solo porque se modela con confianza baja.
- fac-18 (estado de cuenta): se escala por suma de lineas distinta del saldo.
