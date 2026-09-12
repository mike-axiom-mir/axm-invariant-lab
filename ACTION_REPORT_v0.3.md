# Action report v0.3 — Monolith Pipeline Fabric refinement

## Question tested

Can Invariant Lab independently consume a second real AXM donor contract and preserve the seed's cross-repo invariant shape — candidate transport/testing must not silently grant authority — without rewriting Monolith semantics or claiming seed rung 6 adoption?

## Starting evidence

`main` started at `dd0f6daa6e0ba437408b0efa029124246769b893` with no open PRs. The prior cross-implementation lane had exact-head GitHub Actions success and explicitly identified a separately authored donor translation/refinement as the strongest non-duplicative next step.

Historical v0.1/v0.2 branches remain present but do not occupy this semantic lane.

## Donor inspected

`mike-axiom-mir/axm-monolith` at exact commit `acb751a40913f0d094dc809cde7a0b43b34ae30d`.

Pinned contract/source blobs:

- `AXM_MODULE.json`: `a8a8688b867853f0d141b011f8092da4654ad3cf`;
- `schemas/PIPELINE_FABRIC.schema.json`: `37f048944bc6ec1f2c6c8b372b830139d1a43395`;
- `tools/pipeline_fabric.py`: `f3ce407fdab30faf09c08ffa6cdb1b9f989fb659`.

The donor explicitly declares Pipeline Fabric as candidate evidence only and emits automatic execution/install/merge/CANON flags as false.

## Exact delta

NEW:

- `adapters/monolith_pipeline_fabric.py`: read-only PASS/FAIL/HOLD refinement adapter;
- `fixtures/monolith-pipeline-fabric-v0.1.json`: minimal pinned donor-contract fixture with exact source provenance;
- six focused regressions for safe, contradictory, unknown, semantic-upgrade, missing-evidence, and read-only behavior;
- deterministic retained refinement receipt and `--check` tool;
- `MONOLITH_PIPELINE_REFINEMENT.md` with donor mapping, falsifiers, and evidence ceiling.

PRESERVED:

- primary bounded explorer and all four tiny models;
- independent path verifier and rung-5 exploration claim;
- TruthGrid adapter and evidence;
- counterexample packet contract;
- original research seed and donor ownership.

## Falsifier

This lane fails if the adapter:

- accepts any automatic authority flag that is not explicitly false;
- treats missing authority/candidate evidence as safe;
- permits an unrecognized stronger pipeline status such as `VERIFIED` under the pinned v0.1 contract;
- mutates donor input;
- or needs to reinterpret Monolith product logic instead of consuming the declared contract.

## Evidence result before publication

A standalone local fixture gate for the new adapter/tests produced **6/6 PASS**.

The retained safe contract fixture produces PASS. Deliberate `automatic_execution: true` produces FAIL. Removing `automatic_merge` produces HOLD. Replacing a candidate status with `VERIFIED` produces FAIL. Omitting candidate evidence produces HOLD. Input remains byte-equivalent at the Python object level after inspection.

Repository-wide exact-head GitHub Actions remains the required integration gate before merge.

## Evidence level decision

**Do not promote the repository to seed rung 6.**

This is a separately authored refinement fixture against a second real AXM donor contract. It reduces the shared-model risk from v0.2 and demonstrates that the invariant vocabulary can map cleanly onto Monolith's explicit candidate/authority boundary.

Seed rung 6 requires at least two real AXM systems to use Invariant Lab's result without semantic rewriting. That adoption has not happened here.

## Root check

**Truth:** missing evidence HOLDs; contradictory explicit authority FAILs; donor schema/source are pinned; runtime/full-stack proof is not claimed.

**Agency / non-domination:** the adapter cannot execute, install, merge, promote, or grant CANON authority.

**Continuity:** Monolith remains authoritative for Pipeline Fabric semantics; no donor files are modified and source identity is preserved.

**Wisdom before speed:** one small donor adapter closes a specific evidence gap; no solver, universal model, or generic framework expansion.

## What remains unknown

- a real captured Monolith full-stack Pipeline Fabric export rather than a contract-shaped fixture;
- whether another external AXM repo consumes `invariant-result` or counterexample packets directly;
- whether two such consumers preserve semantics unchanged;
- tractability on larger state spaces;
- whether mature formal tooling adds enough value to justify added complexity.

## Next evidence frontier

The next strongest step is actual **consumer adoption**: one external AXM repo should consume an Invariant Lab result/packet through a narrow declared contract, then a materially different second repo should do the same before seed rung 6 is claimed.
