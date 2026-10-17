# Graph Report - docs  (2026-10-17)

## Corpus Check
- 2 files · ~859 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 15 nodes · 21 edges · 3 communities (2 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3e2cce88`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- construir_guia.py
- Documentación del proyecto
- n

## God Nodes (most connected - your core abstractions)
1. `cr()` - 5 edges
2. `muestras()` - 4 edges
3. `Documentación del proyecto` - 4 edges
4. `lum()` - 3 edges
5. `n()` - 3 edges
6. `letra()` - 3 edges
7. `tabla()` - 3 edges
8. `exigir()` - 2 edges
9. `Dónde está la fuente de verdad` - 1 edges
10. `Páginas publicadas (copia local)` - 1 edges

## Surprising Connections (you probably didn't know these)
- `tabla()` --calls--> `cr()`  [EXTRACTED]
  design-system/construir_guia.py → design-system/construir_guia.py  _Bridges community 0 → community 2_

## Import Cycles
- None detected.

## Communities (3 total, 1 thin omitted)

### Community 0 - "construir_guia.py"
Cohesion: 0.43
Nodes (5): cr(), exigir(), letra(), lum(), muestras()

### Community 1 - "Documentación del proyecto"
Cohesion: 0.40
Nodes (4): Aviso, Documentación del proyecto, Dónde está la fuente de verdad, Páginas publicadas (copia local)

## Knowledge Gaps
- **3 isolated node(s):** `Dónde está la fuente de verdad`, `Páginas publicadas (copia local)`, `Aviso`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 6 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cr()` connect `construir_guia.py` to `n`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `muestras()` connect `construir_guia.py` to `n`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **What connects `Dónde está la fuente de verdad`, `Páginas publicadas (copia local)`, `Aviso` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._