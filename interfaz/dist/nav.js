// Navegacion comun y guion de la demo. Solo DOM con textContent: nunca HTML crudo.
const PAGINAS = [
  { href: "index.html", texto: "Decisiones" },
  { href: "reglas.html", texto: "Reglas" },
  { href: "marcador.html", texto: "Marcador" },
  { href: "bandeja.html", texto: "Bandeja simulada" },
  { href: "ataque.html", texto: "Ataque" },
];
const ESCENAS = [
  { pagina: "index.html?muestra=foto-04-andino-cambio-cuenta&pestana=documento", titulo: "1. Cambio de cuenta", texto: "Sin control, esta factura se paga. Aquí se escala: la cuenta 9021 no es la registrada (4417) y el motivo está escrito. Luego, en la pestaña Resumen, actúe como CFO: rechace con una nota y vea el historial." },
  { pagina: "bandeja.html", titulo: "2. Las trampas", texto: "Abra cada muestra: el texto de una factura es un dato, no una orden. Decide el motor, con su regla." },
  { pagina: "index.html?muestra=fac-01&pestana=recibo", titulo: "3. El recibo", texto: "Cada decisión es un recibo firmado: pulse Verificar firma. Luego, en el panel Verificar sin esta aplicación, el auditor descarga el paquete y lo comprueba con su propio script." },
  { pagina: "ataque.html", titulo: "4. El ataque", texto: "El mandato v1 deja un hueco (facturas partidas); el v2 lo cierra. Nos atacamos primero." },
  { pagina: "marcador.html", titulo: "5. Cierre honesto", texto: "La cifra y, debajo, lo que esta cifra no prueba." },
];

function el(tag, attrs = {}, texto = "", hijos = []) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v));
  e.textContent = texto;
  hijos.forEach((h) => e.append(h));
  return e;
}

function irA(n) {
  const u = new URL(ESCENAS[n - 1].pagina, location.href);
  u.searchParams.set("demo", n);
  location.href = u.href;
}

function aplicarTema(t) { document.documentElement.dataset.tema = t === "oscuro" ? "oscuro" : ""; }

const ROLES = [["analista", "Analista"], ["cfo", "CFO"]];

