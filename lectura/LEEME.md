# Lectura: dependencias de los canales

- `pypdf` (instalado en el venv) extrae el texto local de los PDF y detecta los cifrados. Instalar con `pip install pypdf`.
- Correo y chat usan solo la biblioteca estandar.
- `extracciones_multicanal/` guarda las lecturas congeladas (`manual-congelada`) de los 16 documentos de `datos/documentos/`; el nombre es el del archivo sin extension.
- El `Reply-To` del correo queda en `evidencia.reply_to` (el contrato no tiene otro campo para ese dato).
