import unittest

from src.bounded_explorer import Invariant, Transition, explore
from models import no_silent_authority, no_auto_canon, rollback_continuity, selective_inheritance


class ExplorerTests(unittest.TestCase):
    def test_safe_models_pass(self):
        for model in [
            no_silent_authority,
            no_auto_canon,
            rollback_continuity,
            selective_inheritance,
        ]:
            with self.subTest(model=model.__name__):
                result = explore(
                    model.initial_state(),
                    model.SAFE_TRANSITIONS,
                    model.INVARIANTS,
                    max_depth=model.MAX_DEPTH,
                )
                self.assertEqual("PASS", result.status)
                self.assertEqual([], result.counterexamples)

    def test_fault_models_fail(self):
        for model in [
            no_silent_authority,
            no_auto_canon,
            rollback_continuity,
            selective_inheritance,
        ]:
            with self.subTest(model=model.__name__):
                result = explore(
                    model.initial_state(),
                    model.FAULT_TRANSITIONS,
                    model.INVARIANTS,
                    max_depth=model.MAX_DEPTH,
                )
                self.assertEqual("FAIL", result.status)
                self.assertTrue(result.counterexamples)

    def test_authority_counterexample_is_shortest(self):
        result = explore(
            no_silent_authority.initial_state(),
            no_silent_authority.FAULT_TRANSITIONS,
            no_silent_authority.INVARIANTS,
            max_depth=no_silent_authority.MAX_DEPTH,
        )
        first = result.counterexamples[0]
        self.assertEqual(2, len(first.trace))
        self.assertEqual("propose-write-candidate", first.trace[0].transition)
        self.assertEqual("FAULT-inherit-candidate-authority", first.trace[1].transition)

    def test_rollback_safe_relation_survives_post_restore_forward_progress(self):
        result = explore(
            rollback_continuity.initial_state(),
            rollback_continuity.SAFE_TRANSITIONS,
            rollback_continuity.INVARIANTS,
            max_depth=rollback_continuity.FORMAL_AUDIT_DEPTH,
        )
        self.assertEqual("PASS", result.status)
        self.assertEqual([], result.counterexamples)

    def test_stale_rollback_receipt_fault_is_detected_after_restore(self):
        result = explore(
            rollback_continuity.initial_state(),
            rollback_continuity.STALE_RECEIPT_FAULT_TRANSITIONS,
            rollback_continuity.INVARIANTS,
            max_depth=rollback_continuity.FORMAL_AUDIT_DEPTH,
        )
        self.assertEqual("FAIL", result.status)
        first = result.counterexamples[0]
        self.assertEqual(5, len(first.trace))
        self.assertEqual(
            [
                "mutate-S0-to-S1",
                "checkpoint-S1",
                "mutate-S1-to-S2",
                "rollback-to-S1",
                "FAULT-forward-mutation-keeps-stale-rollback-receipt",
            ],
            [step.transition for step in first.trace],
        )

    def test_unknown_is_hold_not_pass(self):
        initial = {"observed": None}
        invariants = [
            Invariant(
                "known-field",
                lambda s: None if s["observed"] is None else s["observed"] is True,
                "field must be observed true",
            )
        ]
        result = explore(initial, [], invariants, max_depth=0)
        self.assertEqual("HOLD", result.status)
        self.assertEqual(1, len(result.unknowns))

    def test_breadth_first_prefers_one_step_failure(self):
        initial = {"ok": True, "stage": 0}
        transitions = [
            Transition("slow-1", lambda s: s["stage"] == 0, lambda s: {**s, "stage": 1}),
            Transition("slow-2", lambda s: s["stage"] == 1, lambda s: {**s, "ok": False, "stage": 2}),
            Transition("fast", lambda s: s["stage"] == 0, lambda s: {**s, "ok": False, "stage": 9}),
        ]
        invariant = [Invariant("ok", lambda s: s["ok"], "ok remains true")]
        result = explore(initial, transitions, invariant, max_depth=2)
        self.assertEqual(1, len(result.counterexamples[0].trace))
        self.assertEqual("fast", result.counterexamples[0].trace[0].transition)


if __name__ == "__main__":
    unittest.main()
