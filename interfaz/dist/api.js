const VEREDICTOS = {
  PAGAR: { color: "text-pagar", icono: "✓", clase: "chip-pagar", texto: "Pagar", autonomia: "Autónomo bajo reglas" },
  FRENAR: { color: "text-frenar", icono: "✕", clase: "chip-frenar", texto: "Frenar", autonomia: "Frenada por las reglas" },
  ESCALAR: { color: "text-escalar", icono: "▲", clase: "chip-escalar", texto: "Escalar", autonomia: "Requiere una persona" },
  REGISTRAR: { color: "text-registrar", icono: "●", clase: "chip-registrar", texto: "Registrar", autonomia: "Solo registrada" },
};

// El servidor manda ISO UTC; se muestra HH:MM local, o el texto tal cual si no es una fecha.
function horaCorta(iso) {
  const d = new Date(iso);
  return isNaN(d) ? iso : d.toLocaleTimeString("es", { hour: "2-digit", minute: "2-digit", hour12: false });
}
const ESTADO_VERIF = {
  ok: { icono: "✓", texto: "Cumple", clase: "text-pagar" },
  falla: { icono: "✕", texto: "Falla", clase: "text-frenar" },
  no_evaluada: { icono: "–", texto: "No evaluada", clase: "text-texto-3" },
};

// sessionStorage con respaldo en memoria si el navegador lo bloquea.
const memoria = {
  datos: {},
  leer(k) { try { const v = sessionStorage.getItem(k); if (v) return JSON.parse(v); } catch { /* respaldo */ } return this.datos[k] ?? null; },
  guardar(k, v) { this.datos[k] = v; try { sessionStorage.setItem(k, JSON.stringify(v)); } catch { /* respaldo */ } },
  borrar(k) { delete this.datos[k]; try { sessionStorage.removeItem(k); } catch { /* respaldo */ } },
};

// Cliente unico de la API: sesion, rol e Idempotency-Key en cada POST.
const api = {
  sesion: null,
  rol: memoria.leer("rol") || "analista",
  mandato_version: "",
  lectura: null,
  cabeceras() {
    const c = { "X-Rol": this.rol };
    if (this.sesion) c["X-Sesion-Id"] = this.sesion;
    return c;
  },
  // Descarga con la sesion (un enlace directo no la envia) y entrega por blob.
  async descargar(ruta, nombre) {
    const r = await fetch(ruta, { headers: this.cabeceras() }).catch(() => null);
    if (!r || !r.ok) throw new Error(`No se pudo descargar ${nombre}${r ? ` (error ${r.status})` : ": no hay conexión con el servidor"}.`);
    const enlace = Object.assign(document.createElement("a"), { href: URL.createObjectURL(await r.blob()), download: nombre });
    document.body.append(enlace);
    enlace.click();
    enlace.remove();
    setTimeout(() => URL.revokeObjectURL(enlace.href), 1000);
  },
  async pedir(metodo, ruta, cuerpo) {
    const cabeceras = this.cabeceras();
    if (metodo === "POST") cabeceras["Idempotency-Key"] = crypto.randomUUID();
    if (cuerpo !== undefined) cabeceras["Content-Type"] = "application/json";
    const r = await fetch(ruta, { method: metodo, headers: cabeceras, body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo) });
    const datos = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(datos.mensaje || datos.detail || `Error ${r.status}`);
    return datos;
  },
  async iniciar() {
    let s = memoria.leer("sesion");
    this.sesion = s ? s.sesion_id : null;
    if (s) { try { await this.pedir("GET", "/api/mandato"); } catch { s = null; } }
    if (!s) {
      this.sesion = null;
      s = await this.pedir("POST", "/api/sesion");
      memoria.guardar("sesion", s);
      memoria.borrar("muestras");
      this.sesion = s.sesion_id;
    }
    this.lectura = s.lectura;
    this.mandato_version = s.mandato_version;
    document.dispatchEvent(new CustomEvent("sesion-lista"));
    return s;
  },
  async reiniciar() {
    await this.pedir("POST", "/api/sesion/reiniciar");
    memoria.borrar("muestras");
  },
  muestrasCargadas: () => memoria.leer("muestras") || {},
  // Una muestra se carga una sola vez por sesion: cargarla de nuevo se leeria como factura duplicada.
  async cargarUna(id) {
    const hechas = api.muestrasCargadas();
    if (!hechas[id]) { hechas[id] = (await api.cargarMuestra(id)).id; memoria.guardar("muestras", hechas); }
    return hechas[id];
  },
  // Por defecto solo el set curado de demo-set.json; todas=true acumula topes y repeticiones entre muestras.
  async cargarSet(avance, todas = false) {
    const todasLasMuestras = await api.muestras();
    const curado = todas ? null : (await (await fetch("demo-set.json")).json()).ids;
    const muestras = curado ? curado.map((id) => todasLasMuestras.find((m) => m.id === id) || { id, titulo: id }) : todasLasMuestras, fallos = [];
    for (const [i, m] of muestras.entries()) {
      avance(i + 1, muestras.length, m.titulo);
      try { await api.cargarUna(m.id); } catch (e) { fallos.push(m.titulo + ": " + e.message); }
    }
    return { total: muestras.length, fallos };
  },
  decisiones: () => api.pedir("GET", "/api/decisiones?estado=todas"),
  detalle: (id) => api.pedir("GET", `/api/decisiones/${encodeURIComponent(id)}`),
  recibo: (id) => api.pedir("GET", `/api/recibos/${encodeURIComponent(id)}`),
  verificarRecibo: (id) => api.pedir("POST", `/api/recibos/${encodeURIComponent(id)}/verificar`),
  ciclo: () => api.pedir("GET", "/api/ciclo"),
  mandato: () => api.pedir("GET", "/api/mandato"),
  proveedores: () => api.pedir("GET", "/api/proveedores"),
  marcador: () => api.pedir("GET", "/api/marcador"),
  muestras: () => api.pedir("GET", "/api/muestras"),
  cargarMuestra: (id) => api.pedir("POST", `/api/muestras/${encodeURIComponent(id)}/cargar`),
  pentest: (mandato_base, semilla) => api.pedir("POST", "/api/pentest/ejecutar", { mandato_base, semilla }),
  arena: (semilla) => api.pedir("POST", "/api/arena/ejecutar", { semilla }),
  aprobar: (id, nota) => api.pedir("POST", `/api/decisiones/${encodeURIComponent(id)}/aprobar`, { nota }),
  autorizar: (id) => api.pedir("POST", `/api/decisiones/${encodeURIComponent(id)}/autorizar`),
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
