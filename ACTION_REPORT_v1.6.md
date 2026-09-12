# AXM Invariant Lab — Action Report v1.6

## Decision

**GROW / INV-19 promoted in evidence class, without a higher proof claim.**

The previous machine-discovery integrity work was repository-local: `AXM_MODULE.json` could be checked for structural discoverability, but no independent AXM consumer had to understand the resulting discovery surface. This run closes that specific gap with one pinned external consumer rather than adding more self-lint rules.

## Bounded advance

Invariant Lab now derives two public-safe discovery surfaces from the already-authoritative `AXM_MODULE.json` declarations:

- `.axm/discovery-public.json`
- `registry/capabilities.jsonl`

`src/public_discovery.py` preserves each declared capability id and its existing `evidence.status`; it exports no capability implementation, donor model, private content, or automatic authority. `tools/check_public_discovery.py --check` fails on missing/stale generated surfaces and refuses publication while the existing local discovery contract is FAIL/HOLD.

The independent compatibility gate then checks out exact AXM Discovery Buddy commit `a1e28aba31c453023298e01ce4e54107c3f74583`, pins scanner blob `6d69c9eb85cc518dfcd6e43e8c9426ef168d392f`, and executes that scanner against Invariant Lab's public marker and capability registry. The external normalized capability id/status map must equal `AXM_MODULE.json` one-for-one. Its deterministic receipt is retained at `evidence/discovery_buddy_compatibility.json`.

## Evidence

The first complete hosted run after the implementation, `34721351012` at branch head `d1a6bfea354f8406febb2eb03108fa7ce503cbae`, completed **SUCCESS** on Python 3.11 and 3.13. Both jobs passed the full inherited unit/refinement/evidence chain plus:

- machine discovery integrity;
- public discovery projection drift check;
- checkout of the exact pinned Discovery Buddy consumer;
- Discovery Buddy cross-repository compatibility check.

The new focused unit file adds eight adversarial/projection cases covering valid generation, explicit public opt-in shape, id/status preservation, non-authority truth fields, stale registry rejection, missing marker rejection, future-schema HOLD, and invalid-local-entrypoint publication refusal.

At this snapshot the external consumer accepted **14** capability records. The retained public-marker SHA-256 is `5bb86622f8f246780a781488cd6a85df532c1f18923c205d7f13124968230c2f`; the projected registry SHA-256 is `2504092d92b6a27019adc12b72441b8728ce2ac35696801609f114d7813f7154`.

## Root gate

- **Truth:** external compatibility is executed by the exact pinned independent scanner; declaration is explicitly not runtime proof.
- **Agency / non-domination:** public discovery requires an explicit marker and grants no execution, install, merge, promotion, or CANON authority.
- **Continuity:** public surfaces are deterministic projections of `AXM_MODULE.json`; drift fails CI, and consumer-source drift cannot be silently substituted.
- **Wisdom before speed:** one real external consumer was added instead of broadening into a generic registry framework or claiming semantics the consumer never checks.

## Evidence ceiling

INV-19 now has real cross-repository consumer evidence for the discovery surface. That does **not** mean the discovered capabilities themselves are correct, deployed, callable, or semantically compatible with arbitrary consumers. It does not promote general model fidelity beyond seed rung 5. It also does not claim seed rung 6 for this discovery surface from a single external consumer; the counterexample packet keeps its separate already-earned rung-6 status.

## Next useful frontier

A second materially independent discovery consumer or a consumer that actually resolves one advertised capability entrypoint without executing it could raise the discovery evidence class. Repeating more local lint cases or pinning another copy of the same Discovery Buddy parser would mostly be churn and should HOLD.
