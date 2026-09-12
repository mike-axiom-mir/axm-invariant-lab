"""Tiny authority model with optional synthetic fault injection."""

from copy import deepcopy
from src.bounded_explorer import Invariant, Transition

MAX_DEPTH = 3
LIMITATIONS = [
    "abstract single actor",
    "authority is a small string set, not a real permission system",
    "fault transition is synthetic and is not a claim about a donor repository",
]


def initial_state():
    return {
        "actor": "worker",
        "baselineAuthority": ["observe"],
        "explicitGrants": [],
        "candidate": None,
        "authority": ["observe"],
    }


def _sorted(values):
    return sorted(set(values))


def propose_write(state):
    state["candidate"] = {"capability": "write", "stage": "tested"}
    return state


def explicit_grant(state):
    state["explicitGrants"] = _sorted(state["explicitGrants"] + ["write"])
    state["authority"] = _sorted(state["authority"] + ["write"])
    return state


def buggy_inherit_candidate(state):
    state["authority"] = _sorted(
        state["authority"] + [state["candidate"]["capability"]]
    )
    return state


def allowed_authority(state):
    allowed = set(state["baselineAuthority"]) | set(state["explicitGrants"])
    return set(state["authority"]).issubset(allowed)


INVARIANTS = [
    Invariant(
        name="INV-01-no-silent-authority-escalation",
        predicate=allowed_authority,
        description="Runtime authority must be a subset of baseline authority plus explicit grants.",
    )
]

SAFE_TRANSITIONS = [
    Transition("propose-write-candidate", lambda s: s["candidate"] is None, propose_write),
    Transition(
        "explicitly-grant-write",
        lambda s: "write" not in s["explicitGrants"],
        explicit_grant,
    ),
]

FAULT_TRANSITIONS = SAFE_TRANSITIONS + [
    Transition(
        "FAULT-inherit-candidate-authority",
        lambda s: s["candidate"] is not None and "write" not in s["authority"],
        buggy_inherit_candidate,
    )
]
