import unittest

from formal.z3_inv03 import solve_case
from tools.run_z3_inv03_comparison import build_receipt


class Z3Inv03ComparisonTests(unittest.TestCase):
    def test_safe_relation_survives_post_rollback_forward_progress(self):
        result = solve_case(fault_mode="none", max_depth=6)
        self.assertEqual(result.status, "PASS")
        self.assertIsNone(result.witness_depth)
        self.assertEqual(result.trace, ())

    def test_wrong_target_fault_finds_shortest_four_step_counterexample(self):
        result = solve_case(fault_mode="wrong-target", max_depth=6)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.witness_depth, 4)
        self.assertEqual(
            result.trace,
            (
                "mutate-S0-to-S1",
                "checkpoint-S1",
                "mutate-S1-to-S2",
                "FAULT-rollback-reports-S1-but-restores-S9",
            ),
        )

    def test_stale_receipt_fault_finds_shortest_five_step_counterexample(self):
        result = solve_case(fault_mode="stale-receipt", max_depth=6)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.witness_depth, 5)
        self.assertEqual(
            result.trace,
            (
                "mutate-S0-to-S1",
                "checkpoint-S1",
                "mutate-S1-to-S2",
                "rollback-to-S1",
                "FAULT-forward-mutation-keeps-stale-rollback-receipt",
            ),
        )

    def test_depth_four_does_not_expose_stale_receipt_fault_yet(self):
        result = solve_case(fault_mode="stale-receipt", max_depth=4)
        self.assertEqual(result.status, "PASS")
        self.assertIsNone(result.witness_depth)

    def test_primary_and_solver_receipt_agree(self):
        receipt = build_receipt()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["issues"], [])
        self.assertEqual(receipt["maxDepth"], 6)
        self.assertEqual(receipt["solver"]["packagePin"], "z3-solver==5.1.0.0")
        self.assertFalse(receipt["authority"]["canon"])
        self.assertFalse(receipt["authority"]["execution"])
        self.assertFalse(receipt["authority"]["merge"])
        self.assertFalse(receipt["authority"]["promotion"])


if __name__ == "__main__":
    unittest.main()
