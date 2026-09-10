#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py -- crossy-visuals orchestrator
========================================

The single entry point of this repository. Every step draws one block's
banner + badges + details as SVG (versioned, in ``img/<block>/``) and
rasterises them to PNG via resvg-py, in-process, with the vendored Fira Sans
-- no Mermaid CLI, no Node, no system fonts required.

Usage (from the repository root)::

    python main.py                     all steps, in order
    python main.py --list              print steps and exit
    python main.py --only block3       one step
    python main.py --from block2       this step and everything after
    python main.py --skip block4       everything but this
    python main.py --dry-run           print the plan, run nothing
    python main.py --strict            warnings become errors (what CI runs)

As of S1 (repo skeleton), every step is a stub that reports "nothing to do":
content lands step by step in S2-S6 (see PRIMER.md Teil B/C).

Authors: Anja Gerber and Florian Thiery
Licence: MIT (this script) / CC BY 4.0 (the figures it produces)
"""

from __future__ import annotations

import argparse
import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "py"))

# Ordered steps: (id, module name, one-line description)
STEPS: list[tuple[str, str, str]] = [
    ("block1", "step_block1", "Crossy architecture (OCMDP / MaCHeCO / JNL)"),
    ("block2", "step_block2", "Crosswalk rules R1-R5 and correspondence types"),
    ("block3", "step_block3", "JNL junctions (schema- and instance-level)"),
    ("block4", "step_block4", "CrossyBase curation and publication pipeline"),
    ("system", "step_system", "Consolidated system architecture diagram"),
]
STEP_IDS = [s[0] for s in STEPS]


def resolve_selection(only: str | None, frm: str | None, skip: str | None) -> list[str]:
    ids = list(STEP_IDS)
    if only:
        if only not in ids:
            raise SystemExit(f"unknown step '{only}'; choices: {', '.join(ids)}")
        return [only]
    if frm:
        if frm not in ids:
            raise SystemExit(f"unknown step '{frm}'; choices: {', '.join(ids)}")
        return ids[ids.index(frm):]
    if skip:
        if skip not in ids:
            raise SystemExit(f"unknown step '{skip}'; choices: {', '.join(ids)}")
        return [s for s in ids if s != skip]
    return ids


def run_step(step_id: str, module_name: str, *, strict: bool) -> tuple[int, float]:
    module = importlib.import_module(module_name)  # lazy: only on actual run
    start = time.perf_counter()
    try:
        written = module.main()
    except Exception as exc:  # noqa: BLE001 -- surfaced to the caller below
        if strict:
            raise
        print(f"  ! {step_id} failed: {exc}", file=sys.stderr)
        written = []
    elapsed = time.perf_counter() - start
    count = len(written) if written else 0
    label = f"{count} file(s) written" if count else "nothing to do"
    print(f"  - {step_id}: {label} ({elapsed:.2f}s)")
    return count, elapsed


def main() -> None:
    parser = argparse.ArgumentParser(description="crossy-visuals build orchestrator")
    parser.add_argument("--list", action="store_true", help="print steps and exit")
    parser.add_argument("--only", metavar="STEP", help="run exactly one step")
    parser.add_argument("--from", dest="frm", metavar="STEP", help="run this step and everything after")
    parser.add_argument("--skip", metavar="STEP", help="run everything but this step")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    parser.add_argument("--strict", action="store_true", help="warnings become errors (CI mode)")
    args = parser.parse_args()

    if args.list:
        for step_id, module_name, desc in STEPS:
            print(f"{step_id:8s} {module_name:16s} {desc}")
        return

    selected = resolve_selection(args.only, args.frm, args.skip)

    if args.dry_run:
        print("plan:")
        for step_id, module_name, desc in STEPS:
            marker = "->" if step_id in selected else "  "
            print(f" {marker} {step_id:8s} {desc}")
        return

    print(f"crossy-visuals: running {len(selected)} step(s)")
    totals: list[tuple[str, int, float]] = []
    for step_id, module_name, _desc in STEPS:
        if step_id not in selected:
            continue
        count, elapsed = run_step(step_id, module_name, strict=args.strict)
        totals.append((step_id, count, elapsed))

    total_time = sum(t for _, _, t in totals) or 1e-9
    print("\ntiming:")
    for step_id, count, elapsed in totals:
        share = 100 * elapsed / total_time
        print(f"  {step_id:8s} {elapsed:6.2f}s  {share:5.1f}%  ({count} file(s))")


if __name__ == "__main__":
    main()
