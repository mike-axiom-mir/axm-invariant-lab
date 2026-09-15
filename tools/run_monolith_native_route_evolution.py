#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any

from adapters.monolith_native_route_evolution import (
    DONOR_REPOSITORY,
    SCHEMA,
    inspect,
)

EVIDENCE_SCHEMA = "axm.invariant-lab.monolith-native-route-evolution-evidence/v0.1"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = ROOT / "evidence" / "monolith-native-route-evolution-v2.5.json"


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _load_donor(root: Path):
    path = root / "tools" / "totality_native_smokes.py"
    spec = importlib.util.spec_from_file_location("pinned_totality_native_smokes", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load donor totality_native_smokes.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _provenance(donor_root: Path) -> dict[str, str]:
    return {
        "repository": DONOR_REPOSITORY,
        "commit": _git(donor_root, "rev-parse", "HEAD"),
        "tool_blob": _git(donor_root, "rev-parse", "HEAD:tools/totality_native_smokes.py"),
        "test_blob": _git(donor_root, "rev-parse", "HEAD:tests/test_totality_native_smokes.py"),
    }


def _endpoint(recipe: dict[str, Any]) -> dict[str, Any]:
    return {
        "address": recipe["address"],
        "repository": recipe["repository"],
        "commit": recipe["commit"],
        "adapter": {
            "status": "callable_native_command_verified",
            "source_capability_execution": True,
        },
    }


def _normalize_plan(payload: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in payload.get("recipes", []):
        rows.append({
            "id": row.get("id"),
            "address": row.get("address"),
            "repository": row.get("repository"),
            "commit": row.get("commit"),
            "args": row.get("args"),
            "status": row.get("status"),
            "executed": row.get("executed"),
        })
    return {"status": payload.get("status"), "mode": payload.get("mode"), "recipes": rows}


def _run_plan(module: Any, endpoints: list[dict[str, Any]]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "EXECUTION_FABRIC.json").write_text(
            json.dumps({"schema": "synthetic-invariant-probe/v0.1", "endpoints": endpoints}, sort_keys=True),
            encoding="utf-8",
        )
        return module.run(root, execute=False)


def collect(donor_root: Path) -> dict[str, Any]:
    donor_root = donor_root.resolve()
    donor = _provenance(donor_root)
    module = _load_donor(donor_root)
    recipes = [dict(row) for row in module.RECIPES]
    if not recipes:
        raise RuntimeError("donor exposes no learned native-smoke recipes")

    endpoints = [_endpoint(recipe) for recipe in recipes]
    baseline = _run_plan(module, endpoints)
    first = recipes[0]

    changed_ref = [dict(row) for row in endpoints]
    changed_ref[0] = {**changed_ref[0], "commit": "0" * 40}
    changed_payload = _run_plan(module, changed_ref)

    unverified = [dict(row) for row in endpoints]
    unverified[0] = {
        **unverified[0],
        "adapter": {"status": "native_command_discovered_unprobed", "source_capability_execution": False},
    }
    unverified_payload = _run_plan(module, unverified)
    missing_payload = _run_plan(module, endpoints[1:])

    def first_status(payload: dict[str, Any]) -> tuple[str | None, bool | None]:
        for row in payload.get("recipes", []):
            if row.get("id") == first.get("id"):
                return row.get("status"), row.get("executed")
        return None, None

    changed_status, changed_executed = first_status(changed_payload)
    unverified_status, unverified_executed = first_status(unverified_payload)
    missing_status, missing_executed = first_status(missing_payload)

    observation = {
        "schema": SCHEMA,
        "donor": donor,
        "plan": _normalize_plan(baseline),
        "falsifiers": {
            "changed_ref": {
                "overall_status": changed_payload.get("status"),
                "row_status": changed_status,
                "executed": changed_executed,
            },
            "unverified_native": {
                "overall_status": unverified_payload.get("status"),
                "row_status": unverified_status,
                "executed": unverified_executed,
            },
            "missing_endpoint": {
                "overall_status": missing_payload.get("status"),
                "row_status": missing_status,
                "executed": missing_executed,
            },
        },
        "authority": {"execution": False, "merge": False, "promotion": False, "canon": False},
        "truth_boundary": baseline.get("truth_boundary"),
    }
    return {
        "schema": EVIDENCE_SCHEMA,
        "observation": observation,
        "result": inspect(observation),
        "evidence_ceiling": (
            "One exact pinned Monolith native-route planning implementation. Planning eligibility is not source execution, "
            "product acceptance, deployment, merge/promotion/CANON authority, or proof of future donor commits."
        ),
    }


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_EVIDENCE)
    args = parser.parse_args()

    payload = collect(args.donor_root)
    data = canonical_bytes(payload)
    if args.check:
        if not args.output.is_file():
            print(f"HOLD: retained evidence missing: {args.output}")
            return 2
        expected = args.output.read_bytes()
        if expected != data:
            print("FAIL: retained native-route evolution evidence drift")
            print(f"generated_sha256={hashlib.sha256(data).hexdigest()}")
            print(f"retained_sha256={hashlib.sha256(expected).hexdigest()}")
            return 1
        if payload["result"]["status"] != "PASS":
            print(json.dumps(payload["result"], indent=2, sort_keys=True))
            return 1
        print(f"PASS: INV-20 native-route evolution evidence; recipes={len(payload['observation']['plan']['recipes'])}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["result"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
