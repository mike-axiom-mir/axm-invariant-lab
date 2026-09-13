#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.truthgrid_client_intent import build_receipt  # noqa: E402

FIXTURE = ROOT / "fixtures" / "truthgrid-client-intent-v1.projection.json"
EVIDENCE = ROOT / "evidence" / "TRUTHGRID_CLIENT_INTENT_REFINEMENT.json"


def render() -> dict:
    return build_receipt(json.loads(FIXTURE.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = render()
    if args.check:
        retained = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        if current != retained:
            print("FAIL: retained TruthGrid client-intent evidence drifted")
            return 1
        print("PASS: TruthGrid client-intent evidence matches retained receipt")
        return 0
    EVIDENCE.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(current, indent=2, sort_keys=True))
    return 0 if current["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
