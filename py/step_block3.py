#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block3.py -- Block 3: JNL junctions (the four-chain block)
==================================================================

Source: primer chapter 4.4; structural reference
``data/raw/crossybase-figures/fig03_jnl_subtypes.mmd``. JNL has a mascot
variant (Crossy_OMJO, purple) -- used once in the banner header as the
"seal of authenticity" for the whole block; the four junction-type badges
are text seals in the same purple rather than four copies of the same
photo (which would carry no distinguishing information).

Writes:

    banner  jnl-junctions-overview.svg/.png
    badge   schema-junction-badge / graph-junction-badge /
            terminology-concept-badge / terminology-individual-badge
            .svg/.png
    detail  schema-junction-detail / graph-junction-detail /
            terminology-concept-detail / terminology-individual-detail
            .svg/.png

Run standalone: ``python py/step_block3.py``
"""

from __future__ import annotations

import visuals_utils as vu

OUT = vu.BLOCK_DIRS["block3"]

JNL = vu.COMPONENT_COLORS["jnl"]           # purple -- JNL's own colour
METADATA = vu.CATEGORY_COLORS["metadata"]  # blue -- metadata-side entities
DOMAIN = vu.CATEGORY_COLORS["domain"]      # coral -- domain-side entities
TERMINOLOGY = vu.CATEGORY_COLORS["terminology"]  # green -- concepts/individuals

JNL_TEXT = "#2d1a4a"
METADATA_TEXT = "#042c53"
DOMAIN_TEXT = "#4a1b0c"
TERMINOLOGY_TEXT = "#173404"


# --------------------------------------------------------------------------- #
# Badges -- text seals in JNL purple (all four are JNL sub-mechanisms; the
# mascot photo appears once, in the banner header, not four times over)
# --------------------------------------------------------------------------- #
BADGES = {
    "schema-junction": ("Schema", "junction"),
    "graph-junction": ("Graph", "junction"),
    "terminology-concept": ("Concept", "terminology junction"),
    "terminology-individual": ("Individual", "terminology junction"),
}


def build_badges() -> list[str]:
    written = []
    for name, (title, subtitle) in BADGES.items():
        svg = (
            f'<svg width="480" height="480" viewBox="0 0 480 480" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f'<title>{name} badge</title>\n'
            + vu.svg_badge_seal(240, 240, 228, title, subtitle,
                                 fill=JNL["fill"], stroke=JNL["stroke"],
                                 text_color=JNL_TEXT, stroke_width=8)
            + "\n</svg>\n"
        )
        svg_path = OUT / f"{name}-badge.svg"
        png_path = OUT / f"{name}-badge.png"
        vu.write_svg(svg_path, svg)
        vu.write_png_from_svg(svg_path, png_path, zoom=1.0)
        written += [str(svg_path), str(png_path)]
    return written


def seal_header(x: float, y: float, title_badge: str, title: str, subtitle: str) -> str:
    return vu.svg_header_seal(x, y, title_badge, JNL["fill"], JNL["stroke"], JNL_TEXT,
                               title, subtitle)


def mascot_header(x: float, y: float, title: str, subtitle: str) -> str:
    data_uri = vu.image_data_uri(vu.crop_badge_image("jnl", size=200))
    return vu.svg_header(x, y, data_uri, JNL["fill"], JNL["stroke"], title, subtitle)


# --------------------------------------------------------------------------- #
# Banner -- schema-level junction constrains the three instance-level ones
# --------------------------------------------------------------------------- #
def build_banner() -> list[str]:
    W = 1250

    parts = [
        f'<svg width="{W}" height="560" viewBox="0 0 {W} 560" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>The Junction Node Layer: schema-level and instance-level junctions</title>",
        vu.ARROW_DEFS,
        mascot_header(40, 20, "JNL \u2014 the junction Crossy", "schema- and instance-level junctions"),
    ]

    # -- schema-level junction --------------------------------------------------
    parts.append(vu.svg_dashed_container(40, 120, W - 80, 170, "Schema-level junction \u2014 asserted once per term"))
    y = 170
    b1w = vu.box_width("OCMDP term", "e.g. \u2018location\u2019", min_width=220)
    b2w = vu.box_width("MaCHeCO entity", "e.g. E53 Place", min_width=220)
    cx = W / 2
    x1 = cx - b1w - 100
    x2 = cx + 100
    parts += [
        vu.svg_box(x1, y, b1w, 80, "OCMDP term", "e.g. \u2018location\u2019",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + 40, x2, y + 40, "admissible class"),
        vu.svg_box(x2, y, b2w, 80, "MaCHeCO entity", "e.g. E53 Place",
                   fill=DOMAIN["fill"], stroke=DOMAIN["stroke"], text_color=DOMAIN_TEXT),
    ]

    # -- constrains ---------------------------------------------------------
    parts.append(f'<text x="{cx:.1f}" y="283" text-anchor="middle" font-family="Fira Sans" '
                 f'font-weight="500" font-size="13" fill="{JNL_TEXT}">constrains</text>')
    parts.append(vu.svg_arrow(cx, 290, cx, 318, stroke=JNL["stroke"]))

    # -- instance-level junctions ------------------------------------------
    parts.append(vu.svg_dashed_container(40, 320, W - 80, 200, "Instance-level junctions"))

    group_w = (W - 80 - 2 * 40) / 3  # container width minus two internal gaps
    gy = 410

    def mini_chain(gx: float, label: str, b1: tuple[str, str], b2: tuple[str, str],
                    rel: str, colors1: dict, text1: str, colors2: dict, text2: str) -> list[str]:
        bw = (group_w - 90) / 2
        out = [f'<text x="{gx + group_w/2:.1f}" y="{gy - 14:.1f}" text-anchor="middle" '
               f'font-family="Fira Sans" font-weight="500" font-size="13" '
               f'fill="{JNL_TEXT}">{label}</text>']
        out.append(vu.svg_box(gx, gy, bw, 80, b1[0], b1[1], fill=colors1["fill"],
                               stroke=colors1["stroke"], text_color=text1))
        out.append(vu.svg_arrow_labeled(gx + bw, gy + 40, gx + bw + 90, gy + 40, rel))
        out.append(vu.svg_box(gx + bw + 90, gy, bw, 80, b2[0], b2[1], fill=colors2["fill"],
                               stroke=colors2["stroke"], text_color=text2))
        return out

    parts += mini_chain(
        80, "Graph junction",
        ("Metadata resource", "dataset, record, FDO"), ("Domain entity", "e.g. crm:E22"),
        "describes", METADATA, METADATA_TEXT, DOMAIN, DOMAIN_TEXT,
    )
    parts += mini_chain(
        80 + group_w + 40, "Terminology \u00b7 concept",
        ("Node object", "as concept"), ("Terminology concept", "Getty AAT, DANTE"),
        "exactMatch", DOMAIN, DOMAIN_TEXT, TERMINOLOGY, TERMINOLOGY_TEXT,
    )
    parts += mini_chain(
        80 + 2 * (group_w + 40), "Terminology \u00b7 individual",
        ("Individual", "a specific place, object"), ("Authority item", "Wikidata, OSM"),
        "sameAs", DOMAIN, DOMAIN_TEXT, TERMINOLOGY, TERMINOLOGY_TEXT,
    )

    parts.append("</svg>\n")
    svg = "\n".join(parts)
    svg_path, png_path = OUT / "jnl-junctions-overview.svg", OUT / "jnl-junctions-overview.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


# --------------------------------------------------------------------------- #
# Details
# --------------------------------------------------------------------------- #
def _caption(x: float, y: float, lines: list[str]) -> str:
    return "\n".join(
        f'<text x="{x:.1f}" y="{y + i * 20:.1f}" font-family="Fira Sans" font-size="13" '
        f'fill="#5f5e5a">{vu.xml_escape(line)}</text>' for i, line in enumerate(lines)
    )


def build_schema_junction_detail() -> list[str]:
    W, H = 1000, 420
    header = seal_header(40, 30, "Schema", "Block 3 -- schema-level junction", "asserted once per term")

    y, h = 130, 90
    b1w = vu.box_width("OCMDP term", "location / related person / type", min_width=260)
    b2w = vu.box_width("MaCHeCO entity", "admissible object class", min_width=240)
    x1, x2 = 60, 60 + b1w + 210
    body = [
        vu.svg_box(x1, y, b1w, h, "OCMDP term", "the property",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + h / 2, x2, y + h / 2, "declares admissible class"),
        vu.svg_box(x2, y, b2w, h, "MaCHeCO entity", "the object position",
                   fill=DOMAIN["fill"], stroke=DOMAIN["stroke"], text_color=DOMAIN_TEXT),
    ]

    # worked examples table (primer 4.4.1)
    rows = [("location", "Place"), ("related person", "Actor"), ("type", "Concept")]
    ty = 260
    body.append('<text x="60" y="' + str(ty) + '" font-family="Fira Sans" font-weight="500" '
                'font-size="13" fill="#2c2c2a">Examples</text>')
    for i, (term, cls) in enumerate(rows):
        ry = ty + 30 + i * 34
        body.append(vu.svg_box(60, ry, 220, 26, term, "", fill=METADATA["fill"],
                                stroke=METADATA["stroke"], text_color=METADATA_TEXT, rx=6))
        body.append(vu.svg_arrow(280, ry + 13, 340, ry + 13))
        body.append(vu.svg_box(340, ry, 220, 26, cls, "", fill=DOMAIN["fill"],
                                stroke=DOMAIN["stroke"], text_color=DOMAIN_TEXT, rx=6))

    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>The schema-level junction</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / "schema-junction-detail.svg", OUT / "schema-junction-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_graph_junction_detail() -> list[str]:
    W, H = 960, 340
    header = seal_header(40, 30, "Graph", "Block 3 -- graph junction", "instance-level")

    y, h = 140, 90
    b1w = vu.box_width("Metadata resource", "dataset, record, FDO", min_width=230)
    b2w = vu.box_width("Domain entity", "e.g. crm:E22, crm:E53", min_width=230)
    x1, x2 = 60, 60 + b1w + 170
    body = [
        vu.svg_box(x1, y, b1w, h, "Metadata resource", "dataset, record, FDO",
                   fill=METADATA["fill"], stroke=METADATA["stroke"], text_color=METADATA_TEXT),
        f'<text x="{x1 + b1w/2:.1f}" y="{y + h + 24:.1f}" text-anchor="middle" '
        f'font-family="Fira Sans" font-size="12" fill="#5f5e5a">in the metadata graph</text>',
        vu.svg_arrow_labeled(x1 + b1w, y + h / 2, x2, y + h / 2, "describes / is about"),
        vu.svg_box(x2, y, b2w, h, "Domain entity", "e.g. crm:E22, crm:E53",
                   fill=DOMAIN["fill"], stroke=DOMAIN["stroke"], text_color=DOMAIN_TEXT),
        f'<text x="{x2 + b2w/2:.1f}" y="{y + h + 24:.1f}" text-anchor="middle" '
        f'font-family="Fira Sans" font-size="12" fill="#5f5e5a">in the research data graph</text>',
        _caption(40, 280, [
            "The connection that lets a query start in the metadata graph \u2014 a licence, a",
            "responsible institution \u2014 and end in the research data graph, with an object and its find spot.",
        ]),
    ]
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>The graph junction</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / "graph-junction-detail.svg", OUT / "graph-junction-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def _terminology_junction_detail(name: str, badge_title: str, header_title: str,
                                  b1: tuple[str, str], rel: str, b2: tuple[str, str],
                                  caption: list[str]) -> list[str]:
    W, H = 900, 340
    header = seal_header(40, 30, badge_title, header_title, "terminology junction")

    y, h = 140, 90
    b1w = vu.box_width(b1[0], b1[1], min_width=230)
    b2w = vu.box_width(b2[0], b2[1], min_width=230)
    x1, x2 = 60, 60 + b1w + 100
    body = [
        vu.svg_box(x1, y, b1w, h, b1[0], b1[1],
                   fill=DOMAIN["fill"], stroke=DOMAIN["stroke"], text_color=DOMAIN_TEXT),
        vu.svg_arrow_labeled(x1 + b1w, y + h / 2, x2, y + h / 2, rel),
        vu.svg_box(x2, y, b2w, h, b2[0], b2[1],
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),
        _caption(40, 280, caption),
    ]
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>{header_title}</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / f"{name}.svg", OUT / f"{name}.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_terminology_concept_detail() -> list[str]:
    return _terminology_junction_detail(
        "terminology-concept-detail", "Concept", "Block 3 -- terminology junction, concept level",
        ("Node object", "as concept"), "skos:exactMatch",
        ("Terminology concept", "e.g. Getty AAT"),
        [
            "A node object \u2014 an object type, a material \u2014 is matched to a concept in a",
            "controlled vocabulary. This is a graded matching relation, not an identity claim.",
        ],
    )


def build_terminology_individual_detail() -> list[str]:
    return _terminology_junction_detail(
        "terminology-individual-detail", "Individual", "Block 3 -- terminology junction, individual level",
        ("Individual", "a specific place, object"), "owl:sameAs",
        ("Authority item", "Wikidata, GeoNames, OSM"),
        [
            "A specific entity \u2014 a cave, a monument \u2014 is identified with an authority item.",
            "Asserting sameAs on a concept, or exactMatch on an individual, is a modelling error (4.4.2).",
        ],
    )


def main() -> list[str]:
    vu.ensure_dirs()
    written: list[str] = []
    written += build_badges()
    written += build_banner()
    written += build_schema_junction_detail()
    written += build_graph_junction_detail()
    written += build_terminology_concept_detail()
    written += build_terminology_individual_detail()
    return written


if __name__ == "__main__":
    written = main()
    print(f"block3: {len(written)} file(s) written" if written else "block3: nothing to do")
