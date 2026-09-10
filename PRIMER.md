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

**Befund 2026-09-10 (img/source gesichtet):** Florian hat bereits ein
fertiges Crossy-Maskottchen (Vektor-SVG + PNG, kein eingebettetes Raster) in
vier Farbvarianten: `Crossy.png/.svg` (Basis, grau/silber), `Crossy_MaCHeCO`
(grün), `Crossy_OCMDP` (petrol/teal), `Crossy_OMJO` (violett = **JNL**,
bestätigt: "OMJO ist Junktion daher das J darin"). Jede Variante zeigt Crossy
auf einem Wissensgraphen aus Kreisen/Dreiecken/Sternen, durch Pfeile
verbunden — die Netzwerk-Metapher war schon fertig gezeichnet. Dominante
Körperfarben aus den PNGs gezogen (`data/raw`-artige Stichprobe, nicht
Pixel-für-Pixel-exakt): Basis `#909090`, MaCHeCO `#206048`, OCMDP `#386870`,
JNL `#482870`. Das ersetzt die ursprüngliche Idee einer einzigen
"Komponenten"-Purpur-Farbe für alle drei Crossys (siehe A4-Revision).

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
| Komponenten-Farben | **Revision:** nicht ein gemeinsames Purpur für "Komponenten", sondern die echten Maskottchen-Farben pro Crossy — OCMDP Teal `#386870`, MaCHeCO Grün `#206048`, JNL Violett `#482870`, System/neutral Grau `#909090`. Sechs-Kategorie-Schema (validation/publication/…) aus den `.mmd` bleibt für Blöcke 2–4 bestehen, dort gibt es kein Maskottchen | 2026-09-10 |
| OMJO | = JNL-Variante des Maskottchens ("Junktion", daher J) | 2026-09-10, bestätigt von Florian |
| Badges als Maskottchen-Ausschnitt | Kopf-Crop (Bildanteil 44–90 % Breite, 0–44 % Höhe, generalisiert über alle vier Varianten), quadratisch gepolstert, als Medaillon (Kreis in Komponentenfarbe) gerahmt | 2026-09-10 |
| Kopf-Crop-Fraktion | **Dritte Korrektur:** `(0.47, 0.0, 0.83, 0.45)` behob die Verjüngung, aber der Crop war nicht quadratisch — das nachträgliche Auf-Quadrat-Polstern (`pad_frac`) fügte transparente Streifen oben/unten hinzu, die im Kreis als flache Farbfläche durchschienen (derselbe "Kinn abgeschnitten"-Effekt, nur eine Ebene tiefer). Neu: Crop ist von vornherein quadratisch (`BADGE_HEAD_TOP_FRAC`/`BADGE_HEAD_BOTTOM_FRAC`/`BADGE_HEAD_CENTER_X_FRAC` statt eines Rechtecks; Seitenlänge = vertikale Spanne in Pixeln, keine Polsterung mehr nötig). Kopf füllt jetzt den Kreis randvoll | 2026-09-10 |
| Zoom-Stufe | **Vierte Korrektur:** `BADGE_HEAD_BOTTOM_FRAC = 0.45` wirkte zu nah rangezoomt ("das ist zu nah rangezoomt"). Auf `0.52` erweitert — mehr Luft um den Kopf, ohne die Graph-Dekoration wieder einzufangen (gegen alle drei Varianten geprüft) | 2026-09-10 |
| Pfeil-Label-Abstand | **Design-Feinschliff (nach S6):** `svg_arrow_labeled()` hatte nur 8px Abstand zwischen Pfeillinie und Label-Baseline — wirkte wie Text, der auf dem Pfeil sitzt, statt darüber zu schweben (Florian am JNL-Banner aufgefallen). Auf 14px erhöht. Betrifft alle 27 Stellen, die `svg_arrow_labeled()` nutzen (Block 2–4, System) — alle nachgeprüft, keine neuen Kollisionen | 2026-09-10 |
| Schema-Level-Container-Innenabstand | Boxen berührten exakt den unteren Container-Rand (0px Polsterung) in Block 3s Banner, während "Instance-level junctions" ~30px Polsterung hatte — Container-Höhe von 130 auf 170 erhöht, nachfolgende Koordinaten verschoben | 2026-09-10 |
| Arrow-Marker in resvg | `context-stroke` (aus dem Chat-Visualizer-Muster übernommen) wird von resvg NICHT unterstützt — Pfeilspitzen blieben unsichtbar. Fest auf `#73726c` gepinnt (`ARROW_STROKE` in `visuals_utils.py`) | 2026-09-10 |

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
| S2 | Block 1 — Crossy-Architektur (Banner + 3 Badges + 3 Details) | **erledigt (dieser Chat)** |
| S3 | Block 2 — Crosswalk-Regeln (Banner + 3 Badges + 4 Details) | **erledigt (dieser Chat)** |
| S4 | Block 3 — JNL-Junctions (Banner + 4 Badges + 4 Details) | **erledigt (dieser Chat)** |
| S5 | Block 4 — CrossyBase-Pipeline (Banner + 4 Badges + 4 Details) | **erledigt (dieser Chat)** |
| S6 | System-Architektur (konsolidiertes Diagramm) | **erledigt (dieser Chat)** |

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

