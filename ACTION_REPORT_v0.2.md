# Action report v0.2 — cross-implementation verifier

## Question tested

Can a second, deliberately different bounded-search implementation corroborate the primary explorer's retained tiny-model results without sharing its visited-state pruning logic, and can that second implementation fail closed when exhaustive path enumeration becomes too expensive?

## Starting evidence

Before this run, `main` was at `0f0570266b3e41cd8623e77e32a6025fcad2182f` with no open PRs. The prior push CI completed successfully. The preserved research seed identifies seed evidence rung 5 as **CROSS-IMPLEMENTATION: a second implementation or independent verifier agrees on a bounded claim**.

The existing `axm/v0.1-bounded-invariant-explorer` branch is historical v0.1 work and does not occupy this semantic lane.

## Exact delta

NEW:

- `src/reference_verifier.py`: dependency-free bounded path enumerator;
- no call to the primary `explore(...)` implementation inside the reference verifier;
- no visited-state pruning in the reference algorithm;
- explicit `max_path_nodes` tractability budget;
- incomplete enumeration forbids PASS and returns HOLD unless an actual invariant failure was observed;
- `src/cross_verifier.py`: compares bounded observable claims from both implementations;
- retained `evidence/cross-verification-latest.json` receipt;
- deterministic cross-verification receipt check in CI.

PRESERVED:

- the primary BFS explorer remains the shortest-counterexample implementation;
- donor semantics and model predicates/transitions are unchanged;
- the TruthGrid refinement adapter is unchanged;
- the counterexample packet contract is unchanged;
- the original research seed remains provenance.

## Falsifier

This lane fails if any retained safe/fault tiny-model case disagrees on bounded status, reachable unique-state count, failing invariant names, or unknown invariant names; or if reference budget exhaustion can silently report PASS.

## Evidence result

The retained cross-implementation receipt contains **8/8 AGREE cases**:

- four safe variants: PASS in both implementations;
- four synthetic fault variants: FAIL in both implementations;
- every case agrees on reachable unique-state count;
- every case agrees on failing and unknown invariant names;
- all eight reference enumerations completed inside the declared 100,000 path-node budget.

Focused new tests also verify:

- safe/fault agreement across all four models;
- HOLD agreement for an unknown observation;
- path-budget exhaustion produces HOLD rather than an unearned PASS;
- a concrete observed failure remains FAIL even if later path enumeration is budget-limited.

## Evidence level decision

**Promote only the bounded exploration semantics to seed rung 5 / CROSS-IMPLEMENTATION.**

This promotion does not automatically upgrade every artifact in the repository. In particular, the counterexample packet remains fixture-tested and donor refinement/cross-repo adoption remain below rung 5/6 unless their own evidence advances.

## Critical limitation

The two implementations are algorithmically separate but consume the **same authored transition and invariant functions**. This is an independent check of search/exploration semantics, not an independent formalization of the donor system. A shared model mistake can still make both implementations agree incorrectly about reality.

## Root check

**Truth:** disagreement is explicit; incomplete reference enumeration HOLDs; no proof claim escapes the model boundary.

**Agency / non-domination:** verifier output grants no execution, merge, device, network, promotion, or CANON authority.

**Continuity:** primary explorer, donor adapters, evidence formats, source identity, and research provenance remain intact.

**Wisdom before speed:** this is a small second implementation over existing tiny models, not solver integration or a universal AXM formal model.

## What remains unknown

- whether a separately authored model translation reaches the same result;
- whether a second real AXM repository can consume the invariant/counterexample contract without semantic rewriting;
- tractability beyond the current tiny models;
- whether a mature solver/model checker adds enough value to justify its complexity;
- real-environment correspondence between modeled claims and deployed systems.

## Next evidence frontier

The strongest non-duplicative next step is now **rung 6 / CROSS-REPO** evidence or a separately authored translation/refinement check. Another third search implementation would likely be lower-value churn unless a concrete divergence or tractability problem motivates it.
