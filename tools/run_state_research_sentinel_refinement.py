#!/usr/bin/env python3
"""Generate/check deterministic evidence for the State Research Sentinel refinement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.state_research_workfloor_sentinel import inspect  # noqa: E402

FIXTURE = ROOT / "fixtures" / "state-research-workfloor-sentinel-v1.projection.json"
EVIDENCE = ROOT / "evidence" / "STATE_RESEARCH_SENTINEL_REFINEMENT.json"


def render(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def build_evidence() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = inspect(fixture)
    return {
        "schema": "axm.invariant-lab.state-research-sentinel-refinement/v0.1",
        "source": fixture["source"],
        "projection": fixture["projection"],
        "invariant": {
            "id": "INV-13",
            "statement": "Every oracle-required check for a sparse transition must be awakened; a missed required check forbids an oracle-equivalence claim for that step.",
        },
        "result": result.to_dict(),
        "observed_boundary": {
            "bug_run": result.derived.get("dependency_bug_run.invariant_status"),
            "repaired_run": result.derived.get("repaired_run.invariant_status"),
            "claim": "one pinned Workfloor Sentinel execution artifact only",
        },
        "truth_boundary": "PASS means the mechanically selected explicit donor fields are internally consistent with INV-13 and distinguish the known dependency bug from its repaired run. It does not execute State Research, prove unseen dependency completeness, or promote general model fidelity beyond the existing rung-5 boundary.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = render(build_evidence())
    if args.check:
        if not EVIDENCE.exists():
            print(f"missing retained evidence: {EVIDENCE}", file=sys.stderr)
            return 2
        if EVIDENCE.read_text(encoding="utf-8") != text:
            print("retained State Research Sentinel refinement evidence drifted", file=sys.stderr)
            return 1
        print("State Research Sentinel refinement evidence: PASS")
        return 0
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
