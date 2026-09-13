#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.universal_creation_donor_execution import (  # noqa: E402
    DONOR_COMMIT,
    DONOR_TOOL,
    PINNED_BLOBS,
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


def render(donor_root: Path) -> dict:
    provenance_checks: list[dict] = []
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
    except (RuntimeError, OSError) as exc:
        return build_receipt(
            {},
            provenance_checks=provenance_checks,
            provenance_failures=provenance_failures + [f"could not verify donor git provenance: {exc}"],
        )

    tool = donor_root / DONOR_TOOL
    run = subprocess.run(
        [sys.executable, str(tool)],
        cwd=donor_root,
        capture_output=True,
        text=True,
        check=False,
    )
    provenance_checks.append({"check": "donor-owned-receipt-command-exited-zero", "ok": run.returncode == 0})
    if run.returncode != 0:
        provenance_failures.append(
            "donor-owned receipt command failed: " + (run.stderr.strip() or f"exit {run.returncode}")
        )
        return build_receipt(
            {},
            provenance_checks=provenance_checks,
            provenance_failures=provenance_failures,
        )

    try:
        donor_receipt = json.loads(run.stdout)
    except json.JSONDecodeError as exc:
        provenance_failures.append(f"donor-owned receipt was not valid JSON: {exc}")
        donor_receipt = {}

    return build_receipt(
        donor_receipt,
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
    if args.check:
        if result["status"] == "PASS":
            print("PASS: pinned Universal Creation donor-owned INV-10 execution matches the refinement boundary")
            return 0
        print(f"{result['status']}: donor-owned INV-10 execution did not satisfy the refinement boundary")
        return 1
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
