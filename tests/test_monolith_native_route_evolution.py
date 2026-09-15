import unittest

from adapters.monolith_native_route_evolution import (
    DONOR_COMMIT,
    DONOR_REPOSITORY,
    DONOR_TEST_BLOB,
    DONOR_TOOL_BLOB,
    EXPECTED_RECIPE_IDS,
    SCHEMA,
    inspect,
)


def baseline():
    recipes = []
    for idx, recipe_id in enumerate(EXPECTED_RECIPE_IDS):
        recipes.append({
            "id": recipe_id,
            "address": f"module-{idx}::native.command/python-project-script/tool-{idx}",
            "repository": f"mike-axiom-mir/module-{idx}",
            "commit": f"{idx:040x}"[-40:],
            "args": ["--help"],
            "status": "READY",
            "executed": False,
        })
    return {
        "schema": SCHEMA,
        "donor": {
            "repository": DONOR_REPOSITORY,
            "commit": DONOR_COMMIT,
            "tool_blob": DONOR_TOOL_BLOB,
            "test_blob": DONOR_TEST_BLOB,
        },
        "plan": {"status": "PASS", "mode": "plan", "recipes": recipes},
        "falsifiers": {
            "changed_ref": {"overall_status": "HOLD", "row_status": "HOLD_RECIPE_REF_MISMATCH", "executed": False},
            "unverified_native": {"overall_status": "HOLD", "row_status": "HOLD_NO_VERIFIED_NATIVE_EVIDENCE", "executed": False},
            "missing_endpoint": {"overall_status": "HOLD", "row_status": "HOLD_ENDPOINT_MISSING", "executed": False},
        },
        "authority": {"execution": False, "merge": False, "promotion": False, "canon": False},
        "truth_boundary": "Only exact pinned refs with retained VERIFIED native-command evidence are eligible. Changed refs are HOLD until revalidated; copied-workspace smoke success is not CANON or product acceptance.",
    }


class NativeRouteEvolutionTest(unittest.TestCase):
    def test_baseline_passes(self):
        self.assertEqual("PASS", inspect(baseline())["status"])

    def test_future_schema_holds(self):
        data = baseline(); data["schema"] = "future/v9"
        self.assertEqual("HOLD", inspect(data)["status"])

    def test_missing_plan_holds(self):
        data = baseline(); del data["plan"]
        self.assertEqual("HOLD", inspect(data)["status"])

    def test_donor_commit_drift_fails(self):
        data = baseline(); data["donor"]["commit"] = "0" * 40
        result = inspect(data)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("donor_commit_drift", result["failures"])

    def test_plan_must_not_execute(self):
        data = baseline(); data["plan"]["recipes"][0]["executed"] = True
        result = inspect(data)
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any(x.startswith("plan_silently_executed") for x in result["failures"]))

    def test_changed_ref_must_hold(self):
        data = baseline(); data["falsifiers"]["changed_ref"]["overall_status"] = "PASS"
        self.assertEqual("FAIL", inspect(data)["status"])

    def test_unverified_native_must_hold(self):
        data = baseline(); data["falsifiers"]["unverified_native"]["row_status"] = "READY"
        self.assertEqual("FAIL", inspect(data)["status"])

    def test_missing_endpoint_must_hold(self):
        data = baseline(); data["falsifiers"]["missing_endpoint"]["row_status"] = "READY"
        self.assertEqual("FAIL", inspect(data)["status"])

    def test_recipe_identity_drift_fails(self):
        data = baseline(); data["plan"]["recipes"] = list(reversed(data["plan"]["recipes"]))
        self.assertEqual("FAIL", inspect(data)["status"])

    def test_authority_escalation_fails(self):
        data = baseline(); data["authority"]["canon"] = True
        result = inspect(data)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("authority_escalation:canon", result["failures"])

    def test_truth_boundary_must_preserve_nonpromotion(self):
        data = baseline(); data["truth_boundary"] = "Changed refs are HOLD."
        self.assertEqual("FAIL", inspect(data)["status"])


if __name__ == "__main__":
    unittest.main()
