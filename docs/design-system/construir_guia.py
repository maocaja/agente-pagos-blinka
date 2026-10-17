#!/usr/bin/env python3
"""Genera guia-de-estilo.html desde tokens.css y falla si un par de colores no cumple su contraste.

Uso: python3 construir_guia.py
Despues: npx @tailwindcss/cli -i entrada.css -o guia.css --minify
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
css = (AQUI / "tokens.css").read_text()


def bloque(selector):
    m = re.search(re.escape(selector) + r"\s*\{(.*?)\n\}", css, re.S)
    return dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", m.group(1)))


CLARO = bloque(":root {\n  color-scheme: light;") if False else None


def tema(nombre):
    if nombre == "claro":
        m = re.search(r":root \{\n  color-scheme: light;(.*?)\n\}", css, re.S)
    else:
        m = re.search(r'\[data-tema="oscuro"\] \{\n  color-scheme: dark;(.*?)\n\}', css, re.S)
    return dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", m.group(1)))


PAPEL = dict(re.findall(r"--(papel[a-z0-9-]*):\s*(#[0-9A-Fa-f]{6})", re.search(r":root, \[data-tema=\"oscuro\"\] \{(.*?)\n\}", css, re.S).group(1)))
TEMAS = {"claro": tema("claro"), "oscuro": tema("oscuro")}


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def cr(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def n(x):
    return f"{x:.1f}".replace(".", ",")


SUPERFICIES = ["lienzo", "panel", "elevado"]
TEXTOS = [("texto", "Texto principal"), ("texto-2", "Texto secundario"), ("texto-3", "Texto terciario"),
          ("veredicto-pagar", "Pagar"), ("veredicto-frenar", "Frenar"), ("veredicto-escalar", "Escalar"), ("veredicto-registrar", "Registrar")]
fallos = []


def exigir(nombre, a, b, minimo):
    r = cr(a, b)
    if r < minimo:
        fallos.append(f"{nombre}: {a} sobre {b} = {r:.2f}, minimo {minimo}")


for t, v in TEMAS.items():
    for s in SUPERFICIES:
        for k, _ in TEXTOS:
            exigir(f"{t}/{k} sobre {s}", v[k], v[s], 4.5)
        exigir(f"{t}/linea-fuerte sobre {s}", v["linea-fuerte"], v[s], 3.0)
    exigir(f"{t}/texto del boton sobre acento", v["acento-txt"], v["acento"], 4.5)
    exigir(f"{t}/sello sobre panel", v["sello"], v["panel"], 4.5)
    exigir(f"{t}/sello sobre lienzo", v["sello"], v["lienzo"], 4.5)
exigir("papel-texto sobre papel", PAPEL["papel-texto"], PAPEL["papel"], 4.5)
exigir("papel-2 sobre papel", PAPEL["papel-2"], PAPEL["papel"], 4.5)
exigir("papel-sello sobre papel", PAPEL["papel-sello"], PAPEL["papel"], 4.5)
if fallos:
    print("La guia NO se genero: hay pares de color que no cumplen.", *fallos, sep="\n  ")
    sys.exit(1)


def letra(h):
    return "#111720" if lum(h) > 0.35 else "#FFFFFF"


def muestras(t):
    v = TEMAS[t]
    filas = [("lienzo", "Lienzo", "Fondo de la pantalla"), ("panel", "Panel", "Barra, paneles y campos"), ("elevado", "Elevado", "Cajón, avisos y filas activas"),
             ("linea", "Línea", "Solo separadores"), ("linea-fuerte", "Línea fuerte", "Bordes de controles"),
             ("acento", "Acento", "Acción principal y foco"), ("sello", "Sello", "Firma del recibo y rol simulado")]
    out = []
    for k, nom, uso in filas:
        h = v[k]
        out.append(f'<div class="rounded-[14px] border border-linea-fuerte p-3.5" style="background:{h};color:{letra(h)}"><p class="font-semibold">{nom}</p><p class="text-[15px] opacity-90">{h}</p><p class="text-[15px] opacity-80">{uso}</p></div>')
    ver = [("veredicto-pagar", "PAGAR", "pagar"), ("veredicto-frenar", "FRENAR", "frenar"), ("veredicto-escalar", "ESCALAR", "escalar"), ("veredicto-registrar", "REGISTRAR", "registrar")]
    out2 = "".join(f'<div class="rounded-[14px] p-3.5 border" style="border-color:{v[k]};background:{v["panel"]}"><p class="font-semibold" style="color:{v[k]}">{nom}</p><p class="text-[15px]" style="color:{v["texto-2"]}">{v[k]}, {n(cr(v[k], v["panel"]))}:1 sobre el panel</p></div>' for k, nom, _ in ver)
    txt = "".join(f'<div class="rounded-[14px] p-3.5 border" style="background:{v["panel"]};border-color:{v["linea"]}"><p class="font-semibold" style="color:{v[k]}">{nom}</p><p class="text-[15px]" style="color:{v["texto-2"]}">{v[k]}, {n(cr(v[k], v["lienzo"]))}:1</p></div>' for k, nom in TEXTOS[:3])
    return ('<div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">' + "".join(out) + '</div>'
            '<div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 mt-2.5">' + txt + '</div>'
            '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-2.5">' + out2 + '</div>')


def tabla(t):
    v = TEMAS[t]
    filas = []
    for k, nom in TEXTOS:
        celdas = "".join(f"<td class='py-2 pr-4'>{n(cr(v[k], v[s]))}</td>" for s in SUPERFICIES)
        filas.append(f"<tr class='border-b border-linea'><td class='py-2 pr-4'><span class='inline-block w-3 h-3 rounded-full mr-2 align-middle' style='background:{v[k]}'></span>{nom} <span class='text-texto-3 text-[15px]'>{v[k]}</span></td>{celdas}</tr>")
    celdas = "".join(f"<td class='py-2 pr-4'>{n(cr(v['linea-fuerte'], v[s]))}</td>" for s in SUPERFICIES)
    filas.append(f"<tr class='border-b border-linea'><td class='py-2 pr-4'>Línea fuerte <span class='text-texto-3 text-[15px]'>{v['linea-fuerte']}</span></td>{celdas}</tr>")
    return ("<div class='overflow-x-auto'><table class='w-full max-w-[44rem] text-left cifra'><thead><tr class='text-texto-2 text-[15px] border-b border-linea-fuerte'><th class='py-2 pr-4 font-medium'>Par</th><th class='py-2 pr-4 font-medium'>Lienzo</th><th class='py-2 pr-4 font-medium'>Panel</th><th class='py-2 font-medium'>Elevado</th></tr></thead><tbody>"
            + "".join(filas) + "</tbody></table></div>")


extra = (f"Botón principal: {n(cr(TEMAS['claro']['acento-txt'], TEMAS['claro']['acento']))}:1 en el tema claro y {n(cr(TEMAS['oscuro']['acento-txt'], TEMAS['oscuro']['acento']))}:1 en el oscuro. "
         f"Recibo: texto {n(cr(PAPEL['papel-texto'], PAPEL['papel']))}:1, apoyo {n(cr(PAPEL['papel-2'], PAPEL['papel']))}:1 y sello {n(cr(PAPEL['papel-sello'], PAPEL['papel']))}:1 sobre el papel. "
         f"Sello del rol simulado: {n(cr(TEMAS['claro']['sello'], TEMAS['claro']['panel']))}:1 en el tema claro y {n(cr(TEMAS['oscuro']['sello'], TEMAS['oscuro']['panel']))}:1 en el oscuro.")

html = (AQUI / "plantilla-guia.html").read_text()
html = (html.replace("@@MUESTRAS_CLARO@@", muestras("claro")).replace("@@MUESTRAS_OSCURO@@", muestras("oscuro"))
        .replace("@@TABLA_CLARO@@", tabla("claro")).replace("@@TABLA_OSCURO@@", tabla("oscuro")).replace("@@EXTRA_CONTRASTE@@", extra))
(AQUI / "guia-de-estilo.html").write_text(html)
print("Guia generada. Todos los pares de contraste cumplen (texto 4,5:1, bordes 3:1).")
