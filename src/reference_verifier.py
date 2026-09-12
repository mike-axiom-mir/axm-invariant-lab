"""Independent bounded path enumerator for cross-checking the primary explorer.

This verifier deliberately does not import or call ``explore`` and does not prune
revisited states. It enumerates legal paths up to the same declared depth, then
compares only bounded observable claims such as PASS/FAIL/HOLD and the set of
reachable JSON-shaped states. It shares the model transition/predicate functions,
so agreement cross-checks exploration semantics, not the correctness of the model.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Mapping

State = Mapping[str, Any]


def _state_key(state: State) -> str:
    return json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _state_digest(keys: set[str]) -> str:
    payload = "\n".join(sorted(keys)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class ReferenceResult:
    status: str
    complete: bool
    max_depth: int
    unique_states: int
    path_nodes: int
    path_transitions: int
    failing_invariants: tuple[str, ...]
    unknown_invariants: tuple[str, ...]
    reachable_state_digest: str
    budget: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "complete": self.complete,
            "maxDepth": self.max_depth,
            "uniqueStates": self.unique_states,
            "pathNodes": self.path_nodes,
            "pathTransitions": self.path_transitions,
            "failingInvariants": list(self.failing_invariants),
            "unknownInvariants": list(self.unknown_invariants),
            "reachableStateDigest": self.reachable_state_digest,
            "pathNodeBudget": self.budget,
        }


def verify_paths(
    initial_state: State,
    transitions: Iterable[Any],
    invariants: Iterable[Any],
    *,
    max_depth: int,
    max_path_nodes: int = 100_000,
) -> ReferenceResult:
    """Enumerate every legal path up to ``max_depth`` without state de-duplication.

    The node budget is an explicit tractability guard. If the budget prevents full
    enumeration, PASS is forbidden and the result becomes HOLD unless a concrete
    modeled invariant failure was already observed.
    """
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")
    if max_path_nodes < 1:
        raise ValueError("max_path_nodes must be >= 1")

    transitions = tuple(transitions)
    invariants = tuple(invariants)
    stack: list[tuple[dict[str, Any], int]] = [(deepcopy(dict(initial_state)), 0)]
    state_keys: set[str] = set()
    failing: set[str] = set()
    unknown: set[str] = set()
    path_nodes = 0
    path_transitions = 0

    while stack and path_nodes < max_path_nodes:
        state, depth = stack.pop()
        path_nodes += 1
        state_keys.add(_state_key(state))

        for invariant in invariants:
            outcome = invariant.predicate(state)
            if outcome is False:
                failing.add(str(invariant.name))
            elif outcome is None:
                unknown.add(str(invariant.name))

        if depth >= max_depth:
            continue

        successors: list[dict[str, Any]] = []
        for transition in transitions:
            if not transition.guard(state):
                continue
            path_transitions += 1
            next_state = transition.apply(deepcopy(state))
            if not isinstance(next_state, dict):
                raise TypeError(f"transition {transition.name!r} must return dict state")
            successors.append(next_state)

        # Reverse so authored transition order remains stable under a LIFO stack.
        for next_state in reversed(successors):
            stack.append((next_state, depth + 1))

    complete = not stack
    if failing:
        status = "FAIL"
    elif unknown or not complete:
        status = "HOLD"
    else:
        status = "PASS"

    return ReferenceResult(
        status=status,
        complete=complete,
        max_depth=max_depth,
        unique_states=len(state_keys),
        path_nodes=path_nodes,
        path_transitions=path_transitions,
        failing_invariants=tuple(sorted(failing)),
        unknown_invariants=tuple(sorted(unknown)),
        reachable_state_digest=_state_digest(state_keys),
        budget=max_path_nodes,
    )
