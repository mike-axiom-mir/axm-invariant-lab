from __future__ import annotations

from copy import deepcopy
from typing import Any

SCHEMA = "axm.invariant-lab.monolith-native-route-evolution-observation/v0.1"
RESULT_SCHEMA = "axm.invariant-lab.refinement-result/v0.1"
DONOR_REPOSITORY = "mike-axiom-mir/axm-monolith"
DONOR_COMMIT = "8ce73a54d488805b126fe7fa64eac1ec2b28e900"
DONOR_TOOL_BLOB = "4286dbd2ef550841889644c56b620abda5cdf504"
DONOR_TEST_BLOB = "d41f5e0aa727f0718df2e4f783431de98f185b96"
EXPECTED_RECIPE_IDS = (
    "game-assets-forge-self-test",
    "universal-creation-cli-help",
    "framestate-cli-help",
    "machine-voice-cli-help",
    "city-p2p-cli-help",
    "walmi-public-capability-verify",
    "front-door-validate",
    "living-city-headless-main",
    "grammar-102-capability-snapshot-export",
    "factual-space-cli-help",
    "factual-rooted-crew-verify-roots",
    "factual-ship-blueprint-validate",
    "factual-ship-interior-validate",
    "factual-handoff-full-audit",
    "factual-package-seal-check",
)


def _result(status: str, failures: list[str], unknowns: list[str], observed: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "invariant": "INV-20",
        "status": status,
        "failures": failures,
        "unknowns": unknowns,
        "observed": observed,
        "authority": {
            "execution": False,
            "merge": False,
            "promotion": False,
            "canon": False,
        },
        "truth_boundary": (
            "This refinement checks one pinned Monolith native-route planning gate. READY means eligible "
            "for a separate explicit execution attempt; it is not execution, verification of product behavior, "
            "deployment, merge, promotion, or CANON authority."
        ),
    }


def inspect(observation: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    unknowns: list[str] = []
    observed: dict[str, Any] = {}

    if not isinstance(observation, dict):
        return _result("HOLD", [], ["observation_not_object"], observed)
    if observation.get("schema") != SCHEMA:
        return _result("HOLD", [], ["unsupported_or_missing_observation_schema"], observed)

    donor = observation.get("donor")
    plan = observation.get("plan")
    falsifiers = observation.get("falsifiers")
    authority = observation.get("authority")
    if not isinstance(donor, dict):
        unknowns.append("missing_donor_provenance")
    if not isinstance(plan, dict):
        unknowns.append("missing_plan_observation")
    if not isinstance(falsifiers, dict):
        unknowns.append("missing_falsifier_observations")
    if not isinstance(authority, dict):
        unknowns.append("missing_authority_boundary")
    if unknowns:
        return _result("HOLD", failures, unknowns, observed)

    expected_provenance = {
        "repository": DONOR_REPOSITORY,
        "commit": DONOR_COMMIT,
        "tool_blob": DONOR_TOOL_BLOB,
        "test_blob": DONOR_TEST_BLOB,
    }
    for key, expected in expected_provenance.items():
        if donor.get(key) != expected:
            failures.append(f"donor_{key}_drift")

    recipes = plan.get("recipes")
    if not isinstance(recipes, list):
        unknowns.append("plan_recipes_missing")
        recipes = []
    else:
        recipe_ids = [row.get("id") for row in recipes if isinstance(row, dict)]
        observed["recipe_count"] = len(recipes)
        observed["recipe_ids"] = recipe_ids
        if tuple(recipe_ids) != EXPECTED_RECIPE_IDS:
            failures.append("recipe_identity_or_order_drift")
        if len(set(recipe_ids)) != len(recipe_ids):
            failures.append("duplicate_recipe_id")
        for row in recipes:
            if not isinstance(row, dict):
                failures.append("non_object_recipe_row")
                continue
            if row.get("status") != "READY":
                failures.append(f"recipe_not_ready:{row.get('id')}")
            if row.get("executed") is not False:
                failures.append(f"plan_silently_executed:{row.get('id')}")
            address = row.get("address")
            if not isinstance(address, str) or "::native.command/" not in address:
                failures.append(f"recipe_not_native_command:{row.get('id')}")
            commit = row.get("commit")
            if not isinstance(commit, str) or len(commit) != 40:
                failures.append(f"recipe_commit_not_pinned:{row.get('id')}")
            if not isinstance(row.get("repository"), str) or not row["repository"].startswith("mike-axiom-mir/"):
                failures.append(f"recipe_repository_not_explicit:{row.get('id')}")

    observed["plan_status"] = plan.get("status")
    observed["plan_mode"] = plan.get("mode")
    if plan.get("mode") != "plan":
        failures.append("observation_not_plan_mode")
    if plan.get("status") != "PASS":
        failures.append("exact_pinned_plan_not_pass")

    expected_falsifiers = {
        "changed_ref": "HOLD_RECIPE_REF_MISMATCH",
        "unverified_native": "HOLD_NO_VERIFIED_NATIVE_EVIDENCE",
        "missing_endpoint": "HOLD_ENDPOINT_MISSING",
    }
    for name, expected_row_status in expected_falsifiers.items():
        item = falsifiers.get(name)
        if not isinstance(item, dict):
            unknowns.append(f"missing_falsifier:{name}")
            continue
        if item.get("overall_status") != "HOLD":
            failures.append(f"falsifier_fail_open:{name}")
        if item.get("row_status") != expected_row_status:
            failures.append(f"falsifier_wrong_reason:{name}")
        if item.get("executed") is not False:
            failures.append(f"falsifier_executed:{name}")

    expected_authority = {
        "execution": False,
        "merge": False,
        "promotion": False,
        "canon": False,
    }
    for key, expected in expected_authority.items():
        if authority.get(key) is not expected:
            failures.append(f"authority_escalation:{key}")

    boundary = observation.get("truth_boundary")
    if not isinstance(boundary, str):
        unknowns.append("missing_truth_boundary")
    else:
        lowered = boundary.lower()
        if "changed refs are hold" not in lowered:
            failures.append("truth_boundary_lost_changed_ref_hold")
        if "not canon" not in lowered or "product acceptance" not in lowered:
            failures.append("truth_boundary_lost_nonpromotion")

    if failures:
        status = "FAIL"
    elif unknowns:
        status = "HOLD"
    else:
        status = "PASS"
    return _result(status, failures, unknowns, observed)


def copy_with(observation: dict[str, Any], *path_and_value: Any) -> dict[str, Any]:
    """Tiny test helper: deep copy then set one nested path/value pair sequence."""
    out = deepcopy(observation)
    *path, value = path_and_value
    node = out
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    return out
