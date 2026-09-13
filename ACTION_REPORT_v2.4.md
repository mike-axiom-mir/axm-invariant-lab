# Action Report v2.4 — pinned donor-owned Monolith finalization refinement

## Question tested

After INV-20 survived one frozen Connected Monolith package, does the same non-promotion boundary survive the now-published Monolith plumbing/finalization implementation when another repository executes it directly?

## Starting state inspected

- Invariant Lab `main`: `a1a78c1fe27560564b9e5e212ccf9027a0ebabd6`
- latest Invariant Lab `main` workflow: successful on that exact commit
- open Invariant Lab PRs at activation: none
- preserved provenance: `RESEARCH_SEED_v0.1.md`
- existing INV-20 evidence: receipt-level v2.2 plus frozen-archive cross-artifact v2.3

The current Monolith donor was also inspected. `mike-axiom-mir/axm-monolith` had independently advanced to merge commit `9586e1d11af4ef5a475105f4568627c7a5fdb312`, where repository-owned plumbing/finalization, explicit callable execution, execution-ledger evidence, and fail-closed connected packaging were merged. Its exact-main `Assembly unit tests` workflow was successful.

Semantic-overlap decision: **EXTEND INV-20**, do not create another invariant. This is a new evidence class for the same boundary: donor-owned implementation execution rather than another Monolith data projection.

## Exact delta

Added a pinned cross-repository donor-finalization refinement that:

1. verifies the exact Monolith donor commit and five semantic/test blobs;
2. runs the donor's own six connected-finalization tests;
3. constructs a bounded two-callable probe outside the donor repo;
4. observes plumbing with two declarations and zero source-execution claims;
5. confirms packaging fails closed when a required address lacks an execution ledger;
6. explicitly executes only one of the two declared callables;
7. confirms the execution ledger records exactly that one address, not the unrequested second callable;
8. confirms packaging occurs only after required evidence passes and binds only the requested address; and
9. preserves no-execution/no-merge/no-promotion/no-CANON authority in the refinement receipt.

Added nine adversarial Invariant Lab tests covering missing observation HOLD, declaration-to-execution promotion, fail-open required-address packaging, execution-scope leakage, required-set widening, package-boundary promotion, authority escalation, and provenance override.

## Local evidence before publication

- new focused Invariant Lab adapter suite: **9/9 PASS**
- Python syntax compilation for adapter, runner, and focused tests: **PASS**
- direct donor execution was not claimed locally because this environment cannot clone GitHub; the exact donor checkout and execution are therefore a hosted-CI gate, not a local claim

## Donor evidence boundary

The pinned donor finalizer itself states that connected packaging proves package integrity plus only explicitly required workflow/callable evidence and preserves unrelated execution gaps. Its callable ledger separately records exact validated invocation receipts and says accepted evidence does not promote unrelated capabilities or grant merge/CANON authority.

This refinement does not rewrite those semantics; it tests that they remain observable through the published donor implementation.

## Four-root gate

**Truth:** declaration, execution receipt, package requirement, and unrelated callable state remain separate; missing donor observations HOLD and provenance drift FAILs.

**Agency / non-domination:** source execution in the probe requires the donor's explicit `allow_execution=true`; the refinement receipt grants no execution, merge, promotion, or CANON authority.

**Continuity:** INV-20 is extended in place, the frozen v0.3.2 evidence remains retained, the donor is pinned by commit/blob identity, and no donor source is rewritten.

**Wisdom before speed:** one two-callable probe exercises the state transition directly; no attempt is made to model or execute the whole Monolith.

## Evidence ceiling

If hosted CI passes, this establishes a cross-repository executable refinement over one exact published Monolith implementation. It does not prove arbitrary donor commits, arbitrary packages, all runtimes, all candidate pipelines, deployment, safety/quality, or constitutional authority. General model fidelity therefore remains at the existing seed rung rather than being promoted by count or scale alone.
