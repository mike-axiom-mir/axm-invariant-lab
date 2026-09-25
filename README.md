# AXM Invariant Lab

**Status:** working experimental capability / cross-implementation exploration evidence / pinned donor contract refinements plus donor execution and runtime-observation refinements / measured tractability boundary / counterexample packet CROSS-REPO evidence / not CANON / no merge or execution authority.

The original `RESEARCH_SEED_v0.1.md` is preserved as provenance. It was the kickstart document, not a permanent requirement that this repository remain research-only. Fresh evidence decides the repo's current status.

AXM Invariant Lab is a small dependency-free capability for asking a different question than ordinary example tests:

> Across the bounded state space we explicitly modeled, can any reachable legal transition sequence violate a declared invariant?

The repository is deliberately narrow. It does not replace unit, integration, fuzz, replay, checkpoint, or real-environment testing. It does not prove unmodeled code or the real world.

## Grounded capability

The current implementation contains:

- a dependency-free breadth-first bounded state explorer;
- tri-state invariant results: PASS / FAIL / HOLD (unknown is never treated as safe);
- four tiny AXM-shaped models;
- shortest counterexample traces for state invariants;
- a reusable counterexample packet schema;
- a bounded TruthGrid evidence refinement adapter;
- synthetic fault-injection fixtures that demonstrate transition-order failure detection;
- a second dependency-free path-enumeration verifier that does not call the primary explorer or prune revisited states;
- cross-implementation agreement receipts with an explicit path-node tractability budget;
- a deterministic tractability probe showing where all-path enumeration reaches that budget while visited-state exploration remains small;
- a read-only AXM Monolith Pipeline Fabric v0.1 refinement adapter pinned to an exact donor contract, preserving candidate-only status and explicit no-automatic-authority fields;
- a read-only AXM State Research Workfloor Sentinel refinement over one pinned execution-results artifact, mechanically checking necessary-vs-awakened wakeups across the known dependency bug and repaired run without reimplementing donor checks;
- a read-only AXM State Research Wakeup Fuzzer refinement that derives one omitted required wake from runtime-observed activation, actual output change, and sparse mismatch **without using the donor `necessary`/`missed` fields**, then checks four separate repaired transitions across full-scan/sparse/observed records;
- two real external consumers of `axm.invariant-lab.counterexample/v0.1`: AXM Monolith and AXM Profession Mesh;
- an external-consumer registry and producer-side blob-identity guard so later packet/schema drift cannot silently claim compatibility with pinned consumers;
- a distinct-consumer guard so the same repository cannot be counted twice by accident;
- deterministic tests and evidence generation.

The primary callable surface is `src.bounded_explorer.explore(...)`. The independent bounded cross-check is `src.reference_verifier.verify_paths(...)`, composed through `src.cross_verifier.cross_verify(...)`. The tractability probe is `src.tractability_probe.run_probe(...)`. Donor refinement surfaces live under `adapters/`. Consumer continuity is checked by `tools/check_external_consumers.py`. Machine discovery is declared in `AXM_MODULE.json`.

## Evidence levels

### Bounded exploration semantics — rung 5 / CROSS-IMPLEMENTATION

The bounded **exploration semantics** remain at the seed's **rung 5 / CROSS-IMPLEMENTATION** boundary:

- the retained four safe models and four fault-injected variants produce **8/8 cross-implementation agreements**;
- both implementations agree on PASS/FAIL status, reachable unique-state count, failing invariant names, and unknown invariant names for those retained cases;
- the reference verifier fully enumerates those cases inside its explicit path-node budget;
- budget exhaustion forbids an unearned PASS and produces HOLD unless a concrete modeled failure has already been observed;
- the earlier adversarial evidence remains: safe models PASS, injected faults FAIL, missing donor evidence HOLDs, and the TruthGrid refinement fixture detects an adversarial `rollbackRef` mutation.

