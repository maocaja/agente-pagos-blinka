// Componentes Alpine de Reglas, Marcador, Bandeja y Ataque. El servidor decide; aqui solo se muestra.
const PARAMETROS = [
  { k: "umbral_aprobacion_menor", texto: "Umbral de aprobación", tipo: "dinero" },
  { k: "tope_pago_menor", texto: "Límite por pago", tipo: "dinero" },
  { k: "presupuesto_periodo_menor", texto: "Límite por periodo", tipo: "dinero" },
  { k: "tope_acumulado_proveedor", texto: "Tope acumulado por proveedor", tipo: "tope" },
  { k: "monedas_permitidas", texto: "Monedas permitidas", tipo: "lista" },
  { k: "tolerancia_acuerdo_pct", texto: "Tolerancia frente a lo acordado (%)", tipo: "texto" },
  { k: "vigencia_recibo_h", texto: "Vigencia del recibo (horas)", tipo: "texto" },
  { k: "tope_gasto_corrida_microusd", texto: "Tope de gasto de modelos (microUSD)", tipo: "texto" },
];

async function cargarMonedas() { return (await (await fetch("monedas.json")).json()).monedas; }

function reglas() {
  return {
    mandato: null, proveedores: [], monedas: {}, error: null, parametros: PARAMETROS, edicion: {}, previa: null, ocupado: false,
    async init() {
      try {
        this.monedas = await cargarMonedas();
        await api.iniciar();
        [this.mandato, this.proveedores] = await Promise.all([api.mandato(), api.proveedores()]);
      } catch (e) { this.error = e.message; }
    },
    get editables() { return PARAMETROS.filter((p) => p.tipo === "dinero"); },
    async verPrevia() {
      this.error = null; this.previa = null;
      const cambios = Object.fromEntries(Object.entries(this.edicion).filter(([k, v]) => String(v).trim() !== "" && String(v).trim() !== this.mandato.parametros[k]));
      if (!Object.keys(cambios).length) { this.error = "Cambie al menos un valor antes de pedir la vista previa."; return; }
      if (!Object.values(cambios).every((v) => /^\d+$/.test(String(v).trim()))) { this.error = "Escriba enteros en unidades menores, sin puntos ni comas."; return; }
      this.ocupado = true;
      try { this.previa = await api.previaMandato(Object.fromEntries(Object.entries(cambios).map(([k, v]) => [k, String(v).trim()]))); } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    valor(p) {
      if (!this.mandato) return "";
      const v = this.mandato.parametros[p.k], base = this.mandato.parametros.moneda_base;
      if (p.tipo === "dinero") return dinero.texto(v, base, this.monedas);
      if (p.tipo === "tope") return v.activo ? dinero.texto(v.monto_menor, base, this.monedas) : "Desactivado";
      return p.tipo === "lista" ? v.join(", ") : String(v);
    },
  };
}

function marcador() {
  return {
    m: null, noPrueba: [], error: null,
    async init() {
      try {
        await api.iniciar();
        [this.m, this.noPrueba] = await Promise.all([api.marcador(), api.arena(7).then((a) => a.no_prueba)]);
      } catch (e) { this.error = e.message; }
    },
    get cifra() { if (!this.m) return ""; return this.m.pagos_indebidos === null ? "?" : String(this.m.pagos_indebidos); },
    get tarjetas() {
      const m = this.m;
      if (!m) return [];
      return [["aciertos-reglas", "Aciertos de las reglas", m.aciertos_reglas], ["aciertos-e2e", "Aciertos de extremo a extremo", m.aciertos_extremo_a_extremo],
        ["autonomia", "Autonomía", m.autonomia], ["escalada", "Escalada innecesaria", m.escalada_innecesaria], ["costo", "Costo de lecturas guardadas", this.costo]]
        .map(([id, texto, valor]) => ({ id, texto, valor }));
    },
    get costo() { if (!this.m) return ""; const u = Number(this.m.costo.lecturas_guardadas_microusd) / 1e6; return "USD " + u.toFixed(4).replace(".", ","); },
  };
}

function bandeja() {
  return {
    muestras: [], cargadas: {}, sel: null, nombres: {}, error: null, ocupado: false, progreso: "", veredictos: VEREDICTOS,
    async init() {
      try {
        await api.iniciar();
        this.muestras = await api.muestras();
        this.nombres = Object.fromEntries((await (await fetch("reglas.registro.json")).json()).reglas.map((r) => [r.id, r.nombre]));
        await this.recuperar();
      } catch (e) { this.error = e.message; }
    },
    // Lo cargado en otra pantalla se recupera de la sesion, no se vuelve a cargar.
    async recuperar() {
      const hechas = api.muestrasCargadas();
      await Promise.all(this.muestras.filter((m) => hechas[m.id] && !this.cargadas[m.id]).map(async (m) => {
        this.cargadas[m.id] = await api.detalle(hechas[m.id]);
      }));
    },
    async abrir(m) {
      this.error = null; this.ocupado = true;
      try {
        await api.cargarUna(m.id);
        await this.recuperar();
        this.sel = m;
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    async cargarSet(todas = false) {
      this.error = null; this.progreso = ""; this.ocupado = true;
      try {
        const r = await api.cargarSet((i, n, t) => { this.progreso = `Cargando ${i} de ${n}: ${t}`; }, todas);
        await this.recuperar();
        this.progreso = `Set cargado: ${r.total - r.fallos.length} de ${r.total}.`;
        if (r.fallos.length) this.error = r.fallos.join(" | ");
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    get actual() { return this.sel && this.cargadas[this.sel.id]; },
    get detuvo() { return this.actual ? this.actual.decision.reglas.filter((r) => r.estado === "falla") : []; },
  };
}

const ESTRATEGIAS = {
  E1: "Partir una compra en facturas bajo el umbral del mismo proveedor",
  E2: "Facturas justo en el umbral y una unidad menor sobre él",
  E3: "Redondeo de moneda que cruza el umbral",
  E4: "Número de factura reformateado para repetir un pago",
  E5: "Proveedor nuevo: pago pequeño y luego uno grande",
  E6: "Cambio de cuenta después de una aprobación",
};
const CLASES = { verificada: "Coincide con el verificador", pago_indebido: "Pago indebido", desvio_conservador: "Desvio conservador" };
const porEstrategia = (casos) => casos.reduce((g, c) => { (g[c.id.split("-")[0]] ||= []).push(c); return g; }, {});

function ataque() {
  return {
    semilla: 7, v1: null, v2: null, arena: null, sel: null, error: null, ocupado: false, clases: CLASES,
    async init() { try { await api.iniciar(); await this.ejecutar(); } catch (e) { this.error = e.message; } },
    async ejecutar() {
      this.error = null; this.ocupado = true; this.sel = null;
      try {
        const s = Number(this.semilla);
        [this.v1, this.v2, this.arena] = await Promise.all([api.pentest("v1", s), api.pentest("v2", s), api.arena(s)]);
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    get filas() {
      if (!this.v1) return [];
      const g1 = porEstrategia(this.v1.casos), g2 = porEstrategia(this.v2.casos);
      return Object.keys(g1).map((k) => ({ clave: k, nombre: ESTRATEGIAS[k] || k, v1: g1[k], v2: g2[k] || [], hueco: g1[k].some((c) => c.clase === "pago_indebido"), huecoV2: (g2[k] || []).some((c) => c.clase === "pago_indebido") }));
    },
    get huecos() { return this.v1 ? this.v1.recuentos.pagos_indebidos : 0; },
    get huecosV2() { return this.v2 ? this.v2.recuentos.pagos_indebidos : 0; },
    resumen(casos) { const n = casos.filter((c) => c.clase === "pago_indebido").length; return n ? n + " pago(s) indebido(s)" : "sin pagos indebidos"; },
    get noPrueba() { return this.arena ? this.arena.no_prueba : []; },
  };
}

const ESTADOS_AVISO = {
  enviada: { icono: "✓", texto: "Enviada", clase: "chip-pagar" },
  simulada: { icono: "◌", texto: "Simulada, sin configurar", clase: "chip-sombra" },
  fallida: { icono: "✕", texto: "Fallida", clase: "chip-frenar" },
};

function notificaciones() {
  return {
    avisos: [], filtro: "todos", error: null, resultado: null, confirmando: false, ocupado: false, estados: ESTADOS_AVISO,
    async init() {
      try { await api.iniciar(); await this.cargar(); } catch (e) { this.error = e.message; }
    },
    async cargar() { this.avisos = await api.notificaciones(); },
    get visibles() { return this.filtro === "todos" ? this.avisos : this.avisos.filter((a) => a.estado === this.filtro); },
    hora: horaCorta,
    est(a) { return ESTADOS_AVISO[a.estado] || { icono: "?", texto: "Estado desconocido", clase: "chip-sombra" }; },
    async probar() {
      this.ocupado = true; this.error = null; this.resultado = null;
      try { this.resultado = await api.probarNotificacion(); await this.cargar(); } catch (e) { this.error = e.message; }
      this.ocupado = false; this.confirmando = false;
    },
  };
}
