#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_block1.py -- Block 1: Crossy architecture
================================================

Planned content (not yet implemented -- this is the S1 skeleton stub; see
PRIMER.md Teil C, step S2):

    banner  crossy-architecture-overview   three worlds (metadata / research
                                            data / terminology), the three
                                            Crossys, the NFDI4Objects KG
    badge   ocmdp-badge / macheco-badge / jnl-badge
    detail  ocmdp-detail    application metadata schemata -> OCMDP -> NCMDP
    detail  macheco-detail  application ontologies -> MaCHeCO -> CIDOC CRM
                             -> BFO/NFDIcore
    detail  jnl-detail      JNL couples OCMDP, MaCHeCO and controlled
                             vocabularies

Source: primer chapter 4.1; structural reference
``data/raw/crossybase-figures/fig02_components_and_layers.mmd``.

Run standalone: ``python py/step_block1.py``
"""

from __future__ import annotations

import visuals_utils as vu


def main() -> list[str]:
    vu.ensure_dirs()
    # No figures drawn yet -- S1 only wires the skeleton. Returning an empty
    # list is what main.py reports as "nothing to do" for this step.
    return []


if __name__ == "__main__":
    written = main()
    print(f"block1: {len(written)} file(s) written" if written else "block1: nothing to do")
