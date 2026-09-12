# AXM Invariant Lab — Action Report v1.5

Date: 2026-09-12

## Question tested

Can Invariant Lab turn its previously observed machine-discovery omission into a small falsifiable continuity invariant, rather than relying on one-off tests for individual capabilities?

## Pre-work overlap scan

- `main` base: `1fecddd2a45ce3f2ce3d6e242b0f243765cfa63e`.
- No open pull requests existed at claim time.
- Existing branches were historical completed growth lanes; no active branch covered global `AXM_MODULE.json` structural integrity.
- Latest `main` CI for the base completed successfully.
- The preserved `RESEARCH_SEED_v0.1.md` remains provenance; fresh executable evidence controls current status.

## Exact delta

Added INV-19 machine-discovery integrity with:

- dependency-free `src/discovery_contract.py` structural inspection;
- PASS / FAIL / HOLD semantics;
- local path-confinement and existence checks;
- top-level Python symbol checking by static AST inspection without importing donor/capability code;
- Python CLI path agreement and required bounded `--check` declaration;
- duplicate capability-ID detection;
- explicit HOLD for future schema majors or entrypoint kinds the checker does not understand;
- deterministic retained evidence;
- nine adversarial/fail-closed unit tests;
- a dedicated CI evidence gate and documentation.

## Focused evidence

The isolated INV-19 unit suite passed **9/9** before publication. Its falsifiers cover missing files, missing symbols, command/path mismatch, advertised CLI without `--check`, path escape, duplicate capability IDs, unsupported entrypoint kinds, and unsupported schema majors.

The retained baseline describes the current v1.3 manifest as 14 capabilities and 25 advertised entrypoints with zero FAIL/HOLD findings. Hosted CI is the integration check because it runs the verifier against the complete repository rather than the focused temporary fixture.

## Root gate

**Truth:** machine-discovery claims are checked against repository structure; unknown future kinds HOLD instead of silently passing. Static symbol checking is explicitly not execution/semantic proof.

**Agency / non-domination:** the receipt carries all authority fields false and cannot execute advertised entrypoints.

**Continuity:** this converts the earlier machine-discovery omission into a repository-wide drift guard without rewriting existing capability semantics.

**Wisdom before speed:** the run adds one small structural checker instead of another donor model, solver layer, or universal framework.

## Evidence ceiling

INV-19 is repository-local structural evidence. It does not prove advertised capability semantics, deployment, donor runtime fidelity, or real-environment behavior. General model fidelity remains seed rung 5; counterexample-packet external use remains separately rung 6.

## Next frontier

If the gate stays stable, the next higher-value move is external compatibility evidence for the discovery contract or another materially different donor refinement. More manifest lint rules should be added only when a concrete failure class justifies them.