### S2 — Block 1: Crossy-Architektur

**Ziel:** Banner + 3 Badges + 3 Details, mit dem echten Maskottchen statt
erfundener Node/Edge-Symbolik.

**Substanz:**
- `crop_badge_image()`, `image_data_uri()`, `SOURCE_MASCOTS`,
  `COMPONENT_COLORS` in `visuals_utils.py` (liest `img/source/Crossy*.png`,
  Pillow-Abhängigkeit neu in `requirements.txt`).
- Generische SVG-Bausteine (`svg_box`, `svg_arrow`, `svg_dashed_container`,
  `svg_badge_medallion`, `svg_header`, `box_width`/`text_width`) in
  `visuals_utils.py`, damit `step_block2..4` nicht bei null anfangen.
- `step_block1.py`: 3 Badges (Medaillon in Komponentenfarbe), 1 Banner
  (drei Welten, drei Crossys, JNL-Kopplung, KG-Output), 3 Details
  (OCMDP-Kette, MaCHeCO-Kette, JNL-Hub-Diagramm), jedes Detail mit
  Badge+Kopfzeile.

**Abnahme:** `python main.py --only block1` läuft durch, 14 Dateien; zweimal
laufen lassen → `git status` bleibt leer.

**Erledigt 2026-09-10:**
- `img/source/` erfolgreich über `raw.githubusercontent.com` gezogen (REST-
  API-Rate-Limit war nur für die `contents`/`git/trees`-Endpunkte relevant,
  Rohdateien selbst sind öffentlich erreichbar).
- Kopf-Crop-Fraktion zunächst als (0.44, 0.0, 0.90, 0.44) gegen Basis- und
  OCMDP-Variante visuell verifiziert; **nach Feedback korrigiert** auf
  (0.46, 0.0, 0.84, 0.40), weil die erste Fassung ein Fragment der
  Graph-Dekoration (Stern/Dreieck) am Bildrand stehen ließ. Zweite Fassung
  gegen alle vier Varianten geprüft.
- Zwei Render-Bugs gefunden und behoben: `context-stroke` an den
  Pfeilmarkern wird von resvg ignoriert (Pfeilspitzen unsichtbar) → fest auf
  `#73726c` gepinnt; z-Order im JNL-Detail verdeckte die Pfeilspitzen am
  Medaillon-Rand → Medaillon zuerst zeichnen, Pfeile und Boxen danach.
- Determinismus doppelt verifiziert: einmal im Sandbox-Build, einmal auf
  einer frisch aus dem S1-Zip wiederhergestellten Kopie mit angewendetem
  Patch — beide Läufe byte-identisch zueinander und über zwei Durchläufe.

### S3 — Block 2: Crosswalk-Regeln

