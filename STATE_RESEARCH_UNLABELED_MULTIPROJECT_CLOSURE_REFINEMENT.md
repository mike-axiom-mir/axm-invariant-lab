# State Research Unlabeled Multi-Project Closure Refinement

## Status

Working experimental refinement capability. Not CANON. No execution, merge, installation, device, network, or constitutional authority is granted by this result.

## Question

Does final oracle equality by itself justify a closure claim when a held-out trace contains silent stale outputs, and can the same bounded relation be checked across more than one real AXM project/version while preserving checkpoint trust boundaries?

## Pinned donor boundary

Repository: `mike-axiom-mir/axm-state-research`

Pinned commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`

Pinned evidence:

- `experiments/06-unlabeled-multiproject-closure-challenge/results/raw/benchmark_results.json`
  - Git blob: `f6be4ae9b42e9c2edbb114d2d85ce1c5689660e7`
- `experiments/06-unlabeled-multiproject-closure-challenge/results/raw/checkpoint_receipts.json`
  - Git blob: `541cfe64e15fb580ae575cb38e243ac49ffa9350`
- `experiments/06-unlabeled-multiproject-closure-challenge/FINAL_REPORT.md`
  - Git blob: `316aea1d795acc1c6a503fdac6800bbd60c35782`

The frozen held-out manifest hash is `2d3b07b3f5eaf5bac06c739d7ff3e3ac9a45f71daff757b7c18d37eb601da251`. It contains ten mutations and no declared-risk labels. The two held-out project identities are Workfloor Sentinel v0.1.0 and Adaptive Closure v0.1.0.

## INV-16

> A cross-project closure claim is not supported by final equality alone: every held-out project/version must retain zero silent-stale outputs through the trace, and absent/corrupt checkpoints must be quarantined and reconstructed only from verified source with provenance.

This is deliberately distinct from INV-15. INV-15 retained a minimized held-out observed-read counterexample where final equality itself failed. INV-16 tests a harder failure mode: `OBSERVED_READS` finishes oracle-equal on both held-out projects while still retaining eight silent-stale outputs during the trace.

## Mechanical projection

The fixture does not execute or copy State Research routing code. It projects only explicit donor evidence needed for the relation:

- held-out manifest identity, project identities, mutation count, and unlabeled status;
- `OBSERVED_READS` final equality, silent-stale totals, counterexample count, and per-project trace outcomes;
- `COMBINED_STRUCTURAL_OBSERVED` final equality, silent-stale totals, bounded work counts, and per-project outcomes;
- checkpoint validation and reconstruction receipts for the two held-out projects.

The projection explicitly excludes donor `necessary_wakes`, `missed_wakes`, timing measurements, and the scoring implementation details.

## Result

On the exact pinned donor evidence:

- `OBSERVED_READS` ends with `final_oracle_equality = true` but retains **8 silent-stale outputs**, four on each held-out project, with maximum silent-stale windows of four;
- therefore final equality alone **FAILs INV-16** as a closure criterion;
- the separately selected `COMBINED_STRUCTURAL_OBSERVED` candidate ends equal with **0 silent-stale outputs** on both held-out projects;
- candidate counted check work is **597**, below the held-out full-oracle reference of **1,955** check executions;
- the corrupt Adaptive Closure checkpoint and absent Workfloor Sentinel checkpoint are both marked `quarantined_untrusted` and reconstructed only through `quarantine_then_reconstruct_from_verified_source` with retained source/replacement identities;
- no unresolved checkpoint recovery remains in the selected candidate records.

The retained adapter performs 60 exact checks over this projection. Missing required evidence becomes HOLD; contradictory identity, trace, project-distinctness, work, or checkpoint evidence becomes FAIL.

## Evidence ceiling

This result does **not** promote general model fidelity beyond seed rung 5 / CROSS-IMPLEMENTATION.

The donor offline oracle still decides hidden staleness and equality. Invariant Lab does not independently derive that oracle, execute either donor project, prove the combined policy generally sufficient, or establish behavior under organic histories, concurrency, effectful checks, new project families, or cross-machine checkpoint trust.

The useful advance is narrower: the lab now carries a cross-project, unlabeled, execution-evidence refinement showing that end-state equality can hide transient correctness failures and that checkpoint trust must remain part of the closure claim.

## Four-root merge boundary

- **Truth:** final equality is not promoted over retained transient failures; unknown or missing fields HOLD; donor scoring remains donor scoring.
- **Agency / non-domination:** the adapter is read-only and grants no execution or authority.
- **Continuity:** donor repository, commit, file paths, Git blobs, project identities, and checkpoint provenance remain explicit.
- **Wisdom before speed:** this reuses one frozen two-project challenge rather than creating a larger generic framework or a duplicate State Research implementation.
