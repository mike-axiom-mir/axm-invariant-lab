import unittest

from formal.z3_inv01 import solve_case
from tools.run_z3_inv01_comparison import build_receipt


class Z3Inv01ComparisonTests(unittest.TestCase):
    def test_safe_relation_has_no_counterexample_through_bound(self):
        result = solve_case(include_fault=False, max_depth=3)
        self.assertEqual(result.status, "PASS")
        self.assertIsNone(result.witness_depth)
        self.assertEqual(result.trace, ())

    def test_fault_relation_finds_shortest_two_step_counterexample(self):
        result = solve_case(include_fault=True, max_depth=3)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.witness_depth, 2)
        self.assertEqual(
            result.trace,
            ("propose-write-candidate", "FAULT-inherit-candidate-authority"),
        )

    def test_bound_one_does_not_overclaim_fault_absence(self):
        result = solve_case(include_fault=True, max_depth=1)
        self.assertEqual(result.status, "PASS")
        self.assertIsNone(result.witness_depth)

    def test_primary_and_solver_receipt_agree(self):
        receipt = build_receipt()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["issues"], [])
        self.assertEqual(receipt["solver"]["packagePin"], "z3-solver==5.1.0.0")
        self.assertFalse(receipt["authority"]["canon"])
        self.assertFalse(receipt["authority"]["execution"])
        self.assertFalse(receipt["authority"]["merge"])
        self.assertFalse(receipt["authority"]["promotion"])


if __name__ == "__main__":
    unittest.main()
