"""Deterministic work-count probe for Invariant Lab's two exploration strategies.

The fixture deliberately uses two distinct legal transition names that reconverge on
one next state. Visited-state BFS therefore grows with unique states while all-path
enumeration grows with path multiplicity. This is a tractability probe, not a general
benchmark or an AXM safety model.
"""
from __future__ import annotations

from typing import Any

from src.bounded_explorer import Invariant, Transition, explore
from src.reference_verifier import verify_paths

PROBE_DEPTHS = (12, 15, 16)
PATH_NODE_BUDGET = 100_000


def build_reconverging_model(depth: int):
    if depth < 0:
        raise ValueError("depth must be >= 0")

    def guard(state):
        return int(state["step"]) < depth

    def advance(state):
        state["step"] = int(state["step"]) + 1
        return state

    transitions = (
        Transition("advance.alpha", guard, advance),
        Transition("advance.beta", guard, advance),
    )
    invariants = (
        Invariant(
            "step.within-bound",
            lambda state: 0 <= int(state["step"]) <= depth,
            "The synthetic step counter never exceeds the declared probe depth.",
        ),
    )
    return {"step": 0}, transitions, invariants


def run_probe(depth: int, *, path_node_budget: int = PATH_NODE_BUDGET) -> dict[str, Any]:
    initial, transitions, invariants = build_reconverging_model(depth)
    primary = explore(initial, transitions, invariants, max_depth=depth)
    reference = verify_paths(
        initial,
        transitions,
        invariants,
        max_depth=depth,
        max_path_nodes=path_node_budget,
    )
    return {
        "depth": depth,
        "primaryStatus": primary.status,
        "primaryUniqueStates": primary.explored_states,
        "primaryTransitions": primary.explored_transitions,
        "referenceStatus": reference.status,
        "referenceComplete": reference.complete,
        "referenceUniqueStates": reference.unique_states,
        "referencePathNodes": reference.path_nodes,
        "referencePathTransitions": reference.path_transitions,
        "pathNodeBudget": path_node_budget,
    }


def build_tractability_receipt(
    depths=PROBE_DEPTHS,
    *,
    path_node_budget: int = PATH_NODE_BUDGET,
) -> dict[str, Any]:
    depths = tuple(int(depth) for depth in depths)
    if not depths:
        raise ValueError("at least one probe depth is required")

    cases = [run_probe(depth, path_node_budget=path_node_budget) for depth in depths]
    complete = [case["depth"] for case in cases if case["referenceComplete"]]
    held = [case["depth"] for case in cases if not case["referenceComplete"]]

    return {
        "schemaVersion": "0.1",
        "evidenceClass": "TRACTABILITY-MEASUREMENT",
        "claim": "On a deterministic reconverging two-branch model, the visited-state explorer remains complete through depth 16 while the independent all-path verifier reaches its 100000-node budget and correctly returns HOLD at depth 16.",
        "modelShape": "two distinct legal transition names advance one shared integer step, so path count grows exponentially while unique reachable state count grows linearly",
        "measurement": "deterministic work counts only; no wall-clock performance claim",
        "pathNodeBudget": path_node_budget,
        "depths": list(depths),
        "largestCompleteReferenceDepth": max(complete) if complete else None,
        "firstIncompleteReferenceDepth": min(held) if held else None,
        "cases": cases,
        "truthBoundary": "This is a synthetic tractability probe for the repository's two current exploration strategies. It does not predict arbitrary AXM model size, solver performance, memory limits, donor-runtime cost, or real-world safety. A primary PASS still applies only to the exact bounded state model; reference budget exhaustion is HOLD, never PASS.",
    }
