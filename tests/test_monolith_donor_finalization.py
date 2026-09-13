from __future__ import annotations

import copy
import unittest

from adapters.monolith_donor_finalization import (
    EXECUTED_ADDRESS,
    OBSERVATION_SCHEMA,
    UNREQUESTED_ADDRESS,
    build_receipt,
    inspect,
)


def valid_observation() -> dict:
    return {
        "schema": OBSERVATION_SCHEMA,
        "donorTests": {"testsRun": 6, "failures": 0, "errors": 0, "ok": True},
        "preExecution": {
            "declaredCallableCount": 2,
            "sourceCallableExecuted": 0,
            "plumbingStatus": "PLUMBING_INSTALLED_WITH_EXPLICIT_EXECUTION_BOUNDARY",
        },
        "unprovenRequiredAddress": {"address": EXECUTED_ADDRESS, "blocked": True},
        "explicitExecution": {
            "requestedAddresses": [EXECUTED_ADDRESS],
            "executedAddresses": [EXECUTED_ADDRESS],
            "acceptedExercisedReceipts": 1,
            "registryDeclaredCallableCount": 2,
            "packageStatus": "PACKAGED_AFTER_REQUIRED_EVIDENCE_PASS",
        },
        "package": {
            "requiredCallableAddresses": [EXECUTED_ADDRESS],
            "truthBoundary": (
                "File hashes prove package integrity. Workflow/callable receipts prove only the explicitly required routes. "
                "Unbound leaf declarations and candidate compositions remain unexecuted."
            ),
        },
        "authority": {"execution": False, "merge": False, "promotion": False, "canon": False},
    }


class MonolithDonorFinalizationTests(unittest.TestCase):
    def test_grounded_donor_observation_passes(self) -> None:
        result = inspect(valid_observation())
        self.assertEqual(result.status, "PASS")
        self.assertFalse(result.failures)
        self.assertFalse(result.unknowns)

    def test_missing_execution_observation_holds(self) -> None:
        observation = valid_observation()
        del observation["explicitExecution"]
        result = inspect(observation)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("explicitExecution", result.unknowns)

    def test_declaration_cannot_silently_become_execution(self) -> None:
        observation = valid_observation()
        observation["preExecution"]["sourceCallableExecuted"] = 2
        self.assertEqual(inspect(observation).status, "FAIL")

    def test_unproven_required_address_must_fail_closed(self) -> None:
        observation = valid_observation()
        observation["unprovenRequiredAddress"]["blocked"] = False
        self.assertEqual(inspect(observation).status, "FAIL")

    def test_execution_evidence_cannot_leak_to_unrequested_callable(self) -> None:
        observation = valid_observation()
        observation["explicitExecution"]["executedAddresses"].append(UNREQUESTED_ADDRESS)
        result = inspect(observation)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("leaked" in item or "unrequested" in item for item in result.failures))

    def test_package_required_scope_cannot_widen(self) -> None:
        observation = valid_observation()
        observation["package"]["requiredCallableAddresses"].append(UNREQUESTED_ADDRESS)
        self.assertEqual(inspect(observation).status, "FAIL")

    def test_package_truth_boundary_cannot_promote_unrelated_gaps(self) -> None:
        observation = valid_observation()
        observation["package"]["truthBoundary"] = "Package integrity proves every capability is executable."
        self.assertEqual(inspect(observation).status, "FAIL")

    def test_authority_escalation_fails(self) -> None:
        observation = valid_observation()
        observation["authority"]["canon"] = True
        self.assertEqual(inspect(observation).status, "FAIL")

    def test_provenance_failure_overrides_semantic_pass(self) -> None:
        result = build_receipt(
            copy.deepcopy(valid_observation()),
            provenance_checks=[{"check": "pinned-donor-commit", "ok": False}],
            provenance_failures=["donor checkout drifted"],
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("donor checkout drifted", result["failures"])
        self.assertTrue(all(value is False for value in result["authority"].values()))


if __name__ == "__main__":
    unittest.main()