**Ziel:** Banner + 3 Badges + 4 Details für R1–R5 und das Korrespondenztyp-
Vokabular. Kein Maskottchen (keine Crossy-Variante für "Regeln"), daher die
Sechs-Kategorie-Palette aus den `.mmd`-Quellen.

**Substanz:**
- `svg_arrow_labeled()`, `svg_badge_seal()`, `svg_header_seal()` in
  `visuals_utils.py` — Textsiegel-Badges (farbiger Kreis + Regel-Kürzel)
  für Blöcke ohne Maskottchen, beschriftete Pfeile für Regel-Kanten.
- `step_block2.py`: 3 Badges (R1·R2 / R3·R4 / R5), 1 Banner (beide Spuren
  in einem gestrichelten Container, ein Pfeil runter zu R5/SHACL/KG-Zeile),
  4 Details (ontology-track, metadata-track, terminology-binding je mit
  Regeltext als Bildunterschrift; correspondence-types als eigenständiges
  Referenzdiagramm ohne Badge, drei Ebenen in eigenen Containern).

**Abnahme:** `python main.py --only block2` läuft durch, 16 Dateien; zweimal
laufen lassen → `git status` bleibt leer.

**Erledigt 2026-09-10:**
- Layout-Ansatz bewusst vereinfacht gegenüber `fig04_rule_cascade.mmd`: statt
  jede Spur einzeln zum SHACL-Knoten zu verdrahten (führte beim Entwerfen zu
  Pfeilen, die durch fremde Boxen laufen, weil beide Spuren dieselben
  Spalten-x-Positionen belegen), sind beide Spuren in einem gemeinsamen
  gestrichelten Container zusammengefasst, mit einem einzelnen Pfeil vom
  Container zur R5/SHACL/KG-Zeile. Präzision pro Regel bleibt den
  Detail-Diagrammen vorbehalten.
- Zwei Render-Bugs gefunden und behoben: der Pfeil von "Admissible
  terminologies" zu den drei Beispiel-Tags zeigte nur auf die mittlere
  (DANTE) statt auf alle drei — jetzt Fächer-Pfeile zu jedem Tag einzeln;
  die R5-Bildunterschrift lief rechts aus dem Canvas — Canvas verbreitert
  und auf zwei Zeilen umgebrochen.
- Banner hatte ~150px unbenutzten Leerraum am unteren Rand (viewBox-Höhe
  nicht an den tatsächlichen Inhalt angepasst) — korrigiert.
- Determinismus doppelt verifiziert (Sandbox-Build + frische Kette aus
  S1 + allen fünf Block-1-Patches + diesem Patch).

### S4 — Block 3: JNL-Junctions

**Ziel:** die eigentliche 4er-Kette — Banner + 4 Badges + 4 Details für
Schema-Junction und die drei Instanz-Junctions (Graph, Terminologie ·
Konzept, Terminologie · Individuum).

**Substanz:**
- Badges als Textsiegel in JNL-Violett (alle vier sind JNL-Submechanismen);
  das Maskottchen-Foto erscheint nur einmal, im Banner-Header, nicht viermal.
- Banner: gestrichelter Container "Schema-level junction" oben, Pfeil
  "constrains" runter zu gestricheltem Container "Instance-level junctions"
  mit den drei Mini-Ketten nebeneinander.
- 4 Details, `schema-junction-detail` zusätzlich mit einer Beispieltabelle
  (location→Place, related person→Actor, type→Concept aus Primer 4.4.1).

**Abnahme:** `python main.py --only block3` läuft durch, 18 Dateien; zweimal
laufen lassen → `git status` bleibt leer.

**Erledigt 2026-09-10:**
- Mehrere Pfeilbeschriftungen liefen anfangs in die Folge-Box hinein
  ("declares admissible cla|ss", "describ|es", "exactMa|tch", "sameA|s") —
  Lücken zwischen den Boxen durchgängig vergrößert (Banner-Mini-Ketten von
  30px auf 90px, Schema-Junction-Detail auf 210px, Graph-Junction-Detail auf
  170px). `svg_arrow_labeled()` prüft die Lückenbreite nicht automatisch —
  das bleibt manuelle Sorgfalt beim Bauen jedes Details.
