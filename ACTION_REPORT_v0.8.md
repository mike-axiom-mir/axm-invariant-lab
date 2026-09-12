# AXM Invariant Lab — Action Report v0.8

## Question

Can the lab close the v0.7 fidelity gap by deriving a required wake from independent executable donor observation, without copying donor scheduling logic or trusting the donor's `necessary_check_ids` / missed-wakeup oracle fields?

## Pre-run state

- `main`: `8dbcf37c55d86fe9778628764de1505c10bbb491`.
- Open PRs before claim: none.
- Historical branches were previous merged growth lanes; no semantic overlap for Wakeup Fuzzer runtime-observation refinement was found.
- Latest pre-run `main` workflow `34695361273`: SUCCESS.
- `RESEARCH_SEED_v0.1.md` remains provenance and evidence-ladder guidance, not a research-only restriction.
- General bounded exploration/model fidelity remained rung 5; packet/result consumption remained rung 6.

## Chosen bounded advance

Use AXM State Research experiment `03-wakeup-fuzzer`, not another search engine, solver, consumer, or generic framework.

Pinned donor evidence:

- repository `mike-axiom-mir/axm-state-research`;
- commit `cf891d3614d472b1426fbdc4304e4e9fe290fb24`;
- minimized `counterexample.json` blob `2598facfdf681a60aa5a25f083818b143b5cee8b`;
- `fuzz_transitions_100.jsonl` blob `79cd00c865e9d21a211fd132dff4679182378795`.

The donor's observed-read scheduler is runtime instrumentation. Its own architecture explicitly warns that cold observation can miss branch-dependent dependencies and that dynamic/external reads and concurrency require stronger evidence. The lab preserves those limits.

## New invariant

**INV-14**

> When runtime-observed activation identifies a check omitted by declared sparse routing, and that check produces an output change that appears in the sparse mismatch set, sparse oracle-equivalence must be rejected for that transition.

## Independent derivation boundary

The v0.8 projection explicitly excludes donor fields:

`necessary`, `necessary_count`, `necessary_hash`, `missed`, `missed_wakes`.

For the minimized broken mutation `f001 = 80`, Invariant Lab derives:

- observed-only awakened IDs = `check_00000`;
- observed-only changed IDs = `check_00000`;
- sparse mismatch IDs = `check_00000`.

The three runtime signals converge on the same omitted wake. Declared sparse reports output non-equivalence while observed-read execution reports equivalence with no mismatch.

Four separate repaired donor transitions are also pinned from the 100-transition execution record. For each transition, `full_scan`, `declared_sparse`, and `observed` agree on mutation identity, changed-output count/hash, final output hash, and empty mismatch lists.

## Implementation

Added:

- `adapters/state_research_wakeup_fuzzer.py`;
- `fixtures/state-research-wakeup-fuzzer-v1.projection.json`;
- `tests/test_state_research_wakeup_fuzzer.py`;
- `tools/run_state_research_wakeup_fuzzer_refinement.py`;
- `evidence/STATE_RESEARCH_WAKEUP_FUZZER_REFINEMENT.json`;
- `STATE_RESEARCH_WAKEUP_FUZZER_REFINEMENT.md`;
- INV-14 vocabulary entry;
- CI/evidence gate, README boundary, and AXM module discovery entry.

## Evidence

Focused local v0.8 adapter gate before publication: **7/7 PASS**.

Deterministic v0.8 evidence regeneration/check: **PASS**.

Exact source-head hosted push evidence on implementation head `144e6ffdae352ad9acb5e8323ff6561d495bae75`, workflow run `34697862432`:

- checkout confirmed exact branch head `144e6ffdae352ad9acb5e8323ff6561d495bae75`;
- Python 3.11 job: SUCCESS;
- Python 3.13 job: SUCCESS;
- repository unit/refinement suite: **42/42 PASS** on Python 3.11;
- deterministic primary evidence: PASS;
- cross-implementation evidence: **8 cases match**;
- Monolith refinement: PASS;
- tractability boundary: PASS;
- two-consumer continuity: PASS;
- State Research Sentinel refinement: PASS;
- new State Research Wakeup Fuzzer runtime-observation refinement: PASS.

PR integration workflow `34697874814` also completed SUCCESS on both Python versions against GitHub's generated merge ref for PR #9. It is integration evidence, not mislabeled as source-head checkout evidence.

## Evidence promotion decision

A new reusable narrow capability is justified and declared as `invariant.refinement.state-research-wakeup-fuzzer` with evidence status `pinned_runtime_observation_triangulated`.

**No general evidence-rung promotion.**

Why:

- the omitted wake is no longer derived from donor `necessary` / `missed` fields;
- but the observed-read scheduler remains donor instrumentation;
- observed reads are explicitly not proven complete for unseen branches, dynamic/external reads, or concurrency;
- one minimized broken trace and four repaired transitions are refined here;
- Invariant Lab does not execute or reconstruct the donor scheduler/checks;
- no solver or real-environment proof is claimed.

Therefore packet/result external consumption remains seed rung 6, while bounded exploration/general model fidelity remains seed rung 5.

## Root check

**Truth:** exact donor commit/path/blob identities, selected lines, excluded oracle fields, derived sets, exact source-head CI, and evidence ceiling are explicit. Missing required evidence HOLDs.

**Agency / non-domination:** adapter is read-only and grants no donor, execution, merge, install, network, or CANON authority.

**Continuity:** v0.7 remains intact as a distinct oracle-field refinement; no earlier evidence class is silently rewritten or promoted.

**Wisdom before speed:** one falsifiable runtime-observation relation was preferred over adding a solver, universal model, duplicate donor runtime, or more consumers without a concrete evidence need.

## Limitations and next useful frontier

This does not prove the Wakeup Fuzzer observed-read mechanism is complete. A stronger next step would need either bounded instrumentation whose completeness can itself be established for an executable donor surface, or a materially different independent observation mechanism deriving the same dependency relation. Merely adding more transitions from the same instrumentation would increase sample quantity but not the evidence class.

If that stronger boundary cannot be grounded without recreating donor implementation semantics inside Invariant Lab, HOLD is preferable to more machinery.
