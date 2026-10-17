const ESTADOS = { pendiente: "Espera aprobación", rechazada: "Rechazada por el CFO", reevaluada: "Aprobada y reevaluada", denegada: "Denegada por el guardián", vencida: "Vencida" };

function app() {
  return {
    rol: "analista", sesion: null, monedas: {}, marcador: null,
    decisiones: [], facturas: {}, filtro: "TODAS", error: null, cargando: true,
    sel: null, factura: null, recibo: null, tecnica: false,
    ciclo: null, muestras: [], historial: [], estadoOrden: null, nota: "", ocupado: false, progreso: "", copia: "", copiaError: null, resultado: null, verifRecibo: null, imagenFalla: false,
    veredictos: VEREDICTOS, estados: ESTADOS, estadoVerif: ESTADO_VERIF,
    filtros: [["TODAS", "Todas"], ["PAGAR", "Pagar"], ["FRENAR", "Frenar"], ["ESCALAR", "Escalar"], ["PENDIENTES", "Pendientes de aprobación"]],

    async init() {
      try {
        this.monedas = (await (await fetch("monedas.json")).json()).monedas;
        this.sesion = await api.iniciar();
        api.marcador().then((m) => { this.marcador = m; }, () => {});
        api.muestras().then((m) => { this.muestras = m; }, () => {});
        await this.cargarCiclo();
        await this.cargarLista();
        await this.abrirDesdeUrl();
      } catch (e) { this.error = e.message; }
      this.cargando = false;
    },
    // Si el servidor aun no sirve el ciclo, la pantalla sigue sin ese bloque.
    async cargarCiclo() { try { this.ciclo = await api.ciclo(); } catch { this.ciclo = null; } },
    get porcentajeReservado() {
      const c = this.ciclo;
      return c && Number(c.presupuesto_menor) > 0 ? Math.min(100, Math.round(Number(c.reservado_menor) * 100 / Number(c.presupuesto_menor))) : 0;
    },
    dineroCiclo(menor) { return dinero.texto(menor, this.ciclo.moneda, this.monedas); },
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
        await this.cargarCiclo();
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    async descargar(ruta, nombre) {
      this.error = null;
      try { await api.descargar(ruta, nombre); } catch (e) { this.error = e.message; }
    },
    hora: horaCorta,
    get vigentes() { return this.decisiones.filter((d) => d.estado !== "reevaluada"); },
    get visibles() {
      const f = this.filtro;
      return this.vigentes.filter((d) => f === "TODAS" || (f === "PENDIENTES" ? d.estado === "pendiente" : d.veredicto === f));
    },
    get resumen() {
      const v = this.vigentes, n = (f) => v.filter(f).length;
      return [["documentos", "Documentos", v.length], ["autorizadas", "Autorizadas para pago", n((d) => d.veredicto === "PAGAR")],
        ["frenados", "Frenados", n((d) => d.veredicto === "FRENAR")], ["escalados", "Escalados", n((d) => d.veredicto === "ESCALAR")],
        ["pendientes", "Pendientes de aprobación", n((d) => d.estado === "pendiente")]];
    },
    // La frase solo se muestra si el marcador real la respalda.
    get garantia() {
      const m = this.marcador;
      return m && m.pagos_indebidos === 0 && m.verificados > 0 ? `Verificación independiente de las ${m.verificados} facturas del set: 0 pagos indebidos.` : "";
    },
    f(d) { return this.facturas[d.id]; },
    proveedor(d) { return this.f(d)?.emisor?.nombre || d.factura_id; },
    canal(d) { return this.f(d)?.documento?.canal || ""; },
    aprobo(d) { return d.reevaluacion_de ? "CFO" : ""; },
    cambiarRol(r) { this.rol = r; api.rol = r; },
    async abrir(d) {
      this.sel = d; this.historial = []; this.estadoOrden = null; this.recibo = null; this.resultado = null; this.verifRecibo = null; this.tecnica = false; this.error = null; this.imagenFalla = false;
      try {
        const r = await api.detalle(d.id);
        this.factura = r.factura; this.historial = r.historial || []; this.estadoOrden = r.estado_orden ?? null;
        if (d.recibo_id) { this.recibo = await api.recibo(d.recibo_id); this.copia = JSON.stringify(this.recibo, null, 2); }
      } catch (e) { this.error = e.message; }
      if (matchMedia("(max-width: 1023px)").matches) this.$nextTick(() => this.$refs.detalle?.scrollIntoView({ block: "start" }));
    },
    // El documento original solo existe para las muestras cargadas; la reevaluacion hereda el de su decision de origen.
    get muestraId() {
      if (!this.sel) return "";
      const hechas = api.muestrasCargadas(), ids = [this.sel.id, this.sel.reevaluacion_de];
      return Object.keys(hechas).find((k) => ids.includes(hechas[k])) || "";
    },
    get original() { return (this.muestras.find((m) => m.id === this.muestraId) || {}).original || ""; },
    // El servidor describe un binario como "documento binario: nombre.ext"; la extension decide como mostrarlo.
    get tipoOriginal() {
      const ext = (/^documento binario: .*\.(\w+)$/.exec(this.original) || [])[1]?.toLowerCase();
      return ["jpg", "jpeg", "png", "webp", "gif"].includes(ext) ? "imagen" : ext === "pdf" ? "pdf" : "texto";
    },
    get urlArchivo() { return `/api/muestras/${encodeURIComponent(this.muestraId)}/archivo`; },
    get leido() {
      const f = this.factura;
      if (!f) return [];
      return [["Proveedor", f.emisor.nombre], ["Factura", f.referencias.numero], ["Total", f.montos.moneda + " " + this.entero(f.montos.total_menor, f.montos.moneda) + this.centavos(f.montos.total_menor, f.montos.moneda)],
        ["Cuenta", f.cuenta.pais + " ****" + f.cuenta.ultimos4]];
    },
    get diferencias() { return this.sel ? this.sel.reglas.filter((r) => r.estado === "falla") : []; },
    get etapas() {
      const o = this.estadoOrden;
      return [["decision", "Decisión", this.sel ? this.veredictos[this.sel.veredicto].texto : "", true],
        ["autorizada", "Autorizada", o ? "Sí" : "No", !!o],
        ["orden", "Orden emitida (simulada)", o === "orden_simulada_emitida" ? "Sí" : "No", o === "orden_simulada_emitida"]];
    },
    get puedeDecidir() { return this.rol === "cfo"; },
    get esperaAprobacion() { return this.sel && this.sel.veredicto === "ESCALAR" && this.sel.estado === "pendiente"; },
    async decidir(accion) {
      this.error = null; this.ocupado = true;
      try {
        const r = await api[accion](this.sel.id, this.nota);
        this.nota = "";
        await this.cargarLista();
        await this.cargarCiclo();
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
