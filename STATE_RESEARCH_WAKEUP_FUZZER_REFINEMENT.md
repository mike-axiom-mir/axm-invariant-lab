# State Research Wakeup Fuzzer refinement

## Scope

This refinement asks one narrow question over pinned donor execution evidence:

> Can a required sparse wake be derived from runtime observation rather than accepted from the donor's `necessary` / `missed` oracle fields?

Pinned donor:

- repository: `mike-axiom-mir/axm-state-research`
- commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`
- minimized counterexample: `experiments/03-wakeup-fuzzer/results/raw/counterexample.json` @ blob `2598facfdf681a60aa5a25f083818b143b5cee8b`
- repaired trace sample: `experiments/03-wakeup-fuzzer/results/raw/fuzz_transitions_100.jsonl` @ blob `79cd00c865e9d21a211fd132dff4679182378795`

The donor architecture says its observed-read scheduler instruments fields read by handlers and that its full-scan oracle executes every check. It also explicitly warns that observed reads are not generally complete for unobserved branches, external/dynamic reads, or concurrency. This refinement preserves that boundary.

## INV-14

> When runtime-observed activation identifies a check omitted by declared sparse routing, and that check produces an output change that appears in the sparse mismatch set, sparse oracle-equivalence must be rejected for that transition.

For the donor's one-mutation minimized counterexample, Invariant Lab does **not** use `necessary`, `necessary_count`, `necessary_hash`, `missed`, or `missed_wakes` to derive the omitted check.

It independently computes three sets from donor-emitted runtime records:

```text
observed-only awakened = observed.awakened - declared_sparse.awakened
observed-only changed  = observed.changed  - declared_sparse.changed
sparse mismatch        = declared_sparse.mismatched_outputs
```

All three equal `{check_00000}`. The sparse scheduler reports non-equivalence while the runtime-observed scheduler converges with no mismatch.

The retained fixture also carries four different repaired transitions from the donor's 100-transition record. For each, the full-scan, declared-sparse, and observed-read records agree on mutation identity, changed-output count/hash, final output hash, and empty mismatch list. These are independent bounded transition observations, not a general proof.

## Truth boundary

This is stronger than v0.7's use of donor-declared necessity because the new derived omitted wake does not consume the donor `necessary` or `missed` fields. It is still not independent proof of all donor dependencies:

- the observed-read scheduler is donor instrumentation;
- cold-start observation can miss branch-dependent reads;
- dynamic/external reads and concurrency remain outside the donor experiment's claim;
- only one minimized broken trace and four retained repaired transitions are refined here;
- Invariant Lab does not execute or reimplement the donor scheduler/checks;
- no general evidence-rung promotion is made.

Therefore bounded exploration/general model fidelity remains seed rung 5. Counterexample-packet external consumption remains separately rung 6.
