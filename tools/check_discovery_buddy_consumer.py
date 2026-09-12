#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "evidence" / "discovery_buddy_compatibility.json"
CONSUMER_REPO = "mike-axiom-mir/axm-discovery-buddy"
CONSUMER_COMMIT = "a1e28aba31c453023298e01ce4e54107c3f74583"
CONSUMER_SCANNER_BLOB_SHA1 = "6d69c9eb85cc518dfcd6e43e8c9426ef168d392f"
NORMALIZED_CAPABILITY_SCHEMA = "axm.discovery-capability/v0.1"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _load_scanner(buddy_root: Path):
    scanner_path = buddy_root / "discovery_buddy" / "scanner.py"
    if not scanner_path.is_file():
        raise FileNotFoundError(scanner_path)
    data = scanner_path.read_bytes()
    blob = _git_blob_sha1(data)
    if blob != CONSUMER_SCANNER_BLOB_SHA1:
        raise ValueError(f"consumer scanner blob drift: {blob}")
    spec = importlib.util.spec_from_file_location("axm_discovery_buddy_pinned_scanner", scanner_path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load pinned Discovery Buddy scanner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_receipt(buddy_root: Path) -> dict[str, Any]:
    issues: list[str] = []
    try:
        scanner = _load_scanner(buddy_root)
    except (OSError, ValueError, ImportError) as exc:
        return {
            "schema": "axm.invariant-lab.discovery-buddy-compatibility/v0.1",
            "status": "HOLD",
            "consumerRepo": CONSUMER_REPO,
            "consumerCommit": CONSUMER_COMMIT,
            "consumerScannerBlobSha1": CONSUMER_SCANNER_BLOB_SHA1,
            "issues": [str(exc)],
            "authority": {"execution": False, "merge": False, "promotion": False, "canon": False},
            "truthBoundary": "External scanner source is unavailable or no longer matches the exact pinned consumer boundary; no compatibility claim is emitted.",
        }

    manifest = json.loads((ROOT / "AXM_MODULE.json").read_text(encoding="utf-8"))
    expected_rows = {
        item["id"]: item["evidence"]["status"]
        for item in manifest["capabilities"]
    }
    marker = scanner.read_public_marker(ROOT)
    capabilities = scanner.read_capabilities(ROOT)
    observed_rows = {item["id"]: item.get("status") for item in capabilities.get("records", [])}
    sources = capabilities.get("sources", [])

    if not marker.get("eligible"):
        issues.append(f"public marker is not eligible: {marker.get('error') or 'unknown'}")
    if marker.get("repo") != "mike-axiom-mir/axm-invariant-lab":
        issues.append("public marker repository identity changed")
    if observed_rows != expected_rows:
        issues.append("Discovery Buddy normalized capability ids/statuses do not equal AXM_MODULE declarations")
    if len(sources) != 1 or sources[0].get("path") != "registry/capabilities.jsonl":
        issues.append("Discovery Buddy did not consume exactly registry/capabilities.jsonl")
    if any(source.get("errors") for source in sources):
        issues.append("Discovery Buddy reported capability-registry parse errors")
    if any(item.get("schema") != NORMALIZED_CAPABILITY_SCHEMA for item in capabilities.get("records", [])):
        issues.append("Discovery Buddy normalized capability schema changed")

    status = "PASS" if not issues else "FAIL"
    return {
        "schema": "axm.invariant-lab.discovery-buddy-compatibility/v0.1",
        "status": status,
        "consumerRepo": CONSUMER_REPO,
        "consumerCommit": CONSUMER_COMMIT,
        "consumerScannerBlobSha1": CONSUMER_SCANNER_BLOB_SHA1,
        "consumerNormalizedCapabilitySchema": NORMALIZED_CAPABILITY_SCHEMA,
        "publicMarkerSha256": marker.get("sha256"),
        "registrySha256": sources[0].get("sha256") if len(sources) == 1 else None,
        "capabilityCount": len(observed_rows),
        "capabilitySetSha256": _sha256_json(sorted(observed_rows)),
        "capabilityStatusMapSha256": _sha256_json(observed_rows),
        "issues": issues,
        "authority": {"execution": False, "merge": False, "promotion": False, "canon": False},
        "truthBoundary": (
            "Executes the exact pinned AXM Discovery Buddy scanner against Invariant Lab's public marker and capability "
            "registry and checks one-to-one capability id/evidence-status preservation. This is cross-repository discovery "
            "compatibility evidence only; it does not execute discovered capabilities, prove semantics or deployment, "
            "or grant authority."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Invariant Lab with an exact pinned Discovery Buddy consumer.")
    parser.add_argument("--buddy-root", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    receipt = build_receipt(Path(args.buddy_root).resolve())
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    if receipt["status"] == "HOLD":
        return 2
    if receipt["status"] != "PASS":
        return 1
    if args.check:
        expected = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
        if receipt != expected:
            print("discovery-buddy-consumer: retained evidence drift", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
