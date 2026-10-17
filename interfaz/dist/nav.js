// Navegacion comun y guion de la demo. Solo DOM con textContent: nunca HTML crudo.
const PAGINAS = [
  { href: "index.html", texto: "Decisiones" },
  { href: "reglas.html", texto: "Reglas" },
  { href: "marcador.html", texto: "Marcador" },
  { href: "bandeja.html", texto: "Bandeja" },
  { href: "ataque.html", texto: "Ataque" },
];
const ESCENAS = [
  { pagina: "index.html?decision=dec_11", titulo: "1. Cambio de cuenta", texto: "Sin el agente, esta factura se paga. Con el agente se escala y el motivo esta escrito: la cuenta no es la registrada." },
  { pagina: "bandeja.html", titulo: "2. Las trampas", texto: "Abra cada muestra: el texto de una factura es un dato, no una orden. Decide el motor, con su regla." },
  { pagina: "index.html?decision=dec_01&tecnica=1", titulo: "3. El recibo", texto: "Altere un byte de la copia y pida al guardian que verifique: rechaza con el motivo." },
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

function montarNav() {
  const actual = location.pathname.split("/").pop() || "index.html";
  const paso = Number(new URLSearchParams(location.search).get("demo")) || 0;
  const barra = el("nav", { class: "flex flex-wrap items-center gap-2 border-b border-linea px-6 py-2", "aria-label": "Paginas", "data-testid": "nav" });
  PAGINAS.forEach((p) => {
    const a = el("a", { href: p.href, class: "btn btn-fantasma", "data-testid": "nav-" + p.href.replace(".html", "") }, p.texto);
    if (p.href === actual) a.setAttribute("aria-current", "page");
    barra.append(a);
  });
  const lectura = el("span", { class: "etiqueta-simulada ml-auto", "data-testid": "lectura" });
  const rotular = () => { lectura.textContent = api.lectura === "en_vivo" ? "Lectura en vivo" : api.lectura === "guardada" ? "Lectura guardada" : ""; };
  document.addEventListener("sesion-lista", rotular);
  rotular();
  const confirmar = el("span", { class: "hidden items-center gap-2", "data-testid": "demo-confirmacion", role: "alertdialog" }, "Reiniciar la sesion y empezar el guion?");
  const demo = el("button", { type: "button", class: "btn btn-primario", "data-testid": "demo" }, "Demo");
  const si = el("button", { type: "button", class: "btn btn-peligro", "data-testid": "demo-confirmar" }, "Reiniciar");
  const no = el("button", { type: "button", class: "btn btn-sec", "data-testid": "demo-cancelar" }, "Cancelar");
  confirmar.append(si, no);
  const cerrar = () => { confirmar.classList.add("hidden"); confirmar.classList.remove("flex"); demo.classList.remove("hidden"); };
  demo.onclick = () => { confirmar.classList.remove("hidden"); confirmar.classList.add("flex"); demo.classList.add("hidden"); si.focus(); };
  no.onclick = cerrar;
  si.onclick = async () => {
    si.disabled = true;
    try { await api.pedir("POST", "/api/sesion/reiniciar"); irA(1); } catch (e) { confirmar.textContent = e.message; }
  };
  barra.append(lectura, confirmar, demo);
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
    if (ev.key === "ArrowRight") mover(1);
    else if (ev.key === "ArrowLeft") mover(-1);
    else if (ev.key === "Escape") salirGuia();
  });
  document.body.append(panel);
}

document.addEventListener("DOMContentLoaded", montarNav);
