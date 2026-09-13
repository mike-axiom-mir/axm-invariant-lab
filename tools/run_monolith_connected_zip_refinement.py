#!/usr/bin/env python3
"""Generate/verify retained evidence for Connected Monolith callability INV-20."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.monolith_connected_zip import inspect

FIXTURE = ROOT / "fixtures" / "monolith-connected-zip-v0.3.2.receipt.json"
OUT = ROOT / "evidence" / "monolith-connected-zip-refinement-latest.json"
EXPECTED_FIXTURE_SHA256 = "06588a18e592a5b553562ad9a4c5b6f911c943fc4bbcee6ebf86ee56afddcc93"


def fixture_sha256() -> str:
    return hashlib.sha256(FIXTURE.read_bytes()).hexdigest()


def build_receipt() -> dict:
    source = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = inspect(source)
    return {
        "schemaVersion": "0.1",
        "evidenceClass": "USER-SUPPLIED-MONOLITH-RESULT-REFINEMENT",
        "claim": (
            "For the exact supplied Connected Monolith v0.3.2 result receipt, endpoint "
            "classification is internally coherent and explicit callable coverage remains "
            "3 endpoints; addressability, wiring, blocked states, and candidate composition "
            "are not promoted into broader callability or verification."
        ),
        "source": {
            "file": FIXTURE.name,
            "sha256": fixture_sha256(),
            "zipSha256Claim": source.get("zip_sha256"),
            "schema": source.get("schema"),
        },
        "result": result.to_dict(),
        "truthBoundary": (
            "The retained source is a user-supplied local-build result receipt, not the "
            "194 MB archive or its snapshot receipt. This check proves only properties "
            "explicitly present in that receipt and the consumer non-promotion rules tested "
            "here. It does not independently verify archive contents, every endpoint, the "
            "Blackline Relay implementation, deployment, execution, merge, or CANON authority."
        ),
    }


def encoded(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    observed_sha = fixture_sha256()
    if observed_sha != EXPECTED_FIXTURE_SHA256:
        print(
            f"Connected Monolith source receipt drifted: {observed_sha} != {EXPECTED_FIXTURE_SHA256}",
            file=sys.stderr,
        )
        return 1

    payload = build_receipt()
    text = encoded(payload)

    if args.check:
        if not OUT.exists():
            print(f"missing retained evidence: {OUT}", file=sys.stderr)
            return 2
        if OUT.read_text(encoding="utf-8") != text:
            print("Connected Monolith refinement evidence drifted; regenerate and inspect", file=sys.stderr)
            return 1
        if payload["result"]["status"] != "PASS":
            print("Connected Monolith result receipt does not PASS", file=sys.stderr)
            return 1
        print("Connected Monolith callability refinement evidence matches pinned source receipt")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
