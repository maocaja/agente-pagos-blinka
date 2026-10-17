const VEREDICTOS = {
  PAGAR: { icono: "✓", clase: "chip-pagar", texto: "Pagar" },
  FRENAR: { icono: "✕", clase: "chip-frenar", texto: "Frenar" },
  ESCALAR: { icono: "▲", clase: "chip-escalar", texto: "Escalar" },
  REGISTRAR: { icono: "●", clase: "chip-registrar", texto: "Registrar" },
};
const ESTADO_VERIF = {
  ok: { icono: "✓", texto: "Cumple", clase: "text-pagar" },
  falla: { icono: "✕", texto: "Falla", clase: "text-frenar" },
  no_evaluada: { icono: "–", texto: "No evaluada", clase: "text-texto-3" },
};

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
  mandato: () => api.pedir("GET", "/api/mandato"),
  proveedores: () => api.pedir("GET", "/api/proveedores"),
  marcador: () => api.pedir("GET", "/api/marcador"),
  muestras: () => api.pedir("GET", "/api/muestras"),
  cargarMuestra: (id) => api.pedir("POST", `/api/muestras/${encodeURIComponent(id)}/cargar`),
  pentest: (mandato_base, semilla) => api.pedir("POST", "/api/pentest/ejecutar", { mandato_base, semilla }),
  arena: (semilla) => api.pedir("POST", "/api/arena/ejecutar", { semilla }),
  aprobar: (id, nota) => api.pedir("POST", `/api/decisiones/${encodeURIComponent(id)}/aprobar`, { nota }),
  rechazar: (id, nota) => api.pedir("POST", `/api/decisiones/${encodeURIComponent(id)}/rechazar`, { nota }),
  previaMandato: (parametros) => api.pedir("POST", "/api/mandato/previa", { parametros }),
  guardian: (orden, recibo) => api.pedir("POST", "/api/guardian/verificar", { orden, recibo, aprobacion: null }),
};

// Formato de dinero en unidades menores (texto entero); el exponente sale de monedas.json.
const dinero = {
  exponente: (monedas, moneda) => (monedas[moneda] || { exponente: 2 }).exponente,
  entero(menor, exp) {
    const s = String(menor).padStart(exp + 1, "0");
    return s.slice(0, s.length - exp).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  },
  centavos: (menor, exp) => (exp ? "," + String(menor).padStart(exp + 1, "0").slice(-exp) : ""),
  texto: (menor, moneda, monedas) => { const e = dinero.exponente(monedas, moneda); return moneda + " " + dinero.entero(menor, e) + dinero.centavos(menor, e); },
};
