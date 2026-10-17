const ESTADOS = { pendiente: "Espera aprobación", rechazada: "Rechazada por el CFO", reevaluada: "Aprobada y reevaluada", denegada: "Denegada por el guardián", vencida: "Vencida" };

const ROTULO = { PAGAR: "Decisión de pagar", FRENAR: "Frenada", ESCALAR: "Escalada", REGISTRAR: "Registrada" };
// Primero lo que mas conviene mirar; lo no listado va despues de R9.
const RIESGO = { R4: 0, R8: 0, R2b: 0, R6: 1, R10: 1, R5: 2, R1: 3, R9: 4 };
const FORMATOS = { texto: "TXT", pdf: "PDF", imagen: "IMG", xml: "XML", csv: "CSV" };
const CANALES = { correo: "Correo", chat: "Chat", pdf: "PDF", imagen: "Foto", xml: "XML", hoja: "Hoja" };
const TIPOS = { factura: "Factura", cuenta_de_cobro: "Cuenta de cobro", nota_de_credito: "Nota de crédito", estado_de_cuenta: "Estado de cuenta", proforma: "Proforma", anticipo: "Anticipo", desconocido: "Desconocido" };
const CAMPO_ORIGEN = { cuenta: "cuenta", "montos.total_menor": "monto_total", "montos.moneda": "moneda", "referencias.numero": "numero_factura", "proveedor_asignado.proveedor_id": "proveedor" };
const FILTROS_ESTADO = [["TODAS", "Todos"], ["PENDIENTES", "Pendientes de aprobación"], ["PAGAR", "Con decisión de pagar"], ["FRENAR", "Frenadas"], ["ESCALAR", "Escaladas"], ["REGISTRAR", "Registradas"]];

const sinTildes = (t) => String(t).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
function fechaCorta(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
  return m ? new Date(+m[1], +m[2] - 1, +m[3]).toLocaleDateString("es", { day: "numeric", month: "short", year: "numeric" }) : "";
}
function riesgo(d) {
  const fallas = d.reglas.filter((r) => r.estado === "falla").map((r) => RIESGO[r.id] ?? 5);
  return (d.estado === "pendiente" ? 0 : 10) + (fallas.length ? Math.min(...fallas) : 6);
}

const NIVEL = { ok: { icono: "✓", color: "text-pagar" }, aviso: { icono: "!", color: "text-escalar" }, falla: { icono: "✕", color: "text-frenar" } };

// Un paso por etapa, con lo que dicen la factura canonica y la decision: frase corta y detalle.
function pasosProceso(f, d, nombres) {
  const l = f.lectura, v = f.verificaciones, evaluadas = d.reglas.filter((r) => r.estado !== "omitida");
  const fallan = evaluadas.filter((r) => r.estado === "falla");
  const malas = [["esquema", "esquema"], ["dinero_presente", "importes"], ["suma_lineas", "suma de líneas"]].filter(([k]) => v[k] === "falla").map(([, t]) => t);
  if (v.cita_evidencia === "falla") malas.push("cita en el documento");
  if (v.tipo === "discrepancia") malas.push("tipo de documento");
  if (v.segunda_lectura.estado === "difiere") malas.push("segunda lectura");
  const sinCita = v.cita_evidencia === "no_verificable";
  const conf = Math.round(Math.min(...Object.values(f.confianza), 1) * 100);
  const nivelValidacion = malas.length ? "falla" : sinCita ? "aviso" : "ok";
  const nivelReglas = !fallan.length ? "ok" : fallan.some((r) => r.accion_si_falla === "FRENAR") ? "falla" : "aviso";
  const ver = VEREDICTOS[d.veredicto];
  return [
    { id: "lectura", titulo: "Lectura", ...NIVEL[l.motivo_falla ? "falla" : "ok"], corto: l.motivo_falla ? "No se pudo leer" : `Confianza ${conf} %`,
      texto: l.motivo_falla ? "No se pudo leer: " + l.motivo_falla.replaceAll("_", " ") + "." : `Leída ${l.metodo === "modelo" ? "con modelo" : "con lector estructurado"}${l.desde_cache ? " (lectura guardada)" : ""}; confianza mínima ${conf} %.` },
    { id: "validacion", titulo: "Validación", ...NIVEL[nivelValidacion], corto: malas.length ? "No coincide" : sinCita ? "Cita sin comprobar" : "Coincide",
      texto: malas.length ? "No coincide: " + malas.join(", ") + "." : "Esquema, importes y suma de líneas coinciden." + (sinCita ? " La cita no se pudo comprobar en el original." : "") },
    { id: "reglas", titulo: "Reglas", ...NIVEL[nivelReglas], corto: fallan.length ? `${fallan.length} de ${evaluadas.length} no cumplen` : `${evaluadas.length} cumplen`,
      texto: fallan.length ? `${fallan.length} de ${evaluadas.length} reglas evaluadas no cumplen: ${fallan.map((r) => nombres[r.id] || r.id).join(", ")}.` : `Las ${evaluadas.length} reglas evaluadas cumplen.` },
    { id: "decision", titulo: "Decisión", icono: ver.icono, color: ver.color, corto: ROTULO[d.veredicto], texto: ROTULO[d.veredicto] + (d.modo_autonomia === "autonomo" ? "" : " (modo sombra)") + "." },
  ];
}

