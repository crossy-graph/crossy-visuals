#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visuals_utils.py -- shared constants, palette, paths and writers
==================================================================

Every step module imports from here rather than repeating a hex code or a
path computation. This is the single place that knows:

* where things live (``ROOT``, ``IMG``, ``DATA_RAW``, ``FONTS``, ``SOURCE``),
* the Crossy colour palette (``CROSSY_PURPLE``, ``CROSSY_GOLD``,
  ``CATEGORY_COLORS``), taken verbatim from the ``classDef`` blocks already
  used across the seven CrossyBase primer figures (``data/raw/
  crossybase-figures/*.mmd``) rather than invented fresh,
* the symbol vocabulary (``SYMBOLS``) that step modules draw with,
* deterministic writers for SVG source and PNG output.

Authors: Anja Gerber and Florian Thiery
Licence: MIT (this script) / CC BY 4.0 (the figures it produces)
"""

from __future__ import annotations

import hashlib
from pathlib import Path

# --------------------------------------------------------------------------- #
# Release marker -- NOT datetime.now(). Bump by hand when the content set
# changes; this is what appears in generated file headers, if any ever do.
# --------------------------------------------------------------------------- #
RELEASE = "2026-09-10"

# --------------------------------------------------------------------------- #
# Paths, resolved relative to the repository root
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
DATA_RAW = ROOT / "data" / "raw"
CROSSYBASE_FIGURES = DATA_RAW / "crossybase-figures"  # the 7 .mmd, read-only
SOURCE = IMG / "source"  # Florian's raw reference graphics, not a render input
FONTS = ROOT / "fonts"

FONT_REGULAR = FONTS / "FiraSans-Regular.ttf"
FONT_MEDIUM = FONTS / "FiraSans-Medium.ttf"

BLOCK_DIRS = {
    "block1": IMG / "block-1-crossy-architecture",
    "block2": IMG / "block-2-crosswalk-rules",
    "block3": IMG / "block-3-jnl-junctions",
    "block4": IMG / "block-4-crossybase-pipeline",
    "system": IMG / "system-architecture",
}


def ensure_dirs() -> None:
    """Create every output directory this repo writes into. Idempotent."""
    for path in BLOCK_DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# Palette -- taken from the classDef blocks already shared by all seven
# crossybase-figures .mmd sources (comp / md / dom / term / val / out).
# Decided 2026-09-10: formalise rather than reinvent (see PRIMER.md A4).
# --------------------------------------------------------------------------- #

# House colour pair (the two poles of the story: the components themselves,
# and what they ultimately feed) -- mirrors CHUBLETS_PURPLE / CHUBLETS_GOLD.
CROSSY_PURPLE = "#5b3fa0"  # components: OCMDP / MaCHeCO / JNL
CROSSY_GOLD = "#8a7420"    # publication: the federated knowledge graph

# Six-way category palette. Each entry is (fill, stroke) exactly as used in
# the .mmd classDef blocks, so a figure rebuilt here and a figure still open
# in the old Mermaid preview read as the same visual language.
CATEGORY_COLORS: dict[str, dict[str, str]] = {
    "component": {"fill": "#e8e0f5", "stroke": CROSSY_PURPLE},     # OCMDP/MaCHeCO/JNL
    "metadata": {"fill": "#dde9fb", "stroke": "#2a5ab5"},          # properties / edges
    "domain": {"fill": "#fde8dd", "stroke": "#b5512a"},            # classes / nodes
    "terminology": {"fill": "#e2f0dd", "stroke": "#3d7a2a"},       # concepts / individuals
    "validation": {"fill": "#f5dede", "stroke": "#a03030"},        # SHACL / rules
    "publication": {"fill": "#f5f0d8", "stroke": CROSSY_GOLD},     # KG / reuse
}

# --------------------------------------------------------------------------- #
# Symbol vocabulary -- drawn from the primer's own terminology (chapter 7.2:
# Terms are "the edges", Entities are "the classes ... the nodes"), not
# invented icons. A proposal (A4, 2026-09-10) -- expect to adjust once the
# first details are drawn against real content.
# --------------------------------------------------------------------------- #
SYMBOLS: dict[str, str] = {
    "component": "node-edge cluster (a small node and edge sharing a joint)",
    "metadata": "edge -- short line, open arrowhead",
    "domain": "node -- filled circle",
    "junction": "diamond where two connectors meet",
    "terminology_concept": "single ring (skos:exactMatch)",
    "terminology_individual": "double ring (owl:sameAs) -- deliberately distinct "
    "from the single ring; primer 4.4.2 warns against conflating the two",
    "validation": "diamond outline with a check mark (a SHACL shape, literally)",
    "publication": "three dots joined by two short edges (a small graph)",
}

FONT_SANS = "Fira Sans"

# --------------------------------------------------------------------------- #
# Crossy mascot -- Florian's own artwork, img/source/Crossy*.png (+ .svg).
# Four skins confirmed 2026-09-10 (A4): grey/silver = neutral house colour,
# green = MaCHeCO, teal = OCMDP, purple = JNL ("OMJO" = the Junction skin).
# These colours are now authoritative for the three components -- they
# replace the single shared "component" purple the palette started with.
# --------------------------------------------------------------------------- #
SOURCE_MASCOTS: dict[str, Path] = {
    "system": SOURCE / "Crossy.png",
    "macheco": SOURCE / "Crossy_MaCHeCO.png",
    "ocmdp": SOURCE / "Crossy_OCMDP.png",
    "jnl": SOURCE / "Crossy_OMJO.png",
}

COMPONENT_COLORS: dict[str, dict[str, str]] = {
    "system": {"fill": "#e8e8e8", "stroke": "#909090"},
    "macheco": {"fill": "#dcece3", "stroke": "#206048"},
    "ocmdp": {"fill": "#dce8ea", "stroke": "#386870"},
    "jnl": {"fill": "#e6dcee", "stroke": "#482870"},
}

# Head framing for badge medallions. Defined as a vertical span (fractions
# of image height, constant 2000px across all four source PNGs) plus a
# horizontal centre point -- the crop is built as an exact square from
# these two numbers, so no padding is ever added. Three revisions
# 2026-09-10 (see PRIMER.md A4):
#   v1 (0.44, 0.0, 0.90, 0.44) rect crop -- star/triangle fragment visible.
#   v2 (0.46, 0.0, 0.84, 0.40) rect crop -- fragment gone, but the bottom
#      edge landed on the still-wide neck, reading as a flat cut.
#   v3 (0.47, 0.0, 0.83, 0.45) rect crop -- taper fixed, but the crop
#      itself wasn't square: padding it out to a square canvas (pad_frac)
#      added transparent bands top/bottom that show as a flat colour
#      "shelf" inside the circle once clipped -- exactly the cut Florian
#      was still seeing, just one layer further down in the pipeline.
#   v4 -- square by construction, no padding at all: fixed vertical span,
#      horizontal centre point, side length = vertical span in pixels.
#      First pass at 0.45 fixed the flat-band problem but read as too
#      tightly zoomed in ("das ist zu nah rangezoomt") -- widened the span
#      to 0.52 for more headroom; still clear of the graph-decoration
#      fragment (checked against all three coloured variants).
BADGE_HEAD_TOP_FRAC = 0.0
BADGE_HEAD_BOTTOM_FRAC = 0.52
BADGE_HEAD_CENTER_X_FRAC = 0.635


def crop_badge_image(component: str, size: int = 480):
    """
    Crop the given component's mascot to a head badge: an exact square, no
    padding. Vertical span and horizontal centre are fixed fractions
    (``BADGE_HEAD_*``, tuned against all three coloured variants); the
    square's side is simply the vertical span in source pixels, so the
    result is square by construction and needs no transparent fill to
    square it up afterwards -- that fill was the source of the flat band
    Florian kept seeing at the bottom of earlier revisions. Returns a PIL
    Image (RGBA); caller embeds it as a base64 PNG via
    :func:`image_data_uri`. Requires Pillow, imported lazily.
    """
    from PIL import Image

    path = SOURCE_MASCOTS[component]
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    top = int(h * BADGE_HEAD_TOP_FRAC)
    bottom = int(h * BADGE_HEAD_BOTTOM_FRAC)
    side = bottom - top
    cx = int(w * BADGE_HEAD_CENTER_X_FRAC)
    left = cx - side // 2
    right = left + side
    crop = im.crop((left, top, right, bottom))
    return crop.resize((size, size), Image.LANCZOS)


def image_data_uri(image) -> str:
    """PNG-encode a PIL Image to a base64 data: URI for inline SVG embedding."""
    import base64
    import io

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


# --------------------------------------------------------------------------- #
# Small SVG-building helpers shared by every step_block*.py. Deliberately
# minimal -- this is not a general diagram library, just enough to stop
# every step from repeating the same box/arrow math by hand.
# --------------------------------------------------------------------------- #
ARROW_STROKE = "#73726c"

# NOTE: the CSS `context-stroke` keyword (used for marker-inherits-line-colour
# in browser-rendered SVG) is not supported by resvg -- the marker path was
# rendering with no visible stroke at all until this was pinned to a fixed
# colour. If arrow colour ever needs to vary per line, define a second
# named marker rather than relying on context-stroke again (verified
# 2026-09-10 while building Block 1).
ARROW_DEFS = (
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
    'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    f'<path d="M2 1L8 5L2 9" fill="none" stroke="{ARROW_STROKE}" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
)


def xml_escape(s: str) -> str:
    """Escape the five XML predefined entities. Every helper that places
    caller-supplied text into an SVG text node must run it through this --
    an unescaped ``&`` is a malformed-XML parse failure at render time, not
    a warning, as ``step_system.py``'s first draft found out."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def text_width(s: str, size: int = 14) -> float:
    """Rough width estimate (Fira Sans is close to 0.56*size per character)."""
    return len(s) * size * 0.56


def box_width(title: str, subtitle: str = "", *, min_width: float = 140, pad: float = 28) -> float:
    t = text_width(title, 14)
    s = text_width(subtitle, 12) if subtitle else 0
    return max(min_width, t + pad, s + pad)


def svg_box(x: float, y: float, w: float, h: float, title: str, subtitle: str = "",
            *, fill: str = "#f1efe8", stroke: str = "#5f5e5a", text_color: str = "#2c2c2a",
            rx: float = 10) -> str:
    title, subtitle = xml_escape(title), xml_escape(subtitle)
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>']
    cx = x + w / 2
    if subtitle:
        parts.append(f'<text x="{cx:.1f}" y="{y + h/2 - 8:.1f}" text-anchor="middle" '
                      f'font-family="Fira Sans" font-weight="500" font-size="14" '
                      f'fill="{text_color}">{title}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{y + h/2 + 12:.1f}" text-anchor="middle" '
                      f'font-family="Fira Sans" font-size="12" fill="{text_color}" '
                      f'opacity="0.75">{subtitle}</text>')
    else:
        parts.append(f'<text x="{cx:.1f}" y="{y + h/2:.1f}" text-anchor="middle" '
                      f'dominant-baseline="central" font-family="Fira Sans" '
                      f'font-weight="500" font-size="14" fill="{text_color}">{title}</text>')
    return "\n".join(parts)


def svg_arrow(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#73726c") -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="1.5" marker-end="url(#arrow)"/>')


def svg_arrow_labeled(x1: float, y1: float, x2: float, y2: float, label: str,
                       *, stroke: str = "#73726c", label_color: str = "#2c2c2a",
                       above: bool = True) -> str:
    """Straight arrow with a short label centred on it. Caller is responsible
    for leaving enough gap between boxes for the label not to collide with
    either -- there is no automatic width check here, unlike box_width()."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dy = -8 if above else 16
    return (
        svg_arrow(x1, y1, x2, y2, stroke=stroke)
        + f'\n<text x="{mx:.1f}" y="{my + dy:.1f}" text-anchor="middle" '
        f'font-family="Fira Sans" font-weight="500" font-size="12" '
        f'fill="{label_color}">{xml_escape(label)}</text>'
    )


def svg_arrow_l(points: list[tuple[float, float]], *, stroke: str = "#73726c") -> str:
    d = " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return (f'<path d="M {d}" fill="none" stroke="{stroke}" stroke-width="1.5" '
            f'marker-end="url(#arrow)"/>')


def svg_dashed_container(x: float, y: float, w: float, h: float, label: str,
                          *, stroke: str = "#888780") -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" '
            f'fill="none" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="6 5"/>\n'
            f'<text x="{x + 16:.1f}" y="{y + 26:.1f}" font-family="Fira Sans" '
            f'font-weight="500" font-size="13" fill="{stroke}">{xml_escape(label)}</text>')


def svg_badge_medallion(cx: float, cy: float, r: float, data_uri: str,
                         *, fill: str, stroke: str, stroke_width: float = 4) -> str:
    clip_id = f"clip-{int(cx)}-{int(cy)}-{int(r)}"
    d = r * 2 * 0.975
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + stroke_width/2:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
        f'<clipPath id="{clip_id}"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"/></clipPath>\n'
        f'<image href="{data_uri}" x="{cx - d/2:.1f}" y="{cy - d/2:.1f}" '
        f'width="{d:.1f}" height="{d:.1f}" clip-path="url(#{clip_id})"/>'
    )


def svg_badge_seal(cx: float, cy: float, r: float, title: str, subtitle: str,
                    *, fill: str, stroke: str, text_color: str,
                    stroke_width: float = 6) -> str:
    """Text-only badge medallion for blocks with no mascot variant: a
    coloured circle with a bold rule/id label and a short subtitle. Same
    visual family as svg_badge_medallion (image-based), used where there is
    no Crossy skin to crop from."""
    title, subtitle = xml_escape(title), xml_escape(subtitle)
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
        f'<text x="{cx:.1f}" y="{cy - 6:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" '
        f'font-size="{r * 0.34:.1f}" fill="{text_color}">{title}</text>\n'
        f'<text x="{cx:.1f}" y="{cy + r * 0.34:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="Fira Sans" font-size="{r * 0.15:.1f}" '
        f'fill="{text_color}" opacity="0.8">{subtitle}</text>'
    )


def svg_header_seal(x: float, y: float, title_badge: str, badge_fill: str, badge_stroke: str,
                     badge_text_color: str, title: str, subtitle: str, *, badge_r: float = 26) -> str:
    """Like svg_header, but for a text-seal badge instead of a mascot image."""
    parts = [svg_badge_seal(x + badge_r, y + badge_r, badge_r, title_badge, "",
                             fill=badge_fill, stroke=badge_stroke, text_color=badge_text_color,
                             stroke_width=3)]
    tx = x + badge_r * 2 + 16
    parts.append(f'<text x="{tx:.1f}" y="{y + badge_r - 8:.1f}" font-family="Fira Sans" '
                 f'font-weight="500" font-size="15" fill="#2c2c2a">{xml_escape(title)}</text>')
    parts.append(f'<text x="{tx:.1f}" y="{y + badge_r + 12:.1f}" font-family="Fira Sans" '
                 f'font-size="12" fill="#5f5e5a">{xml_escape(subtitle)}</text>')
    return "\n".join(parts)


def svg_header(x: float, y: float, badge_data_uri: str, badge_fill: str, badge_stroke: str,
               title: str, subtitle: str, *, badge_r: float = 26) -> str:
    """Small badge + 'Block N - Title' header, repeated atop every detail
    diagram so it stays visibly tied to its badge (chublets-visuals convention)."""
    parts = [svg_badge_medallion(x + badge_r, y + badge_r, badge_r, badge_data_uri,
                                  fill=badge_fill, stroke=badge_stroke, stroke_width=3)]
    tx = x + badge_r * 2 + 16
    parts.append(f'<text x="{tx:.1f}" y="{y + badge_r - 8:.1f}" font-family="Fira Sans" '
                 f'font-weight="500" font-size="15" fill="#2c2c2a">{xml_escape(title)}</text>')
    parts.append(f'<text x="{tx:.1f}" y="{y + badge_r + 12:.1f}" font-family="Fira Sans" '
                 f'font-size="12" fill="#5f5e5a">{xml_escape(subtitle)}</text>')
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Deterministic writers
# --------------------------------------------------------------------------- #
def content_fingerprint(data: bytes) -> str:
    """Short, stable fingerprint for logging / --strict checks."""
    return hashlib.sha256(data).hexdigest()[:12]


def write_svg(path: Path, svg_markup: str) -> str:
    """
    Write SVG source deterministically: UTF-8, exactly one trailing newline,
    no injected timestamps or random ids. The caller is responsible for not
    putting either into ``svg_markup`` in the first place -- unlike a
    matplotlib pipeline, we author the markup ourselves, so there is nothing
    here to patch after the fact.
    """
    text = svg_markup.strip("\n") + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return content_fingerprint(text.encode("utf-8"))


def write_png_from_svg(svg_path: Path, png_path: Path, *, zoom: float = 2.0) -> str:
    """
    Rasterise an already-written SVG file to PNG via resvg-py, using the
    vendored Fira Sans weights rather than whatever fonts happen to be on
    the build machine (see fonts/). ``resvg_py.svg_to_bytes`` returns plain
    PNG bytes with no embedded creation timestamp, so -- unlike matplotlib's
    ``savefig`` -- no post-write patching is needed for byte-identical
    rebuilds; run twice and diff to confirm before relying on that.
    """
    import resvg_py  # imported lazily so --list/--dry-run stay cheap

    png_bytes = resvg_py.svg_to_bytes(
        svg_path=str(svg_path),
        background=None,  # transparent
        skip_system_fonts=True,
        font_files=[str(FONT_REGULAR), str(FONT_MEDIUM)],
        zoom=zoom,
    )
    png_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.write_bytes(png_bytes)
    return content_fingerprint(png_bytes)
