#!/usr/bin/env python3
"""Check that local producer bytes still match contracts pinned by external consumers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_SCHEMA = "axm.invariant-lab.external-consumers/v0.1"
OUTPUT_SCHEMA = "axm.invariant-lab.external-consumer-check/v0.1"


def git_blob_sha(raw: bytes) -> str:
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(header + raw).hexdigest()


def check_registry(root: Path, registry: dict[str, Any]) -> dict[str, Any]:
    if registry.get("schema") != REGISTRY_SCHEMA:
        raise ValueError("unsupported registry schema")
    consumers = registry.get("consumers")
    if not isinstance(consumers, list) or not consumers:
        raise ValueError("consumers must be a non-empty list")

    results = []
    for item in consumers:
        if not isinstance(item, dict):
            raise ValueError("consumer entry must be object")
        for key in (
            "consumerRepo",
            "consumerCommit",
            "capability",
            "packetPath",
            "packetBlob",
            "schemaPath",
            "schemaBlob",
            "status",
        ):
            if not isinstance(item.get(key), str) or not item[key]:
                raise ValueError(f"consumer missing {key}")
        if item["status"] != "active_pinned_consumer":
            raise ValueError("unknown consumer status")

        packet_path = root / item["packetPath"]
        schema_path = root / item["schemaPath"]
        if not packet_path.is_file() or not schema_path.is_file():
            raise ValueError("pinned producer file missing")

        packet_actual = git_blob_sha(packet_path.read_bytes())
        schema_actual = git_blob_sha(schema_path.read_bytes())
        compatible = packet_actual == item["packetBlob"] and schema_actual == item["schemaBlob"]
        results.append(
            {
                "consumerRepo": item["consumerRepo"],
                "consumerCommit": item["consumerCommit"],
                "capability": item["capability"],
                "packetBlobExpected": item["packetBlob"],
                "packetBlobActual": packet_actual,
                "schemaBlobExpected": item["schemaBlob"],
                "schemaBlobActual": schema_actual,
                "compatible": compatible,
            }
        )

    return {
        "schema": OUTPUT_SCHEMA,
        "consumerCount": len(results),
        "allPinnedProducerContractsIntact": all(result["compatible"] for result in results),
        "consumers": results,
        "authority": {
            "merge": False,
            "canon": False,
            "execution": False,
            "promotion": False,
        },
        "truthBoundary": "Checks only that local producer bytes still match contracts pinned by registered consumers. It does not re-run or attest the external consumer runtime.",
    }


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    registry = json.loads((ROOT / "EXTERNAL_CONSUMERS.json").read_text(encoding="utf-8"))
    result = check_registry(ROOT, registry)
    if not result["allPinnedProducerContractsIntact"]:
        raise SystemExit("external consumer compatibility: FAIL")

    target = ROOT / "evidence" / "external-consumers-latest.json"
    expected = stable_json(result)
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            raise SystemExit("stale external consumer evidence")
        print("external consumer evidence check: PASS")
        return

    target.write_text(expected, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
