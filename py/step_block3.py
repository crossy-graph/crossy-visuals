#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block3.py -- Block 3: JNL junctions (the four-chain block)
==================================================================

Planned content (not yet implemented -- see PRIMER.md Teil C, step S4):

    banner  jnl-junctions-overview         schema-level junction constrains
                                            three instance-level junctions
    badge   schema-junction-badge / graph-junction-badge /
            terminology-concept-badge / terminology-individual-badge
    detail  schema-junction-detail          OCMDP term declares admissible
                                             MaCHeCO class
    detail  graph-junction-detail           metadata resource <-> domain entity
    detail  terminology-concept-detail      node object <-> terminology concept
                                             (skos:exactMatch)
    detail  terminology-individual-detail   individual <-> authority item
                                             (owl:sameAs)
    optional  modelling-error-callout       the classic confusion (sameAs<->
                                             concept, exactMatch<->individual)

Source: primer chapter 4.4; structural reference
``data/raw/crossybase-figures/fig03_jnl_subtypes.mmd``.

Run standalone: ``python py/step_block3.py``
"""

from __future__ import annotations

import visuals_utils as vu


def main() -> list[str]:
    vu.ensure_dirs()
    return []


if __name__ == "__main__":
    written = main()
    print(f"block3: {len(written)} file(s) written" if written else "block3: nothing to do")
