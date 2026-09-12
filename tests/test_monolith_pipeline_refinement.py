import copy
import json
from pathlib import Path
import unittest

from adapters.monolith_pipeline_fabric import inspect

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "monolith-pipeline-fabric-v0.1.json"


class MonolithPipelineRefinementTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_pinned_v01_contract_shape_passes(self):
        fixture = self.load_fixture()
        result = inspect(fixture["descriptor"], fixture["candidates"])
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failures, [])
        self.assertEqual(result.unknowns, [])

    def test_automatic_authority_escalation_fails(self):
        fixture = self.load_fixture()
        fixture["descriptor"]["authority"]["automatic_execution"] = True
        result = inspect(fixture["descriptor"], fixture["candidates"])
        self.assertEqual(result.status, "FAIL")
        self.assertIn("automatic_execution is not explicitly false", result.failures)

    def test_missing_authority_evidence_holds(self):
        fixture = self.load_fixture()
        del fixture["descriptor"]["authority"]["automatic_merge"]
        result = inspect(fixture["descriptor"], fixture["candidates"])
        self.assertEqual(result.status, "HOLD")
        self.assertIn("descriptor.authority.automatic_merge", result.unknowns)

    def test_candidate_status_cannot_silently_upgrade(self):
        fixture = self.load_fixture()
        fixture["candidates"]["pipelines"][0]["status"] = "VERIFIED"
        result = inspect(fixture["descriptor"], fixture["candidates"])
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("candidate-only" in failure for failure in result.failures))

    def test_missing_candidates_evidence_holds(self):
        fixture = self.load_fixture()
        result = inspect(fixture["descriptor"], None)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("candidates", result.unknowns)

    def test_adapter_is_read_only(self):
        fixture = self.load_fixture()
        before = copy.deepcopy(fixture)
        inspect(fixture["descriptor"], fixture["candidates"])
        self.assertEqual(fixture, before)


if __name__ == "__main__":
    unittest.main()
