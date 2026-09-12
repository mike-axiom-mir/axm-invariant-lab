#!/usr/bin/env python3
"""Compare INV-01 bounded exploration with an independent pinned Z3 encoding."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from formal.z3_inv01 import solve_case
from models import no_silent_authority
from src.bounded_explorer import explore


EVIDENCE_PATH = ROOT / "evidence" / "z3_inv01_comparison.json"
PACKAGE_PIN = "z3-solver==5.1.0.0"


def _primary_case(transitions):
    result = explore(
        no_silent_authority.initial_state(),
        transitions,
        no_silent_authority.INVARIANTS,
        max_depth=no_silent_authority.MAX_DEPTH,
    )
    if result.counterexamples:
        first = result.counterexamples[0]
        trace = [step.transition for step in first.trace]
        depth = len(trace)
    else:
        trace = []
        depth = None
    return {"status": result.status, "witnessDepth": depth, "trace": trace}


def build_receipt() -> dict:
    primary_safe = _primary_case(no_silent_authority.SAFE_TRANSITIONS)
    primary_fault = _primary_case(no_silent_authority.FAULT_TRANSITIONS)
    solver_safe = solve_case(include_fault=False, max_depth=no_silent_authority.MAX_DEPTH)
    solver_fault = solve_case(include_fault=True, max_depth=no_silent_authority.MAX_DEPTH)

    cases = [
        {
            "case": "safe",
            "primary": primary_safe,
            "solver": {
                "status": solver_safe.status,
                "witnessDepth": solver_safe.witness_depth,
                "trace": list(solver_safe.trace),
            },
        },
        {
            "case": "fault",
            "primary": primary_fault,
            "solver": {
                "status": solver_fault.status,
                "witnessDepth": solver_fault.witness_depth,
                "trace": list(solver_fault.trace),
            },
        },
    ]

    issues = []
    for case in cases:
        if case["primary"] != case["solver"]:
            issues.append(f"{case['case']}: primary/solver result mismatch")

    if primary_safe["status"] != "PASS":
        issues.append("safe case did not PASS in the primary explorer")
    if primary_fault["status"] != "FAIL":
        issues.append("fault case did not FAIL in the primary explorer")
    if primary_fault["witnessDepth"] != 2:
        issues.append("fault case did not retain the expected two-step minimal witness")

    return {
        "authority": {
            "canon": False,
            "execution": False,
            "merge": False,
            "promotion": False,
        },
        "cases": cases,
        "invariant": "INV-01-no-silent-authority-escalation",
        "issues": issues,
        "maxDepth": no_silent_authority.MAX_DEPTH,
        "model": "models/no_silent_authority.py",
        "schema": "axm.invariant-lab.z3-comparison/v0.1",
        "solver": {
            "engine": "Z3 SMT",
            "packagePin": PACKAGE_PIN,
            "relation": "independently authored three-boolean symbolic transition relation",
        },
        "status": "PASS" if not issues else "FAIL",
        "truthBoundary": (
            "This compares the primary breadth-first explorer with an independently authored "
            "Z3 encoding of only the tiny INV-01 authority model through depth 3. Agreement "
            "strengthens the modeled search claim but does not prove donor fidelity, unmodeled "
            "software, arbitrary AXM authority semantics, or real-world behavior."
        ),
    }


def _render(receipt: dict) -> str:
    return json.dumps(receipt, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    receipt = build_receipt()
    rendered = _render(receipt)

    if args.check:
        if not EVIDENCE_PATH.exists():
            print(f"HOLD: missing retained evidence {EVIDENCE_PATH}")
            return 1
        if EVIDENCE_PATH.read_text(encoding="utf-8") != rendered:
            print("FAIL: retained Z3 comparison evidence drifted")
            return 1
        if receipt["status"] != "PASS":
            print(json.dumps(receipt, indent=2, sort_keys=True))
            return 1
        print("PASS: retained Z3 INV-01 comparison matches current bounded semantics")
        return 0

    EVIDENCE_PATH.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
