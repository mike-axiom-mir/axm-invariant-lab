"""Independent Z3 encoding for the bounded INV-01 authority model.

This module intentionally does not import or call the repository's authored
Transition guards/apply functions. It restates the tiny three-boolean transition
relation symbolically so a mature SMT solver can challenge the primary explorer
through a materially different execution mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass

from z3 import And, Bool, Int, Not, Or, Solver, sat


PROPOSE = 0
GRANT = 1
FAULT_INHERIT = 2
ACTION_NAMES = {
    PROPOSE: "propose-write-candidate",
    GRANT: "explicitly-grant-write",
    FAULT_INHERIT: "FAULT-inherit-candidate-authority",
}


@dataclass(frozen=True)
class SolverResult:
    status: str
    witness_depth: int | None
    trace: tuple[str, ...]


def _solver_for_exact_depth(depth: int, *, include_fault: bool) -> tuple[Solver, list[Int]]:
    if depth < 0:
        raise ValueError("depth must be >= 0")

    candidate = [Bool(f"candidate_{index}") for index in range(depth + 1)]
    granted = [Bool(f"granted_{index}") for index in range(depth + 1)]
    write_authority = [Bool(f"write_authority_{index}") for index in range(depth + 1)]
    actions = [Int(f"action_{index}") for index in range(depth)]

    solver = Solver()
    solver.add(Not(candidate[0]), Not(granted[0]), Not(write_authority[0]))

    for index, action in enumerate(actions):
        branches = [
            And(
                action == PROPOSE,
                Not(candidate[index]),
                candidate[index + 1],
                granted[index + 1] == granted[index],
                write_authority[index + 1] == write_authority[index],
            ),
            And(
                action == GRANT,
                Not(granted[index]),
                candidate[index + 1] == candidate[index],
                granted[index + 1],
                write_authority[index + 1],
            ),
        ]
        if include_fault:
            branches.append(
                And(
                    action == FAULT_INHERIT,
                    candidate[index],
                    Not(write_authority[index]),
                    candidate[index + 1] == candidate[index],
                    granted[index + 1] == granted[index],
                    write_authority[index + 1],
                )
            )
        solver.add(Or(*branches))

    # INV-01 reduced to the only non-baseline capability in this model:
    # write authority may exist only after an explicit write grant.
    solver.add(And(write_authority[depth], Not(granted[depth])))
    return solver, actions


def solve_case(*, include_fault: bool, max_depth: int) -> SolverResult:
    """Search shortest exact-depth counterexample up to ``max_depth``."""
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    for depth in range(max_depth + 1):
        solver, actions = _solver_for_exact_depth(depth, include_fault=include_fault)
        if solver.check() != sat:
            continue
        model = solver.model()
        trace = tuple(ACTION_NAMES[model.eval(action).as_long()] for action in actions)
        return SolverResult(status="FAIL", witness_depth=depth, trace=trace)

    return SolverResult(status="PASS", witness_depth=None, trace=())
