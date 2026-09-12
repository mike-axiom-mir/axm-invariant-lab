import copy
import json
from pathlib import Path
import unittest

from adapters.truthgrid_evidence import inspect

ROOT = Path(__file__).resolve().parents[1]


class TruthGridRefinementTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(
            (ROOT / "fixtures" / "truthgrid-foundation-extract.json").read_text(encoding="utf-8")
        )

    def test_current_extract_passes_bounded_checks(self):
        result = inspect(self.load_fixture())
        self.assertEqual("PASS", result.status)
        self.assertEqual([], result.failures)
        self.assertEqual([], result.unknowns)

    def test_wrong_rollback_ref_fails(self):
        receipt = self.load_fixture()
        receipt["ticks"][1]["merge"]["rollbackRef"] = "revision:99"
        result = inspect(receipt)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("rollbackRef" in item for item in result.failures))

    def test_missing_evidence_holds(self):
        receipt = self.load_fixture()
        del receipt["ticks"][0]["merge"]["rollbackRef"]
        result = inspect(receipt)
        self.assertEqual("HOLD", result.status)
        self.assertIn("ticks[0].merge.rollbackRef", result.unknowns)

    def test_hash_contradiction_fails(self):
        receipt = self.load_fixture()
        receipt["twoInstance"]["hashB"] = "different"
        result = inspect(receipt)
        self.assertEqual("FAIL", result.status)


if __name__ == "__main__":
    unittest.main()