The rung-5 exploration claim remains intentionally narrow. Both exploration verifiers consume the **same authored transition and invariant functions**. Agreement cross-checks the search/exploration implementation; it does not independently prove that the model faithfully represents donor code.

A second donor boundary is mapped through the Monolith Pipeline Fabric v0.1 refinement fixture. The adapter checks explicit `automatic_execution/install/merge/canon = false` fields and candidate-only pipeline statuses; contradictory values FAIL and missing evidence HOLDs.

A further, narrower execution-evidence boundary is mapped from AXM State Research Workfloor Sentinel. The pinned donor artifact records a dependency-bug run and repaired run over the same designed mutation. Invariant Lab mechanically projects explicit `necessary_check_ids`, `awakened_check_ids`, reported misses/mismatches, equivalence flags, and final hashes. Candidate invariant **INV-13** independently derives `necessary - awakened`: the known bug run FAILs with `cross--report-matches-raw-results` missed, while the repaired run PASSes and converges to the same final oracle hash. This is stronger than a prose/contract-only fixture because the source is a donor-generated execution-results artifact, but the donor oracle still supplies necessity. See `STATE_RESEARCH_SENTINEL_REFINEMENT.md`.

**INV-14 closes part of that specific limitation without changing the evidence rung.** The pinned Wakeup Fuzzer counterexample is evaluated without the donor `necessary` or `missed` fields. Invariant Lab derives the omitted `check_00000` because the runtime observed-read scheduler wakes it while declared sparse does not, the check changes only in the observed record, and the sparse mismatch set contains the same ID. Four additional repaired transitions agree across full-scan, declared-sparse, and observed-read execution records. This is independently derived from donor runtime observations, but the observed-read mechanism itself is donor instrumentation and explicitly does not prove completeness for unseen branches, dynamic/external reads, or concurrency. See `STATE_RESEARCH_WAKEUP_FUZZER_REFINEMENT.md`.

The retained tractability probe adds a separate operational boundary without promoting the exploration evidence rung. On an authored reconverging two-branch model with a 100,000 path-node budget, the reference verifier completes depth 15 at **65,535 path nodes**, then reaches the budget and returns **HOLD at depth 16**, while the visited-state explorer still completes with only **17 unique states**. These are deterministic work counts, not wall-clock performance claims. See `TRACTABILITY_BOUNDARY.md`.

### Counterexample packet external use — rung 6 / CROSS-REPO

The existing `axm.invariant-lab.counterexample/v0.1` result contract has reached the seed's **rung 6 / CROSS-REPO** boundary through two materially different real AXM consumers:

1. **AXM Monolith** consumes the exact FAIL/HOLD packet as evidence-only, preserves the status, rejects unsupported PASS/future fields, requires all authority fields false, hashes the source bytes, and does not mutate pipeline status. Its final consumer candidate passed the full **56-test** Monolith suite before merge.

2. **AXM Profession Mesh** consumes content-addressed packet bytes as a transport/admission evidence input. It preserves FAIL/HOLD verbatim, maps FAIL -> local `quarantine` and HOLD -> local `hold`, can never return candidate acceptance from invariant evidence, and rejects authority escalation, unsupported PASS/fields, or digest mismatch. Its exact PR candidate passed hosted Node 22 `npm test`, including the existing Mesh authority-boundary test and the new consumer test, before merge.

Those systems are materially different in role: one is a whole-stack assembly/analysis surface; the other is a package transport/discovery/admission layer. Neither changes the producer FAIL/HOLD meaning or grants authority from the packet.

This rung-6 promotion applies **only to external consumption of the counterexample packet/result contract**. It does not promote model fidelity, donor-runtime proof, solver proof, or real-environment validation.

Invariant Lab keeps `EXTERNAL_CONSUMERS.json` and checks that the local packet/schema Git blob identities still match both consumers' exact pins. Producer-byte drift fails closed until compatibility is deliberately reviewed. Duplicate consumer repositories are rejected.

