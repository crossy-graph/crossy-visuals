#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_system.py -- consolidated system architecture
=====================================================

Planned content (not yet implemented -- see PRIMER.md Teil C, step S6):

    crossy-system-architecture   one bird's-eye diagram consolidating Block 1
                                  (the three Crossys), Block 3 (JNL as the
                                  coupling) and Block 4 (the CrossyBase
                                  pipeline) -- analogous to
                                  chublets-software-architecture. Should read
                                  its structure from step_block1/3/4 rather
                                  than duplicating layout numbers, once those
                                  exist.

Run standalone: ``python py/step_system.py``
"""

from __future__ import annotations

import visuals_utils as vu


def main() -> list[str]:
    vu.ensure_dirs()
    return []


if __name__ == "__main__":
    written = main()
    print(f"system: {len(written)} file(s) written" if written else "system: nothing to do")
