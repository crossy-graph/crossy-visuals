#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block1.py -- Block 1: Crossy architecture
================================================

Source: primer chapter 4.1; structural reference
``data/raw/crossybase-figures/fig02_components_and_layers.mmd``.
Mascot: ``img/source/Crossy*.png`` (Florian's artwork; see PRIMER.md A4 for
the confirmed colour-to-component mapping).

Writes:

    banner  crossy-architecture-overview.svg/.png
    badge   ocmdp-badge / macheco-badge / jnl-badge  .svg/.png
    detail  ocmdp-detail / macheco-detail / jnl-detail  .svg/.png

Run standalone: ``python py/step_block1.py``
"""

from __future__ import annotations

import visuals_utils as vu

OUT = vu.BLOCK_DIRS["block1"]

BADGE_R = 480  # px, square badge canvas


# --------------------------------------------------------------------------- #
# Badges -- cropped from the mascot, medallion-framed in the component colour
# --------------------------------------------------------------------------- #
def build_badges() -> list[str]:
    written = []
    for component in ("ocmdp", "macheco", "jnl"):
        img = vu.crop_badge_image(component, size=BADGE_R)
        data_uri = vu.image_data_uri(img)
        colors = vu.COMPONENT_COLORS[component]
        cx = cy = BADGE_R / 2
        r = BADGE_R / 2 - 12
        svg = (
            f'<svg width="{BADGE_R}" height="{BADGE_R}" viewBox="0 0 {BADGE_R} {BADGE_R}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f'<title>{component.upper()} badge</title>\n'
            + vu.svg_badge_medallion(cx, cy, r, data_uri, fill=colors["fill"],
                                      stroke=colors["stroke"], stroke_width=8)
            + "\n</svg>\n"
        )
        svg_path = OUT / f"{component}-badge.svg"
        png_path = OUT / f"{component}-badge.png"
        vu.write_svg(svg_path, svg)
        vu.write_png_from_svg(svg_path, png_path, zoom=1.0)
        written.append(str(svg_path))
        written.append(str(png_path))
    return written


def badge_data_uri(component: str, size: int = 200) -> str:
    """Smaller badge crop for embedding inside the banner/detail diagrams."""
    return vu.image_data_uri(vu.crop_badge_image(component, size=size))


# --------------------------------------------------------------------------- #
# Banner -- the three worlds, the three Crossys, the JNL coupling, the KG
# --------------------------------------------------------------------------- #
def build_banner() -> list[str]:
    W, H = 1200, 720
    ocmdp = vu.COMPONENT_COLORS["ocmdp"]
    macheco = vu.COMPONENT_COLORS["macheco"]
    jnl = vu.COMPONENT_COLORS["jnl"]

    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>The Crossys as crosswalk components in a layered architecture</title>",
        vu.ARROW_DEFS,
    ]

    # -- three world containers ------------------------------------------------
    box_w, box_h, gap, top = 360, 260, 20, 40
    x1, x2, x3 = 40, 40 + box_w + gap, 40 + 2 * (box_w + gap)
    parts.append(vu.svg_dashed_container(x1, top, box_w, box_h, "Metadata world"))
    parts.append(vu.svg_dashed_container(x2, top, box_w, box_h, "Research data world"))
    parts.append(vu.svg_dashed_container(x3, top, box_w, box_h, "Terminology world"))

    badge_r = 70
    c1x, c2x, c3x = x1 + box_w / 2, x2 + box_w / 2, x3 + box_w / 2
    badge_cy = top + 120

    parts.append(vu.svg_badge_medallion(c1x, badge_cy, badge_r, badge_data_uri("ocmdp"),
                                         fill=ocmdp["fill"], stroke=ocmdp["stroke"]))
    parts.append(f'<text x="{c1x:.1f}" y="{badge_cy + badge_r + 26:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="16" '
                 f'fill="{ocmdp["stroke"]}">OCMDP</text>')
    parts.append(f'<text x="{c1x:.1f}" y="{badge_cy + badge_r + 46:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-size="12" fill="#5f5e5a">properties / edges</text>')

    parts.append(vu.svg_badge_medallion(c2x, badge_cy, badge_r, badge_data_uri("macheco"),
                                         fill=macheco["fill"], stroke=macheco["stroke"]))
    parts.append(f'<text x="{c2x:.1f}" y="{badge_cy + badge_r + 26:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="16" '
                 f'fill="{macheco["stroke"]}">MaCHeCO</text>')
    parts.append(f'<text x="{c2x:.1f}" y="{badge_cy + badge_r + 46:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-size="12" fill="#5f5e5a">classes / nodes</text>')

    # terminology world: no mascot, plain label block
    parts.append(f'<text x="{c3x:.1f}" y="{badge_cy - 6:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="15" '
                 f'fill="#3d7a2a">controlled vocabularies,</text>')
    parts.append(f'<text x="{c3x:.1f}" y="{badge_cy + 16:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="15" '
                 f'fill="#3d7a2a">thesauri, authority files</text>')
    parts.append(f'<text x="{c3x:.1f}" y="{badge_cy + 42:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-size="12" fill="#5f5e5a">via TS4NFDI, DANTE, BARTOC</text>')

    # -- JNL, the coupling component -------------------------------------------
    jnl_cx, jnl_cy, jnl_r = W / 2, 470, 92
    parts.append(vu.svg_arrow(x1 + box_w / 2, top + box_h, jnl_cx - 80, jnl_cy - jnl_r - 4))
    parts.append(vu.svg_arrow(x2 + box_w / 2, top + box_h, jnl_cx, jnl_cy - jnl_r - 4))
    parts.append(vu.svg_arrow(x3 + box_w / 2, top + box_h, jnl_cx + 80, jnl_cy - jnl_r - 4))
    parts.append(vu.svg_badge_medallion(jnl_cx, jnl_cy, jnl_r, badge_data_uri("jnl"),
                                         fill=jnl["fill"], stroke=jnl["stroke"], stroke_width=6))
    parts.append(f'<text x="{jnl_cx:.1f}" y="{jnl_cy + jnl_r + 30:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="18" '
                 f'fill="{jnl["stroke"]}">JNL</text>')
    parts.append(f'<text x="{jnl_cx:.1f}" y="{jnl_cy + jnl_r + 52:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-size="13" fill="#5f5e5a">couples the components '
                 f'and binds terminologies</text>')

    # -- output: the federated knowledge graph ---------------------------------
    kg_w, kg_h = 460, 70
    kg_x, kg_y = W / 2 - kg_w / 2, 640
    # arrow starts below the two-line JNL label, not at the badge edge, so the
    # connector does not cross through the label text
    parts.append(vu.svg_arrow(jnl_cx, jnl_cy + jnl_r + 68, jnl_cx, kg_y))
    parts.append(vu.svg_box(kg_x, kg_y, kg_w, kg_h, "NFDI4Objects Knowledge Graph",
                             fill="#f5f0d8", stroke="#8a7420", text_color="#412402"))

    parts.append("</svg>\n")
    svg = "\n".join(parts)
    svg_path = OUT / "crossy-architecture-overview.svg"
    png_path = OUT / "crossy-architecture-overview.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


# --------------------------------------------------------------------------- #
# Details -- one focused diagram per component, each headed by its own badge
# --------------------------------------------------------------------------- #
def _detail_shell(title_svg: str, header: str, body: str, W: int, H: int) -> str:
    return (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
        f'<title>{title_svg}</title>\n{vu.ARROW_DEFS}\n{header}\n{body}\n</svg>\n'
    )


def build_ocmdp_detail() -> list[str]:
    W, H = 900, 300
    ocmdp = vu.COMPONENT_COLORS["ocmdp"]
    header = vu.svg_header(40, 30, badge_data_uri("ocmdp"), ocmdp["fill"], ocmdp["stroke"],
                            "Block 1 -- OCMDP", "the metadata Crossy")

    y, h = 160, 90
    b1w = vu.box_width("Application metadata", "schema element", min_width=230)
    b2w = vu.box_width("OCMDP", "core term", min_width=170)
    b3w = vu.box_width("NCMDP", "NFDI Core Metadata Profile", min_width=250)
    x1 = 40
    x2 = x1 + b1w + 60
    x3 = x2 + b2w + 60

    body = "\n".join([
        vu.svg_box(x1, y, b1w, h, "Application metadata", "schema element",
                   fill="#dde9fb", stroke="#2a5ab5", text_color="#042c53"),
        vu.svg_arrow(x1 + b1w, y + h / 2, x2, y + h / 2),
        vu.svg_box(x2, y, b2w, h, "OCMDP", "core term",
                   fill=ocmdp["fill"], stroke=ocmdp["stroke"], text_color="#04342c"),
        vu.svg_arrow(x2 + b2w, y + h / 2, x3, y + h / 2),
        vu.svg_box(x3, y, b3w, h, "NCMDP", "NFDI Core Metadata Profile",
                   fill="#f5f0d8", stroke="#8a7420", text_color="#412402"),
    ])
    svg = _detail_shell("Application metadata schemata reach the NCMDP through OCMDP",
                         header, body, W, H)
    svg_path, png_path = OUT / "ocmdp-detail.svg", OUT / "ocmdp-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_macheco_detail() -> list[str]:
    W, H = 1080, 300
    macheco = vu.COMPONENT_COLORS["macheco"]
    header = vu.svg_header(40, 30, badge_data_uri("macheco"), macheco["fill"], macheco["stroke"],
                            "Block 1 -- MaCHeCO", "the ontology Crossy")

    y, h = 160, 90
    b1w = vu.box_width("Application ontology", "class", min_width=230)
    b2w = vu.box_width("MaCHeCO", "class / node", min_width=180)
    b3w = vu.box_width("CIDOC CRM", "+ extensions", min_width=190)
    b4w = vu.box_width("BFO / NFDIcore", "reference alignment", min_width=220)
    x1 = 40
    x2 = x1 + b1w + 50
    x3 = x2 + b2w + 50
    x4 = x3 + b3w + 50

    body = "\n".join([
        vu.svg_box(x1, y, b1w, h, "Application ontology", "class",
                   fill="#fde8dd", stroke="#b5512a", text_color="#4a1b0c"),
        vu.svg_arrow(x1 + b1w, y + h / 2, x2, y + h / 2),
        vu.svg_box(x2, y, b2w, h, "MaCHeCO", "class / node",
                   fill=macheco["fill"], stroke=macheco["stroke"], text_color="#04342c"),
        vu.svg_arrow(x2 + b2w, y + h / 2, x3, y + h / 2),
        vu.svg_box(x3, y, b3w, h, "CIDOC CRM", "+ extensions",
                   fill="#fde8dd", stroke="#b5512a", text_color="#4a1b0c"),
        vu.svg_arrow(x3 + b3w, y + h / 2, x4, y + h / 2),
        vu.svg_box(x4, y, b4w, h, "BFO / NFDIcore", "reference alignment",
                   fill="#f5f0d8", stroke="#8a7420", text_color="#412402"),
    ])
    svg = _detail_shell("Application ontologies reach BFO and NFDIcore through MaCHeCO and CIDOC CRM",
                         header, body, W, H)
    svg_path, png_path = OUT / "macheco-detail.svg", OUT / "macheco-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_jnl_detail() -> list[str]:
    W, H = 900, 500
    jnl = vu.COMPONENT_COLORS["jnl"]
    ocmdp = vu.COMPONENT_COLORS["ocmdp"]
    macheco = vu.COMPONENT_COLORS["macheco"]
    header = vu.svg_header(40, 30, badge_data_uri("jnl"), jnl["fill"], jnl["stroke"],
                            "Block 1 -- JNL", "the junction Crossy")

    hub_cx, hub_cy, hub_r = W / 2, 260, 80
    spoke_w, spoke_h = 200, 80
    ocmdp_x, ocmdp_y = hub_cx - 320, hub_cy - spoke_h / 2
    macheco_x, macheco_y = hub_cx + 120, hub_cy - spoke_h / 2
    voc_x, voc_y = hub_cx - 100, hub_cy + hub_r + 60

    # medallion first (bottom layer) so the arrowheads that end at its edge
    # draw on top of it rather than being covered by it; boxes last so a
    # rounded corner never clips an arrow stub
    body = "\n".join([
        vu.svg_badge_medallion(hub_cx, hub_cy, hub_r, badge_data_uri("jnl"),
                                fill=jnl["fill"], stroke=jnl["stroke"], stroke_width=6),
        vu.svg_arrow(ocmdp_x + spoke_w, ocmdp_y + spoke_h / 2, hub_cx - hub_r, hub_cy),
        vu.svg_arrow(macheco_x, macheco_y + spoke_h / 2, hub_cx + hub_r, hub_cy),
        vu.svg_arrow(hub_cx, hub_cy + hub_r, voc_x + 100, voc_y),
        vu.svg_box(ocmdp_x, ocmdp_y, spoke_w, spoke_h, "OCMDP", "properties",
                   fill=ocmdp["fill"], stroke=ocmdp["stroke"], text_color="#042c53"),
        vu.svg_box(macheco_x, macheco_y, spoke_w, spoke_h, "MaCHeCO", "classes",
                   fill=macheco["fill"], stroke=macheco["stroke"], text_color="#04342c"),
        vu.svg_box(voc_x, voc_y, 200, 60, "Vocabularies", "terminologies, authority files",
                   fill="#e2f0dd", stroke="#3d7a2a", text_color="#173404"),
    ])
    svg = _detail_shell("The JNL couples OCMDP, MaCHeCO and controlled vocabularies",
                         header, body, W, H)
    svg_path, png_path = OUT / "jnl-detail.svg", OUT / "jnl-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def main() -> list[str]:
    vu.ensure_dirs()
    written: list[str] = []
    written += build_badges()
    written += build_banner()
    written += build_ocmdp_detail()
    written += build_macheco_detail()
    written += build_jnl_detail()
    return written


if __name__ == "__main__":
    written = main()
    print(f"block1: {len(written)} file(s) written" if written else "block1: nothing to do")
