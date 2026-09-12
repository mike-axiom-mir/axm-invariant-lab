# Invariant contract v0.1

## Vocabulary

**State** — a finite JSON-shaped observation used by one model.

**Transition** — a named state-to-state operation with an explicit precondition.

**Invariant** — a predicate that must hold for every reachable modeled state.

**Unknown** — a predicate result that cannot be decided from the available
state/evidence. Unknown is represented as `None` and produces HOLD, never PASS.

**Counterexample** — the shortest trace found by breadth-first exploration from
the declared initial state to a state that violates one invariant.

**Bound** — the maximum transition depth explored. A bounded PASS is not a
general proof.

## Required model contract

Every model must declare:

1. one explicit initial state;
2. a finite transition set;
3. at least one invariant;
4. an exploration depth;
5. what the model leaves out;
6. whether fault-injection transitions are synthetic.

Transitions must be deterministic for the same input state. Models may not
perform network, filesystem, device, merge, release, installation, or CANON
actions.

## Result semantics

- `PASS`: every evaluated reachable state satisfied every invariant and no
  unknown evaluation occurred inside the bound.
- `FAIL`: at least one invariant was false. The result includes a shortest
  counterexample trace.
- `HOLD`: no invariant was false, but at least one evaluation was unknown.

Priority is `FAIL > HOLD > PASS`.

## Root boundary

The four AXM roots remain constitutional merge gates. This repository may model
concrete observable consequences derived from them, but does not reduce the
meaning of Truth, Agency/non-domination, Continuity, or Wisdom-before-speed to a
boolean formula.

Technical execution permission is not constitutional authority.

## Evidence ceiling

A model result proves only its exact bounded claim. It cannot silently promote a
candidate, donor result, branch, PR, package, machine, person, or AI output to
CANON.
