# Universal Creation donor-fidelity refinement — INV-10

## Status

**Reusable read-only refinement capability / pinned donor source+test+documentation projection / not CANON.**

This promotes candidate invariant **INV-10** from `MODEL/ADAPTER LATER` to an executable bounded refinement because Universal Creation now exposes a concrete detached donor adapter whose semantics directly exercise source identity, explicit HOLD state, and fail-closed versioning.

## Pinned donor boundary

Repository: `mike-axiom-mir/axm-universal-creation`

Commit: `8c8a313fa076a49f947df594e6997b7def267ac9`

Pinned blobs:

- `MATERIAL_DONOR_ADAPTER.md` — `7cc4129924df0a4934b609fa29913643ce5e6c1a`
- `src/axm_uc/material_donor.py` — `8e2504714825b38c07754eb90c23158c3794df51`
- `tests/test_material_donor.py` — `8288592d647ae8687f4daf670b6bcb84c695d97b`

No open Universal Creation PR matched this donor-fidelity boundary during the overlap scan. The adapter remains owned by Universal Creation; Invariant Lab consumes a mechanical projection and does not replace or rewrite it.

## Bounded claim

Within the pinned material-donor boundary, adaptation preserves declared donor identity and does not silently reinterpret ambiguous donor state as safe or complete.

The retained projection requires four donor behaviors already present in source/tests:

1. a complete adaptation retains donor pack/library identity, accepted entry IDs, source metadata, and explicit channel routing while keeping rendering verification false;
2. an entry with `channelHint: unassigned` remains a visible partial HOLD and strict mode refuses it;
3. a duplicate-channel family remains held while already accepted standalone textures remain reusable;
4. an unsupported donor version fails closed.

## Falsifiers

The refinement FAILs when any retained contradiction is injected, including:

- donor repository/commit/blob identity drift;
- pack/library identity changing across adaptation;
- accepted entry source metadata disappearing;
- an unassigned channel being guessed, discarded, or promoted out of HOLD;
- a duplicate family channel silently becoming an accepted family;
- detached descriptor adaptation claiming rendering verification;
- unsupported donor versions no longer failing closed.

Required evidence that is absent becomes HOLD rather than PASS.

## Important meaning boundary

`source identity` here means the donor identities actually carried by the pinned adapter: repository/commit/blob identity at the refinement boundary, donor pack/library identity in the result, accepted entry IDs, and retained entry `source` metadata. It does **not** prove authorship, legal provenance, semantic truth of the source metadata, image validity, or renderer behavior.

`held/ambiguous` here means donor state that the adapter itself cannot map exactly under its declared grammar. Invariant Lab does not infer a missing material channel, repair a donor family, or decide that held state is safe.

## Reuse surfaces

- Python: `adapters.universal_creation_donor_fidelity.inspect(...)`
- Evidence receipt: `adapters.universal_creation_donor_fidelity.build_receipt(...)`
- CLI drift gate: `python tools/run_universal_creation_donor_fidelity.py --check`
- Retained fixture: `fixtures/universal-creation-material-donor-v1.projection.json`
- Retained evidence: `evidence/UNIVERSAL_CREATION_DONOR_FIDELITY_INV10.json`

## Evidence ceiling

This is pinned donor source+test+documentation refinement evidence. It makes INV-10 executable on one concrete donor boundary, but it does **not** raise the repository's general model-fidelity claim beyond seed rung 5. It does not prove arbitrary donor adapters, real rendering, material correctness, authorship, deployment, network behavior, or constitutional/CANON authority.
