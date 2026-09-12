import copy
import json
from pathlib import Path
import unittest

from adapters.state_research_workfloor_sentinel import inspect

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "state-research-workfloor-sentinel-v1.projection.json"


class StateResearchWorkfloorSentinelTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_pinned_donor_projection_refines_bug_then_repair(self):
        result = inspect(self.load_fixture())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failures, [])
        self.assertEqual(result.unknowns, [])
        self.assertEqual(result.derived["dependency_bug_run.invariant_status"], "FAIL")
        self.assertEqual(result.derived["repaired_run.invariant_status"], "PASS")
        self.assertEqual(
            result.derived["dependency_bug_run.derived_missed_check_ids"],
            ["cross--report-matches-raw-results"],
        )

    def test_silent_missing_wakeup_in_repaired_projection_fails(self):
        fixture = self.load_fixture()
        fixture["repaired_run"]["step"]["awakened_check_ids"].remove(
            "cross--report-matches-raw-results"
        )
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("reported misses" in failure for failure in result.failures))

    def test_missing_required_evidence_holds(self):
        fixture = self.load_fixture()
        del fixture["repaired_run"]["final_sparse_check_results_hash"]
        result = inspect(fixture)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("repaired_run.final_sparse_check_results_hash", result.unknowns)

    def test_source_identity_drift_fails(self):
        fixture = self.load_fixture()
        fixture["source"]["git_blob_sha"] = "0" * 40
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("source.git_blob_sha" in failure for failure in result.failures))

    def test_equivalence_cannot_contradict_mismatch_list(self):
        fixture = self.load_fixture()
        fixture["dependency_bug_run"]["step"]["sparse_output_equivalent_to_oracle"] = True
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("equivalence flag" in failure for failure in result.failures))

    def test_adapter_is_read_only(self):
        fixture = self.load_fixture()
        before = copy.deepcopy(fixture)
        inspect(fixture)
        self.assertEqual(fixture, before)


if __name__ == "__main__":
    unittest.main()
