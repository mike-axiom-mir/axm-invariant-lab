#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.public_discovery import inspect, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check or regenerate bounded public discovery surfaces.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    manifest = json.loads((ROOT / "AXM_MODULE.json").read_text(encoding="utf-8"))
    result = inspect(ROOT, manifest) if args.check else write_outputs(ROOT, manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result.get("status") == "PASS":
        return 0
    if result.get("status") == "HOLD":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
