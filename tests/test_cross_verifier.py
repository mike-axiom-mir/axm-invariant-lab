import unittest
from models import no_auto_canon, no_silent_authority, rollback_continuity, selective_inheritance
from src.bounded_explorer import Invariant, Transition
from src.cross_verifier import cross_verify
from src.reference_verifier import verify_paths

MODELS=(no_silent_authority,no_auto_canon,rollback_continuity,selective_inheritance)

class CrossVerifierTests(unittest.TestCase):
    def test_independent_verifier_agrees_on_safe_and_fault_models(self):
        for model in MODELS:
            for label, transitions, expected in (("safe",model.SAFE_TRANSITIONS,"PASS"),("fault",model.FAULT_TRANSITIONS,"FAIL")):
                with self.subTest(model=model.__name__,variant=label):
                    result=cross_verify(model.initial_state(),transitions,model.INVARIANTS,max_depth=model.MAX_DEPTH)
                    self.assertEqual("AGREE",result.status)
                    self.assertEqual(expected,result.primary["status"])
                    self.assertTrue(result.reference.complete)
                    self.assertTrue(all(result.agreements.values()))

    def test_unknown_hold_agrees(self):
        invariants=[Invariant("known",lambda s: None if s["observed"] is None else s["observed"],"must be known")]
        result=cross_verify({"observed":None},[],invariants,max_depth=0)
        self.assertEqual("AGREE",result.status)
        self.assertEqual("HOLD",result.primary["status"])
        self.assertEqual(("known",),result.reference.unknown_invariants)

    def test_reference_budget_forbids_unearned_pass(self):
        transitions=[Transition("toggle",lambda s:True,lambda s:{"bit":not s["bit"]})]
        invariants=[Invariant("boolean",lambda s:isinstance(s["bit"],bool),"bit stays boolean")]
        result=verify_paths({"bit":False},transitions,invariants,max_depth=20,max_path_nodes=3)
        self.assertFalse(result.complete)
        self.assertEqual("HOLD",result.status)

    def test_budget_exhaustion_does_not_erase_observed_failure(self):
        transitions=[Transition("break",lambda s:True,lambda s:{"ok":False})]
        invariants=[Invariant("ok",lambda s:s["ok"],"ok remains true")]
        result=verify_paths({"ok":True},transitions,invariants,max_depth=20,max_path_nodes=2)
        self.assertFalse(result.complete)
        self.assertEqual("FAIL",result.status)
        self.assertEqual(("ok",),result.failing_invariants)

if __name__=="__main__": unittest.main()
