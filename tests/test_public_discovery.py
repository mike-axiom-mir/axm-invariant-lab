from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from src.public_discovery import build_capability_records, build_public_marker, inspect, write_outputs


class PublicDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "tools").mkdir()
        (self.root / "src" / "cap.py").write_text("def inspect():\n    return 'ok'\n", encoding="utf-8")
        (self.root / "tools" / "check.py").write_text("print('ok')\n", encoding="utf-8")
        self.manifest = {
            "schema_version": "1.3",
            "module": {"name": "demo", "purpose": "bounded demo"},
            "capabilities": [
                {
                    "id": "z.capability",
                    "description": "z demo",
                    "provides": ["evidence.z"],
                    "accepts": [],
                    "tags": ["demo"],
                    "evidence": {"status": "z_status", "ceiling": "fixture-only"},
                },
                {
                    "id": "a.capability",
                    "description": "a demo",
                    "provides": ["evidence.a"],
                    "accepts": [],
                    "tags": ["demo"],
                    "evidence": {"status": "a_status", "ceiling": "fixture-only"},
                },
            ],
            "entrypoints": [
                {"kind": "python-library", "path": "src/cap.py", "symbol": "inspect"},
                {"kind": "python-cli", "path": "tools/check.py", "command": "python tools/check.py --check"},
            ],
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_write_then_inspect_passes(self) -> None:
        result = write_outputs(self.root, self.manifest)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["capabilityCount"], 2)
        self.assertFalse(any(result["authority"].values()))

    def test_public_marker_is_explicit_and_bounded(self) -> None:
        marker = build_public_marker()
        self.assertEqual(marker["schema"], "axm.discovery-public/v1")
        self.assertEqual(marker["repo"], "mike-axiom-mir/axm-invariant-lab")
        self.assertIs(marker["public"], True)
        self.assertEqual(set(marker), {"schema", "repo", "display_name", "public"})

    def test_registry_preserves_ids_and_evidence_status(self) -> None:
        rows = build_capability_records(self.manifest)
        self.assertEqual([row["id"] for row in rows], ["a.capability", "z.capability"])
        self.assertEqual([row["status"] for row in rows], ["a_status", "z_status"])
        self.assertTrue(all(row["source_evidence"] == ["AXM_MODULE.json"] for row in rows))

    def test_registry_never_grants_authority_or_runtime_proof(self) -> None:
        rows = build_capability_records(self.manifest)
        for row in rows:
            self.assertFalse(row["truth"]["declaration_is_runtime_proof"])
            self.assertFalse(row["truth"]["grants_authority"])
            self.assertTrue(row["truth"]["generated_from_module_manifest"])

    def test_stale_registry_fails(self) -> None:
        self.assertEqual(write_outputs(self.root, self.manifest)["status"], "PASS")
        (self.root / "registry" / "capabilities.jsonl").write_text("{}\n", encoding="utf-8")
        result = inspect(self.root, self.manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("output-stale", {item["code"] for item in result["failures"]})

    def test_missing_public_marker_fails(self) -> None:
        self.assertEqual(write_outputs(self.root, self.manifest)["status"], "PASS")
        (self.root / ".axm" / "discovery-public.json").unlink()
        result = inspect(self.root, self.manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("output-missing", {item["code"] for item in result["failures"]})

    def test_unknown_manifest_schema_holds_and_is_not_published(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["schema_version"] = "2.0"
        result = write_outputs(self.root, manifest)
        self.assertEqual(result["status"], "HOLD")
        self.assertFalse((self.root / ".axm" / "discovery-public.json").exists())
        self.assertFalse((self.root / "registry" / "capabilities.jsonl").exists())

    def test_invalid_local_entrypoint_blocks_publication(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"][0]["path"] = "src/missing.py"
        result = write_outputs(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse((self.root / "registry" / "capabilities.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
