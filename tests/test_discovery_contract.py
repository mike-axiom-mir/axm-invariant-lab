from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from src.discovery_contract import inspect


class DiscoveryContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "tools").mkdir()
        (self.root / "src" / "cap.py").write_text("def inspect():\n    return 'ok'\n", encoding="utf-8")
        (self.root / "tools" / "check.py").write_text("print('ok')\n", encoding="utf-8")
        self.manifest = {
            "schema_version": "1.4",
            "module": {"name": "demo", "purpose": "bounded demo"},
            "capabilities": [
                {
                    "id": "demo.capability",
                    "description": "demo",
                    "provides": ["evidence.demo"],
                    "accepts": [],
                    "tags": ["demo"],
                    "evidence": {"status": "fixture_tested", "ceiling": "fixture-only"},
                }
            ],
            "entrypoints": [
                {"kind": "python-library", "path": "src/cap.py", "symbol": "inspect"},
                {"kind": "python-cli", "path": "tools/check.py", "command": "python tools/check.py --check"},
            ],
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_manifest_passes(self) -> None:
        result = inspect(self.root, self.manifest)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checkedEntrypointCount"], 2)
        self.assertFalse(any(result["authority"].values()))

    def test_missing_entrypoint_file_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"][0]["path"] = "src/missing.py"
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("entrypoint.path.missing", {item["code"] for item in result["failures"]})

    def test_missing_library_symbol_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"][0]["symbol"] = "missing"
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("entrypoint.symbol.absent", {item["code"] for item in result["failures"]})

    def test_cli_path_mismatch_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"][1]["command"] = "python tools/other.py --check"
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("entrypoint.command.path-mismatch", {item["code"] for item in result["failures"]})

    def test_cli_without_check_mode_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"][1]["command"] = "python tools/check.py"
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("entrypoint.command.no-check", {item["code"] for item in result["failures"]})

    def test_path_escape_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"][0]["path"] = "../outside.py"
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("entrypoint.path.invalid", {item["code"] for item in result["failures"]})

    def test_duplicate_capability_id_fails(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["capabilities"].append(copy.deepcopy(manifest["capabilities"][0]))
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("capability.id.duplicate", {item["code"] for item in result["failures"]})

    def test_unknown_entrypoint_kind_holds(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoints"].append({"kind": "future-runtime", "path": "src/cap.py"})
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["failureCount"], 0)
        self.assertIn("entrypoint.kind.unsupported", {item["code"] for item in result["holds"]})

    def test_unsupported_schema_major_holds(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["schema_version"] = "2.0"
        result = inspect(self.root, manifest)
        self.assertEqual(result["status"], "HOLD")
        self.assertIn("manifest.schema.unsupported", {item["code"] for item in result["holds"]})


if __name__ == "__main__":
    unittest.main()
