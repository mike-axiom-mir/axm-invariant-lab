"""Independent Z3 encoding for bounded INV-03 rollback continuity.

This module does not import the authored rollback transition functions. It
restates a tiny rollback/checkpoint relation symbolically so Z3 can challenge
both the wrong-target fault and the stale-receipt lifecycle fault independently
of the primary Python transition execution path.
"""

from __future__ import annotations

from dataclasses import dataclass

from z3 import And, Bool, Int, Not, Or, Solver, sat


S0 = 0
S1 = 1
S2 = 2
S9 = 9

MUTATE_S1 = 0
CHECKPOINT_S1 = 1
MUTATE_S2 = 2
ROLLBACK_S1 = 3
FAULT_WRONG_TARGET = 4
FAULT_STALE_RECEIPT = 5

ACTION_NAMES = {
    MUTATE_S1: "mutate-S0-to-S1",
    CHECKPOINT_S1: "checkpoint-S1",
    MUTATE_S2: "mutate-S1-to-S2",
    ROLLBACK_S1: "rollback-to-S1",
    FAULT_WRONG_TARGET: "FAULT-rollback-reports-S1-but-restores-S9",
    FAULT_STALE_RECEIPT: "FAULT-forward-mutation-keeps-stale-rollback-receipt",
}

FAULT_MODES = {"none", "wrong-target", "stale-receipt"}


@dataclass(frozen=True)
class SolverResult:
    status: str
    witness_depth: int | None
    trace: tuple[str, ...]


def _solver_for_exact_depth(depth: int, *, fault_mode: str) -> tuple[Solver, list[Int]]:
    if depth < 0:
        raise ValueError("depth must be >= 0")
    if fault_mode not in FAULT_MODES:
        raise ValueError(f"unsupported fault_mode: {fault_mode}")

    current = [Int(f"current_{index}") for index in range(depth + 1)]
    known_good_s1 = [Bool(f"known_good_s1_{index}") for index in range(depth + 1)]
    history_s1 = [Bool(f"history_s1_{index}") for index in range(depth + 1)]
    receipt_active = [Bool(f"receipt_active_{index}") for index in range(depth + 1)]
    receipt_target_s1 = [Bool(f"receipt_target_s1_{index}") for index in range(depth + 1)]
    actions = [Int(f"action_{index}") for index in range(depth)]

    solver = Solver()
    solver.add(
        current[0] == S0,
        Not(known_good_s1[0]),
        Not(history_s1[0]),
        Not(receipt_active[0]),
        Not(receipt_target_s1[0]),
    )

    for index, action in enumerate(actions):
        branches = [
            And(
                action == MUTATE_S1,
                current[index] == S0,
                current[index + 1] == S1,
                known_good_s1[index + 1] == known_good_s1[index],
                history_s1[index + 1],
                receipt_active[index + 1] == receipt_active[index],
                receipt_target_s1[index + 1] == receipt_target_s1[index],
            ),
            And(
                action == CHECKPOINT_S1,
                current[index] == S1,
                Not(known_good_s1[index]),
                current[index + 1] == current[index],
                known_good_s1[index + 1],
                history_s1[index + 1] == history_s1[index],
                receipt_active[index + 1] == receipt_active[index],
                receipt_target_s1[index + 1] == receipt_target_s1[index],
            ),
            And(
                action == MUTATE_S2,
                current[index] == S1,
                current[index + 1] == S2,
                known_good_s1[index + 1] == known_good_s1[index],
                history_s1[index + 1] == history_s1[index],
                Not(receipt_active[index + 1]),
                Not(receipt_target_s1[index + 1]),
            ),
            And(
                action == ROLLBACK_S1,
                current[index] == S2,
                known_good_s1[index],
                current[index + 1] == S1,
                known_good_s1[index + 1] == known_good_s1[index],
                history_s1[index + 1] == history_s1[index],
                receipt_active[index + 1],
                receipt_target_s1[index + 1],
            ),
        ]

        if fault_mode == "wrong-target":
            branches.append(
                And(
                    action == FAULT_WRONG_TARGET,
                    current[index] == S2,
                    known_good_s1[index],
                    current[index + 1] == S9,
                    known_good_s1[index + 1] == known_good_s1[index],
                    history_s1[index + 1] == history_s1[index],
                    receipt_active[index + 1],
                    receipt_target_s1[index + 1],
                )
            )
        elif fault_mode == "stale-receipt":
            branches.append(
                And(
                    action == FAULT_STALE_RECEIPT,
                    current[index] == S1,
                    receipt_active[index],
                    current[index + 1] == S2,
                    known_good_s1[index + 1] == known_good_s1[index],
                    history_s1[index + 1] == history_s1[index],
                    receipt_active[index + 1] == receipt_active[index],
                    receipt_target_s1[index + 1] == receipt_target_s1[index],
                )
            )

        solver.add(Or(*branches))

    violation = And(
        receipt_active[depth],
        Or(
            Not(receipt_target_s1[depth]),
            current[depth] != S1,
            Not(known_good_s1[depth]),
            Not(history_s1[depth]),
        ),
    )
    solver.add(violation)
    return solver, actions


def solve_case(*, fault_mode: str, max_depth: int) -> SolverResult:
    """Search the shortest exact-depth INV-03 counterexample up to ``max_depth``."""
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")
    if fault_mode not in FAULT_MODES:
        raise ValueError(f"unsupported fault_mode: {fault_mode}")

    for depth in range(max_depth + 1):
        solver, actions = _solver_for_exact_depth(depth, fault_mode=fault_mode)
        if solver.check() != sat:
            continue
        model = solver.model()
        trace = tuple(ACTION_NAMES[model.eval(action).as_long()] for action in actions)
        return SolverResult(status="FAIL", witness_depth=depth, trace=trace)

    return SolverResult(status="PASS", witness_depth=None, trace=())
