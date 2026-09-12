from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from src.discovery_contract import inspect as inspect_local_discovery

OUTPUT_SCHEMA = "axm.invariant-lab.public-discovery/v0.1"
PUBLIC_MARKER_SCHEMA = "axm.discovery-public/v1"
CAPABILITY_SCHEMA = "axm.public-capability/v1"
REPO_ID = "mike-axiom-mir/axm-invariant-lab"
PROVIDER_ID = "axm-invariant-lab"
DISPLAY_NAME = "AXM Invariant Lab"
PUBLIC_MARKER_PATH = Path(".axm/discovery-public.json")
CAPABILITY_REGISTRY_PATH = Path("registry/capabilities.jsonl")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_public_marker() -> dict[str, Any]:
    return {
        "schema": PUBLIC_MARKER_SCHEMA,
        "repo": REPO_ID,
        "display_name": DISPLAY_NAME,
        "public": True,
    }


def build_capability_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list):
        raise ValueError("manifest capabilities must be a list")

    rows: list[dict[str, Any]] = []
    for capability in capabilities:
        if not isinstance(capability, dict):
            raise ValueError("capability declaration must be an object")
        capability_id = capability.get("id")
        evidence = capability.get("evidence")
        if not isinstance(capability_id, str) or not capability_id:
            raise ValueError("capability id must be a non-empty string")
        if not isinstance(evidence, dict) or not isinstance(evidence.get("status"), str):
            raise ValueError(f"capability {capability_id!r} needs evidence.status")
        status = evidence["status"]
        rows.append(
            {
                "schema": CAPABILITY_SCHEMA,
                "id": capability_id,
                "providers": [PROVIDER_ID],
                "consumers": [],
                "status": status,
                "provider_statuses": [{"id": PROVIDER_ID, "status": status}],
                "source_evidence": ["AXM_MODULE.json"],
                "truth": {
                    "declaration_is_runtime_proof": False,
                    "generated_from_module_manifest": True,
                    "grants_authority": False,
                },
            }
        )
    rows.sort(key=lambda row: row["id"])
    return rows


def build_outputs(manifest: dict[str, Any]) -> dict[Path, str]:
    marker_text = json.dumps(build_public_marker(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    records = build_capability_records(manifest)
    registry_text = "".join(_canonical_json(row) + "\n" for row in records)
    return {
        PUBLIC_MARKER_PATH: marker_text,
        CAPABILITY_REGISTRY_PATH: registry_text,
    }


def write_outputs(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    local = inspect_local_discovery(root, manifest)
    if local["status"] != "PASS":
        return {
            "schema": OUTPUT_SCHEMA,
            "status": local["status"],
            "reason": "local machine-discovery integrity must PASS before public projection",
            "localDiscovery": local,
        }
    outputs = build_outputs(manifest)
    for relative, text in outputs.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return inspect(root, manifest)


def inspect(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    local = inspect_local_discovery(root, manifest)
    failures: list[dict[str, str]] = []
    holds: list[dict[str, str]] = []

    if local["status"] == "FAIL":
        failures.append({
            "code": "local-discovery-failed",
            "message": "AXM_MODULE local structural discovery integrity failed; public export is not trustworthy.",
        })
    elif local["status"] == "HOLD":
        holds.append({
            "code": "local-discovery-held",
            "message": "AXM_MODULE uses discovery semantics this projector does not fully understand.",
        })

    try:
        outputs = build_outputs(manifest)
    except ValueError as exc:
        failures.append({"code": "projection-invalid", "message": str(exc)})
        outputs = {}

    output_digests: dict[str, str] = {}
    for relative, expected in outputs.items():
        key = relative.as_posix()
        output_digests[key] = _sha256_text(expected)
        target = root / relative
        if not target.is_file():
            failures.append({"code": "output-missing", "message": f"missing generated discovery surface: {key}"})
            continue
        try:
            actual = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            failures.append({"code": "output-unreadable", "message": f"cannot read {key}: {exc}"})
            continue
        if actual != expected:
            failures.append({"code": "output-stale", "message": f"generated discovery surface drifted from AXM_MODULE.json: {key}"})

    status = "FAIL" if failures else ("HOLD" if holds else "PASS")
    capability_count = len(manifest.get("capabilities", [])) if isinstance(manifest.get("capabilities"), list) else 0
    return {
        "schema": OUTPUT_SCHEMA,
        "status": status,
        "capabilityCount": capability_count,
        "outputDigests": output_digests,
        "failures": failures,
        "holds": holds,
        "authority": {
            "execution": False,
            "installation": False,
            "merge": False,
            "promotion": False,
            "canon": False,
        },
        "truthBoundary": (
            "Projects only the already-declared AXM_MODULE capability identities and evidence-status strings into "
            "the bounded public marker/capability-registry surfaces understood by AXM Discovery Buddy. It does not "
            "execute capabilities, validate their semantics, publish private files, or grant authority."
        ),
    }
