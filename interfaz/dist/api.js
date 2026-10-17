// Cliente unico de la API: sesion, rol e Idempotency-Key en cada POST.
const api = {
  sesion: null,
  rol: "analista",
  async pedir(metodo, ruta, cuerpo) {
    const cabeceras = { "X-Rol": this.rol };
    if (this.sesion) cabeceras["X-Sesion-Id"] = this.sesion;
    if (metodo === "POST") cabeceras["Idempotency-Key"] = crypto.randomUUID();
    if (cuerpo !== undefined) cabeceras["Content-Type"] = "application/json";
    const r = await fetch(ruta, { method: metodo, headers: cabeceras, body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo) });
    const datos = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(datos.mensaje || datos.detail || `Error ${r.status}`);
    return datos;
  },
  async iniciar() {
    const s = await this.pedir("POST", "/api/sesion");
    this.sesion = s.sesion_id;
    return s;
  },
  decisiones: () => api.pedir("GET", "/api/decisiones?estado=todas"),
  detalle: (id) => api.pedir("GET", `/api/decisiones/${encodeURIComponent(id)}`),
  recibo: (id) => api.pedir("GET", `/api/recibos/${encodeURIComponent(id)}`),
  verificarRecibo: (id) => api.pedir("POST", `/api/recibos/${encodeURIComponent(id)}/verificar`),
  guardian: (orden, recibo) => api.pedir("POST", "/api/guardian/verificar", { orden, recibo, aprobacion: null }),
};
