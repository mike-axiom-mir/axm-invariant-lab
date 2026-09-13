import copy
import json
from pathlib import Path
import unittest

from adapters.monolith_connected_archive import inspect_projection

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "monolith-connected-archive-v0.3.2.projection.json"


class MonolithConnectedArchiveRefinementTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_exact_archive_projection_passes(self):
        result = inspect_projection(self.load_fixture())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failures, [])
        self.assertEqual(result.unknowns, [])
        self.assertEqual(result.metrics["snapshot_verified_file_count"], 15955)
        self.assertEqual(result.metrics["endpoint_count"], 23472)
        self.assertEqual(result.metrics["blocked_endpoint_count"], 23316)
        self.assertEqual(result.metrics["explicit_callable_endpoint_count"], 3)
        self.assertEqual(result.metrics["composition_count"], 80)
        self.assertEqual(result.metrics["compositions_containing_callable_stage"], 7)
        self.assertEqual(result.metrics["composition_step_occurrence_count"], 384)
        self.assertEqual(result.metrics["test_adapter_ready_endpoint_count"], 37)
        self.assertEqual(result.metrics["test_command_count"], 127)
        self.assertEqual(result.metrics["test_command_failed_count"], 28)
        self.assertEqual(result.metrics["test_command_timed_out_count"], 3)

    def test_snapshot_mismatch_fails(self):
        projection = self.load_fixture()
        projection["snapshot_integrity"]["mismatch_count"] = 1
        projection["snapshot_integrity"]["verified_count"] -= 1
        result = inspect_projection(projection)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("snapshot receipt" in failure for failure in result.failures))

    def test_blocked_gap_disagreement_fails(self):
        projection = self.load_fixture()
        projection["gaps"]["blocked_endpoint_count"] -= 1
        result = inspect_projection(projection)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("gap registry" in failure for failure in result.failures))

    def test_leaf_declaration_cannot_be_promoted_callable(self):
        projection = self.load_fixture()
        projection["leaf_registry"]["declared_callable_count"] = 1
        result = inspect_projection(projection)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("leaf registry silently promotes declarations into callable evidence", result.failures)

    def test_named_workflow_scope_leak_fails(self):
        projection = self.load_fixture()
        projection["compositions"]["callable_scope_violation_ids"] = ["composition-003"]
        result = inspect_projection(projection)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("callability leaked" in failure for failure in result.failures))

    def test_all_callable_candidate_composition_fails(self):
        projection = self.load_fixture()
        projection["compositions"]["all_steps_named_workflow_callable_count"] = 1
        result = inspect_projection(projection)
        self.assertEqual(result.status, "FAIL")

    def test_test_adapter_readiness_is_not_test_success(self):
        result = inspect_projection(
            self.load_fixture(), consumer_claim={"test_adapter_ready_means_tests_passed": True}
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("consumer equates test-adapter readiness with passing tests", result.failures)

    def test_package_integrity_is_not_semantic_correctness(self):
        result = inspect_projection(
            self.load_fixture(), consumer_claim={"package_integrity_proves_semantics": True}
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("consumer equates package byte integrity with semantic correctness", result.failures)

    def test_future_projection_schema_holds(self):
        projection = self.load_fixture()
        projection["schema"] = "axm.invariant-lab.monolith-connected-archive-projection/v9"
        result = inspect_projection(projection)
        self.assertEqual(result.status, "HOLD")
        self.assertTrue(any(item.startswith("unsupported schema:") for item in result.unknowns))

    def test_future_source_schema_holds(self):
        projection = self.load_fixture()
        projection["compositions"]["schema"] = "axm.monolith.executable-compositions/v9"
        result = inspect_projection(projection)
        self.assertEqual(result.status, "HOLD")
        self.assertTrue(any("unsupported compositions.schema" in item for item in result.unknowns))

    def test_consumer_promotions_fail(self):
        flags = [
            "candidate_compositions_executable",
            "named_workflow_callability_transfers_to_compositions",
            "declarations_are_callable",
            "blocked_gaps_may_be_filled_by_guessing",
        ]
        for flag in flags:
            with self.subTest(flag=flag):
                result = inspect_projection(self.load_fixture(), consumer_claim={flag: True})
                self.assertEqual(result.status, "FAIL")

    def test_adapter_is_read_only(self):
        projection = self.load_fixture()
        before = copy.deepcopy(projection)
        inspect_projection(projection, consumer_claim={"candidate_compositions_executable": False})
        self.assertEqual(projection, before)


if __name__ == "__main__":
    unittest.main()
