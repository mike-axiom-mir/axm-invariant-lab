#!/usr/bin/env python3
"""Retain/check the bounded archive-backed INV-20 projection evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.monolith_connected_archive import inspect_projection, project_archive

FIXTURE = ROOT / "fixtures" / "monolith-connected-archive-v0.3.2.projection.json"
EVIDENCE = ROOT / "evidence" / "monolith-connected-archive-refinement-v0.3.2.json"


def _canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _fixture_sha256(projection: dict) -> str:
    return "sha256:" + hashlib.sha256(_canonical_bytes(projection)).hexdigest()


def build_evidence(projection: dict) -> dict:
    result = inspect_projection(projection)
    return {
        "schema": "axm.invariant-lab.monolith-connected-archive-refinement-evidence/v0.1",
        "invariant": "INV-20",
        "status": result.status,
        "source_archive": projection.get("source_archive"),
        "projection_schema": projection.get("schema"),
        "projection_sha256": _fixture_sha256(projection),
        "snapshot_integrity": projection.get("snapshot_integrity"),
        "result": result.to_dict(),
        "claims": {
            "package_bytes_verified_against_internal_snapshot_receipt": True,
            "addressable_implies_callable": False,
            "wired_implies_executable": False,
            "declared_leaf_implies_callable": False,
            "named_workflow_scope_transfers_to_candidate_compositions": False,
            "test_adapter_ready_implies_tests_passed": False,
            "package_integrity_implies_semantic_correctness": False,
            "constitutional_authority_granted": False,
        },
        "limitations": [
            "The full 194 MB archive is not committed to Invariant Lab or available in ordinary CI.",
            "CI rechecks the retained deterministic projection and evidence, not the original ZIP bytes.",
            "Archive hashing proves byte identity/integrity only; it does not prove authorship or arbitrary semantic/runtime correctness.",
            "The archive reader does not execute packaged source code, launch surfaces, or rerun the named workflow.",
            "The composition check is a bounded cross-artifact scope check over the frozen v0.3.2 package, not a proof for future Monolith schemas.",
            "No merge, CANON, device, network, installation, or constitutional authority is created by this evidence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if retained evidence drifts")
    parser.add_argument("--archive", type=Path, help="optionally reproduce the projection from an actual ZIP before checking")
    args = parser.parse_args()

    retained_projection = json.loads(FIXTURE.read_text(encoding="utf-8"))
    projection = retained_projection
    if args.archive is not None:
        live_projection = project_archive(args.archive)
        if live_projection != retained_projection:
            print("FAIL: live archive projection differs from retained fixture")
            return 1
        projection = live_projection

    evidence = build_evidence(projection)
    rendered = _canonical_bytes(evidence)

    if args.check:
        if evidence["status"] != "PASS":
            print(json.dumps(evidence, indent=2, sort_keys=True))
            return 1
        if not EVIDENCE.exists() or EVIDENCE.read_bytes() != rendered:
            print("FAIL: retained archive-backed INV-20 evidence drifted")
            return 1
        print(
            "PASS: archive-backed INV-20 projection remains byte-integrity checked, "
            "scope-bounded, and non-promoting"
        )
        return 0

    EVIDENCE.write_bytes(rendered)
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if evidence["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
