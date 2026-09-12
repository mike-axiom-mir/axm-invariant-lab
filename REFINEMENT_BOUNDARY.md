# Refinement boundary v0.1

Formal models and implementation evidence are different layers.

## Direction

`real donor evidence -> bounded adapter observation -> invariant evaluation`

The direction is intentionally one-way. A PASS in this repository does not
rewrite donor state, approve donor code, merge a branch, or become CANON.

## First donor adapter: TruthGrid foundation evidence

The v0.1 adapter reads a bounded extracted fixture from
`axm-TruthGrid/evidence/benchmark-latest.json` and checks only fields the donor
already exposes:

- two-instance equality is explicitly true;
- the final hashes agree with the declared final hash;
- each merge `resultingHash` equals the tick hash;
- each `rollbackRef` names the merge `baseRevision`;
- `resultingRevision` advances exactly one from `baseRevision`.

Missing required evidence produces HOLD. Contradictory evidence produces FAIL.

This does **not** re-run TruthGrid, authenticate its producer, or prove
cross-device determinism. It is a refinement seam between an existing executable
receipt and a small invariant observation.

## Future refinement rule

A new adapter must:

1. pin donor repo/path/version or content identity;
2. use donor-declared fields rather than infer hidden state;
3. preserve unknowns as HOLD;
4. never mutate the donor;
5. state exactly which model predicate the evidence supports;
6. include an adversarial mutation proving the adapter can reject or HOLD a
   malformed/contradictory receipt.
