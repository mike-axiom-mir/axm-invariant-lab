# Action Report v2.5 — Monolith native-route evolution refinement

## Question tested

Does INV-20 still hold after AXM Monolith evolved beyond the earlier connected-package/finalization implementation into a broader learned native-command route layer?

## Starting state inspected

- Invariant Lab `main`: `33e1075d361e869b6be712c86467a36fd5e4ae0c`
- latest semantic INV-20 lane already merged through v2.4
- later public-checkpoint release changed release plumbing only, not invariant semantics
- open Invariant Lab PRs at activation: none
- current Monolith `main`: `8ce73a54d488805b126fe7fa64eac1ec2b28e900`
- current Monolith change explicitly retained additional factual-space native smoke routes

Semantic-overlap decision: **EXTEND INV-20**. Do not create INV-21 and do not add another large endpoint model.

## Exact delta

Added one pinned evolution refinement that:

1. pins the current Monolith donor commit plus the native-smoke tool/test blobs;
2. executes the donor's own native-route planning logic against a synthetic fabric containing all 15 retained exact-ref recipes;
3. requires every route to be `READY` but `executed: false` in plan mode;
4. changes the first route's producer commit and requires HOLD;
5. removes verified native-command evidence and requires HOLD;
6. removes the endpoint and requires HOLD;
7. preserves the donor truth boundary that copied-workspace smoke success is not CANON or product acceptance; and
8. emits a no-authority PASS/FAIL/HOLD refinement receipt.

Added 11 focused adversarial tests covering schema/missing-evidence HOLD, donor provenance drift, silent execution during planning, changed-ref fail-open behavior, unverified-route fail-open behavior, missing-endpoint fail-open behavior, recipe identity drift, authority escalation, and truth-boundary erosion.

## Local evidence before publication

- focused new adapter suite: **11/11 PASS**
- adapter, runner, and focused test Python compilation: **PASS**
- direct current-donor checkout cannot run locally because this execution environment cannot resolve GitHub; exact donor checkout and donor-owned execution are therefore hosted-CI gates

## Four-root gate

**Truth:** route eligibility is tied to exact endpoint + producer ref + retained verified native-command evidence. READY is not execution. Unknown/future observation shapes HOLD.

**Agency / non-domination:** the probe never takes the donor execution path and the refinement grants no execution, merge, promotion, or CANON authority.

**Continuity:** INV-20 is extended in place and all earlier receipt/archive/finalization evidence remains retained. The current donor is pinned by exact commit and blob identities.

**Wisdom before speed:** the experiment uses the donor's 15 retained routes and three falsifiers rather than attempting to model the rapidly growing Monolith totality.

## Evidence ceiling

If hosted CI passes, this establishes that INV-20's non-promotion boundary survives one materially evolved Monolith native-route planning implementation. It does not prove source-command success, product behavior, arbitrary native routes, future donor commits, deployment, safety/quality, or constitutional authority. General model fidelity remains at the existing evidence ceiling.
