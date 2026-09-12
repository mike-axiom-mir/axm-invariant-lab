# State Research Cross-Version Opaque Recovery Refinement

## Status

Working experimental refinement capability. Not CANON. No execution, merge, installation, device, network, or constitutional authority is granted by this result.

## Question

When an opaque deterministic evaluator keeps the same public contract but its source identity changes—or the current source is unavailable—what evidence is sufficient to keep presenting its result as resolved?

## Pinned donor boundary

Repository: `mike-axiom-mir/axm-state-research`

Pinned commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`

Pinned evidence:

- `experiments/07-cross-version-opaque-recovery-challenge/results/raw/benchmark_results.json`
  - Git blob: `748f8d4c232cbe1952800c904ba69f9b3158acb9`
- `experiments/07-cross-version-opaque-recovery-challenge/results/raw/provenance_receipts.jsonl`
  - Git blob: `b5a771bbc6682e4042608442e9b13653e499face`
- `experiments/07-cross-version-opaque-recovery-challenge/FINAL_REPORT.md`
  - Git blob: `d263438ed7e021fb2cd228b462486bf561e78bbb`
- `experiments/07-cross-version-opaque-recovery-challenge/ARCHITECTURE.md`
  - Git blob: `2768bd92f74e6285fed68bd14e9ba4bd06c26b9a`

The frozen held-out manifest SHA-256 is `976e4bd3153ff2cc9201417f19e5d33e8f2eeff00f778f203e7b34e49e25d188`.

## INV-17

> Opaque evaluator results/checkpoints must not cross evaluator-source identity changes as if semantics were unchanged. Changed available source needs grounded re-execution or separately established compatibility evidence; unavailable source keeps affected outputs explicitly unresolved and escalated rather than reconstructing unknown semantics.

This is deliberately narrower than a general code-version theorem. It is a refinement over one frozen two-version synthetic donor challenge.

## Mechanical projection

The fixture does not execute or copy the donor evaluator, router, scoring oracle, or hidden dependency. It projects only:

- held-out challenge identity and frozen gate size;
- comparison-policy outcome counters that retain concrete failures;
- the selected `VERSION_AWARE_BOUNDED` outcome/work counters;
- per-version source availability/change, checkpoint case, coverage, wrong-result count, unresolved IDs, and work;
- candidate checkpoint-validation receipts for the source-hash mismatch and absent checkpoint;
- the seven v3 `retain_unresolved_and_escalate` receipts over the initial snapshot plus six transitions.

The projection explicitly excludes scoring-oracle answers, opaque evaluator source/code, any inferred hidden dependency path, and host timing measurements.

## Result

On the exact pinned donor evidence:

- `BROKEN_SPARSE` produces **6 wrong resolved outputs** and performs **1 untrusted checkpoint replay**;
- `OBSERVED_ONLY` and `STRUCTURAL_ONLY` each produce **4 wrong resolved outputs** even though they quarantine the invalid checkpoint;
- `VERSION_AWARE_BOUNDED` produces **0 wrong resolved outputs**, **0 false abstentions**, **0 untrusted checkpoint replays**, and resolves **91.6667%** of decisions with **41** counted operations versus **168** full-oracle executions;
- for v2, current source is available but changed from training; the v1-bound checkpoint is quarantined for `evaluator_source_hash_mismatch`, and bounded changed-source execution leaves **0 wrong resolved outputs** and **0 final unresolved nodes**;
- for v3, current source is unavailable and the checkpoint is absent; the candidate does not invent semantics. `opaque-guard` and `safety-summary` remain unresolved, and seven provenance receipts retain and escalate that uncertainty across the initial state plus all six transitions;
- `ABSTAIN_ALL` demonstrates the other failure extreme: zero wrong resolved outputs by resolving nothing, producing **154 false abstentions**.

Missing required evidence becomes HOLD. Identity drift, loss of the retained failure controls, stale replay permission, wrong resolved candidate output, disappearing source-version change, fabricated v3 resolution, missing escalation, or loss of the bounded-work relation becomes FAIL.

## Evidence ceiling

This result does **not** promote general model fidelity beyond seed rung 5 / CROSS-IMPLEMENTATION.

The donor offline oracle still scores correctness and false abstention. The worlds, evaluator versions, and source-unavailability condition are synthetic controlled fixtures. Invariant Lab does not execute the donor evaluator, discover the hidden v2 dependency, prove source hashes sufficient semantic identities in general, prove the candidate efficient at scale, or show that unavailable real-world code can be reconstructed.

The useful advance is narrower: source identity is now carried as explicit semantic provenance in a falsifiable refinement, and missing semantics are treated as an unresolved boundary rather than silently guessed from state or stale checkpoints.

## Four-root merge boundary

- **Truth:** changed/missing evaluator semantics remain visible; zero wrong-resolved output is not confused with full knowledge or general proof.
- **Agency / non-domination:** the adapter is read-only and grants no execution or authority.
- **Continuity:** donor repository, commit, file/blob identities, version state, checkpoint reason, and escalation receipts remain explicit.
- **Wisdom before speed:** one frozen challenge is refined instead of recreating opaque execution or building a generic versioning framework.
