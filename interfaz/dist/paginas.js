// Componentes Alpine de Reglas, Marcador, Bandeja y Ataque. El servidor decide; aqui solo se muestra.
const PARAMETROS = [
  { k: "umbral_aprobacion_menor", texto: "Umbral de aprobacion", tipo: "dinero" },
  { k: "tope_pago_menor", texto: "Limite por pago", tipo: "dinero" },
  { k: "presupuesto_periodo_menor", texto: "Limite por periodo", tipo: "dinero" },
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
        ["autonomia", "Autonomia", m.autonomia], ["escalada", "Escalada innecesaria", m.escalada_innecesaria], ["costo", "Costo de lecturas guardadas", this.costo]]
        .map(([id, texto, valor]) => ({ id, texto, valor }));
    },
    get costo() { if (!this.m) return ""; const u = Number(this.m.costo.lecturas_guardadas_microusd) / 1e6; return "USD " + u.toFixed(4).replace(".", ","); },
  };
}

function bandeja() {
  return {
    muestras: [], cargadas: {}, sel: null, nombres: {}, error: null, ocupado: false, veredictos: VEREDICTOS,
    async init() {
      try {
        await api.iniciar();
        this.muestras = await api.muestras();
        this.nombres = Object.fromEntries((await (await fetch("reglas.registro.json")).json()).reglas.map((r) => [r.id, r.nombre]));
      } catch (e) { this.error = e.message; }
    },
    async abrir(m) {
      this.error = null; this.ocupado = true;
      try {
        if (!this.cargadas[m.id]) {
          const decision = await api.cargarMuestra(m.id);
          this.cargadas[m.id] = { decision, factura: (await api.detalle(decision.id)).factura };
        }
        this.sel = m;
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    async cargarTodas() { for (const m of this.muestras) await this.abrir(m); },
    get actual() { return this.sel && this.cargadas[this.sel.id]; },
    get detuvo() { return this.actual ? this.actual.decision.reglas.filter((r) => r.estado === "falla") : []; },
  };
}

function ataque() {
  return {
    semilla: 7, v1: null, v2: null, arena: null, monedas: {}, base: "USD", sel: null, error: null, ocupado: false,
    async init() {
      try { this.monedas = await cargarMonedas(); await api.iniciar(); this.base = (await api.mandato()).parametros.moneda_base; await this.ejecutar(); } catch (e) { this.error = e.message; }
    },
    async ejecutar() {
      this.error = null; this.ocupado = true; this.sel = null;
      try {
        const s = Number(this.semilla);
        [this.v1, this.v2, this.arena] = await Promise.all([api.pentest("v1", s), api.pentest("v2", s), api.arena(s)]);
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    get filas() { return this.v1 ? this.v1.estrategias.map((e, i) => ({ ...e, v2: this.v2.estrategias[i] })) : []; },
    get huecos() { return this.filas.filter((f) => f.hueco).length; },
    get huecosV2() { return this.filas.filter((f) => f.v2.hueco).length; },
    motivo(f) {
      if (!f.hueco) return "El motor devolvio " + f.resultado + ", igual a lo esperado: bloqueada.";
      const pago = f.pagado_menor ? " Se habrian pagado " + dinero.texto(f.pagado_menor, this.base, this.monedas) + "." : "";
      return "Hueco de politica en el mandato v1." + pago + (f.v2.hueco ? " El v2 no lo cierra." : " El v2 lo cierra.");
    },
  };
}
