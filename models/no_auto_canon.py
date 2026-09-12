"""Candidate lifecycle model: testing/transport alone cannot create CANON state."""

from src.bounded_explorer import Invariant, Transition

MAX_DEPTH = 4
LIMITATIONS = [
    "CANON is modeled as one boolean outcome",
    "the constitutional root judgment behind an explicit decision is outside this model",
    "fault transition is synthetic",
]


def initial_state():
    return {
        "candidateStage": "draft",
        "rootDecision": "none",
        "canon": False,
    }


def test_candidate(state):
    state["candidateStage"] = "tested"
    return state


def transport_candidate(state):
    state["candidateStage"] = "transported"
    return state


def explicit_root_admission(state):
    state["rootDecision"] = "admit"
    state["canon"] = True
    return state


def buggy_transport_promotes(state):
    state["candidateStage"] = "transported"
    state["canon"] = True
    return state


def canon_has_explicit_decision(state):
    return (not state["canon"]) or state["rootDecision"] == "admit"


INVARIANTS = [
    Invariant(
        "INV-02-no-auto-canon",
        canon_has_explicit_decision,
        "CANON state requires an explicit modeled root-admission decision.",
    )
]

SAFE_TRANSITIONS = [
    Transition("test-candidate", lambda s: s["candidateStage"] == "draft", test_candidate),
    Transition(
        "transport-candidate",
        lambda s: s["candidateStage"] in {"draft", "tested"},
        transport_candidate,
    ),
    Transition(
        "explicit-root-admission",
        lambda s: s["candidateStage"] in {"tested", "transported"} and not s["canon"],
        explicit_root_admission,
    ),
]

FAULT_TRANSITIONS = SAFE_TRANSITIONS + [
    Transition(
        "FAULT-transport-promotes-canon",
        lambda s: s["candidateStage"] == "tested" and not s["canon"],
        buggy_transport_promotes,
    )
]
