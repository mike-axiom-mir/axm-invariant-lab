#!/usr/bin/env python3
"""Compare INV-03 rollback continuity with an independent pinned Z3 encoding."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from formal.z3_inv03 import solve_case
from models import rollback_continuity
from src.bounded_explorer import explore


EVIDENCE_PATH = ROOT / "evidence" / "z3_inv03_comparison.json"
PACKAGE_PIN = "z3-solver==5.1.0.0"


def _primary_case(transitions):
    result = explore(
        rollback_continuity.initial_state(),
        transitions,
        rollback_continuity.INVARIANTS,
        max_depth=rollback_continuity.FORMAL_AUDIT_DEPTH,
    )
    if result.counterexamples:
        first = result.counterexamples[0]
        trace = [step.transition for step in first.trace]
        depth = len(trace)
    else:
        trace = []
        depth = None
    return {"status": result.status, "witnessDepth": depth, "trace": trace}


def _solver_case(fault_mode: str):
    result = solve_case(
        fault_mode=fault_mode,
        max_depth=rollback_continuity.FORMAL_AUDIT_DEPTH,
    )
    return {
        "status": result.status,
        "witnessDepth": result.witness_depth,
        "trace": list(result.trace),
    }


def build_receipt() -> dict:
    cases = [
        {
            "case": "safe-post-rollback-forward-progress",
            "primary": _primary_case(rollback_continuity.SAFE_TRANSITIONS),
            "solver": _solver_case("none"),
        },
        {
            "case": "wrong-target-fault",
            "primary": _primary_case(rollback_continuity.FAULT_TRANSITIONS),
            "solver": _solver_case("wrong-target"),
        },
        {
            "case": "stale-receipt-lifecycle-fault",
            "primary": _primary_case(rollback_continuity.STALE_RECEIPT_FAULT_TRANSITIONS),
            "solver": _solver_case("stale-receipt"),
        },
    ]

    issues = []
    for case in cases:
        if case["primary"] != case["solver"]:
            issues.append(f"{case['case']}: primary/solver result mismatch")

    by_name = {case["case"]: case["primary"] for case in cases}
    if by_name["safe-post-rollback-forward-progress"]["status"] != "PASS":
        issues.append("safe relation did not remain PASS after rollback and later forward progress")
    if by_name["wrong-target-fault"] != {
        "status": "FAIL",
        "witnessDepth": 4,
        "trace": [
            "mutate-S0-to-S1",
            "checkpoint-S1",
            "mutate-S1-to-S2",
            "FAULT-rollback-reports-S1-but-restores-S9",
        ],
    }:
        issues.append("wrong-target fault did not retain the expected shortest four-step witness")
    if by_name["stale-receipt-lifecycle-fault"] != {
        "status": "FAIL",
        "witnessDepth": 5,
        "trace": [
            "mutate-S0-to-S1",
            "checkpoint-S1",
            "mutate-S1-to-S2",
            "rollback-to-S1",
            "FAULT-forward-mutation-keeps-stale-rollback-receipt",
        ],
    }:
        issues.append("stale-receipt fault did not retain the expected shortest five-step witness")

    return {
        "authority": {
            "canon": False,
            "execution": False,
            "merge": False,
            "promotion": False,
        },
        "cases": cases,
        "invariant": "INV-03-rollback-known-good-lineage",
        "issues": issues,
        "maxDepth": rollback_continuity.FORMAL_AUDIT_DEPTH,
        "model": "models/rollback_continuity.py",
        "repairBoundary": (
            "The model's rollback slot is a current rollback assertion. A later normal forward "
            "mutation clears it; a synthetic stale-receipt transition preserves the pre-repair "
            "behavior so the depth-5 boundary bug remains falsifiable."
        ),
        "schema": "axm.invariant-lab.z3-comparison/v0.2",
        "solver": {
            "engine": "Z3 SMT",
            "packagePin": PACKAGE_PIN,
            "relation": "independently authored rollback/checkpoint/receipt lifecycle transition relation",
        },
        "status": "PASS" if not issues else "FAIL",
        "truthBoundary": (
            "This compares the primary breadth-first explorer with an independently authored Z3 "
            "encoding of only the tiny INV-03 rollback model through depth 6. It specifically "
            "checks wrong-target rollback and stale current-receipt lifecycle faults. Agreement "
            "does not prove durable storage, crash safety, concurrent writers, donor fidelity, "
            "arbitrary rollback systems, or real-world behavior."
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
            print("FAIL: retained Z3 INV-03 comparison evidence drifted")
            return 1
        if receipt["status"] != "PASS":
            print(json.dumps(receipt, indent=2, sort_keys=True))
            return 1
        print("PASS: retained Z3 INV-03 comparison matches current bounded semantics")
        return 0

    EVIDENCE_PATH.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
