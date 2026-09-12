"""Cross-repo transport model: data may move without authority silently moving with it."""

from src.bounded_explorer import Invariant, Transition

MAX_DEPTH = 3
LIMITATIONS = [
    "small fixed field vocabulary",
    "no package manager or executable loading",
    "fault transition is synthetic",
]


def initial_state():
    return {
        "donor": {
            "payload": "capability-description",
            "sourceId": "donor:A",
            "authority": {"merge": False, "canon": False},
        },
        "consumer": {
            "payload": None,
            "sourceId": None,
            "authority": {"merge": False, "canon": False},
        },
        "explicitAuthorityGrant": False,
    }


def copy_allowlisted_fields(state):
    state["consumer"]["payload"] = state["donor"]["payload"]
    state["consumer"]["sourceId"] = state["donor"]["sourceId"]
    return state


def explicit_authority_grant(state):
    state["explicitAuthorityGrant"] = True
    state["consumer"]["authority"]["merge"] = True
    return state


def buggy_copy_everything(state):
    state["consumer"] = {
        "payload": state["donor"]["payload"],
        "sourceId": state["donor"]["sourceId"],
        "authority": {"merge": True, "canon": True},
    }
    return state


def authority_not_inherited_silently(state):
    auth = state["consumer"]["authority"]
    if state["explicitAuthorityGrant"]:
        return auth["canon"] is False
    return auth["merge"] is False and auth["canon"] is False


INVARIANTS = [
    Invariant(
        "INV-04-selective-inheritance-excludes-authority",
        authority_not_inherited_silently,
        "Transported donor fields must not silently inherit merge/CANON authority.",
    )
]

SAFE_TRANSITIONS = [
    Transition(
        "copy-allowlisted-donor-fields",
        lambda s: s["consumer"]["payload"] is None,
        copy_allowlisted_fields,
    ),
    Transition(
        "explicit-limited-merge-grant",
        lambda s: s["consumer"]["payload"] is not None and not s["explicitAuthorityGrant"],
        explicit_authority_grant,
    ),
]

FAULT_TRANSITIONS = SAFE_TRANSITIONS + [
    Transition(
        "FAULT-copy-donor-with-authority",
        lambda s: s["consumer"]["payload"] is None,
        buggy_copy_everything,
    )
]
