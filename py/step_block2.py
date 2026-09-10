#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block2.py -- Block 2: crosswalk rules and correspondence types
=====================================================================

Planned content (not yet implemented -- see PRIMER.md Teil C, step S3):

    banner  crossy-rule-cascade            metadata track (R3->R4) + ontology
                                            track (R1->R2) + R5 + SHACL gate
                                            -> knowledge graph
    badge   ontology-track-badge (R1+R2) / metadata-track-badge (R3+R4) /
            terminology-binding-badge (R5)
    detail  ontology-track-detail      R1 (rdfs:subClassOf / owl:equivalentClass),
                                        R2 (BFO/NFDIcore alignment)
    detail  metadata-track-detail      R3 (schema -> OCMDP), R4 (OCMDP -> NCMDP,
                                        SKOS)
    detail  terminology-binding-detail R5, admissible terminologies
    detail  correspondence-types-detail  the match-type vocabulary itself
                                          (subClassOf/equivalentClass, skos
                                          exactMatch..relatedMatch, exactMatch
                                          vs. sameAs)

Source: primer chapter 3.6 + 6; structural reference
``data/raw/crossybase-figures/fig01_relation_inventory.mmd`` and
``fig04_rule_cascade.mmd``.

Run standalone: ``python py/step_block2.py``
"""

from __future__ import annotations

import visuals_utils as vu


def main() -> list[str]:
    vu.ensure_dirs()
    return []


if __name__ == "__main__":
    written = main()
    print(f"block2: {len(written)} file(s) written" if written else "block2: nothing to do")
