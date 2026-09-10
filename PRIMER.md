# PRIMER — crossy-visuals

Interner Arbeitsplan. Wird zu Beginn jedes Chats hochgeladen (zusammen mit
dem Repo-Bundle, siehe A5) und am Ende zurückgeschrieben.

## Teil A — Immer gültig

### A1 Ausgangslage

| Repo / Datei | Rolle | Befund |
|---|---|---|
| `crossy-graph/crossy-visuals` (GitHub) | dieses Repo | nur `img/source/` vorhanden, sonst leer, 1 Commit (geprüft 2026-09-10 über GitHub-Weboberfläche; GitHub-REST-API war rate-limited, Inhalt von `img/source/` daher noch nicht im Detail eingesehen — siehe Teil D) |
| `crossybase-figures.zip` (lokal hochgeladen) | inhaltliche Referenz, NICHT die Render-Pipeline dieses Repos | 7 Mermaid-Quellen `fig01`–`fig07` + `py/main.py` (Mermaid-CLI-Renderer, `mmdc` v11.12.0 gepinnt); nach `data/raw/crossybase-figures/` übernommen, unverändert, read-only |
| `CrossyBase_Primer_draft.docx` | Goldstandard für Inhalt | Kap. 4 (Architektur), 6 (Regeln R1–R5), 7 (CrossyBase-Pipeline) sind die Quelle für die vier Blöcke |
| `chublets-software/chublets-visuals` | Referenz-Repo, gleiches Hausmuster | pure-Python + resvg-py, Banner/Badge/Detail-Muster, `CATEGORY_COLORS`, Fira Sans vendored (geprüft 2026-09-10 über GitHub-README) |
| `FDOx-squirrel/fdox-visuals` | Sibling-Repo, gleiches Hausmuster | laut chublets-README vorhanden, noch nicht selbst gesichtet |

**Befund 2026-09-10:** Alle sieben `.mmd`-Quellen benutzen bereits durchgängig
dasselbe informelle Sechs-Farben-Schema (`classDef comp/md/dom/term/val/out`
mit identischen Hex-Werten in jeder Datei). Das wird als `CATEGORY_COLORS`
formalisiert statt neu erfunden (siehe A4).

**Korrektur 2026-09-10:** Die ursprünglich für den Foliensatz-Abgleich
hochgeladene `JCM2026_Muenster_chublets.software.pdf` ist NICHT der
Crossy/Wien-Vortrag, sondern Florians anderer Münster-Talk (chublets.software
/ FAIR4RS-Marketplace). Ohne Auswirkung auf dieses Repo, da der Primer als
Goldstandard gesetzt wurde, nicht der alte Foliensatz.

### A2 Zielbild

```
data/raw/crossybase-figures/*.mmd   Struktur-Quelle (read-only, unverändert)
      │
      ▼  py/step_block*.py          Geometrie + Text je Block (keine Renderlogik)
      │
      ▼  main.py
img/<block>/*.svg                   Quelle, versioniert, nach Block gruppiert
      │
      ▼  resvg-py (in-process)
img/<block>/*.png                   fertige Grafik, transparenter Hintergrund
```

Eigenschaften, an denen sich ein fertiger Block messen lassen muss:

- Zweimaliger Lauf von `python main.py` → `git status` bleibt leer.
- Jede Grafik trägt Block + Rolle (`banner`/`badge`/`detail`) im Dateinamen.
- Farben und Symbole kommen ausschließlich aus `py/visuals_utils.py` — kein
  Hex-Wert wird in einem `step_*.py` dupliziert.
- Läuft ohne externe CLI-Tools (kein `mmdc`, kein Node) — nur `pip install
  -r requirements.txt`.
- `img/source/` wird von keinem Skript gelesen oder überschrieben.

### A3 Querschnittsregeln

- Rohdaten liegen unter `data/raw/`, unverändert, read-only. Was ein Skript
  daraus macht, geht nach `img/`. Damit sieht jede Datei ihrer Lage an, ob
  sie Quelle oder Produkt ist.
