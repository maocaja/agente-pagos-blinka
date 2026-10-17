# Nucleo: arranque

Desde la raiz del repositorio, con el entorno virtual activo:

    uvicorn nucleo.api.principal:app --host 0.0.0.0 --port ${PORT:-8000}

- `/api/*` es la API del contrato; `/` sirve `interfaz/dist` si la carpeta existe (compilarla antes del despliegue).
- `/api/marcador` incluye `evaluacion/salida/resultados-set.json` tal cual cuando existe.
- Rol simulado por la cabecera `X-Rol` (analista o cfo); aprobar y rechazar son del CFO. Quien cargo la factura
  (cabecera `X-Rol` en `POST /api/facturas`) no la aprueba ni la rechaza.
