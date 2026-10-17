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

function app() {
  return {
    rol: "analista", tema: "claro", sesion: null, monedas: {},
    decisiones: [], filtro: "TODAS", error: null, cargando: true,
    sel: null, factura: null, recibo: null, tecnica: false,
    copia: "", copiaError: null, resultado: null, verifRecibo: null,
    veredictos: VEREDICTOS, estadoVerif: ESTADO_VERIF,
    filtros: ["TODAS", "PAGAR", "FRENAR", "ESCALAR", "REGISTRAR"],

    async init() {
      try {
        this.monedas = (await (await fetch("monedas.json")).json()).monedas;
        this.sesion = await api.iniciar();
        this.decisiones = await api.decisiones();
      } catch (e) { this.error = e.message; }
      this.cargando = false;
    },
    get visibles() {
      return this.filtro === "TODAS" ? this.decisiones : this.decisiones.filter((d) => d.veredicto === this.filtro);
    },
    cambiarRol(r) { this.rol = r; api.rol = r; },
    cambiarTema(t) { this.tema = t; document.documentElement.dataset.tema = t === "oscuro" ? "oscuro" : ""; },
    async abrir(d) {
      this.sel = d; this.recibo = null; this.resultado = null; this.verifRecibo = null; this.tecnica = false; this.error = null;
      try {
        this.factura = (await api.detalle(d.id)).factura;
        if (d.recibo_id) { this.recibo = await api.recibo(d.id); this.copia = JSON.stringify(this.recibo, null, 2); }
      } catch (e) { this.error = e.message; }
    },
    entero(menor, moneda) {
      const exp = (this.monedas[moneda] || { exponente: 2 }).exponente;
      const s = String(menor).padStart(exp + 1, "0");
      return s.slice(0, s.length - exp).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    centavos(menor, moneda) {
      const exp = (this.monedas[moneda] || { exponente: 2 }).exponente;
      return exp ? "," + String(menor).padStart(exp + 1, "0").slice(-exp) : "";
    },
    async verificar() {
      this.error = null;
      try { this.verifRecibo = await api.verificarRecibo(this.sel.id); } catch (e) { this.error = e.message; }
    },
    async verificarCopia() {
      this.error = null; this.copiaError = null;
      let copia;
      try { copia = JSON.parse(this.copia); } catch { this.copiaError = "El JSON de la copia no es valido."; return; }
      const o = this.recibo;
      const orden = { recibo_id: o.id, beneficiario_id: o.beneficiario_id, monto_menor: o.monto_menor, moneda: o.moneda, concepto: this.factura?.referencias?.numero || "" };
      try { this.resultado = await api.guardian(orden, copia); } catch (e) { this.error = e.message; }
    },
    restaurar() { this.copia = JSON.stringify(this.recibo, null, 2); this.resultado = null; this.copiaError = null; },
  };
}