function app() {
  return {
    rol: api.rol, sesion: null, monedas: {}, nombresRegla: {}, registro: {},
    decisiones: [], facturas: {}, filtro: "TODAS", busqueda: "", formato: "", canalFiltro: "", masFiltros: false, campo: "", error: null, cargando: true,
    sel: null, factura: null, recibo: null, tecnica: false, pestana: "resumen",
    pestanas: [["resumen", "Resumen"], ["documento", "Documento"], ["recibo", "Recibo"], ["historial", "Historial"]],
    muestras: [], historial: [], estadoOrden: null, nota: "", ocupado: false, progreso: "", copia: "", copiaError: null, resultado: null, verifRecibo: null, imagenFalla: false,
    veredictos: VEREDICTOS, estados: ESTADOS, estadoVerif: ESTADO_VERIF, filtros: FILTROS_ESTADO, formatos: FORMATOS, canales: CANALES,

    async init() {
      try {
        this.monedas = (await (await fetch("monedas.json")).json()).monedas;
        this.nombresRegla = Object.fromEntries((await (await fetch("reglas.registro.json")).json()).reglas.map((r) => [r.id, r.nombre]));
        document.addEventListener("rol-cambiado", (ev) => { this.rol = ev.detail; });
        this.sesion = await api.iniciar();
        api.proveedores().then((ps) => { this.registro = Object.fromEntries(ps.map((p) => [p.id, p.nombre])); }, () => {});
        api.muestras().then((m) => { this.muestras = m; }, () => {});
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
      document.dispatchEvent(new CustomEvent("decisiones-cambiaron", { detail: this.vigentes.filter((d) => d.estado === "pendiente").length }));
    },
    async abrirDesdeUrl() {
      const q = new URLSearchParams(location.search);
      const id = q.get("decision") || api.muestrasCargadas()[q.get("muestra")];
      const d = this.decisiones.find((x) => x.id === id);
      if (d) { await this.abrir(d, q.get("pestana")); this.tecnica = q.get("tecnica") === "1"; }
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
    async descargar(ruta, nombre) {
      this.error = null;
      try { await api.descargar(ruta, nombre); } catch (e) { this.error = e.message; }
    },
    hora: horaCorta,
    get vigentes() { return this.decisiones.filter((d) => d.estado !== "reevaluada"); },
    pasaFiltros(d) {
      const f = this.f(d), e = this.filtro, q = sinTildes(this.busqueda.trim());
      const estado = e === "TODAS" || (e === "PENDIENTES" ? d.estado === "pendiente" : d.veredicto === e);
      const texto = !q || sinTildes(this.proveedor(d) + " " + (f?.referencias?.numero || "")).includes(q);
      return estado && texto && (!this.formato || f?.documento.formato === this.formato) && (!this.canalFiltro || f?.documento.canal === this.canalFiltro);
    },
    get visibles() { return this.vigentes.filter((d) => this.pasaFiltros(d)).sort((a, b) => riesgo(a) - riesgo(b)); },
    valoresReales(clave) { return [...new Set(this.vigentes.map((d) => this.f(d)?.documento[clave]).filter(Boolean))].sort(); },
    get resumen() {
      const v = this.vigentes, n = (f) => v.filter(f).length;
      return [["documentos", "documentos", v.length], ["pendientes", "esperan a una persona", n((d) => d.estado === "pendiente")],
        ["frenados", "frenados", n((d) => d.veredicto === "FRENAR")], ["autorizadas", "con decisión de pagar", n((d) => d.veredicto === "PAGAR")]];
    },
    estadoDe(d) {
      const e = ESTADOS[d.estado];
      if (d.estado === "pendiente") return { ...VEREDICTOS.ESCALAR, texto: e };
      if (e && d.estado !== "reevaluada") return { ...VEREDICTOS.FRENAR, texto: e };
      return { ...VEREDICTOS[d.veredicto], texto: ROTULO[d.veredicto] };
    },
    fecha(d) { return fechaCorta(this.f(d)?.fechas.emision); },
    importe(d) { const m = this.f(d)?.montos; return m ? m.moneda + " " + this.entero(m.total_menor, m.moneda) : ""; },
    centimos(d) { const m = this.f(d)?.montos; return m ? this.centavos(m.total_menor, m.moneda) : ""; },
    f(d) { return this.facturas[d.id]; },
    proveedor(d) { const f = this.f(d); return this.registro[f?.proveedor_asignado?.proveedor_id] || f?.emisor?.nombre || d.factura_id; },
    canal(d) { return this.f(d)?.documento?.canal || ""; },
    aprobo(d) { return d.reevaluacion_de ? "CFO" : ""; },
    async abrir(d, pestana) {
      this.pestana = this.pestanas.some((p) => p[0] === pestana) ? pestana : "resumen";
      this.sel = d; this.historial = []; this.estadoOrden = null; this.recibo = null; this.resultado = null; this.verifRecibo = null; this.tecnica = false; this.error = null; this.imagenFalla = false; this.campo = "";
      try {
        const r = await api.detalle(d.id);
        this.factura = r.factura; this.historial = r.historial || []; this.estadoOrden = r.estado_orden ?? null;
        if (d.recibo_id) { this.recibo = await api.recibo(d.recibo_id); this.copia = JSON.stringify(this.recibo, null, 2); }
        this.campo = CAMPO_ORIGEN[(this.diferencias.find((r) => CAMPO_ORIGEN[r.campo_origen]) || {}).campo_origen] || "";
      } catch (e) { this.error = e.message; }
      if (matchMedia("(max-width: 1279px)").matches) this.$nextTick(() => this.$refs.detalle?.scrollIntoView({ block: "start" }));
    },
    moverPestana(paso) {
      const ids = this.pestanas.map((p) => p[0]);
      this.pestana = ids[(ids.indexOf(this.pestana) + paso + ids.length) % ids.length];
      this.$nextTick(() => document.getElementById("tab-" + this.pestana)?.focus());
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
    get archivo() { return this.muestraId || (this.factura ? this.factura.documento.id : ""); },
    get leido() {
      const f = this.factura;
      if (!f) return [];
      const m = f.montos, ev = f.evidencia || {};
      return [["proveedor", "Proveedor", f.emisor.nombre], ["numero_factura", "Factura", f.referencias.numero],
        ["monto_total", "Total", m.moneda + " " + this.entero(m.total_menor, m.moneda) + this.centavos(m.total_menor, m.moneda)],
        ["cuenta", "Cuenta", f.cuenta ? f.cuenta.pais + " ****" + f.cuenta.ultimos4 : "Sin cuenta"], ["tipo_documento", "Tipo", TIPOS[f.documento.tipo_documento]]]
        .map(([clave, etiqueta, valor]) => ({ clave, etiqueta, valor, cita: ev[clave] || "" }));
    },
    get citaActiva() { return (this.leido.find((c) => c.clave === this.campo) || {}).cita || ""; },
    // Original partido en antes, cita y despues para resaltarla sin HTML crudo.
    get partesOriginal() {
      const o = this.original, c = this.citaActiva, i = c ? o.indexOf(c) : -1;
      return i < 0 ? [o, "", ""] : [o.slice(0, i), c, o.slice(i + c.length)];
    },
    elegirCampo(clave) {
      this.campo = this.campo === clave ? "" : clave;
      this.$nextTick(() => this.$refs.marca?.scrollIntoView({ block: "nearest" }));
    },
    get proceso() { return this.sel && this.factura ? pasosProceso(this.factura, this.sel, this.nombresRegla) : []; },
    get diferencias() { return this.sel ? this.sel.reglas.filter((r) => r.estado === "falla") : []; },
    get etapas() {
      const o = this.estadoOrden, v = this.sel ? VEREDICTOS[this.sel.veredicto] : {};
      return [["decision", "Decisión", this.sel ? ROTULO[this.sel.veredicto] : "", v.color],
        ["autorizada", "Autorizada", o ? "Sí" : "No", o ? "text-pagar" : "text-texto-2"],
        ["orden", "Orden emitida (simulada)", o === "orden_simulada_emitida" ? "Sí" : "No", o === "orden_simulada_emitida" ? "text-pagar" : "text-texto-2"]];
    },
    // El servidor manda eventos en minuscula; se muestran con inicial mayuscula y el rol del CFO en siglas.
    evento(h) { return h.evento.charAt(0).toUpperCase() + h.evento.slice(1) + " · " + (h.actor === "cfo" ? "CFO" : h.actor); },
    get puedeDescargarOrden() { return !!this.estadoOrden; },
    async pedirAutorizacion() {
      this.error = null; this.ocupado = true;
      try {
        this.resultado = await api.autorizar(this.sel.id);
        this.estadoOrden = (await api.detalle(this.sel.id)).estado_orden ?? null;
        await this.cargarLista();
      } catch (e) { this.error = e.message; }
      this.ocupado = false;
    },
    async descargarOrden() {
      await this.descargar("/api/ordenes/" + this.recibo.id + "/pain001", "orden-simulada-" + this.recibo.id + ".xml");
      if (!this.error) this.estadoOrden = (await api.detalle(this.sel.id)).estado_orden ?? this.estadoOrden;
    },
    get puedeDecidir() { return this.rol === "cfo"; },
    get aprobable() { return this.diferencias.every((r) => r.aprobable); },
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
