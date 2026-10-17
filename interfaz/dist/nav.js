// Navegacion comun y guion de la demo. Solo DOM con textContent: nunca HTML crudo.
const PAGINAS = [
  { href: "index.html", texto: "Decisiones" },
  { href: "reglas.html", texto: "Reglas" },
  { href: "marcador.html", texto: "Marcador" },
  { href: "bandeja.html", texto: "Bandeja" },
  { href: "ataque.html", texto: "Ataque" },
];
const ESCENAS = [
  { pagina: "index.html?muestra=foto-04-andino-cambio-cuenta", titulo: "1. Cambio de cuenta", texto: "Sin control, esta factura se paga. Aquí se escala: la cuenta 9021 no es la registrada (4417) y el motivo está escrito. Actúe como CFO, rechace con una nota y vea el historial." },
  { pagina: "bandeja.html", titulo: "2. Las trampas", texto: "Abra cada muestra: el texto de una factura es un dato, no una orden. Decide el motor, con su regla." },
  { pagina: "index.html?muestra=fac-01", titulo: "3. El recibo", texto: "Cada decisión es un recibo firmado: pulse Verificar firma. Luego, en el panel Verificar sin esta aplicación, el auditor descarga el paquete y lo comprueba con su propio script." },
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

function montarOpciones() {
  const tema = el("button", { type: "button", class: "btn btn-sec w-full", "data-testid": "cambiar-tema" });
  const rotular = () => { tema.textContent = memoria.leer("tema") === "oscuro" ? "Tema claro" : "Tema oscuro"; };
  tema.onclick = () => { memoria.guardar("tema", memoria.leer("tema") === "oscuro" ? "claro" : "oscuro"); aplicarTema(memoria.leer("tema")); rotular(); };
  rotular();
  const paquete = el("a", { class: "btn btn-sec w-full", href: "/api/auditoria/paquete", download: "", "data-testid": "descargar-paquete" }, "Paquete de auditoría");
  const falla = el("p", { class: "text-sm text-frenar", role: "alert", "data-testid": "error-descarga" });
  paquete.onclick = async (ev) => {
    ev.preventDefault();
    falla.textContent = "";
    try { await api.descargar("/api/auditoria/paquete", "paquete-auditoria.json"); } catch (e) { falla.textContent = e.message; }
  };
  const menu = el("div", { class: "panel panel-fuerte absolute right-0 z-20 mt-2 grid w-56 gap-2 p-3" }, "", [tema, paquete, falla]);
  return el("details", { class: "relative", "data-testid": "opciones" }, "", [el("summary", { class: "btn btn-sec cursor-pointer list-none" }, "Opciones"), menu]);
}

function montarNav() {
  aplicarTema(memoria.leer("tema"));
  const actual = location.pathname.split("/").pop() || "index.html";
  const paso = Number(new URLSearchParams(location.search).get("demo")) || 0;
  const barra = el("nav", { class: "flex flex-wrap items-center gap-2 border-b border-linea px-4 py-2 sm:px-6", "aria-label": "Paginas", "data-testid": "nav" });
  PAGINAS.forEach((p) => {
    const a = el("a", { href: p.href, class: "btn btn-fantasma", "data-testid": "nav-" + p.href.replace(".html", "") }, p.texto);
    if (p.href === actual) a.setAttribute("aria-current", "page");
    barra.append(a);
  });
  const lectura = el("span", { class: "etiqueta-simulada ml-auto", "data-testid": "lectura" });
  const rotular = () => { lectura.textContent = api.lectura === "en_vivo" ? "Lectura en vivo" : api.lectura === "guardada" ? "Lectura guardada" : ""; };
  document.addEventListener("sesion-lista", rotular);
  rotular();
  const confirmar = el("span", { class: "hidden flex-wrap items-center gap-2", "data-testid": "demo-confirmacion", role: "alertdialog" });
  const aviso = el("span", { role: "status" }, "¿Reiniciar la sesión y empezar el guion?");
  const demo = el("button", { type: "button", class: "btn btn-primario", "data-testid": "demo" }, "Demo");
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
  barra.append(lectura, confirmar, demo, montarOpciones());
  document.body.prepend(barra);
  if (paso >= 1 && paso <= ESCENAS.length) montarGuia(paso);
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") cerrar(); });
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
