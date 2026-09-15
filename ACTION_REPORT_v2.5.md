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

## First hosted run — retained failure, not hidden

PR workflow run `34940130786` was red on the initial published head `d364495b50925ea5b960df277a94aed2636f916d`.

What passed before the red gate:

- complete repository unit/refinement suite: **183/183 PASS** on Python 3.11;
- all inherited evidence gates through INV-20 v2.4: PASS;
- checkout of exact current Monolith donor `8ce73a54d488805b126fe7fa64eac1ec2b28e900`: PASS;
- donor-owned `tests/test_totality_native_smokes.py`: **10/10 PASS**.

The new evidence runner then failed before semantic evaluation with:

`ModuleNotFoundError: No module named 'adapters'`

Cause: running `python tools/run_monolith_native_route_evolution.py` puts `tools/` rather than the repository root at the front of Python's module path. No invariant assertion failed.

Repair: the runner now derives the repository root from `__file__` and explicitly inserts that root into `sys.path` before importing the local adapter. No test or semantic assertion was weakened.

## Four-root gate

**Truth:** route eligibility is tied to exact endpoint + producer ref + retained verified native-command evidence. READY is not execution. Unknown/future observation shapes HOLD. The first hosted runner failure is retained above rather than reported green.

**Agency / non-domination:** the probe never takes the donor execution path and the refinement grants no execution, merge, promotion, or CANON authority.

**Continuity:** INV-20 is extended in place and all earlier receipt/archive/finalization evidence remains retained. The current donor is pinned by exact commit and blob identities.

**Wisdom before speed:** the experiment uses the donor's 15 retained routes and three falsifiers rather than attempting to model the rapidly growing Monolith totality.

## Evidence ceiling

If the repaired exact head passes hosted CI, this establishes that INV-20's non-promotion boundary survives one materially evolved Monolith native-route planning implementation. It does not prove source-command success, product behavior, arbitrary native routes, future donor commits, deployment, safety/quality, or constitutional authority. General model fidelity remains at the existing evidence ceiling.