- Gruppenlabels im Banner kollidierten zunächst mit dem Container-Titel
  (beide zu nah beieinander) — Abstand vergrößert, Container-Titel gekürzt.
- Container-Höhe im Banner an den tatsächlichen Inhalt angepasst (vorher
  ~150px unbenutzter Leerraum unten).
- Determinismus doppelt verifiziert.

### S5 — Block 4: CrossyBase-Pipeline

**Ziel:** Banner + 4 Badges + 4 Details für Curate → Export → Validate →
Publish. Kein Maskottchen (CrossyBase ist die Kuratierungsumgebung, keiner
der drei Crossys) — Sechs-Kategorie-Palette, diesmal deckungsgleich mit den
Original-Farben aus `fig07_export_pipeline.mmd` (`wb`=component/purple,
`proc`=metadata/blue, `val`=validation/red, `out`=publication/gold).

**Substanz:**
- Badges als Textsiegel in den vier Stage-Farben.
- Banner: Migrations-Eingang (Internal spreadsheet) → Curate → Export →
  Validate → Publish, mit gestrichelter "invalid"-Rückkopplungsschleife
  von Validate zu Curate (Bogen oberhalb der Hauptkette) und Fächer-Pfeilen
  von Publish zu drei Reuse-Zielen.
- 4 Details: `curate-detail` (die fünf Entity-Typen aus Primer 7.2, inkl.
  Dictionary/Terms/Entities/Profile/Lists-Beziehungen), `export-detail`
  (SPARQL CONSTRUCT + Python → SKOS/OWL), `validate-detail` (SHACL-Gate mit
  beiden Ausgängen), `publish-detail` (Fächer zu TS4NFDI/DANTE,
  NFDI4Objects-KG, Projekt-Reuse).

**Abnahme:** `python main.py --only block4` läuft durch, 18 Dateien; zweimal
laufen lassen → `git status` bleibt leer.

**Erledigt 2026-09-10:**
- Banner-Canvas zu schmal für den Reuse-Fächer unter "Publish" — von 1300
  auf 1500 verbreitert (rechte Box lief sonst aus dem Bild).
- `curate-detail`: Lücke vor "Entities" zu knapp für das Label "schema
  junction" — von 90 auf 150px vergrößert (derselbe Fehlertyp wie in S4,
  jedes Mal manuell zu prüfen, da `svg_arrow_labeled()` die Breite nicht
  selbst validiert).
- `validate-detail`: "Back to curation"-Box kollidierte anfangs mit der
  Bildunterschrift (beide auf derselben y-Position) — Box nach oben, Bild-
  unterschrift-Start nach unten verschoben, Canvas vergrößert. Der
  "invalid"-Pfeil zielte zudem knapp daneben (Endpunkt lag rechts neben der
  Box statt auf ihr) — Zielpunkt auf die Box-Mitte korrigiert.
- Determinismus doppelt verifiziert.

### S6 — System-Architektur

**Ziel:** ein Bird's-eye-Diagramm, das Block 1 (die drei Crossys, echte
Maskottchen-Badges), Block 3 (JNL als Kopplung) und Block 4 (CrossyBase-
Pipeline, gleiche Stufenfarben) zusammenführt — analog zu
`chublets-software-architecture`.

**Substanz:** `step_system.py` liest Farben/Maskottchen direkt aus den
bestehenden Konstanten (`COMPONENT_COLORS`, `CATEGORY_COLORS`,
`crop_badge_image()`) statt sie zu duplizieren. Drei Ebenen: "The Crossys"
(OCMDP/MaCHeCO-Medaillons oben, JNL-Medaillon mittig darunter mit
Kopplungslinien zu beiden), Pfeil "curated & validated in" zur
"CrossyBase pipeline" (Curate→Export→Validate→Publish, mit der
invalid-Rückkopplungsschleife aus Block 4), Pfeil zur abschließenden
"Federated knowledge graph ecosystem"-Box.

