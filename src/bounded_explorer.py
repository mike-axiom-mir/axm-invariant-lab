"""Dependency-free bounded state exploration for tiny AXM research models."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from collections import deque
from copy import deepcopy
from typing import Any, Callable, Iterable, Mapping
import json

State = Mapping[str, Any]
PredicateResult = bool | None
Guard = Callable[[State], bool]
Apply = Callable[[State], dict[str, Any]]
Predicate = Callable[[State], PredicateResult]


def canonical_state(state: State) -> str:
    """Stable identity for JSON-shaped states."""
    return json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class Transition:
    name: str
    guard: Guard
    apply: Apply


@dataclass(frozen=True)
class Invariant:
    name: str
    predicate: Predicate
    description: str


@dataclass
class TraceStep:
    transition: str
    before: dict[str, Any]
    after: dict[str, Any]


@dataclass
class Counterexample:
    invariant: str
    description: str
    violating_state: dict[str, Any]
    trace: list[TraceStep]

    def to_dict(self) -> dict[str, Any]:
        return {
            "invariant": self.invariant,
            "description": self.description,
            "violatingState": self.violating_state,
            "trace": [asdict(step) for step in self.trace],
            "traceLength": len(self.trace),
        }


@dataclass
class UnknownObservation:
    invariant: str
    state: dict[str, Any]
    trace_length: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "invariant": self.invariant,
            "state": self.state,
            "traceLength": self.trace_length,
        }


@dataclass
class ExplorationResult:
    status: str
    max_depth: int
    explored_states: int
    explored_transitions: int
    counterexamples: list[Counterexample]
    unknowns: list[UnknownObservation]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "maxDepth": self.max_depth,
            "exploredStates": self.explored_states,
            "exploredTransitions": self.explored_transitions,
            "counterexamples": [item.to_dict() for item in self.counterexamples],
            "unknowns": [item.to_dict() for item in self.unknowns],
        }


def _evaluate(
    state: dict[str, Any],
    trace: list[TraceStep],
    invariants: Iterable[Invariant],
    failures: dict[str, Counterexample],
    unknowns: dict[tuple[str, str], UnknownObservation],
) -> None:
    state_key = canonical_state(state)
    for invariant in invariants:
        result = invariant.predicate(state)
        if result is False and invariant.name not in failures:
            failures[invariant.name] = Counterexample(
                invariant=invariant.name,
                description=invariant.description,
                violating_state=deepcopy(state),
                trace=deepcopy(trace),
            )
        elif result is None:
            key = (invariant.name, state_key)
            if key not in unknowns:
                unknowns[key] = UnknownObservation(
                    invariant=invariant.name,
                    state=deepcopy(state),
                    trace_length=len(trace),
                )


def explore(
    initial_state: State,
    transitions: Iterable[Transition],
    invariants: Iterable[Invariant],
    *,
    max_depth: int,
) -> ExplorationResult:
    """Breadth-first exploration; first failure per invariant is shortest by steps."""
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    transitions = tuple(transitions)
    invariants = tuple(invariants)
    initial = deepcopy(dict(initial_state))

    queue = deque([(initial, [])])
    visited = {canonical_state(initial)}
    failures: dict[str, Counterexample] = {}
    unknowns: dict[tuple[str, str], UnknownObservation] = {}
    explored_transitions = 0

    _evaluate(initial, [], invariants, failures, unknowns)

    while queue:
        state, trace = queue.popleft()
        if len(trace) >= max_depth:
            continue

        for transition in transitions:
            if not transition.guard(state):
                continue
            explored_transitions += 1
            next_state = transition.apply(deepcopy(state))
            if not isinstance(next_state, dict):
                raise TypeError(f"transition {transition.name!r} must return dict state")

            step = TraceStep(
                transition=transition.name,
                before=deepcopy(state),
                after=deepcopy(next_state),
            )
            next_trace = trace + [step]
            _evaluate(next_state, next_trace, invariants, failures, unknowns)

            key = canonical_state(next_state)
            if key not in visited:
                visited.add(key)
                queue.append((next_state, next_trace))

    if failures:
        status = "FAIL"
    elif unknowns:
        status = "HOLD"
    else:
        status = "PASS"

    ordered_failures = sorted(
        failures.values(),
        key=lambda item: (len(item.trace), item.invariant),
    )
    ordered_unknowns = sorted(
        unknowns.values(),
        key=lambda item: (item.trace_length, item.invariant, canonical_state(item.state)),
    )

    return ExplorationResult(
        status=status,
        max_depth=max_depth,
        explored_states=len(visited),
        explored_transitions=explored_transitions,
        counterexamples=ordered_failures,
        unknowns=ordered_unknowns,
    )
