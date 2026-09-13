# TruthGrid client-intent refinement — INV-06

## Status

**Reusable read-only refinement capability / pinned donor source+test projection / not CANON.**

This promotes candidate invariant **INV-06** from `ADAPTER NEXT` to an executable adapter because the current TruthGrid implementation exposes a concrete, falsifiable intent-versus-consequence boundary.

## Pinned donor boundary

Repository: `mike-axiom-mir/axm-TruthGrid`

Commit: `e3875e02db14eb9aef040dc2727dc0ccd58d8ff0`

Pinned blobs:

- `src/transport/referee.js` — `074bbf01a75d9422b4b4b0093f9a2540e3ce513b`
- `src/core/engine.js` — `451968447f420b6c13cd24814c61752605fddcbe`
- `tests/determinism.test.js` — `47a60a10a49d8de1ed2bea97efc18fc34ee8af77`

TruthGrid's own verification workflow passed on that exact donor commit before this projection was admitted.

## Bounded claim

Within this pinned donor boundary, a client direction/action is causal **intent**, not a self-declared simulation consequence.

The adapter requires three independent observations already asserted by donor source/tests:

1. **Wire boundary:** hostile manifested-outcome fields (`damage`, `resultingState`, `hit`) appear in submitted client objects but do not survive the referee's canonical wire-intent event.
2. **Conflict adjudication:** A and B can both request the same destination; only one movement manifests and the engine emits a conflict receipt.
3. **Chronology rejection:** a structurally valid future action is rejected and does not advance the actor's accepted client-sequence chronology.

Together these falsify the weaker interpretation that a client's direction or claimed outcome directly determines committed world state.

## Falsifiers

The refinement FAILs when any retained contradiction is injected, including:

- a manifested result field surviving into the transported event;
- both same-destination client moves manifesting as state effects;
- the losing direction manifesting without the expected conflict record;
- a rejected future intent advancing accepted chronology;
- pinned donor repository/commit/source-test blob identity drifting.

Required evidence that is absent becomes HOLD rather than PASS.

## Important meaning boundary

`authoritative consequence` in INV-06 means only **the donor simulation's committed state/receipt outcome**. It does not mean constitutional authority, AXM CANON, merge authority, device authority, or a proof about clients/networks outside this pinned TruthGrid path.

Invariant Lab does not reimplement TruthGrid's engine or referee. The fixture is a mechanical projection of explicit donor source/test assertions, and the adapter only checks that projection plus its exact donor identity.

## Reuse surfaces

- Python: `adapters.truthgrid_client_intent.inspect(...)`
- Evidence receipt: `adapters.truthgrid_client_intent.build_receipt(...)`
- CLI drift gate: `python tools/run_truthgrid_client_intent_refinement.py --check`
- Retained fixture: `fixtures/truthgrid-client-intent-v1.projection.json`
- Retained evidence: `evidence/TRUTHGRID_CLIENT_INTENT_REFINEMENT.json`

## Evidence ceiling

This is pinned donor source+test refinement evidence. It strengthens INV-06 from a prose candidate to executable tooling, but it does **not** raise the repository's general model-fidelity claim beyond seed rung 5. It does not prove real-network clients, hostile peers, authentication, production deployment, all possible TruthGrid actions, or any unmodeled consumer.
