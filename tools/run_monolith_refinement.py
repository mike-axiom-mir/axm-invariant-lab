#!/usr/bin/env python3
"""Generate/verify retained refinement evidence for Monolith Pipeline Fabric v0.1."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.monolith_pipeline_fabric import inspect

FIXTURE = ROOT / "fixtures" / "monolith-pipeline-fabric-v0.1.json"
OUT = ROOT / "evidence" / "monolith-pipeline-refinement-latest.json"


def build_receipt() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = inspect(fixture["descriptor"], fixture["candidates"])
    donor = fixture["donor"]

    return {
        "schemaVersion": "0.1",
        "evidenceClass": "CROSS-REPO-REFINEMENT-FIXTURE",
        "claim": (
            "The invariant-lab read-only adapter preserves AXM Monolith Pipeline Fabric "
            "v0.1 candidate-only status and explicit no-automatic-authority fields for "
            "the pinned donor contract fixture."
        ),
        "donor": donor,
        "result": result.to_dict(),
        "truthBoundary": (
            "This is a separately authored refinement check against an exact pinned "
            "Monolith v0.1 source/schema contract, not evidence that two external AXM "
            "repositories consume invariant-lab output. It does not earn seed rung 6 "
            "CROSS-REPO adoption and is not a full-stack Monolith runtime snapshot."
        ),
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
            print("Monolith refinement evidence drifted; regenerate and inspect", file=sys.stderr)
            return 1
        if payload["result"]["status"] != "PASS":
            print("Monolith refinement fixture does not PASS", file=sys.stderr)
            return 1
        print("Monolith pipeline refinement evidence matches pinned fixture")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
