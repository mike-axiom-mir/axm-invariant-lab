#!/usr/bin/env python3
"""Generate deterministic v0.1 evidence. No timestamps; same code -> same receipt."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.bounded_explorer import explore
from models import no_silent_authority, no_auto_canon, rollback_continuity, selective_inheritance
from adapters.truthgrid_evidence import inspect as inspect_truthgrid


MODELS = [
    ("no_silent_authority", no_silent_authority),
    ("no_auto_canon", no_auto_canon),
    ("rollback_continuity", rollback_continuity),
    ("selective_inheritance", selective_inheritance),
]


def run():
    model_receipts = []
    first_counterexample = None

    for name, model in MODELS:
        safe = explore(
            model.initial_state(),
            model.SAFE_TRANSITIONS,
            model.INVARIANTS,
            max_depth=model.MAX_DEPTH,
        )
        fault = explore(
            model.initial_state(),
            model.FAULT_TRANSITIONS,
            model.INVARIANTS,
            max_depth=model.MAX_DEPTH,
        )

        first_fault = fault.counterexamples[0] if fault.counterexamples else None
        model_receipts.append({
            "model": name,
            "safeStatus": safe.status,
            "safeExploredStates": safe.explored_states,
            "safeExploredTransitions": safe.explored_transitions,
            "faultInjectedStatus": fault.status,
            "faultInvariant": first_fault.invariant if first_fault else None,
            "faultTraceLength": len(first_fault.trace) if first_fault else None,
            "faultTraceTransitions": [step.transition for step in first_fault.trace] if first_fault else [],
            "limitations": model.LIMITATIONS,
        })

        if first_counterexample is None and first_fault is not None:
            first_counterexample = {
                "schema": "axm.invariant-lab.counterexample/v0.1",
                "model": name,
                "claim": first_fault.description,
                "status": "FAIL",
                "bound": model.MAX_DEPTH,
                "invariant": first_fault.invariant,
                "trace": [
                    {
                        "transition": step.transition,
                        "before": step.before,
                        "after": step.after,
                    }
                    for step in first_fault.trace
                ],
                "limitations": model.LIMITATIONS + [
                    "This is a synthetic fault-injection counterexample, not a claim of a donor-repository defect."
                ],
                "authority": {
                    "merge": False,
                    "canon": False,
                    "execution": False,
                    "promotion": False,
                },
            }

    fixture_path = ROOT / "fixtures" / "truthgrid-foundation-extract.json"
    truthgrid = json.loads(fixture_path.read_text(encoding="utf-8"))
    refinement = inspect_truthgrid(truthgrid)

    mutated = deepcopy(truthgrid)
    mutated["ticks"][2]["merge"]["rollbackRef"] = "revision:999"
    mutation_refinement = inspect_truthgrid(mutated)

    evidence = {
        "schema": "axm.invariant-lab.evidence/v0.1",
        "question": "Can a tiny bounded explorer distinguish safe transition systems from transition-order authority/continuity faults without treating unknown evidence as safe?",
        "modelReceipts": model_receipts,
        "truthgridRefinement": {
            "source": truthgrid["source"],
            "baselineStatus": refinement.status,
            "baselineUnknowns": refinement.unknowns,
            "baselineFailures": refinement.failures,
            "adversarialRollbackRefMutationStatus": mutation_refinement.status,
            "adversarialRollbackRefMutationFailures": mutation_refinement.failures,
        },
        "evidenceLevel": {
            "reached": 4,
            "label": "ADVERSARIAL",
            "reason": "Authored safe/fault models are fixture-tested and the TruthGrid adapter is exercised against a contradictory rollbackRef mutation.",
            "notReached": [
                "independent second implementation",
                "live donor repo consumption",
                "real-environment verification",
            ],
        },
        "authority": {
            "merge": False,
            "canon": False,
            "execution": False,
            "promotion": False,
        },
    }
    return first_counterexample, evidence


def stable_json(value):
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    counterexample, evidence = run()
    if counterexample is None:
        raise SystemExit("expected at least one synthetic counterexample")

    targets = {
        ROOT / "evidence" / "first_counterexample_receipt.json": stable_json(counterexample),
        ROOT / "evidence" / "evidence-latest.json": stable_json(evidence),
    }

    if args.check:
        stale = []
        for path, expected in targets.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            raise SystemExit("stale evidence: " + ", ".join(stale))
        print("evidence check: PASS")
        return

    for path, content in targets.items():
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
