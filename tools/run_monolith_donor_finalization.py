#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.monolith_donor_finalization import (  # noqa: E402
    DONOR_COMMIT,
    EXECUTED_ADDRESS,
    OBSERVATION_SCHEMA,
    PINNED_BLOBS,
    UNREQUESTED_ADDRESS,
    build_receipt,
)


def _git(root: Path, *args: str) -> str:
    run = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if run.returncode != 0:
        raise RuntimeError(run.stderr.strip() or "git command failed")
    return run.stdout.strip()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _probe_snapshot(root: Path) -> Path:
    snapshot = root / "snapshot"
    module = snapshot / "modules" / "demo-module"
    module.mkdir(parents=True)
    _write(
        module / "run.py",
        "def double(value):\n"
        "    return {'doubled': value * 2}\n\n"
        "def triple(value):\n"
        "    return {'tripled': value * 3}\n",
    )
    _write(
        module / "AXM_MONOLITH_SOURCE.json",
        json.dumps(
            {
                "repository": "mike-axiom-mir/invariant-probe-module",
                "commit": "a" * 40,
                "visibility": "public",
            }
        ),
    )
    callable_base = {
        "schema": "axm.callable-capability/v0.1",
        "kind": "module-export",
        "runtime": "python",
        "path": "run.py",
        "authority": "none",
        "network": "none",
    }
    _write(
        module / "AXM_MODULE.json",
        json.dumps(
            {
                "capabilities": [
                    {
                        "id": "demo.double",
                        "provides": ["number.doubled"],
                        "accepts": ["number"],
                        "callable": {**callable_base, "export": "double"},
                    },
                    {
                        "id": "demo.triple",
                        "provides": ["number.tripled"],
                        "accepts": ["number"],
                        "callable": {**callable_base, "export": "triple"},
                    },
                ]
            }
        ),
    )
    return snapshot


def _load_finalizer(donor_root: Path):
    tools = donor_root / "tools"
    sys.path.insert(0, str(tools))
    spec = importlib.util.spec_from_file_location(
        "axm_inv20_pinned_finalizer",
        tools / "finalize_connected_snapshot.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load pinned donor finalizer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_donor_tests(donor_root: Path) -> dict[str, Any]:
    run = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_connected_finalization.py",
            "-v",
        ],
        cwd=donor_root,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (run.stdout or "") + "\n" + (run.stderr or "")
    match = re.search(r"Ran\s+(\d+)\s+tests?\s+in", output)
    failures = len(re.findall(r"^FAIL:", output, flags=re.MULTILINE))
    errors = len(re.findall(r"^ERROR:", output, flags=re.MULTILINE))
    return {
        "testsRun": int(match.group(1)) if match else None,
        "failures": failures,
        "errors": errors,
        "ok": run.returncode == 0 and match is not None and failures == 0 and errors == 0,
    }


def _run_probe(donor_root: Path) -> dict[str, Any]:
    finalizer = _load_finalizer(donor_root)
    with tempfile.TemporaryDirectory(prefix="axm-inv20-donor-") as tmp:
        root = Path(tmp)
        snapshot = _probe_snapshot(root)
        plumbing = finalizer.monolith_plumbing.plumb_snapshot(snapshot)

        blocked = False
        try:
            finalizer.package_snapshot(
                snapshot,
                root / "must-not-exist.zip",
                folder_name="AXM-INV20-Probe",
                required_workflow=None,
                required_addresses=[EXECUTED_ADDRESS],
            )
        except finalizer.FinalizationError:
            blocked = True

        plan = root / "plan.json"
        _write(
            plan,
            json.dumps(
                {
                    "schema": "axm.monolith.invocation-plan/v0.1",
                    "invocations": [
                        {
                            "address": EXECUTED_ADDRESS,
                            "request": {
                                "schema": "axm.callable-invocation-request/v0.1",
                                "args": [21],
                            },
                            "allow_execution": True,
                            "required": True,
                        }
                    ],
                }
            ),
        )
        archive = root / "connected.zip"
        result = finalizer.finalize(
            snapshot,
            archive,
            folder_name="AXM-INV20-Probe",
            invocation_plan=plan,
            required_addresses=[EXECUTED_ADDRESS],
        )
        ledger = json.loads((snapshot / "CALLABLE_EXECUTION_LEDGER.json").read_text(encoding="utf-8"))
        package_receipt = json.loads((snapshot / "SNAPSHOT_FILE_RECEIPT.json").read_text(encoding="utf-8"))
        return {
            "preExecution": {
                "declaredCallableCount": plumbing["native_callable_registry"]["declarations"],
                "sourceCallableExecuted": plumbing["native_callable_registry"]["source_callable_executed"],
                "plumbingStatus": plumbing["status"],
            },
            "unprovenRequiredAddress": {
                "address": EXECUTED_ADDRESS,
                "blocked": blocked,
            },
            "explicitExecution": {
                "requestedAddresses": [EXECUTED_ADDRESS],
                "executedAddresses": ledger["executed_addresses"],
                "acceptedExercisedReceipts": ledger["summary"]["accepted_exercised_receipts"],
                "registryDeclaredCallableCount": ledger["summary"]["registry_declared_callable_count"],
                "packageStatus": result["status"],
                "unrequestedAddress": UNREQUESTED_ADDRESS,
            },
            "package": {
                "requiredCallableAddresses": package_receipt["required_callable_addresses"],
                "truthBoundary": package_receipt["truth_boundary"],
            },
        }


def render(donor_root: Path) -> dict[str, Any]:
    provenance_checks: list[dict[str, Any]] = []
    provenance_failures: list[str] = []
    try:
        observed_commit = _git(donor_root, "rev-parse", "HEAD")
        commit_ok = observed_commit == DONOR_COMMIT
        provenance_checks.append({"check": "pinned-donor-commit", "ok": commit_ok})
        if not commit_ok:
            provenance_failures.append(
                f"donor checkout drifted: expected {DONOR_COMMIT}, observed {observed_commit}"
            )
        for path, expected_blob in sorted(PINNED_BLOBS.items()):
            observed_blob = _git(donor_root, "rev-parse", f"HEAD:{path}")
            ok = observed_blob == expected_blob
            provenance_checks.append({"check": f"pinned-donor-blob:{path}", "ok": ok})
            if not ok:
                provenance_failures.append(
                    f"donor blob drifted for {path}: expected {expected_blob}, observed {observed_blob}"
                )
    except (OSError, RuntimeError) as exc:
        return build_receipt(
            {},
            provenance_checks=provenance_checks,
            provenance_failures=provenance_failures + [f"could not verify donor git provenance: {exc}"],
        )

    observation: dict[str, Any] = {
        "schema": OBSERVATION_SCHEMA,
        "authority": {"execution": False, "merge": False, "promotion": False, "canon": False},
    }
    try:
        observation["donorTests"] = _run_donor_tests(donor_root)
        observation.update(_run_probe(donor_root))
    except Exception as exc:
        provenance_failures.append(f"pinned donor execution probe failed: {type(exc).__name__}: {exc}")

    return build_receipt(
        observation,
        provenance_checks=provenance_checks,
        provenance_failures=provenance_failures,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = render(args.donor_root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] == "PASS":
        if args.check:
            print("PASS: pinned Monolith donor finalizer preserves INV-20 execution scope")
        return 0
    if args.check:
        print(f"{result['status']}: pinned Monolith donor finalizer did not satisfy INV-20")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
