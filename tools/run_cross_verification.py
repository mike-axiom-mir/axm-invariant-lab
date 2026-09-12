#!/usr/bin/env python3
"""Generate/verify retained cross-implementation evidence for tiny AXM models."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models import no_auto_canon, no_silent_authority, rollback_continuity, selective_inheritance
from src.cross_verifier import cross_verify

MODELS = (no_silent_authority, no_auto_canon, rollback_continuity, selective_inheritance)
OUT = ROOT / "evidence" / "cross-verification-latest.json"


def build_receipt() -> dict:
    cases = []
    for model in MODELS:
        for variant, transitions in (("safe", model.SAFE_TRANSITIONS), ("fault", model.FAULT_TRANSITIONS)):
            result = cross_verify(
                model.initial_state(),
                transitions,
                model.INVARIANTS,
                max_depth=model.MAX_DEPTH,
            )
            reference = result.reference
            cases.append({
                "model": model.__name__.removeprefix("models."),
                "variant": variant,
                "agreement": result.status,
                "primaryStatus": result.primary["status"],
                "referenceStatus": reference.status,
                "primaryUniqueStates": result.primary["exploredStates"],
                "referenceUniqueStates": reference.unique_states,
                "failingInvariants": list(reference.failing_invariants),
                "unknownInvariants": list(reference.unknown_invariants),
                "referenceComplete": reference.complete,
                "referencePathNodes": reference.path_nodes,
                "referenceStateDigest": reference.reachable_state_digest,
            })

    return {
        "schemaVersion": "0.1",
        "evidenceRung": 5,
        "evidenceClass": "CROSS-IMPLEMENTATION",
        "claim": "A second dependency-free path enumerator agrees with the primary visited-state explorer on bounded status, reachable unique-state count, failing invariant names, and unknown invariant names for all retained safe/fault tiny-model cases.",
        "pathNodeBudgetPerCase": 100_000,
        "caseCount": len(cases),
        "allAgree": all(case["agreement"] == "AGREE" for case in cases),
        "allReferenceRunsComplete": all(case["referenceComplete"] for case in cases),
        "cases": cases,
        "truthBoundary": "Both implementations consume the same authored model transition and invariant functions. Agreement cross-checks exploration semantics only; it does not independently prove model fidelity, donor implementation behavior, cross-repo adoption, or real-world safety.",
    }


def encoded(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_receipt()
    text = encoded(payload)

    if args.check:
        if not OUT.exists():
            print(f"missing retained evidence: {OUT}", file=sys.stderr)
            return 2
        if OUT.read_text(encoding="utf-8") != text:
            print("cross-verification evidence drifted; regenerate and inspect", file=sys.stderr)
            return 1
        if not payload["allAgree"] or not payload["allReferenceRunsComplete"]:
            print("cross-verification is not fully complete/agreed", file=sys.stderr)
            return 1
        print(f"cross-verification evidence matches: {payload['caseCount']} cases")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
