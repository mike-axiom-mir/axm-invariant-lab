# Discovery interoperability boundary — INV-19 v1.6

## Status

INV-19 is now exercised across a real repository boundary, not only against Invariant Lab's own `AXM_MODULE.json` structure.

Invariant Lab deterministically projects the capability identities already declared in `AXM_MODULE.json` into two deliberately narrow public surfaces:

- `.axm/discovery-public.json` — explicit opt-in to public discovery using `axm.discovery-public/v1`.
- `registry/capabilities.jsonl` — one public discovery row per declared capability, preserving the exact capability id and its existing `evidence.status` string.

The generated rows do not copy descriptions, donor fixtures, model contents, or private repository state. They explicitly state that declaration is not runtime proof and grants no authority.

## Independent consumer boundary

The hosted evidence gate executes the scanner from a pinned, materially separate AXM repository:

- consumer: `mike-axiom-mir/axm-discovery-buddy`
- commit: `a1e28aba31c453023298e01ce4e54107c3f74583`
- scanner blob: `6d69c9eb85cc518dfcd6e43e8c9426ef168d392f`

That scanner requires the explicit public marker, reads `registry/capabilities.jsonl`, and normalizes the bounded fields it understands. Invariant Lab then requires the normalized capability id/status map to equal the authoritative `AXM_MODULE.json` declarations one-for-one. The retained receipt is `evidence/discovery_buddy_compatibility.json`.

This is stronger than self-linting because the producer does not control the consumer parser used by the hosted check. Consumer-source drift is fail-closed by the pinned scanner blob.

## What INV-19 now supports

Within this exact boundary, a capability cannot be treated as publicly machine-discoverable merely because a local manifest mentions it. The local manifest must first pass the existing structural discovery check, the public projection must be byte-current with that manifest, and the pinned external Discovery Buddy implementation must independently accept and normalize the same capability identities/statuses.

This is reusable cross-repository discovery compatibility evidence.

## Evidence ceiling

This does **not** prove that any discovered capability works, is deployed, is semantically compatible with a caller, or deserves promotion. Discovery Buddy does not execute the capabilities. Its normalized discovery record is not CANON, merge authority, installation authority, execution authority, or proof of the underlying invariant/model claims.

This run therefore does not promote general model fidelity beyond seed rung 5. It also does not reuse the counterexample packet's separate rung-6 evidence: the discovery surface has one pinned external consumer here, and no higher ladder claim is made merely because that consumer can parse it.

## Failure semantics

- malformed or structurally invalid `AXM_MODULE.json` -> **FAIL**;
- an unsupported future local discovery schema/entrypoint kind -> **HOLD** before publication;
- generated marker/registry drift -> **FAIL**;
- missing or changed pinned Discovery Buddy scanner -> **HOLD** rather than substituting another consumer silently;
- external normalized capability id/status disagreement -> **FAIL**.

These boundaries preserve Truth, Agency/non-domination, Continuity, and Wisdom before speed: public discovery is explicit, semantic claims are not inflated, generated state cannot silently drift, and unfamiliar future semantics stop rather than being guessed.
