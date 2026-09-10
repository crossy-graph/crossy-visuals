#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block4.py -- Block 4: CrossyBase curation and publication pipeline
==========================================================================

Source: primer chapter 7; structural reference
``data/raw/crossybase-figures/fig06_crossybase_entity_types.mmd`` and
``fig07_export_pipeline.mmd``. No mascot (CrossyBase is the curation
environment, not one of the three Crossys), so this block reuses the
six-way CATEGORY_COLORS -- and reuses them exactly as fig07's own classDef
already assigned them (wb=component/purple, proc=metadata/blue,
val=validation/red, out=publication/gold), rather than picking afresh.

Writes:

    banner  crossybase-pipeline.svg/.png
    badge   curate-badge / export-badge / validate-badge / publish-badge
            .svg/.png
    detail  curate-detail / export-detail / validate-detail / publish-detail
            .svg/.png

Run standalone: ``python py/step_block4.py``
"""

from __future__ import annotations

import visuals_utils as vu

OUT = vu.BLOCK_DIRS["block4"]

CURATE = vu.CATEGORY_COLORS["component"]     # purple -- matches fig07 wb
EXPORT = vu.CATEGORY_COLORS["metadata"]      # blue -- matches fig07 proc
VALIDATE = vu.CATEGORY_COLORS["validation"]  # red -- matches fig07 val
PUBLISH = vu.CATEGORY_COLORS["publication"]  # gold -- matches fig07 out
DOMAIN = vu.CATEGORY_COLORS["domain"]        # coral -- entities (fig06)
TERMINOLOGY = vu.CATEGORY_COLORS["terminology"]  # green -- lists (fig06)

CURATE_TEXT = "#26215c"
EXPORT_TEXT = "#042c53"
VALIDATE_TEXT = "#501313"
PUBLISH_TEXT = "#412402"
DOMAIN_TEXT = "#4a1b0c"
TERMINOLOGY_TEXT = "#173404"
NEUTRAL_FILL, NEUTRAL_STROKE, NEUTRAL_TEXT = "#f1efe8", "#888780", "#2c2c2a"

STAGES = {
    "curate": ("Curate", "CrossyBase Wikibase", CURATE, CURATE_TEXT),
    "export": ("Export", "SPARQL + Python", EXPORT, EXPORT_TEXT),
    "validate": ("Validate", "SHACL gate", VALIDATE, VALIDATE_TEXT),
    "publish": ("Publish", "reuse", PUBLISH, PUBLISH_TEXT),
}


# --------------------------------------------------------------------------- #
# Badges
# --------------------------------------------------------------------------- #
def build_badges() -> list[str]:
    written = []
    for name, (title, subtitle, colors, text_color) in STAGES.items():
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


def _header(x: float, y: float, stage: str) -> str:
    title, _, colors, text_color = STAGES[stage]
    return vu.svg_header_seal(x, y, title, colors["fill"], colors["stroke"], text_color,
                               f"Block 4 -- {title.lower()}", STAGES[stage][1])


def _caption(x: float, y: float, lines: list[str]) -> str:
    return "\n".join(
        f'<text x="{x:.1f}" y="{y + i * 20:.1f}" font-family="Fira Sans" font-size="13" '
        f'fill="#5f5e5a">{line}</text>' for i, line in enumerate(lines)
    )


# --------------------------------------------------------------------------- #
# Banner -- Curate -> Export -> Validate -> Publish, with the migration
# input and the invalid feedback loop
# --------------------------------------------------------------------------- #
def build_banner() -> list[str]:
    W, H = 1500, 520
    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>From community curation to published crosswalks</title>",
        vu.ARROW_DEFS,
    ]

    # migration input, above and left of Curate
    xls_w, xls_h = 200, 60
    xls_x, xls_y = 60, 60

    y, h = 220, 100
    names = ["curate", "export", "validate", "publish"]
    widths = [vu.box_width(STAGES[n][0], STAGES[n][1], min_width=220) for n in names]
    gap = 70
    xs = [60]
    for w in widths[:-1]:
        xs.append(xs[-1] + w + gap)

    parts.append(vu.svg_box(xls_x, xls_y, xls_w, xls_h, "Internal spreadsheet", "",
                             fill=NEUTRAL_FILL, stroke=NEUTRAL_STROKE, text_color=NEUTRAL_TEXT))
    parts.append(vu.svg_arrow_labeled(xls_x + xls_w / 2, xls_y + xls_h, xs[0] + widths[0] / 2, y,
                                       "one-off migration"))

    for i, n in enumerate(names):
        title, subtitle, colors, text_color = STAGES[n]
        parts.append(vu.svg_box(xs[i], y, widths[i], h, title, subtitle,
                                 fill=colors["fill"], stroke=colors["stroke"], text_color=text_color))
        if i < len(names) - 1:
            label = "valid" if n == "validate" else ""
            parts.append(vu.svg_arrow_labeled(xs[i] + widths[i], y + h / 2, xs[i + 1], y + h / 2, label))

    # invalid feedback loop: validate -> back to curate, arced above the row
    vx = xs[2] + widths[2] / 2
    cx = xs[0] + widths[0] / 2
    arc_y = y - 70
    parts.append(
        f'<path d="M {vx:.1f} {y:.1f} C {vx:.1f} {arc_y:.1f}, {cx:.1f} {arc_y:.1f}, {cx:.1f} {y:.1f}" '
        f'fill="none" stroke="{VALIDATE["stroke"]}" stroke-width="1.5" stroke-dasharray="5 4" '
        f'marker-end="url(#arrow)"/>'
    )
    parts.append(f'<text x="{(vx + cx) / 2:.1f}" y="{arc_y - 8:.1f}" text-anchor="middle" '
                 f'font-family="Fira Sans" font-weight="500" font-size="13" '
                 f'fill="{VALIDATE["stroke"]}">invalid \u2014 returned to curation</text>')

    # reuse fan-out below Publish
    reuse = ["TS4NFDI / DANTE", "NFDI4Objects KG", "Application projects"]
    ry = y + h + 90
    rw, rgap = 220, 40
    rtotal = len(reuse) * rw + (len(reuse) - 1) * rgap
    px = xs[3] + widths[3] / 2
    rx0 = px - rtotal / 2
    parts.append(vu.svg_arrow(px, y + h, px, ry - 20, stroke=PUBLISH["stroke"]))
    for i, label in enumerate(reuse):
        rx = rx0 + i * (rw + rgap)
        parts.append(vu.svg_arrow(px, ry - 20, rx + rw / 2, ry, stroke=PUBLISH["stroke"]))
        parts.append(vu.svg_box(rx, ry, rw, 60, label, "", fill=NEUTRAL_FILL,
                                 stroke=NEUTRAL_STROKE, text_color=NEUTRAL_TEXT))

    parts.append("</svg>\n")
    svg = "\n".join(parts)
    svg_path, png_path = OUT / "crossybase-pipeline.svg", OUT / "crossybase-pipeline.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


# --------------------------------------------------------------------------- #
# Details
# --------------------------------------------------------------------------- #
def build_curate_detail() -> list[str]:
    W, H = 1050, 460
    header = _header(40, 30, "curate")

    dict_w = vu.box_width("Dictionary", "profile attributes", min_width=180)
    terms_w = vu.box_width("Terms", "properties (edges)", min_width=170)
    ent_w = vu.box_width("Entities", "classes (nodes)", min_width=180)
    prof_w = vu.box_width("Profile", "sub-set of OCMDP", min_width=180)
    lists_w = vu.box_width("Lists", "controlled values", min_width=170)

    y1, h1 = 140, 80
    x_dict = 40
    x_terms = x_dict + dict_w + 90
    x_ent = x_terms + terms_w + 150

    y2, h2 = 320, 80
    x_prof = x_terms - 40
    x_lists = x_prof + prof_w + 90

    body = [
        vu.svg_box(x_dict, y1, dict_w, h1, "Dictionary", "profile attributes",
                   fill=CURATE["fill"], stroke=CURATE["stroke"], text_color=CURATE_TEXT),
        vu.svg_arrow_labeled(x_dict + dict_w, y1 + h1 / 2, x_terms, y1 + h1 / 2, "qualifies"),
        vu.svg_box(x_terms, y1, terms_w, h1, "Terms", "properties (edges)",
                   fill=EXPORT["fill"], stroke=EXPORT["stroke"], text_color=EXPORT_TEXT),
        vu.svg_arrow_labeled(x_terms + terms_w, y1 + h1 / 2, x_ent, y1 + h1 / 2, "schema junction"),
        vu.svg_box(x_ent, y1, ent_w, h1, "Entities", "classes (nodes)",
                   fill=DOMAIN["fill"], stroke=DOMAIN["stroke"], text_color=DOMAIN_TEXT),

        vu.svg_arrow_labeled(x_terms + terms_w / 2 - 10, y1 + h1, x_prof + prof_w / 2 - 10, y2, "grouped by"),
        vu.svg_box(x_prof, y2, prof_w, h2, "Profile", "sub-set of OCMDP",
                   fill=CURATE["fill"], stroke=CURATE["stroke"], text_color=CURATE_TEXT),
        vu.svg_arrow_labeled(x_prof + prof_w, y2 + h2 / 2, x_lists, y2 + h2 / 2, "owns 1:n"),
        vu.svg_box(x_lists, y2, lists_w, h2, "Lists", "controlled values",
                   fill=TERMINOLOGY["fill"], stroke=TERMINOLOGY["stroke"], text_color=TERMINOLOGY_TEXT),

        _caption(40, 440, [
            "Lists also provide the values Terms draw on; every list belongs to exactly one profile "
            "(redundancy across profiles is deliberate, primer 7.2).",
        ]),
    ]
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>The five entity types of the CrossyBase</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / "curate-detail.svg", OUT / "curate-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_export_detail() -> list[str]:
    W, H = 1080, 320
    header = _header(40, 30, "export")

    y, h = 140, 90
    b1w = vu.box_width("CrossyBase", "Wikibase instance", min_width=200)
    b2w = vu.box_width("SPARQL CONSTRUCT", "extracts statements", min_width=230)
    b3w = vu.box_width("Python", "post-processing", min_width=170)
    x1 = 40
    x2 = x1 + b1w + 90
    x3 = x2 + b2w + 90

    out_x = x3 + b3w + 90
    skos_w = vu.box_width("SKOS", "OCMDP", min_width=140)
    owl_w = vu.box_width("OWL", "MaCHeCO", min_width=140)

    body = [
        vu.svg_box(x1, y, b1w, h, "CrossyBase", "Wikibase instance",
                   fill=CURATE["fill"], stroke=CURATE["stroke"], text_color=CURATE_TEXT),
        vu.svg_arrow(x1 + b1w, y + h / 2, x2, y + h / 2),
        vu.svg_box(x2, y, b2w, h, "SPARQL CONSTRUCT", "extracts statements",
                   fill=EXPORT["fill"], stroke=EXPORT["stroke"], text_color=EXPORT_TEXT),
        vu.svg_arrow(x2 + b2w, y + h / 2, x3, y + h / 2),
        vu.svg_box(x3, y, b3w, h, "Python", "post-processing",
                   fill=EXPORT["fill"], stroke=EXPORT["stroke"], text_color=EXPORT_TEXT),
        vu.svg_arrow(x3 + b3w, y + h / 2 - 20, out_x, y + 22),
        vu.svg_arrow(x3 + b3w, y + h / 2 + 20, out_x, y + h - 22),
        vu.svg_box(out_x, y, skos_w, 40, "SKOS", "OCMDP",
                   fill=PUBLISH["fill"], stroke=PUBLISH["stroke"], text_color=PUBLISH_TEXT, rx=8),
        vu.svg_box(out_x, y + h - 40, owl_w, 40, "OWL", "MaCHeCO",
                   fill=PUBLISH["fill"], stroke=PUBLISH["stroke"], text_color=PUBLISH_TEXT, rx=8),
        _caption(40, 270, [
            "SPARQL CONSTRUCT transforms Wikibase statements into the target vocabularies; Python "
            "post-processing handles what SPARQL cannot express conveniently.",
        ]),
    ]
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>From community curation to serialised crosswalks</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / "export-detail.svg", OUT / "export-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_validate_detail() -> list[str]:
    W, H = 1050, 460
    header = _header(40, 30, "validate")

    y, h = 140, 90
    in_w = vu.box_width("SKOS / OWL", "serialised crosswalks", min_width=220)
    shacl_w = vu.box_width("SHACL validation", "R1\u2013R5 as shapes", min_width=230)
    valid_w = vu.box_width("Publish", "", min_width=170)
    invalid_w = vu.box_width("Back to curation", "", min_width=190)

    x1 = 40
    x2 = x1 + in_w + 90
    x3valid = x2 + shacl_w + 90
    invalid_y = y + h + 90
    invalid_box_x = x2 + shacl_w / 2 - invalid_w - 40
    body = [
        vu.svg_box(x1, y, in_w, h, "SKOS / OWL", "serialised crosswalks",
                   fill=EXPORT["fill"], stroke=EXPORT["stroke"], text_color=EXPORT_TEXT),
        vu.svg_arrow(x1 + in_w, y + h / 2, x2, y + h / 2),
        vu.svg_box(x2, y, shacl_w, h, "SHACL validation", "R1\u2013R5 as shapes",
                   fill=VALIDATE["fill"], stroke=VALIDATE["stroke"], text_color=VALIDATE_TEXT),
        vu.svg_arrow_labeled(x2 + shacl_w, y + h / 2 - 15, x3valid, y + 20, "valid"),
        vu.svg_box(x3valid, y - 10, valid_w, 50, "Publish", "",
                   fill=PUBLISH["fill"], stroke=PUBLISH["stroke"], text_color=PUBLISH_TEXT),
        vu.svg_arrow_labeled(x2 + shacl_w / 2, y + h, invalid_box_x + invalid_w / 2, invalid_y, "invalid"),
        vu.svg_box(invalid_box_x, invalid_y, invalid_w, 50, "Back to curation", "",
                   fill=CURATE["fill"], stroke=CURATE["stroke"], text_color=CURATE_TEXT),
        _caption(40, invalid_y + 100, [
            "The direction of the failure path matters: invalid output returns to curation, not to a",
            "downstream fix -- a fix applied in the pipeline would be lost on the next export.",
        ]),
    ]
    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>SHACL validation gates publication</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / "validate-detail.svg", OUT / "validate-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def build_publish_detail() -> list[str]:
    W, H = 900, 340
    header = _header(40, 30, "publish")

    y, h = 140, 90
    src_w = vu.box_width("Validated crosswalks", "", min_width=230)
    x1 = 60
    x2 = x1 + src_w + 90

    reuse = [
        ("TS4NFDI / DANTE", "discoverable, resolvable vocabulary"),
        ("NFDI4Objects KG", "validates and ingests community data"),
        ("Application projects", "check before publishing"),
    ]
    tag_w, tag_gap = 230, 30
    tags_total = len(reuse) * tag_w + (len(reuse) - 1) * tag_gap
    tag_y = 260
    tag_x0 = x2 + tags_total / 2 - tags_total  # placeholder, recomputed below

    body = [
        vu.svg_box(x1, y, src_w, h, "Validated crosswalks", "",
                   fill=VALIDATE["fill"], stroke=VALIDATE["stroke"], text_color=VALIDATE_TEXT),
    ]
    fan_x = x1 + src_w + 40
    body.append(vu.svg_box(fan_x, y, 160, h, "Publish", "",
                            fill=PUBLISH["fill"], stroke=PUBLISH["stroke"], text_color=PUBLISH_TEXT))
    body.append(vu.svg_arrow(x1 + src_w, y + h / 2, fan_x, y + h / 2))

    origin_x = fan_x + 80
    tag_x0 = origin_x - tags_total / 2
    for i, (title, sub) in enumerate(reuse):
        tx = tag_x0 + i * (tag_w + tag_gap)
        body.append(vu.svg_arrow(origin_x, y + h, tx + tag_w / 2, tag_y, stroke=PUBLISH["stroke"]))
        body.append(vu.svg_box(tx, tag_y, tag_w, 70, title, sub, fill=NEUTRAL_FILL,
                                stroke=NEUTRAL_STROKE, text_color=NEUTRAL_TEXT))

    svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
           f'<title>Three consumers of the published crosswalks</title>\n{vu.ARROW_DEFS}\n{header}\n'
           + "\n".join(body) + "\n</svg>\n")
    svg_path, png_path = OUT / "publish-detail.svg", OUT / "publish-detail.png"
    vu.write_svg(svg_path, svg)
    vu.write_png_from_svg(svg_path, png_path, zoom=1.5)
    return [str(svg_path), str(png_path)]


def main() -> list[str]:
    vu.ensure_dirs()
    written: list[str] = []
    written += build_badges()
    written += build_banner()
    written += build_curate_detail()
    written += build_export_detail()
    written += build_validate_detail()
    written += build_publish_detail()
    return written


if __name__ == "__main__":
    written = main()
    print(f"block4: {len(written)} file(s) written" if written else "block4: nothing to do")
