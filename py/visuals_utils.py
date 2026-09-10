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