function montarTema() {
  const tema = el("button", { type: "button", class: "btn btn-sec px-3! py-1.5!", "data-testid": "cambiar-tema" });
  const rotular = () => {
    const oscuro = memoria.leer("tema") === "oscuro";
    tema.textContent = oscuro ? "☀" : "☾";
    tema.setAttribute("aria-label", oscuro ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
    tema.title = tema.getAttribute("aria-label");
  };
  tema.onclick = () => { memoria.guardar("tema", memoria.leer("tema") === "oscuro" ? "claro" : "oscuro"); aplicarTema(memoria.leer("tema")); rotular(); };
  rotular();
  return tema;
}

function montarRol() {
  const botones = ROLES.map(([r, texto]) => el("button", { type: "button", role: "radio", "data-testid": "rol-" + r }, texto));
  const marcar = () => botones.forEach((b, i) => b.setAttribute("aria-checked", String(ROLES[i][0] === api.rol)));
  botones.forEach((b, i) => {
    b.onclick = () => {
      api.rol = ROLES[i][0];
      memoria.guardar("rol", api.rol);
      marcar();
      document.dispatchEvent(new CustomEvent("rol-cambiado", { detail: api.rol }));
    };
  });
  marcar();
  const grupo = el("div", { class: "segmento", role: "radiogroup", "aria-label": "Rol simulado" }, "", botones);
  return el("div", { class: "flex items-center gap-2", "data-testid": "selector-rol" }, "", [el("span", { class: "etiqueta-simulada whitespace-nowrap" }, "rol simulado"), grupo]);
}

function montarDemo() {
  const confirmar = el("span", { class: "hidden flex-wrap items-center gap-2", "data-testid": "demo-confirmacion", role: "alertdialog" });
  const aviso = el("span", { role: "status" }, "¿Reiniciar la sesión y empezar el guion?");
  const demo = el("button", { type: "button", class: "btn btn-primario px-4! py-1.5!", "data-testid": "demo" }, "Demo");
  const si = el("button", { type: "button", class: "btn btn-peligro", "data-testid": "demo-confirmar" }, "Reiniciar");
  const no = el("button", { type: "button", class: "btn btn-sec", "data-testid": "demo-cancelar" }, "Cancelar");
  confirmar.append(aviso, si, no);
  const cerrar = () => { confirmar.classList.add("hidden"); confirmar.classList.remove("flex"); demo.classList.remove("hidden"); };
  demo.onclick = () => { confirmar.classList.remove("hidden"); confirmar.classList.add("flex"); demo.classList.add("hidden"); si.focus(); };
  no.onclick = cerrar;
  si.onclick = async () => {
    si.disabled = no.disabled = true;
    try {
      await api.iniciar();
      await api.reiniciar();
      await api.cargarSet((i, n) => { aviso.textContent = `Cargando el set: ${i} de ${n}`; });
      irA(1);
    } catch (e) { aviso.textContent = e.message; si.disabled = no.disabled = false; }
  };
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") cerrar(); });
  return [confirmar, demo];
}

function montarEncabezado(actual) {
  const empresa = el("span", { class: "truncate font-semibold", "data-testid": "miga-empresa" }, "Mesa de pagos");
  const seccion = PAGINAS.find((p) => p.href === actual) || PAGINAS[0];
  const migas = el("nav", { "aria-label": "Ubicación", class: "flex min-w-0 items-center gap-2 whitespace-nowrap", "data-testid": "migas" }, "", [empresa, el("span", { "aria-hidden": "true", class: "text-texto-3" }, "›"), el("span", {}, seccion.texto)]);
  const mandato = el("span", { class: "whitespace-nowrap text-texto-2", "data-testid": "encabezado-mandato" });
  const ciclo = el("span", { class: "whitespace-nowrap text-texto-2", "data-testid": "encabezado-ciclo" });
  document.addEventListener("sesion-lista", () => { mandato.textContent = "Mandato " + api.mandato_version; });
  document.addEventListener("ciclo-listo", (ev) => { empresa.textContent = ev.detail.empresa; ciclo.textContent = "Ciclo " + ev.detail.ciclo_id; });
  return el("header", { class: "sticky top-0 z-10 flex min-h-[64px] flex-wrap items-center gap-x-4 gap-y-2 border-b border-linea bg-lienzo px-4 py-2 sm:px-6 min-[1100px]:flex-nowrap", "data-testid": "encabezado" }, "", [migas, mandato, ciclo, el("span", { class: "ml-auto" }), montarRol(), ...montarDemo(), montarTema()]);
}

function montarPaquete() {
  const enlace = el("a", { class: "btn btn-fantasma", href: "/api/auditoria/paquete", download: "", "data-testid": "descargar-paquete" }, "Paquete de auditoría");
  const falla = el("p", { class: "text-sm text-frenar", role: "alert", "data-testid": "error-descarga" });
  enlace.onclick = async (ev) => {
    ev.preventDefault();
    falla.textContent = "";
    try { await api.descargar("/api/auditoria/paquete", "paquete-auditoria.json"); } catch (e) { falla.textContent = e.message; }
  };
  return [enlace, falla];
}

function montarTarjetaEmpresa() {
  const nombre = el("p", { class: "font-semibold", "data-testid": "ciclo-empresa" }, "Mesa de pagos");
  const periodo = el("p", { class: "text-sm text-texto-2" });
  const disponible = el("p", { class: "text-sm text-texto-2" });
  const tarjeta = el("div", { class: "panel p-3", "data-testid": "tarjeta-empresa" }, "", [nombre, periodo, disponible]);
  const pintar = (c, monedas) => {
    nombre.textContent = c.empresa;
    periodo.textContent = "Ciclo abierto " + c.ciclo_id;
    disponible.textContent = "Disponible " + dinero.texto(c.disponible_menor, c.moneda, monedas);
    document.dispatchEvent(new CustomEvent("ciclo-listo", { detail: c }));
  };
  const cargar = async () => {
    try { pintar(await api.ciclo(), (await (await fetch("monedas.json")).json()).monedas); } catch { /* la tarjeta queda con el nombre del producto */ }
  };
  return [tarjeta, cargar];
}

function montarLateral(actual) {
  const pendientes = el("span", { class: "chip chip-escalar", "data-testid": "nav-pendientes" });
  const items = PAGINAS.map((p) => {
    const a = el("a", { href: p.href, class: "flex items-center justify-between gap-2 rounded-[10px] px-3 py-2 text-texto-2 hover:bg-elevado aria-[current=page]:bg-elevado aria-[current=page]:font-semibold aria-[current=page]:text-texto", "data-testid": "nav-" + p.href.replace(".html", "") }, p.texto);
    if (p.href === actual) a.setAttribute("aria-current", "page");
    if (p.href === "index.html") a.append(pendientes);
    return a;
  });
  const [tarjeta, cargarCiclo] = montarTarjetaEmpresa();
  const lectura = el("p", { class: "etiqueta-simulada rounded-[10px]! px-3! py-1.5 text-sm", "data-testid": "lectura" });
  const rotular = () => { lectura.textContent = `Datos de demostración, lectura ${api.lectura === "en_vivo" ? "en vivo" : "guardada"}, no se mueve dinero`; };
  const mostrar = (n) => { pendientes.textContent = n; pendientes.style.display = n === 0 ? "none" : ""; };
  const contar = async () => { try { mostrar((await api.decisiones()).filter((d) => d.estado === "pendiente").length); } catch { /* sin contador */ } };
  document.addEventListener("sesion-lista", () => { rotular(); cargarCiclo(); contar(); });
  document.addEventListener("decisiones-cambiaron", (ev) => { cargarCiclo(); mostrar(ev.detail); });
  rotular();
  const lista = el("div", { class: "grid gap-1", role: "list" }, "", items);
  const marca = el("p", { class: "px-1 text-xl font-semibold" }, "Mesa de pagos");
  const cuerpo = el("nav", { class: "grid gap-4", "aria-label": "Secciones", "data-testid": "nav" }, "", [lista]);
  return el("aside", { class: "flex flex-col gap-4 border-b border-linea bg-panel p-4 lg:fixed lg:inset-y-0 lg:left-0 lg:z-20 lg:w-64 lg:border-b-0 lg:border-r lg:overflow-y-auto", "data-testid": "lateral" }, "", [marca, tarjeta, cuerpo, el("div", { class: "grid gap-2 lg:mt-auto" }, "", [...montarPaquete(), lectura])]);
}

function montarNav() {
  aplicarTema(memoria.leer("tema"));
  const actual = location.pathname.split("/").pop() || "index.html";
  const paso = Number(new URLSearchParams(location.search).get("demo")) || 0;
  document.body.classList.add("lg:pl-64");
  document.body.prepend(montarLateral(actual), montarEncabezado(actual));
  if (paso >= 1 && paso <= ESCENAS.length) montarGuia(paso);
}

function montarGuia(paso) {
  const esc = ESCENAS[paso - 1];
  const ant = el("button", { type: "button", class: "btn btn-sec", "data-testid": "guia-anterior" }, "Anterior");
  const sig = el("button", { type: "button", class: "btn btn-primario", "data-testid": "guia-siguiente" }, "Siguiente");
  const salir = el("button", { type: "button", class: "btn btn-fantasma", "data-testid": "guia-salir" }, "Salir (Esc)");
  const panel = el("aside", { class: "panel panel-fuerte fixed inset-x-4 bottom-4 z-10 mx-auto grid max-w-3xl gap-3 p-4", "data-testid": "guia", "aria-label": "Guion de la demo" }, "", [
    el("p", { class: "text-sm text-texto-2" }, `Escena ${paso} de ${ESCENAS.length}`),
    el("p", { class: "text-lg font-semibold", "data-testid": "guia-titulo" }, esc.titulo),
    el("p", {}, esc.texto),
    el("div", { class: "flex flex-wrap gap-2" }, "", [ant, sig, salir]),
  ]);
  const salirGuia = () => { panel.remove(); history.replaceState(null, "", location.pathname + location.search.replace(/[?&]demo=\d+/, "")); };
  const mover = (d) => { const n = paso + d; if (n >= 1 && n <= ESCENAS.length) irA(n); };
  ant.disabled = paso === 1;
  sig.disabled = paso === ESCENAS.length;
  ant.onclick = () => mover(-1);
  sig.onclick = () => mover(1);
  salir.onclick = salirGuia;
  document.addEventListener("keydown", (ev) => {
    if (/^(INPUT|TEXTAREA)$/.test(ev.target.tagName)) return;
    if (ev.key === "ArrowRight") mover(1);
    else if (ev.key === "ArrowLeft") mover(-1);
    else if (ev.key === "Escape") salirGuia();
  });
  document.body.append(panel);
}

document.addEventListener("DOMContentLoaded", montarNav);
