# AXM State Research Workfloor Sentinel refinement

## Status

**Working bounded refinement capability / one pinned donor execution artifact / not a general State Research proof / no authority transfer.**

This lane tests whether one narrow invariant relation survives contact with execution evidence emitted by a separate AXM implementation.

## Donor provenance

The donor remains authoritative for its own semantics and code:

- repository: `mike-axiom-mir/axm-state-research`
- pinned commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`
- donor artifact: `experiments/02-workfloor-sentinel/results/sentinel_results.json`
- donor Git blob: `c5cb479a4955940b170c735bd5ee9d58bcb9c888`
- donor schema: `axm.workfloor-sentinel-results/v1`

The donor reports a deliberately incomplete dependency map and a repaired run over the same seven designed mutations. In the incomplete run, the mutation `break-output-equivalence-claim` has one necessary check that does not wake: `cross--report-matches-raw-results`. The sparse result diverges from the full oracle. In the repaired run, that check wakes and the sparse result remains oracle-equivalent.

Invariant Lab does **not** copy or reimplement Sentinel's router/check logic.

## INV-13

> Every oracle-required check for a sparse transition must be awakened; a missed required check forbids an oracle-equivalence claim for that step.

This is deliberately narrow. It is a relation over donor-emitted sets and result fields, not a claim that Invariant Lab knows which checks *should* be necessary independently of Sentinel's oracle.

## Mechanical projection

`fixtures/state-research-workfloor-sentinel-v1.projection.json` retains only explicitly named fields from the pinned donor artifact. `projection.field_paths` records every selected source path. Values are copied without semantic normalization.

The adapter independently computes only bounded relations such as:

```text
derived_missed = necessary_check_ids - awakened_check_ids
reported_missed == derived_missed
reported_missed subset_of sparse_output_mismatch_ids
```

It also checks that the bug and repaired projections describe the same mutation/necessary set and final oracle target, while the sparse final hash diverges before repair and converges after repair.

This is a refinement projection, not a replacement donor model.

## Evidence

The retained evidence is `evidence/STATE_RESEARCH_SENTINEL_REFINEMENT.json`.

For the pinned projection:

- refinement status: **PASS**;
- dependency-bug run under INV-13: **FAIL**;
- repaired run under INV-13: **PASS**;
- derived missed check in the bug run: `cross--report-matches-raw-results`;
- source repository/commit/path/blob identity checks: PASS;
- same mutation, necessary set, and final oracle target across bug/repaired projections: PASS;
- bug final sparse hash differs from oracle: PASS;
- repaired final sparse hash equals oracle: PASS.

Adversarial tests also require:

- source identity drift -> FAIL;
- a silent newly missed required wake-up in the repaired projection -> FAIL;
- equivalence contradicting a non-empty mismatch set -> FAIL;
- missing required evidence -> HOLD;
- adapter input remains unchanged.

Run:

```bash
python -m unittest tests.test_state_research_workfloor_sentinel -v
python tools/run_state_research_sentinel_refinement.py --check
```

## Evidence ceiling

This is the first Invariant Lab refinement grounded in an execution-results artifact produced by another AXM runtime rather than only a separately authored contract fixture.

It still does **not** justify promoting bounded exploration/model fidelity above seed rung 5:

- only one pinned donor execution artifact is projected;
- the donor oracle determines the `necessary_check_ids`; Invariant Lab does not independently derive necessity from donor source code;
- the donor run covers seven designed mutations, not all possible State Research changes;
- Invariant Lab does not execute the Workfloor Sentinel runtime here;
- the projection intentionally omits donor fields outside INV-13's narrow relation;
- no solver or real-environment proof is implied.

A future fidelity promotion would need an independent way to derive or observe the required transition relation from executable donor behavior/source and compare it across more than one bounded trace without silently reauthoring donor semantics.

## Authority boundary

This adapter reads evidence and returns PASS/FAIL/HOLD. It does not mutate State Research, repair a dependency map, execute donor checks, merge either repository, install anything, or grant execution/CANON authority. Technical evidence remains subordinate to the four AXM roots: Truth, Agency/non-domination, Continuity, and Wisdom before speed.