- Wiederverwendung heißt Kopieren, nicht Referenzieren (Ausnahme: eine
  gemeinsame Ontologie über ihre w3id-IRI — kommt hier nicht vor).
- Kein Zeitstempel im Output. Kein Generator ruft `datetime.now()`; `RELEASE`
  in `visuals_utils.py` ist von Hand zu pflegen.
- Zweimal laufen lassen, `git status` muss leer bleiben — noch nicht
  verifiziert, weil noch keine echte Grafik gezeichnet wird (S1).
- Netzzugriff ist auf den einen Schritt beschränkt, der etwas holt (hier:
  keiner — alles läuft offline gegen `data/raw/` und `fonts/`).
- Sprache: `PRIMER.md` Deutsch; Code, Kommentare, README, Repo-Außenseite
  British English. Kommunikation mit Florian: informelles Deutsch ("du").

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Render-Pipeline | pure-Python + resvg-py (wie chublets/fdox), kein Mermaid-CLI | 2026-09-10 |
| Blockaufteilung | 4 Inhaltsblöcke (Architektur, Regeln, JNL-Junctions, CrossyBase-Pipeline) + System-Architektur | 2026-09-10 |
| Hausfarben-Paar | Purple (`#5b3fa0`, Komponenten) + Gold (`#8a7420`, Publikation) | 2026-09-10 |
| Sechs-Kategorie-Palette | aus den bestehenden `.mmd`-`classDef`-Werten übernommen, nicht neu erfunden | 2026-09-10 |
| Schrift | Fira Sans (wie chublets/fdox), vendored unter `fonts/` (Regular + Medium) | 2026-09-10 |
| Symbolsprache | Node=Kreis, Edge=Pfeil, Junction=Raute, Ring/Doppelring=Konzept/Individuum, Raute+Haken=Validierung, Mini-Graph=Publikation — aus dem Primer-Vokabular (Kap. 7.2) abgeleitet | 2026-09-10, **Vorschlag**, wird agil angepasst sobald die ersten Details gezeichnet sind |
| Use-Cases (A1/A2/B1/B2/B3) & NFDI-Bezug | bewusst NICHT Teil dieses Repos — baut Florian direkt in den Slides | 2026-09-10 |
| `img/source/` | bleibt unverändert, wird direkt im GitHub-Repo von Florian gepflegt, dient als visuelle Referenz, kein Renderinput | 2026-09-10 |
| Zeitdruck (Vortrag 16.9.) | ausdrücklich kein Kriterium für dieses Repo — "wir brauchen hier nur den Visualisierungsgrundstock" | 2026-09-10 |

### A5 Was in welchem Chat hochgeladen wird

Für den nächsten Schritt (S2 ff.) reicht ein Bundle aus PRIMER.md + Repo,
ohne `fonts/` (groß, ändert sich nicht) und ohne `data/raw/` (ändert sich
nicht, außer der Primer wird überarbeitet):

```
robocopy . ..\crossy-visuals-bundle /E /XD .git __pycache__ fonts
Compress-Archive -Path ..\crossy-visuals-bundle\* -DestinationPath ..\crossy-visuals-bundle.zip -Force
```

Nicht hochladen: `fonts/*.ttf` (Binärdateien, unverändert), `__pycache__/`,
`.git/`.

### A6 IRI-Landkarte

Entfällt — dieses Repo publiziert keine eigenen IRIs (keine RDF-Ausgabe).

## Teil B — Schritt-Übersicht

| Schritt | Inhalt | Status |
|---|---|---|
| S0 | Entscheidungen: Render-Pipeline, Blöcke, Farben/Schrift/Symbole | erledigt (A4) |
| S1 | Repo-Skeleton: Layout, `main.py`, `visuals_utils.py`, `requirements.txt`, `LICENSE`, `CITATION.cff`, `.gitignore`, `README.md`, Font-Vendoring | **in Arbeit (dieser Chat)** |
| S2 | Block 1 — Crossy-Architektur (Banner + 3 Badges + 3 Details) | offen |
| S3 | Block 2 — Crosswalk-Regeln (Banner + 3 Badges + 4 Details) | offen |
| S4 | Block 3 — JNL-Junctions (Banner + 4 Badges + 4 Details) | offen |
| S5 | Block 4 — CrossyBase-Pipeline (Banner + 4 Badges + 4 Details) | offen |
| S6 | System-Architektur (konsolidiertes Diagramm) | offen |

