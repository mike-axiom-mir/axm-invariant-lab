# AXM Invariant Lab — Action Report v1.7

## Decision

**GROW / first mature formal-tool comparison, no evidence-rung promotion.**

The previous run closed a cross-repository discovery-consumer gap. This run deliberately moves to a different axis from discovery and donor refinement: seed ladder item 6, comparison of the local bounded semantics with a mature formal tool after those semantics have become stable enough to state precisely.

## Bounded advance

Candidate invariant INV-01 is now checked by two materially different mechanisms:

1. the existing dependency-free breadth-first explorer over the authored Python model; and
2. a separately authored Z3 SMT transition relation that does not call the model's Python transition guards/apply functions.

The comparison is intentionally tiny: only `models/no_silent_authority.py`, only the write-capability abstraction, and only depth 0..3. The formal dependency is isolated in `requirements-formal.txt` and does not become a dependency of the normal core/unit lane.

## Expected falsifier

The safe transition set must have no counterexample through depth 3. The synthetic fault transition set must produce the same unique shortest two-step witness in both mechanisms:

`propose-write-candidate -> FAULT-inherit-candidate-authority`

A depth-1 solver search is also retained as a boundary test: it returns no counterexample because the modeled violation genuinely requires two steps. That result is explicitly bounded rather than promoted into a global safety claim.

## Added evidence surface

- `formal/z3_inv01.py` — independent symbolic encoding;
- `formal_tests/test_z3_inv01.py` — dedicated solver tests outside the dependency-free default suite;
- `tools/run_z3_inv01_comparison.py` — deterministic comparison/evidence gate;
- `evidence/z3_inv01_comparison.json` — retained bounded receipt;
- `FORMAL_TOOL_COMPARISON_INV01.md` — exact truth and authority boundary;
- `requirements-formal.txt` — exact `z3-solver==5.1.0.0` pin;
- hosted CI installation/test/evidence stages for Python 3.11 and 3.13.

## Root gate

- **Truth:** Z3 is used only for the exact bounded model stated in the receipt; independent symbolic agreement is not described as donor proof.
- **Agency / non-domination:** the receipt carries explicit false execution/merge/promotion/CANON authority fields.
- **Continuity:** the existing dependency-free engine and tests are unchanged; the external formal dependency is isolated to its own hosted verification stages.
- **Wisdom before speed:** one already-understood invariant is compared first instead of introducing a generic solver DSL or formalizing the whole AXM stack.

## Evidence ceiling

This is stronger verification diversity inside the seed's **rung 5 / CROSS-IMPLEMENTATION** boundary. It does not promote model fidelity to rung 6 because the Z3 relation is still authored in this repository and does not establish that the tiny model faithfully captures a real donor permission system. The existing counterexample packet retains its separate rung-6 external-consumption claim.

This is also not "solver-backed proof" of AXM generally: the solver checks an exact finite transition relation through a declared depth, and a transcription/shared-concept error can still exist in both the Python and symbolic models.

## Next useful frontier

The next formal-tool advance should happen only if a second invariant has semantics different enough to test whether this method generalizes without creating a duplicate modeling layer, or if a real donor implementation can generate an independently checkable symbolic/refinement relation. Otherwise, more Z3 encodings of nearly identical tiny models should HOLD as complexity without a higher evidence class.
