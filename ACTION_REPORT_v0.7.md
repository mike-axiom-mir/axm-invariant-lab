# AXM Invariant Lab — Action Report v0.7

## Question

Can the lab make a real advance on model-to-implementation fidelity by refining an execution-results artifact emitted by another AXM runtime, without rewriting donor semantics or inflating the evidence rung?

## Pre-run state

- `main`: `f8924f9f5adfd6d2c537cc4e3e228f0797bf9bc5`.
- Open PRs before claim: none.
- Existing historical branches were merged growth lanes; no active semantic overlap for State Research execution-receipt fidelity was found.
- Latest `main` workflow was green.
- `RESEARCH_SEED_v0.1.md` remains provenance, not a research-only restriction.
- Counterexample packet/result external use was already seed rung 6 through Monolith + Profession Mesh.
- Bounded exploration/general model fidelity remained seed rung 5 because both verifiers share authored model functions.

## Chosen bounded advance

Do **not** add a third packet consumer, third search engine, solver, or generic verification layer.

Use AXM State Research Workfloor Sentinel because its donor-owned execution artifact already contains a falsified dependency map and repaired run over the same mutation sequence.

Pinned donor source:

- repository: `mike-axiom-mir/axm-state-research`
- commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`
- artifact: `experiments/02-workfloor-sentinel/results/sentinel_results.json`
- Git blob: `c5cb479a4955940b170c735bd5ee9d58bcb9c888`
- donor schema: `axm.workfloor-sentinel-results/v1`

The donor's own final report states that one missing raw-JSON subscription caused one necessary check to stay asleep, poisoned sparse/oracle equivalence, and that adding the missing subscription reduced missed wake-ups from 1 to 0 across the same seven changes.

## New invariant

**INV-13**

> Every oracle-required check for a sparse transition must be awakened; a missed required check forbids an oracle-equivalence claim for that step.

Formal scope is deliberately limited to explicit donor-emitted wakeup/oracle fields.

## Implementation

Added:

- `adapters/state_research_workfloor_sentinel.py`;
- `fixtures/state-research-workfloor-sentinel-v1.projection.json`;
- `tests/test_state_research_workfloor_sentinel.py`;
- `tools/run_state_research_sentinel_refinement.py`;
- `evidence/STATE_RESEARCH_SENTINEL_REFINEMENT.json`;
- `STATE_RESEARCH_SENTINEL_REFINEMENT.md`;
- INV-13 vocabulary entry;
- AXM module discovery entry and CI gate;
- README status/evidence-boundary update.

The fixture is explicitly a **mechanical field projection**. It lists every selected JSON path and copies values without semantic normalization. The adapter does not reproduce Sentinel checks or router behavior.

The primary independent relation is:

```text
derived_missed = necessary_check_ids - awakened_check_ids
```

For donor sequence 2 / `break-output-equivalence-claim`:

- dependency-bug run: derived miss = `cross--report-matches-raw-results`; INV-13 = FAIL; sparse output mismatch contains the same check; final sparse hash differs from the final oracle hash;
- repaired run: derived miss = empty; INV-13 = PASS; sparse mismatch list empty; final sparse hash equals the same final oracle target.

## Evidence

Focused local adapter tests before publication: **6/6 PASS**.

Hosted PR integration run `34695251282`:

- Python 3.11 job: SUCCESS;
- Python 3.13 job: SUCCESS;
- repository suite: **35/35 PASS** on Python 3.11; Python 3.13 unit/refinement step also SUCCESS;
- deterministic primary evidence: PASS;
- cross-implementation retained evidence: **8 cases match**;
- Monolith refinement evidence: PASS;
- tractability evidence: PASS;
- two-consumer continuity evidence: PASS;
- State Research Sentinel refinement evidence: PASS.

New adversarial coverage proves:

- source identity drift -> FAIL;
- silent newly missed required wake-up -> FAIL;
- equivalence flag contradicting mismatch list -> FAIL;
- missing required donor evidence -> HOLD;
- adapter is read-only.

## Evidence promotion decision

A useful capability is grounded and is exposed as `invariant.refinement.state-research-workfloor`.

**No general evidence-rung promotion.**

Why:

- this is one pinned donor execution-results artifact;
- the donor oracle supplies `necessary_check_ids`;
- Invariant Lab does not independently derive necessity from donor source/runtime behavior;
- the underlying Workfloor experiment covers seven designed mutations;
- the adapter does not execute State Research;
- projection intentionally excludes fields outside INV-13;
- there is no solver or real-environment proof.

Therefore:

- packet/result external consumption remains seed rung 6;
- bounded exploration/general model fidelity remains seed rung 5;
- v0.7 adds a narrower `single_pinned_donor_execution_artifact_refined` evidence class.

## Root check

**Truth:** donor repository, commit, path, blob, schema, exact selected fields, derived relation, and evidence ceiling are explicit. Unknown required evidence HOLDs.

**Agency / non-domination:** adapter is read-only and grants no donor, execution, merge, install, network, or CANON authority.

**Continuity:** existing exploration/packet evidence levels remain unchanged; donor semantics are not replaced; earlier consumers and gates remain green.

**Wisdom before speed:** one falsifiable execution-grounded relation was preferred over adding a solver, universal model, third consumer, or other complexity without a concrete need.

## Limitations

This result does not prove that the Workfloor dependency map is complete for unseen mutations. It does not independently establish which checks should be necessary. It does not prove State Research as a whole, and a donor-reported FAIL is not automatically proof of a donor bug outside the modeled/refined claim.

## Next useful frontier

The strongest remaining fidelity gap is to derive a required transition relation from **independent executable donor observation/source instrumentation**, rather than accepting the donor oracle's `necessary_check_ids`, then compare that independently derived relation with Invariant Lab's model/refinement over more than one bounded trace.

If that cannot be done narrowly without recreating donor logic inside Invariant Lab, HOLD is better than adding more machinery.
