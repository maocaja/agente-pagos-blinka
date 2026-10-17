# Personas y qué esperan encontrar en la aplicación

Fecha: 2026-10-17. Personas inferidas del reto y de los roles del producto; NO verificadas con entrevistas. Sirven para decidir qué va primero en cada pantalla.

## 1. Directora financiera o tesorera (compra y decide)
- **Quién es:** responsable del dinero de la empresa; firma los mandatos y aprueba lo que se escala.
- **Teme:** ser la titular de un pago fraudulento o de un pago fuera de política, y que el agente "haga algo" sin que nadie lo vea.
- **Quiere:** pagar menos a mano sin perder control; poder explicarle a su junta por qué se pagó o no.
- **Lo primero que busca (5 segundos):** cuánto se pagó, cuánto se frenó, cuánto espera su aprobación, y que nada salió de las reglas.
- **Espera encontrar:** una banda de resumen en Decisiones; el panel "Espera aprobación" con la razón en una frase y los botones Aprobar y Rechazar; las reglas que ella definió (Reglas) y qué cambia si las modifica (vista previa).
- **Desconfía si:** ve una cifra sin su alcance, o un botón que aprueba sin reevaluar.

## 2. Analista de cuentas por pagar (usa todos los días)
- **Quién es:** recibe facturas por correo, chat y PDF; hoy las revisa a mano.
- **Teme:** que el agente frene de más y le llene la bandeja de falsas alarmas, o que pague algo que luego le reclamen a ella.
- **Quiere:** que cada escalada traiga el motivo escrito y qué hacer, sin abrir el código ni preguntar.
- **Lo primero que busca:** la lista de pendientes con proveedor, monto y razón; abrir una y ver el documento original junto a lo que el agente leyó.
- **Espera encontrar:** Bandeja (original junto a lo leído), Decisiones con explicación y "qué hacer", el recibo legible, y el chip de veredicto con palabra, no solo color.
- **Desconfía si:** la razón es genérica ("no cumple reglas") o no se ve qué dato leyó el agente.

## 3. Auditor o responsable de riesgo (bloquea o avala)
- **Quién es:** persona que debe poder demostrar, meses después, quién decidió qué y con qué regla.
- **Teme:** un sistema que se audita a sí mismo.
- **Quiere:** verificar sin depender de nosotros.
- **Lo primero que busca:** quién decidió, con qué regla y qué versión del mandato, quién aprobó, y cómo verificarlo por su cuenta.
- **Espera encontrar:** el recibo con regla, versión, hora y firma; el botón "Verificar"; el paquete de auditoría con el script que valida las firmas fuera de la app; el marcador con "lo que esta cifra no prueba"; el pentest y la mutación como evidencia.
- **Objeciones previstas:** "el recibo lo firma el mismo sistema" y "el verificador es suyo". Respuesta visible: clave pública, script independiente y verificador escrito sin leer el motor.

## 4. Jurado de la hackathon (solo ve el video y el pitch)
- **Quién es:** evalúa autonomía, seguridad y explicabilidad; un pago indebido descalifica. No usa la aplicación.
- **Lo primero que busca:** una historia clara en 30 segundos y una prueba de que no se deja engañar.
- **Espera encontrar en pantalla durante el video:** la trampa y su motivo escrito, el recibo alterado rechazado por el guardián, el ataque con v1 contra v2 y la cifra con su alcance.

## Qué debe ver cada persona primero, por pantalla
| Pantalla | Qué debe decir sin hacer clic | Persona principal |
|---|---|---|
| Decisiones | Cuántos documentos, pagados, frenados, escalados y pendientes; cada fila con proveedor, monto, veredicto y razón | Directora, analista |
| Detalle y recibo | Qué regla decidió, qué hacer, versión del mandato y cómo verificar | Analista, auditor |
| Bandeja | El documento original (correo, chat, PDF, foto) junto a lo leído | Analista |
| Reglas | Las reglas de la empresa y qué cambia si las modifica | Directora |
| Marcador | La cifra con su alcance y lo que no prueba | Auditor, jurado |
| Ataque | Qué se intentó, qué pasó con v1 y con v2 | Auditor, jurado |

## Brechas actuales frente a lo que esperan
- Decisiones abre vacía y las sesiones se perdían entre páginas (se corrige en la Ola 12).
- El auditor no puede filtrar decisiones por regla ni ver quién aprobó en la lista; hoy lo ve en el recibo.
- No hay una vista "pendientes de aprobación" como lista propia para la directora; está dentro del detalle.
- Las personas no se han validado con usuarios reales: es la primera pregunta para cualquier entrevista posterior.

## Tareas completas por persona
Ver `construction/interfaz/functional-design/recorridos.md`: el analista contrasta el original con lo leído y prepara la resolución; el CFO la resuelve y ve el historial; el auditor reconstruye la decisión y verifica el recibo fuera de la aplicación; el jurado sigue esos recorridos en el video.
