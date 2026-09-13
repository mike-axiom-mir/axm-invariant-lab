# Connected Monolith direct-archive refinement — INV-20 v2.3

## Status

Grounded reusable bounded capability. Not CANON. Not a general Monolith verifier.

This refines **INV-20** using one exact, user-supplied Connected Monolith archive rather than only its detached result receipt:

> Connected topology, wiring, packaging, or aggregate composition does not by itself establish callability or verification; callable coverage must come from explicit callable evidence and blocked states remain blocked.

The original `RESEARCH_SEED_v0.1.md` remains provenance. Fresh implementation evidence controls this refinement.

## Exact source boundary

The direct archive used to create the retained projection is:

- folder: `AXM_Connected_Monolith_v0.3.2`
- archive bytes: `194320426`
- archive SHA-256: `sha256:f0a0d1d30007d71bb4ded6a9cc03259e5a12ceb7967cd532b12d366ae0cdf55e`
- ZIP member count: `15956`
- internal snapshot receipt: `SNAPSHOT_FILE_RECEIPT.json`
- snapshot-recorded non-receipt files: `15955`

The archive reader checked every snapshot-recorded path against the actual ZIP bytes. The retained source run found:

- missing recorded files: `0`
- byte/hash mismatches: `0`
- extra non-receipt files outside the receipt: `0`

This establishes byte identity/integrity for the frozen package. It does **not** establish source authorship, arbitrary semantic correctness, deployment correctness, or constitutional authority.

## Small projection, not a 23k-endpoint model

`adapters/monolith_connected_archive.py` reads the archive but retains only the evidence needed for bounded cross-artifact checks. It does not copy the endpoint registry into this repository and does not import or execute packaged source code.

The projection pins six internal evidence artifacts by the snapshot receipt:

- `EXECUTION_FABRIC.json`
- `EXECUTION_GAPS.json`
- `LEAF_CAPABILITY_REGISTRY.json`
- `WORKFLOW_REGISTRY.json`
- `EXECUTABLE_COMPOSITIONS.json`
- `evidence/execution-fabric/FULL_POWER_TEST.json`

## Cross-artifact checks

### 1. Blocked really remains blocked

`EXECUTION_FABRIC.json` reports `23248` endpoints blocked for missing callable binding and `68` blocked for missing native contract. Their sum is `23316`, exactly matching `EXECUTION_GAPS.json.blocked_endpoint_count`.

A visible gap is therefore preserved as missing evidence/provider work, not permission to invent compatible semantics.

### 2. Declaration is not execution

The leaf registry reports `23221` canonical leaf capabilities, `50239` declaration occurrences, and `declared_callable_count = 0`. The canonical leaf count also equals the execution fabric's declared-leaf count. This keeps machine-readable declaration evidence distinct from runtime callability.

### 3. Named-workflow callability is scope-bound

The workflow registry contains exactly one callable workflow, `ghost-studio.blackline-3d.v0.4`, with three exact stages:

1. `axm-universal-creation::creation.universal`
2. `Axm-game-assets::asset.game`
3. `axm-ghost-studio::game.studio`

All three corresponding endpoint adapters are `callable_through_named_workflow`. The internal required-workflow receipt is bound to the same workflow ID and reports `EXECUTED_END_TO_END_AND_STRUCTURALLY_ACCEPTED` with `source_capability_executed=true`.

That callability does not transfer merely because the same endpoint address occurs elsewhere.

### 4. Wired candidate composition is not an executed workflow

The package contains `80` executable-composition records. All `80` remain `wired_candidate / candidate_unverified / not_executed`.

Across `384` composition-step occurrences, the endpoint adapter statuses are `271` `blocked_missing_native_contract`, `78` `executable_inspection`, `24` `executable_test_evidence`, `7` `callable_through_named_workflow`, and `4` `blocked_missing_callable_binding`.

Seven candidate compositions contain at least one stage that is callable in the named workflow. **Zero** candidate compositions have every step named-workflow-callable, and **zero** of those seven leaked into an executed/verified composition status.

This is the central archive-backed falsifier for scope leakage: a callable stage embedded in a graph path cannot upgrade the surrounding candidate composition.

### 5. Test adapter readiness is not test success

The full-power probe reports `37` test-adapter-ready endpoints. The broad test evidence separately reports `127` commands: `96` passed, `28` failed, and `3` timed out. Its `37` tested modules split into `25` passed and `12` completed with failures.

Therefore `executable_test_evidence` / test-adapter readiness is an execution/evidence surface, not a synonym for passing tests.

### 6. Packaging grants no automatic authority

The execution fabric keeps automatic CANON, install, merge, network, and source-mutation flags false. Archive presence, hashing, wiring, tests, or workflow execution do not change that boundary.

## PASS / FAIL / HOLD behavior

The adapter returns **PASS** when the supported frozen projection is cross-artifact coherent and no consumer semantic promotion is requested; **FAIL** for explicit contradiction or semantic promotion; and **HOLD** for future/unknown projection or source schemas rather than silently assuming compatibility.

## Reproduction

When the original ZIP is available:

```bash
python tools/run_monolith_connected_archive_refinement.py \
  --archive /path/to/AXM_Connected_Monolith_v0.3.2.zip \
  --check
```

Ordinary repository CI performs the deterministic retained-evidence check:

```bash
python tools/run_monolith_connected_archive_refinement.py --check
```

CI intentionally does not download or commit the ~194 MB archive. The retained projection is small and falsifiable; the source archive identity and snapshot-file hashes remain explicit.

## Evidence ceiling

This run directly verifies one frozen package's byte integrity and bounded cross-artifact semantics. It does **not** prove authorship, arbitrary packaged source behavior, future Monolith schemas, launch/runtime/deployment correctness, network/device behavior, future composition callability, or merge/install/CANON/constitutional authority.

General model-fidelity status therefore does not rise merely because the archive is large. The value is narrower: INV-20 now survives direct package evidence and cross-artifact scope checks instead of only an aggregate receipt.