**Abnahme:** `python main.py --only system` läuft durch, 2 Dateien; zweimal
laufen lassen → `git status` bleibt leer.

**Erledigt 2026-09-10:**
- **Echter XML-Bug gefunden und repo-weit behoben:** das Label "curated &
  validated in" enthielt ein rohes `&` — resvg meldete "malformed entity
  reference" und der Schritt brach komplett ab (erster Fall, in dem ein
  Fehler nicht nur eine Überlappung war, sondern den Build tatsächlich zum
  Scheitern brachte). Ursache: kein Helfer in `visuals_utils.py` escapte
  je Text in ein SVG-Textelement. Fix: `xml_escape()` ergänzt und in
  `svg_box`, `svg_arrow_labeled`, `svg_dashed_container`, `svg_badge_seal`,
  `svg_header`, `svg_header_seal` sowie den drei lokalen `_caption()`-
  Funktionen in `step_block2/3/4.py` angewendet. Blöcke 1–4 danach erneut
  gebaut und bestätigt **byte-identisch** zum vorherigen Stand (kein
  Label dort enthielt Sonderzeichen, der Fix war reine Absicherung).
- JNL-Label kollidierte zunächst mit dem Container-Rand (Label lag
  unterhalb der Container-Bottom-Kante) — Container-Höhe und alle
  nachfolgenden y-Koordinaten angepasst.
- Determinismus doppelt verifiziert; vollständiger `python main.py`-Lauf
  (alle fünf Schritte) bestätigt, dass nichts mehr offen ist.

**Damit sind S1–S6 vollständig.** Alle vier Blöcke plus System-Architektur
sind gebaut, geprüft und committet. Was jetzt noch offen ist, steht in
Teil D.

### Nachtrag 2026-09-10 — Design-Feinschliff am JNL-Banner

Florian hat anhand der hochgeladenen Vorschau am `jnl-junctions-overview`
zwei Layout-Probleme gefunden (nicht Inhalt, reines Aussehen): zu wenig
Abstand zwischen Pfeil und Label, und fehlende Innenpolsterung im
Schema-Level-Container. Beides behoben (siehe A4), alle fünf Schritte neu
gebaut, Blöcke 1 und (bis auf die Label-Abstände) 2/4/System stichprobenartig
gegen Regressionen geprüft, komplettes Repo zweimal durchlaufen lassen —
byte-identisch.

## Teil D — Offene Punkte

- **Symbolsprache für Block 1 ist jetzt das Maskottchen statt erfundener
  Node/Edge-Symbole** — für Block 2–4 (keine Maskottchen-Varianten
  vorhanden) gilt der ursprüngliche Vorschlag aus A4 weiterhin als
  Ausgangspunkt, "agil anpassen" bleibt in Kraft.
- **Badge-Einbettung ist Base64 in der SVG-Quelle** — bläht `img/block-1-*/
  *.svg` auf (~200–650 KB je Datei, PNG-Crop mehrfach eingebettet in Banner
  + 3 Details + 3 Badges). Funktioniert, ist aber nicht besonders
  diff-freundlich. Falls das stört: in einem späteren Schritt auf `xlink:href`
  zu einer einzigen gemeinsamen Datei pro Komponente umstellen, statt der
  Badge-Bilder in jeder Detail-SVG einzeln.
- **Anja Gerbers ORCID fehlt** in `CITATION.cff` (TODO-Platzhalter,
  übernommen aus `crossybase-figures/CITATION.cff`, dort ebenfalls offen).
- **Zenodo-DOI / Versionsnummer** noch nicht vergeben.
- **`FDOx-squirrel/fdox-visuals`** wird im chublets-README als Sibling
  genannt, aber noch nicht selbst gesichtet — falls es vom chublets-Muster
  abweicht, ggf. Anpassungsbedarf an A3/A4.