There is still no solver-backed proof or real-environment validation.

## Run

Python 3.10+; no third-party packages.

```bash
python -m unittest discover -s tests -v
python tools/run_evidence.py --check
python tools/run_cross_verification.py --check
python tools/run_monolith_refinement.py --check
python tools/run_tractability.py --check
python tools/check_external_consumers.py --check
python tools/run_state_research_sentinel_refinement.py --check
python tools/run_state_research_wakeup_fuzzer_refinement.py --check
```

Regenerate retained receipts only when deliberately reviewing a semantic change:

```bash
python tools/run_cross_verification.py
python tools/run_monolith_refinement.py
python tools/run_tractability.py
python tools/check_external_consumers.py
python tools/run_state_research_sentinel_refinement.py
python tools/run_state_research_wakeup_fuzzer_refinement.py
```

## Important truth boundary

A primary PASS means only: **no counterexample was found within the exact model, transition set, invariant predicates, and exploration bound that were run.**

A cross-verification `AGREE` means the independent path enumerator matched the primary bounded result on the compared observables. It does not mean the model itself is correct.

A contract-fixture donor-refinement PASS means only that the exact explicit donor fields represented by the pinned fixture satisfy the adapter contract. It does not prove a full donor runtime or an unobserved field.

A State Research Sentinel execution-refinement PASS means only that the mechanically selected fields from the pinned Workfloor Sentinel results artifact are internally consistent with INV-13 and distinguish the donor's known dependency-bug run from its repaired run. The donor oracle still defines necessity; Invariant Lab does not independently reconstruct that semantics or prove unseen mutations.

A State Research Wakeup Fuzzer refinement PASS means only that the exact pinned records support INV-14: one omitted wake is independently triangulated from observed-read activation, actual output change, and sparse mismatch without consuming donor necessity/miss fields, and four selected repaired transitions agree across three scheduler records. It does not prove observed-read instrumentation complete outside those traces.

A tractability HOLD means the declared comparison budget was exhausted. It is evidence that the independent comparison is incomplete, not evidence against the primary result and not a reason to force a larger budget.

An external-consumer compatibility PASS means only that local producer packet/schema bytes still equal the blobs the registered consumers pinned. It does not remotely execute or attest those consumers.

Rung 6 means only that at least two materially different AXM systems now use the emitted packet/result contract without semantic rewriting. It does not turn the packet into authority and does not strengthen the underlying modeled claim beyond its own evidence.

A FAIL is a counterexample to the modeled/declared claim. It is not automatically proof of a bug in a donor repository.

A HOLD means required evidence or bounded enumeration is incomplete. HOLD never silently becomes PASS.

Synthetic fault traces and tractability fixtures validate the explorers against authored conditions; they do not assert those conditions exist in donor systems.

## Authority boundary

This repository may describe, explore, falsify, cross-check, measure bounded tractability, emit evidence, refine pinned donor evidence, and track consumer compatibility. It does not grant execution, device, network, merge, promotion, installation, or CANON authority. The four AXM roots — Truth, Agency/non-domination, Continuity, and Wisdom before speed — remain the merge gate.

Read `INVARIANT_CONTRACT.md`, `REFINEMENT_BOUNDARY.md`, `MONOLITH_PIPELINE_REFINEMENT.md`, `STATE_RESEARCH_SENTINEL_REFINEMENT.md`, `STATE_RESEARCH_WAKEUP_FUZZER_REFINEMENT.md`, `TRACTABILITY_BOUNDARY.md`, `EXTERNAL_CONSUMERS.md`, `DONOR_SCAN_2026-09-12.md`, and the latest `ACTION_REPORT_v0.*.md` before extending the lab.

## Reusable simulation method

[Simulation experience and reuse](SIMULATION_EXPERIENCE_REUSE.md) connects the shared method to this repository, with existing machinery, proposed experiments and explicit evidence limits.
