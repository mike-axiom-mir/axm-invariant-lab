# Action Report v2.3 — direct Connected Monolith archive refinement

## Question tested

Can INV-20 survive direct inspection of the exact Connected Monolith v0.3.2 archive, rather than only its detached aggregate receipt, without expanding Invariant Lab into a giant Monolith model?

## Starting state inspected

- `main`: `b6fe4457a50cfbe4f695bcdb54e14767dc0d8a06`
- latest `main` workflow: `invariant-lab-tests`, successful on that exact commit
- open Invariant Lab PRs at activation: none
- preserved seed: `RESEARCH_SEED_v0.1.md`
- existing INV-20 lane: receipt-only `adapters/monolith_connected_zip.py`; it explicitly does not inspect the referenced archive

Semantic-overlap decision: **EXTEND INV-20**, do not create INV-21. The unresolved evidence gap is direct archive/cross-artifact verification, not a new invariant concept.

## Exact delta

Added a bounded archive-backed projection/verifier that:

1. hashes the actual ZIP and verifies every path/byte-count/SHA-256 recorded by its internal `SNAPSHOT_FILE_RECEIPT.json`;
2. projects only six relevant internal evidence surfaces rather than copying 23k endpoints into this repo;
3. cross-checks execution-fabric blocked status against the gap registry;
4. cross-checks leaf declaration counts while keeping `declared_callable_count=0` explicit;
5. binds the exact three-stage named workflow to its workflow receipt and endpoint adapter statuses;
6. checks all 80 candidate compositions for named-workflow callability scope leakage;
7. separates test-adapter readiness from actual pass/fail/timeout outcomes;
8. preserves all automatic-authority flags as false;
9. fails on semantic promotion and holds on future/unknown schemas.

## Direct archive evidence

Exact source archive:

- bytes: `194320426`
- SHA-256: `sha256:f0a0d1d30007d71bb4ded6a9cc03259e5a12ceb7967cd532b12d366ae0cdf55e`
- ZIP members: `15956`
- snapshot-recorded non-receipt files checked: `15955`
- missing: `0`
- mismatched: `0`
- extra non-receipt: `0`

Cross-artifact results:

- endpoints: `23472`
- blocked endpoints: `23248 + 68 = 23316`, exactly matching gap registry
- canonical leaf capabilities: `23221`; declared callable: `0`
- explicit named-workflow callable endpoints/stages: `3`
- candidate compositions: `80`; all remain `wired_candidate / candidate_unverified / not_executed`
- composition step occurrences: `384`
- candidate compositions containing at least one named-workflow-callable stage: `7`
- candidate compositions with every step named-workflow-callable: `0`
- scope-leak violations: `0`
- test-adapter-ready endpoints: `37`
- broad test commands: `127 = 96 passed + 28 failed + 3 timed out`

## Falsifiers retained

Focused tests reject snapshot hash mismatch, blocked-count disagreement, declaration-to-callability promotion, named-workflow scope leakage, fully-callable candidate promotion, test-readiness-to-success promotion, package-integrity-to-semantic-correctness promotion, blocked-gap guessing, and silent acceptance of future schemas.

## Local evidence before publication

- focused archive-refinement suite: **12/12 PASS**
- live archive projection exactly equals the retained projection: **PASS**
- live `--archive ... --check` evidence reproduction: **PASS**

The complete inherited repository suite remains a hosted-CI merge gate; local container networking cannot clone GitHub, so no claim of a local full-suite run is made.

## Four-root gate

**Truth:** stronger than v2.2 because package bytes and internal evidence artifacts were checked directly; integrity is not mislabeled semantic proof.

**Agency / non-domination:** no archive evidence grants execution, install, network, source mutation, merge, CANON, or constitutional authority.

**Continuity:** INV-20 is extended rather than renamed/replaced; the receipt-only lane remains useful and the original seed remains provenance.

**Wisdom before speed:** a ~7 KB deterministic projection is retained instead of importing a 194 MB archive or modeling 23k endpoints wholesale.

## Evidence ceiling

This establishes direct byte-integrity plus bounded cross-artifact evidence for one frozen Monolith v0.3.2 package. It does not execute packaged source, rerun the workflow, prove future versions, prove arbitrary semantics, or raise the general model-fidelity rung by itself.