## Teil C — Die Schritte im Detail

### S1 — Repo-Skeleton

**Ziel:** lauffähiges Grundgerüst, noch ohne Bildinhalte.

**Substanz:**
- Layout wie in A2/README beschrieben, fünf `step_*.py`-Stubs (block1–4,
  system), jeder mit dokumentiertem Plan (Banner/Badges/Details) im
  Docstring, aber `main()` gibt `[]` zurück.
- `visuals_utils.py`: `RELEASE`, Pfade, `ensure_dirs()`, `CROSSY_PURPLE`,
  `CROSSY_GOLD`, `CATEGORY_COLORS` (6-teilig, aus den `.mmd`-`classDef`
  übernommen), `SYMBOLS`-Vokabular, `write_svg()`, `write_png_from_svg()`
  (resvg-py, `font_files=[FONT_REGULAR, FONT_MEDIUM]`,
  `skip_system_fonts=True`).
- `data/raw/crossybase-figures/`: die 7 `.mmd` unverändert kopiert.
- `fonts/`: `FiraSans-Regular.ttf`, `FiraSans-Medium.ttf`,
  `LICENSE-FiraSans.txt` (SIL OFL 1.1), aus `github.com/mozilla/Fira`.
- `requirements.txt`: `resvg-py==0.5.0`, mit Begründung im Kommentar.

**Abnahme:** `python main.py` läuft durch und meldet für jeden Schritt
"nichts zu tun"; `git status` bleibt nach zweitem Lauf leer.

**Erledigt 2026-09-10:**
- `resvg-py` als echtes PyPI-Paket verifiziert (`resvg_py.svg_to_bytes`,
  einzige öffentliche Funktion; nimmt `svg_path`/`svg_string`, `font_files`,
  `skip_system_fonts`, `background`, `zoom`, gibt PNG-Bytes ohne eingebetteten
  Zeitstempel zurück — anders als matplotlib braucht es daher **keine**
  `wd_repro`-artige Nachbehandlung für Byte-Identität; noch nicht mit echtem
  Content verifiziert, siehe Teil D).
- Fira Sans (Regular + Medium) per `git clone --depth 1
  https://github.com/mozilla/Fira.git` gezogen und vendored.
- `python main.py`, `python main.py --list`, `--dry-run` in der Sandbox
  gegen das frisch gebaute Skeleton ausgeführt — siehe "Verifiziert" im
  Lieferungs-Kommentar dieses Chats.

## Teil D — Offene Punkte

- **Byte-Identität noch nicht real verifiziert** — erst möglich, sobald S2
  eine echte SVG/PNG schreibt. Dann: zweimal `python main.py --only block1`
  laufen lassen, `git status` und `cmp` auf `img/block-1-*/*.png` prüfen.
- **`img/source/` Inhalt ungesichtet** — GitHub-REST-API war beim Bau dieses
  Skeletts rate-limited; welche Rohgrafiken dort genau liegen (Dateinamen,
  Format) ist unbekannt. Vor S2 kurz nachsehen, ob sie die Blockplanung
  beeinflussen.
- **Symbolsprache ist ein Vorschlag** (siehe A4) — laut Absprache "agil
  anpassen", sobald die ersten Details gezeichnet sind und sich zeigt, ob
  z. B. Ring/Doppelring bei 24–32 px Badge-Größe überhaupt unterscheidbar
  bleiben.
- **Anja Gerbers ORCID fehlt** in `CITATION.cff` (TODO-Platzhalter,
  übernommen aus `crossybase-figures/CITATION.cff`, dort ebenfalls offen).
- **Zenodo-DOI / Versionsnummer** noch nicht vergeben.
- **`FDOx-squirrel/fdox-visuals`** wird im chublets-README als Sibling
  genannt, aber noch nicht selbst gesichtet — falls es vom chublets-Muster
  abweicht, ggf. Anpassungsbedarf an A3/A4.
