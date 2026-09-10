#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block2.py -- Block 2: crosswalk rules and correspondence types
=====================================================================

Source: primer chapter 3.6 + 6; structural reference
``data/raw/crossybase-figures/fig01_relation_inventory.mmd`` and
``fig04_rule_cascade.mmd``. No mascot variant covers this block (rules are
not a Crossy component), so it uses the six-way CATEGORY_COLORS scheme
already shared by all seven crossybase-figures sources rather than the
mascot palette.

Writes:

    banner  crossy-rule-cascade.svg/.png
    badge   ontology-track-badge / metadata-track-badge /
            terminology-binding-badge  .svg/.png
    detail  ontology-track-detail / metadata-track-detail /
            terminology-binding-detail / correspondence-types-detail
            .svg/.png

Run standalone: ``python py/step_block2.py``
"""

from __future__ import annotations

import visuals_utils as vu

OUT = vu.BLOCK_DIRS["block2"]

ONTOLOGY = vu.CATEGORY_COLORS["domain"]        # coral -- classes/nodes
METADATA = vu.CATEGORY_COLORS["metadata"]      # blue -- properties/edges
TERMINOLOGY = vu.CATEGORY_COLORS["terminology"]  # green -- concepts/individuals
VALIDATION = vu.CATEGORY_COLORS["validation"]  # red -- SHACL/rules
PUBLICATION = vu.CATEGORY_COLORS["publication"]  # gold -- KG/reuse

ONTOLOGY_TEXT = "#4a1b0c"
METADATA_TEXT = "#042c53"
TERMINOLOGY_TEXT = "#173404"
VALIDATION_TEXT = "#501313"
PUBLICATION_TEXT = "#412402"


# --------------------------------------------------------------------------- #
# Badges -- text-seal medallions (no mascot for this block)
# --------------------------------------------------------------------------- #
BADGES = {
    "ontology-track": ("R1\u00b7R2", "ontology track", ONTOLOGY, ONTOLOGY_TEXT),
    "metadata-track": ("R3\u00b7R4", "metadata track", METADATA, METADATA_TEXT),
    "terminology-binding": ("R5", "terminology binding", TERMINOLOGY, TERMINOLOGY_TEXT),
}


def build_badges() -> list[str]:
    written = []
    for name, (title, subtitle, colors, text_color) in BADGES.items():
        svg = (
            f'<svg width="480" height="480" viewBox="0 0 480 480" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f'<title>{name} badge</title>\n'
            + vu.svg_badge_seal(240, 240, 228, title, subtitle,
                                 fill=colors["fill"], stroke=colors["stroke"],
                                 text_color=text_color, stroke_width=8)
            + "\n</svg>\n"
        )
        svg_path = OUT / f"{name}-badge.svg"
        png_path = OUT / f"{name}-badge.png"
        vu.write_svg(svg_path, svg)
        vu.write_png_from_svg(svg_path, png_path, zoom=1.0)
        written += [str(svg_path), str(png_path)]
    return written


def badge_seal_small(title: str, subtitle: str, colors: dict, text_color: str, r: float = 26) -> str:
    return vu.svg_badge_seal(r, r, r, title, subtitle, fill=colors["fill"],
                              stroke=colors["stroke"], text_color=text_color, stroke_width=3)


def _header(x: float, y: float, title_badge: str, colors: dict, text_color: str,
            title: str, subtitle: str) -> str:
    return vu.svg_header_seal(x, y, title_badge, colors["fill"], colors["stroke"],
                               text_color, title, subtitle)


# --------------------------------------------------------------------------- #
# Banner -- both rule tracks, grouped, feeding validation and the KG
# --------------------------------------------------------------------------- #
def build_banner() -> list[str]:
    W = 1000

    parts = [
        f'<svg width="{W}" height="560" viewBox="0 0 {W} 560" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>Crosswalk rules as a cascade towards the federated knowledge graphs</title>",
        vu.ARROW_DEFS,
    ]

    # -- outer container: the five rules ---------------------------------------
    parts.append(vu.svg_dashed_container(20, 30, W - 40, 290, "Crosswalk rules R1\u2013R5"))

    # metadata track (top row inside container)
    y1, h = 78, 80
    a1w = vu.box_width("Application metadata", "element", min_width=210)
    a2w = vu.box_width("OCMDP term", "core term", min_width=150)
    a3w = vu.box_width("NCMDP element", "NFDI Core Metadata Profile", min_width=230)
    ax1 = 50
    ax2 = ax1 + a1w + 70
    ax3 = ax2 + a2w + 70
    parts += [
        vu.svg_box(ax1, y1, a1w, h, "Application metadata", "element",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(ax1 + a1w, y1 + h / 2, ax2, y1 + h / 2, "R3"),
        vu.svg_box(ax2, y1, a2w, h, "OCMDP term", "core term",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(ax2 + a2w, y1 + h / 2, ax3, y1 + h / 2, "R4"),
        vu.svg_box(ax3, y1, a3w, h, "NCMDP element", "NFDI Core Metadata Profile",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
    ]

    # ontology track (bottom row inside container)
    y2 = 200
    b1w = vu.box_width("Application ontology", "class", min_width=210)
    b2w = vu.box_width("CIDOC CRM class", "+ extensions", min_width=170)
    b3w = vu.box_width("BFO / NFDIcore", "reference alignment", min_width=200)
    bx1 = 50
    bx2 = bx1 + b1w + 70
    bx3 = bx2 + b2w + 70
    parts += [
        vu.svg_box(bx1, y2, b1w, h, "Application ontology", "class",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
        vu.svg_arrow_labeled(bx1 + b1w, y2 + h / 2, bx2, y2 + h / 2, "R1"),
        vu.svg_box(bx2, y2, b2w, h, "CIDOC CRM class", "+ extensions",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
        vu.svg_arrow_labeled(bx2 + b2w, y2 + h / 2, bx3, y2 + h / 2, "R2"),
        vu.svg_box(bx3, y2, b3w, h, "BFO / NFDIcore", "reference alignment",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
    ]

    # -- single connector from the rules container down to validation ---------
    cx = W / 2
    parts.append(vu.svg_arrow(cx, 320, cx, 400))

    # -- row: R5 note, SHACL gate, knowledge graph -----------------------------
    y3, h3 = 420, 90
    c1w, c2w, c3w = 220, 260, 260
    gap = 50
    total = c1w + c2w + c3w + 2 * gap
    cx1 = (W - total) / 2
    cx2 = cx1 + c1w + gap
    cx3 = cx2 + c2w + gap
    parts += [
        vu.svg_box(cx1, y3, c1w, h3, "R5", "terminology binding",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
        vu.svg_arrow(cx1 + c1w, y3 + h3 / 2, cx2, y3 + h3 / 2),
        vu.svg_box(cx2, y3, c2w, h3, "SHACL validation", "R1\u2013R5 as shapes",
                   fill=VALIDATION["fill"], stroke=VALIDATION["stroke"], text_color=VALIDATION_TEXT),
        vu.svg_arrow(cx2 + c2w, y3 + h3 / 2, cx3, y3 + h3 / 2),
        vu.svg_box(cx3, y3, c3w, h3, "Federated knowledge graph", "NFDI4Objects + NFDI",
                   fill=PUBLICATION["fill"], stroke=PUBLICATION["stroke"], text_color=PUBLICATION_TEXT),
    ]

    parts.append("</svg>\n")
    svg = "\n".join(parts)
    svg_path, png_path = OUT / "crossy-rule-cascade.svg", OUT / "crossy-rule-cascade.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


# --------------------------------------------------------------------------- #
# Details
# --------------------------------------------------------------------------- #
def _caption(x: float, y: float, lines: list[str]) -> str:
    parts = []
    for i, line in enumerate(lines):
        parts.append(f'<text x="{x:.1f}" y="{y + i * 20:.1f}" font-family="Fira Sans" '
                     f'font-size="13" fill="#5f5e5a">{line}</text>')
    return "\n".join(parts)


def build_ontology_track_detail() -> list[str]:
    W, H = 1080, 340
    header = _header(40, 30, "R1\u00b7R2", ONTOLOGY, ONTOLOGY_TEXT,
                      "Block 2 -- ontology track", "R1, R2")

    y, h = 130, 90
    b1w = vu.box_width("Application ontology", "class", min_width=220)
    b2w = vu.box_width("CIDOC CRM class", "+ extensions", min_width=190)
    b3w = vu.box_width("BFO / NFDIcore", "reference alignment", min_width=220)
    x1, x2, x3 = 40, 40 + b1w + 90, 40 + b1w + 90 + b2w + 90

    body = "\n".join([
        vu.svg_box(x1, y, b1w, h, "Application ontology", "class",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + h / 2, x2, y + h / 2, "R1"),
        vu.svg_box(x2, y, b2w, h, "CIDOC CRM class", "+ extensions",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
        vu.svg_arrow_labeled(x2 + b2w, y + h / 2, x3, y + h / 2, "R2"),
        vu.svg_box(x3, y, b3w, h, "BFO / NFDIcore", "reference alignment",
                   fill=PUBLICATION["fill"], stroke=PUBLICATION["stroke"], text_color=PUBLICATION_TEXT),
        _caption(40, 260, [
            "R1 \u2014 every class of an application ontology references a CIDOC CRM class "
            "(rdfs:subClassOf or owl:equivalentClass)",
            "R2 \u2014 CIDOC CRM classes used are themselves aligned to BFO and, through it, NFDIcore",
        ]),
    ])
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>R1 and R2: the ontology track</title>\n{vu.ARROW_DEFS}\n{header}\n{body}\n</svg>\n')
    svg_path, png_path = OUT / "ontology-track-detail.svg", OUT / "ontology-track-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_metadata_track_detail() -> list[str]:
    W, H = 980, 340
    header = _header(40, 30, "R3\u00b7R4", METADATA, METADATA_TEXT,
                      "Block 2 -- metadata track", "R3, R4")

    y, h = 130, 90
    b1w = vu.box_width("Application metadata", "schema element", min_width=220)
    b2w = vu.box_width("OCMDP term", "core term", min_width=170)
    b3w = vu.box_width("NCMDP element", "NFDI Core Metadata Profile", min_width=250)
    x1, x2, x3 = 40, 40 + b1w + 70, 40 + b1w + 70 + b2w + 70

    body = "\n".join([
        vu.svg_box(x1, y, b1w, h, "Application metadata", "schema element",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + h / 2, x2, y + h / 2, "R3"),
        vu.svg_box(x2, y, b2w, h, "OCMDP term", "core term",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(x2 + b2w, y + h / 2, x3, y + h / 2, "R4"),
        vu.svg_box(x3, y, b3w, h, "NCMDP element", "NFDI Core Metadata Profile",
                   fill=PUBLICATION["fill"], stroke=PUBLICATION["stroke"], text_color=PUBLICATION_TEXT),
        _caption(40, 260, [
            "R3 \u2014 every element of an application metadata schema maps to an OCMDP term "
            "(a catch-all term is a legitimate, visible outcome)",
            "R4 \u2014 every OCMDP term is crosswalked to the NCMDP (skos:exactMatch, closeMatch or broadMatch)",
        ]),
    ])
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>R3 and R4: the metadata track</title>\n{vu.ARROW_DEFS}\n{header}\n{body}\n</svg>\n')
    svg_path, png_path = OUT / "metadata-track-detail.svg", OUT / "metadata-track-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_terminology_binding_detail() -> list[str]:
    W, H = 1000, 400
    header = _header(40, 30, "R5", TERMINOLOGY, TERMINOLOGY_TEXT,
                      "Block 2 -- terminology binding", "R5")

    y, h = 130, 90
    b1w = vu.box_width("OCMDP term", "concept or entity object", min_width=230)
    b2w = vu.box_width("Admissible terminologies", "one or more may apply", min_width=280)
    x1 = 60
    x2 = x1 + b1w + 90

    tag_y = 260
    tags = ["TS4NFDI", "DANTE", "BARTOC"]
    tag_w = 130
    tag_gap = 24
    tags_total = len(tags) * tag_w + (len(tags) - 1) * tag_gap
    tag_x0 = x2 + b2w / 2 - tags_total / 2

    body_parts = [
        vu.svg_box(x1, y, b1w, h, "OCMDP term", "concept or entity object",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + h / 2, x2, y + h / 2, "R5"),
        vu.svg_box(x2, y, b2w, h, "Admissible terminologies", "one or more may apply",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
    ]
    # fan out to each example tag, rather than a single arrow that would
    # misleadingly point at only the middle one
    fan_origin_x, fan_origin_y = x2 + b2w / 2, y + h
    for i, tag in enumerate(tags):
        tx = tag_x0 + i * (tag_w + tag_gap)
        body_parts.append(vu.svg_arrow(fan_origin_x, fan_origin_y, tx + tag_w / 2, tag_y))
        body_parts.append(vu.svg_box(tx, tag_y, tag_w, 46, tag, "",
                                      fill="#f1efe8", stroke="#888780", text_color="#2c2c2a", rx=23))
    body_parts.append(_caption(40, 350, [
        "R5 \u2014 every OCMDP term whose object position takes a concept or an",
        "identified entity declares which terminologies or authority files may supply that value",
    ]))

    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>R5: terminology binding</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body_parts) + "\n</svg>\n")
    svg_path, png_path = OUT / "terminology-binding-detail.svg", OUT / "terminology-binding-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_correspondence_types_detail() -> list[str]:
    """The match-type vocabulary itself (primer 3.6 / fig01): what kind of
    correspondence may be asserted at each of the three levels. No badge --
    this is a cross-cutting reference, not tied to one rule."""
    W, H = 980, 620
    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>Types of correspondence used by the Crossys</title>",
        vu.ARROW_DEFS,
        '<text x="40" y="44" font-family="Fira Sans" font-weight="500" font-size="17" '
        'fill="#2c2c2a">Block 2 -- correspondence types</text>',
        '<text x="40" y="66" font-family="Fira Sans" font-size="13" fill="#5f5e5a">'
        'what a crosswalk statement is allowed to assert, by level</text>',
    ]

    # Ontology level
    parts.append(vu.svg_dashed_container(40, 90, W - 80, 120, "Ontology level \u2014 classes / nodes"))
    y = 140
    b1w = vu.box_width("Application ontology class", min_width=220)
    b2w = vu.box_width("CIDOC CRM class", min_width=180)
    x1, x2 = 70, 70 + b1w + 160
    parts += [
        vu.svg_box(x1, y, b1w, 60, "Application ontology class", "",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + 30, x2, y + 30, "subClassOf \u00b7 equivalentClass"),
        vu.svg_box(x2, y, b2w, 60, "CIDOC CRM class", "",
                   fill=ONTOLOGY["fill"], stroke=ONTOLOGY["stroke"], text_color=ONTOLOGY_TEXT),
    ]

    # Metadata level
    parts.append(vu.svg_dashed_container(40, 230, W - 80, 120, "Metadata level \u2014 properties / edges"))
    y = 280
    b1w = vu.box_width("Application metadata element", min_width=230)
    b2w = vu.box_width("OCMDP term", min_width=150)
    x1, x2 = 70, 70 + b1w + 200
    parts += [
        vu.svg_box(x1, y, b1w, 60, "Application metadata element", "",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + 30, x2, y + 30, "exactMatch \u2026 relatedMatch"),
        vu.svg_box(x2, y, b2w, 60, "OCMDP term", "",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
    ]

    # Terminology level -- two mini-rows, deliberately kept apart
    parts.append(vu.svg_dashed_container(40, 370, W - 80, 220, "Terminology level \u2014 concepts / individuals"))
    y3a = 420
    b1w = vu.box_width("Node object as concept", min_width=210)
    b2w = vu.box_width("Terminology concept", min_width=190)
    x1, x2 = 70, 70 + b1w + 150
    parts += [
        vu.svg_box(x1, y3a, b1w, 55, "Node object as concept", "",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y3a + 27, x2, y3a + 27, "skos:exactMatch"),
        vu.svg_box(x2, y3a, b2w, 55, "Terminology concept", "",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
    ]
    y3b = 500
    b3w = vu.box_width("Individual (a specific place, object)", min_width=250)
    b4w = vu.box_width("Authority item", min_width=170)
    x3, x4 = 70, 70 + b3w + 150
    parts += [
        vu.svg_box(x3, y3b, b3w, 55, "Individual (a specific place, object)", "",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
        vu.svg_arrow_labeled(x3 + b3w, y3b + 27, x4, y3b + 27, "owl:sameAs"),
        vu.svg_box(x4, y3b, b4w, 55, "Authority item", "",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
    ]
    parts.append('<text x="70" y="585" font-family="Fira Sans" font-size="12" fill="#5f5e5a">'
                 'keeping the two apart is deliberate: sameAs on a concept, or exactMatch on an '
                 'individual, is a modelling error (primer 4.4.2)</text>')

    parts.append("</svg>\n")
    svg = "\n".join(parts)
    svg_path = OUT / "correspondence-types-detail.svg"
    png_path = OUT / "correspondence-types-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def main() -> list[str]:
    vu.ensure_dirs()
    written: list[str] = []
    written += build_badges()
    written += build_banner()
    written += build_ontology_track_detail()
    written += build_metadata_track_detail()
    written += build_terminology_binding_detail()
    written += build_correspondence_types_detail()
    return written


if __name__ == "__main__":
    written = main()
    print(f"block2: {len(written)} file(s) written" if written else "block2: nothing to do")
