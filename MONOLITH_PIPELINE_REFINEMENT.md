# Monolith Pipeline Fabric refinement boundary

## Purpose

This lane checks one narrow cross-repository claim from the preserved research seed:

> a candidate may be tested and transported but must not silently become authoritative.

The donor is `mike-axiom-mir/axm-monolith` Pipeline Fabric v0.1, pinned at commit `acb751a40913f0d094dc809cde7a0b43b34ae30d`.

## Exact donor contract inspected

Pinned donor files:

- `AXM_MODULE.json` blob `a8a8688b867853f0d141b011f8092da4654ad3cf`;
- `schemas/PIPELINE_FABRIC.schema.json` blob `37f048944bc6ec1f2c6c8b372b830139d1a43395`;
- `tools/pipeline_fabric.py` blob `f3ce407fdab30faf09c08ffa6cdb1b9f989fb659`.

The donor explicitly emits candidate pipeline statuses and an `authority` object whose automatic execution/install/merge/CANON fields are false.

## Adapter mapping

`adapters/monolith_pipeline_fabric.py` reads only explicit donor fields. It does not parse authority from prose and does not execute a candidate path.

PASS requires:

- descriptor schema `axm.monolith.pipeline-fabric/v0.1`;
- source `STACK_ANALYSIS.json`;
- graph/candidates/gaps output names are present;
- `automatic_execution`, `automatic_install`, `automatic_merge`, and `automatic_canon` are explicitly false;
- candidate payload schema `axm.monolith.pipeline-candidates/v0.1`;
- every observed pipeline status remains inside the donor v0.1 candidate-only vocabulary.

A contradictory explicit value is FAIL. Missing required evidence is HOLD.

## Falsifiers

The retained tests deliberately verify that:

1. `automatic_execution: true` becomes FAIL;
2. a missing automatic-authority field becomes HOLD rather than PASS;
3. a pipeline status of `VERIFIED` becomes FAIL because the pinned donor contract did not authorize that semantic upgrade;
4. missing candidate evidence becomes HOLD;
5. inspection does not mutate donor input.

## Evidence ceiling

This is a **cross-repo refinement fixture**, not seed rung 6 CROSS-REPO adoption.

The fixture is separately authored from an exact pinned donor schema/source contract. It is not a captured full-stack Monolith runtime export, and no second external AXM repository currently consumes invariant-lab output as part of its own operation.

Therefore this lane reduces the shared-model risk identified in v0.2 and demonstrates a second real donor boundary, but it does not silently promote the repository beyond its existing rung-5 exploration claim.

## Authority boundary

The adapter can classify explicit evidence PASS / FAIL / HOLD. It grants no execution, installation, device, network, merge, promotion, or CANON authority to Monolith, Invariant Lab, or any consumer.
