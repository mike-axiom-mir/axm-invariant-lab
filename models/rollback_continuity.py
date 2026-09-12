"""Tiny rollback continuity model with bounded receipt-lifecycle faults."""

from src.bounded_explorer import Invariant, Transition

MAX_DEPTH = 4
FORMAL_AUDIT_DEPTH = 6
LIMITATIONS = [
    "digests are symbolic labels rather than bytes",
    "does not model filesystem atomicity or concurrent writers",
    "fault transitions are synthetic",
]


def initial_state():
    return {
        "current": "S0",
        "knownGood": ["S0"],
        "history": ["S0"],
        "rollback": None,
    }


def mutate_s1(state):
    state["current"] = "S1"
    state["history"] = state["history"] + ["S1"]
    return state


def checkpoint_s1(state):
    if "S1" not in state["knownGood"]:
        state["knownGood"] = state["knownGood"] + ["S1"]
    return state


def mutate_s2(state):
    # `rollback` is the current rollback assertion, not a durable historical log.
    # Once normal forward mutation resumes, that assertion is no longer current.
    state["rollback"] = None
    state["current"] = "S2"
    state["history"] = state["history"] + ["S2"]
    return state


def rollback_s1(state):
    state["current"] = "S1"
    state["rollback"] = {"target": "S1", "status": "restored"}
    return state


def buggy_rollback_unknown(state):
    state["current"] = "S9"
    state["rollback"] = {"target": "S1", "status": "restored"}
    return state


def buggy_forward_keeps_stale_rollback(state):
    """Synthetic pre-repair behavior: move forward but keep a stale rollback assertion."""
    state["current"] = "S2"
    state["history"] = state["history"] + ["S2"]
    return state


def restored_is_known_good(state):
    receipt = state["rollback"]
    if receipt is None:
        return True
    if receipt.get("status") != "restored":
        return None
    return (
        state["current"] == receipt.get("target")
        and state["current"] in state["knownGood"]
        and state["current"] in state["history"]
    )


INVARIANTS = [
    Invariant(
        "INV-03-rollback-known-good-lineage",
        restored_is_known_good,
        "A successful rollback must restore its declared target and that target must be known-good lineage.",
    )
]

SAFE_TRANSITIONS = [
    Transition("mutate-S0-to-S1", lambda s: s["current"] == "S0", mutate_s1),
    Transition(
        "checkpoint-S1",
        lambda s: s["current"] == "S1" and "S1" not in s["knownGood"],
        checkpoint_s1,
    ),
    Transition("mutate-S1-to-S2", lambda s: s["current"] == "S1", mutate_s2),
    Transition(
        "rollback-to-S1",
        lambda s: s["current"] == "S2" and "S1" in s["knownGood"],
        rollback_s1,
    ),
]

FAULT_TRANSITIONS = SAFE_TRANSITIONS + [
    Transition(
        "FAULT-rollback-reports-S1-but-restores-S9",
        lambda s: s["current"] == "S2" and "S1" in s["knownGood"],
        buggy_rollback_unknown,
    )
]

STALE_RECEIPT_FAULT_TRANSITIONS = SAFE_TRANSITIONS + [
    Transition(
        "FAULT-forward-mutation-keeps-stale-rollback-receipt",
        lambda s: s["current"] == "S1" and s["rollback"] is not None,
        buggy_forward_keeps_stale_rollback,
    )
]
