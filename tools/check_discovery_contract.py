#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.discovery_contract import inspect


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "AXM_MODULE.json").read_text(encoding="utf-8"))
    result = inspect(ROOT, manifest)
    if result["status"] != "PASS":
        raise SystemExit(f"discovery integrity: {result['status']}")

    target = ROOT / "evidence" / "discovery-integrity-latest.json"
    expected = stable_json(result)
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            raise SystemExit("stale discovery integrity evidence")
        print("discovery integrity evidence check: PASS")
        return

    target.write_text(expected, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
