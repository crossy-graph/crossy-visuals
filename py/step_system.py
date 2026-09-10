#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_system.py -- consolidated system architecture
=====================================================

One bird's-eye diagram consolidating Block 1 (the three Crossys, mascot
badges reused directly), Block 3 (JNL as the coupling between OCMDP and
MaCHeCO) and Block 4 (the CrossyBase pipeline, same stage colours). Reads
its palette from the same constants those blocks use rather than picking
fresh ones -- analogous to chublets-software-architecture.

Writes:

    crossy-system-architecture.svg/.png

Run standalone: ``python py/step_system.py``
"""

from __future__ import annotations

import visuals_utils as vu

OUT = vu.BLOCK_DIRS["system"]

OCMDP = vu.COMPONENT_COLORS["ocmdp"]
MACHECO = vu.COMPONENT_COLORS["macheco"]
JNL = vu.COMPONENT_COLORS["jnl"]

CURATE = vu.CATEGORY_COLORS["component"]
EXPORT = vu.CATEGORY_COLORS["metadata"]
VALIDATE = vu.CATEGORY_COLORS["validation"]
PUBLISH = vu.CATEGORY_COLORS["publication"]

CURATE_TEXT = "#26215c"
EXPORT_TEXT = "#042c53"
VALIDATE_TEXT = "#501313"
PUBLISH_TEXT = "#412402"


def _badge(component: str, cx: float, cy: float, r: float, colors: dict) -> str:
    data_uri = vu.image_data_uri(vu.crop_badge_image(component, size=240))
    return vu.svg_badge_medallion(cx, cy, r, data_uri, fill=colors["fill"],
                                   stroke=colors["stroke"], stroke_width=5)


def build() -> list[str]:
    W, H = 1100, 840

    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>Crossy system architecture: components, junction, curation and publication</title>",
        vu.ARROW_DEFS,
    ]

    # -- The Crossys -------------------------------------------------------
    parts.append(vu.svg_dashed_container(40, 30, W - 80, 340, "The Crossys \u2014 Block 1"))
    ocmdp_cx, ocmdp_cy, r_big = 300, 150, 65
    macheco_cx, macheco_cy = 800, 150
    jnl_cx, jnl_cy, r_jnl = 550, 260, 55

    parts.append(f'<line x1="{ocmdp_cx:.1f}" y1="{ocmdp_cy + r_big:.1f}" x2="{jnl_cx - 40:.1f}" '
                 f'y2="{jnl_cy - 20:.1f}" stroke="{JNL["stroke"]}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{macheco_cx:.1f}" y1="{macheco_cy + r_big:.1f}" x2="{jnl_cx + 40:.1f}" '
                 f'y2="{jnl_cy - 20:.1f}" stroke="{JNL["stroke"]}" stroke-width="1.5"/>')

    parts.append(_badge("ocmdp", ocmdp_cx, ocmdp_cy, r_big, OCMDP))
    parts.append(f'<text x="{ocmdp_cx:.1f}" y="{ocmdp_cy + r_big + 26:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="16" '
                 f'fill="{OCMDP["stroke"]}">OCMDP</text>')

    parts.append(_badge("macheco", macheco_cx, macheco_cy, r_big, MACHECO))
    parts.append(f'<text x="{macheco_cx:.1f}" y="{macheco_cy + r_big + 26:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="16" '
                 f'fill="{MACHECO["stroke"]}">MaCHeCO</text>')

    parts.append(_badge("jnl", jnl_cx, jnl_cy, r_jnl, JNL))
    parts.append(f'<text x="{jnl_cx:.1f}" y="{jnl_cy + r_jnl + 22:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="14" '
                 f'fill="{JNL["stroke"]}">JNL \u2014 the junction (Block 3)</text>')

    # -- connector down to CrossyBase --------------------------------------
    mid_x = W / 2
    parts.append(vu.svg_arrow_labeled(mid_x, 380, mid_x, 440, "curated & validated in"))

    # -- CrossyBase pipeline -------------------------------------------------
    parts.append(vu.svg_dashed_container(40, 460, W - 80, 160, "CrossyBase pipeline \u2014 Block 4"))
    stages = [("Curate", CURATE, CURATE_TEXT), ("Export", EXPORT, EXPORT_TEXT),
              ("Validate", VALIDATE, VALIDATE_TEXT), ("Publish", PUBLISH, PUBLISH_TEXT)]
    stage_w, stage_h, stage_gap = 190, 70, 40
    total = len(stages) * stage_w + (len(stages) - 1) * stage_gap
    sx0 = (W - total) / 2
    sy = 520
    for i, (title, colors, text_color) in enumerate(stages):
        sx = sx0 + i * (stage_w + stage_gap)
        parts.append(vu.svg_box(sx, sy, stage_w, stage_h, title, "",
                                 fill=colors["fill"], stroke=colors["stroke"], text_color=text_color))
        if i < len(stages) - 1:
            parts.append(vu.svg_arrow(sx + stage_w, sy + stage_h / 2, sx + stage_w + stage_gap, sy + stage_h / 2))

    # invalid feedback, small arc above the pipeline row
    curate_cx = sx0 + stage_w / 2
    validate_cx = sx0 + 2 * (stage_w + stage_gap) + stage_w / 2
    arc_y = sy - 35
    parts.append(
        f'<path d="M {validate_cx:.1f} {sy:.1f} C {validate_cx:.1f} {arc_y:.1f}, '
        f'{curate_cx:.1f} {arc_y:.1f}, {curate_cx:.1f} {sy:.1f}" fill="none" '
        f'stroke="{VALIDATE["stroke"]}" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#arrow)"/>'
    )

    # -- Knowledge graph output ---------------------------------------------
    kg_w, kg_h = 480, 80
    kg_x, kg_y = mid_x - kg_w / 2, 700
    parts.append(vu.svg_arrow(mid_x, sy + stage_h, mid_x, kg_y))
    parts.append(vu.svg_box(kg_x, kg_y, kg_w, kg_h, "Federated knowledge graph ecosystem",
                             "NFDI4Objects + the wider NFDI", fill=PUBLISH["fill"],
                             stroke=PUBLISH["stroke"], text_color=PUBLISH_TEXT))

    parts.append("</svg>\n")
    svg = "\n".join(parts)
    svg_path = OUT / "crossy-system-architecture.svg"
    png_path = OUT / "crossy-system-architecture.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def main() -> list[str]:
    vu.ensure_dirs()
    return build()


if __name__ == "__main__":
    written = main()
    print(f"system: {len(written)} file(s) written" if written else "system: nothing to do")
