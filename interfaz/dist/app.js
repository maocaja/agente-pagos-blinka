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
        await this.abrirDesdeUrl();
      } catch (e) { this.error = e.message; }
      this.cargando = false;
    },
    async abrirDesdeUrl() {
      const q = new URLSearchParams(location.search);
      const d = this.decisiones.find((x) => x.id === q.get("decision"));
      if (d) { await this.abrir(d); this.tecnica = q.get("tecnica") === "1"; }
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
    entero(menor, moneda) { return dinero.entero(menor, dinero.exponente(this.monedas, moneda)); },
    centavos(menor, moneda) { return dinero.centavos(menor, dinero.exponente(this.monedas, moneda)); },
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
