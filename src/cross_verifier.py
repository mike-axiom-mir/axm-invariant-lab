"""Cross-implementation agreement checks for tiny AXM invariant models."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Mapping
from src.bounded_explorer import explore
from src.reference_verifier import ReferenceResult, verify_paths

@dataclass(frozen=True)
class CrossVerificationResult:
    status: str
    agreements: dict[str, bool]
    primary: dict[str, Any]
    reference: ReferenceResult
    truth_boundary: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "agreements": dict(sorted(self.agreements.items())),
            "primary": self.primary,
            "reference": self.reference.to_dict(),
            "truthBoundary": self.truth_boundary,
        }

def cross_verify(initial_state: Mapping[str, Any], transitions: Iterable[Any], invariants: Iterable[Any], *, max_depth: int, max_path_nodes: int = 100_000) -> CrossVerificationResult:
    transitions=tuple(transitions); invariants=tuple(invariants)
    primary=explore(initial_state,transitions,invariants,max_depth=max_depth)
    reference=verify_paths(initial_state,transitions,invariants,max_depth=max_depth,max_path_nodes=max_path_nodes)
    primary_failure=sorted({c.invariant for c in primary.counterexamples})
    primary_unknown=sorted({u.invariant for u in primary.unknowns})
    agreements={
        "status": primary.status == reference.status,
        "uniqueStateCount": primary.explored_states == reference.unique_states,
        "failingInvariantNames": primary_failure == list(reference.failing_invariants),
        "unknownInvariantNames": primary_unknown == list(reference.unknown_invariants),
    }
    if not reference.complete:
        status="HOLD"
    elif all(agreements.values()):
        status="AGREE"
    else:
        status="DIVERGE"
    primary_record={
        "status":primary.status,
        "exploredStates":primary.explored_states,
        "exploredTransitions":primary.explored_transitions,
        "failingInvariants":primary_failure,
        "unknownInvariants":primary_unknown,
    }
    return CrossVerificationResult(
        status=status,
        agreements=agreements,
        primary=primary_record,
        reference=reference,
        truth_boundary=("Agreement is between two exploration implementations over the same authored transition and invariant functions. "
                        "It cross-checks bounded exploration semantics; it does not independently validate model fidelity, donor code, or the real world."),
    )
