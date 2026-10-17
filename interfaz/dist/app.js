function app() {
  return {
    rol: "analista", sesion: null, monedas: {}, marcador: null,
    decisiones: [], facturas: {}, filtro: "TODAS", error: null, cargando: true,
    sel: null, factura: null, recibo: null, tecnica: false,
    nota: "", ocupado: false, progreso: "", copia: "", copiaError: null, resultado: null, verifRecibo: null,
    veredictos: VEREDICTOS, estadoVerif: ESTADO_VERIF,
    filtros: [["TODAS", "Todas"], ["PAGAR", "Pagar"], ["FRENAR", "Frenar"], ["ESCALAR", "Escalar"], ["PENDIENTES", "Pendientes de aprobación"]],

    async init() {
      try {
        this.monedas = (await (await fetch("monedas.json")).json()).monedas;
        this.sesion = await api.iniciar();
        api.marcador().then((m) => { this.marcador = m; }, () => {});
        await this.cargarLista();
        await this.abrirDesdeUrl();
      } catch (e) { this.error = e.message; }
      this.cargando = false;
    },
    // Una fila por documento: la decision reevaluada tras aprobar queda reemplazada por la nueva.
    async cargarLista() {
      this.decisiones = await api.decisiones();
      await Promise.all(this.vigentes.filter((d) => !this.facturas[d.id]).map(async (d) => {
        this.facturas[d.id] = (await api.detalle(d.id)).factura;
      }));
    },
    async abrirDesdeUrl() {
      const q = new URLSearchParams(location.search);
      const id = q.get("decision") || api.muestrasCargadas()[q.get("muestra")];
      const d = this.decisiones.find((x) => x.id === id);
      if (d) { await this.abrir(d); this.tecnica = q.get("tecnica") === "1"; }
    },
    async cargarSet() {
      this.error = null; this.ocupado = true;
      try {
        const r = await api.cargarSet((i, n, t) => { this.progreso = `Cargando ${i} de ${n}: ${t}`; });
        this.progreso = r.fallos.length ? `Se cargaron ${r.total - r.fallos.length} de ${r.total}. ${r.fallos[0]}` : "";
        await this.cargarLista();
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    get vigentes() { return this.decisiones.filter((d) => d.estado !== "reevaluada"); },
    get visibles() {
      const f = this.filtro;
      return this.vigentes.filter((d) => f === "TODAS" || (f === "PENDIENTES" ? d.estado === "pendiente" : d.veredicto === f));
    },
    get resumen() {
      const v = this.vigentes, n = (f) => v.filter(f).length;
      return [["documentos", "Documentos", v.length], ["pagados", "Pagados", n((d) => d.veredicto === "PAGAR")],
        ["frenados", "Frenados", n((d) => d.veredicto === "FRENAR")], ["escalados", "Escalados", n((d) => d.veredicto === "ESCALAR")],
        ["pendientes", "Pendientes de aprobación", n((d) => d.estado === "pendiente")]];
    },
    // La frase solo se muestra si el marcador real la respalda.
    get garantia() {
      const m = this.marcador;
      return m && m.pagos_indebidos === 0 && m.verificados > 0 ? `${m.verificados} facturas del set verificadas, 0 pagos indebidos.` : "";
    },
    f(d) { return this.facturas[d.id]; },
    proveedor(d) { return this.f(d)?.emisor?.nombre || d.factura_id; },
    canal(d) { return this.f(d)?.documento?.canal || ""; },
    aprobo(d) { return d.reevaluacion_de ? "CFO" : ""; },
    cambiarRol(r) { this.rol = r; api.rol = r; },
    async abrir(d) {
      this.sel = d; this.recibo = null; this.resultado = null; this.verifRecibo = null; this.tecnica = false; this.error = null;
      try {
        this.factura = (await api.detalle(d.id)).factura;
        if (d.recibo_id) { this.recibo = await api.recibo(d.recibo_id); this.copia = JSON.stringify(this.recibo, null, 2); }
      } catch (e) { this.error = e.message; }
      if (matchMedia("(max-width: 1023px)").matches) this.$nextTick(() => this.$refs.detalle?.scrollIntoView({ block: "start" }));
    },
    get puedeDecidir() { return this.rol === "cfo"; },
    get esperaAprobacion() { return this.sel && this.sel.veredicto === "ESCALAR" && this.sel.estado === "pendiente"; },
    async decidir(accion) {
      this.error = null; this.ocupado = true;
      try {
        const r = await api[accion](this.sel.id, this.nota);
        this.nota = "";
        await this.cargarLista();
        await this.abrir(accion === "aprobar" ? r.decision : this.decisiones.find((d) => d.id === this.sel.id));
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    entero(menor, moneda) { return dinero.entero(menor, dinero.exponente(this.monedas, moneda)); },
    centavos(menor, moneda) { return dinero.centavos(menor, dinero.exponente(this.monedas, moneda)); },
    async verificar() {
      this.error = null;
      try { this.verifRecibo = await api.verificarRecibo(this.recibo.id); } catch (e) { this.error = e.message; }
    },
    async verificarCopia() {
      this.error = null; this.copiaError = null;
      let copia;
      try { copia = JSON.parse(this.copia); } catch { this.copiaError = "El JSON de la copia no es válido."; return; }
      const o = this.recibo;
      const orden = { recibo_id: o.id, beneficiario_id: o.beneficiario_id, monto_menor: o.monto_menor, moneda: o.moneda, concepto: this.factura?.referencias?.numero || "" };
      try { this.resultado = await api.guardian(orden, copia); } catch (e) { this.error = e.message; }
    },
    restaurar() { this.copia = JSON.stringify(this.recibo, null, 2); this.resultado = null; this.copiaError = null; },
  };
}
