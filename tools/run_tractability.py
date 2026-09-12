#!/usr/bin/env python3
"""Generate/verify deterministic tractability evidence for Invariant Lab explorers."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tractability_probe import build_tractability_receipt

OUT = ROOT / "evidence" / "tractability-latest.json"


def encoded(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = build_tractability_receipt()
    text = encoded(payload)

    if args.check:
        if not OUT.exists():
            print(f"missing retained evidence: {OUT}", file=sys.stderr)
            return 2
        if OUT.read_text(encoding="utf-8") != text:
            print("tractability evidence drifted; regenerate and inspect", file=sys.stderr)
            return 1
        if payload["largestCompleteReferenceDepth"] != 15 or payload["firstIncompleteReferenceDepth"] != 16:
            print("tractability boundary changed; inspect before accepting", file=sys.stderr)
            return 1
        if any(case["primaryStatus"] != "PASS" for case in payload["cases"]):
            print("primary explorer unexpectedly failed probe", file=sys.stderr)
            return 1
        print("tractability evidence matches: reference complete through depth 15 and HOLD at depth 16")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
