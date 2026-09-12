# Tractability Boundary

## Question

When does the independent all-path verifier become too expensive to justify continuing exhaustive cross-verification, even though the primary visited-state explorer is still small?

## Probe

`src/tractability_probe.py` uses one intentionally synthetic model:

- state is one integer `step`;
- two separately named legal transitions both advance `step` by one;
- both transitions therefore reconverge on the same next state;
- the invariant only checks that `step` remains inside the declared probe depth.

This shape is useful because it separates two costs cleanly:

- visited-state exploration grows with unique reachable states;
- all-path enumeration grows with path multiplicity.

The retained probe uses a **100,000 path-node budget** and depths 12, 15, and 16. It records deterministic work counts rather than wall-clock timing.

## Retained result

| depth | primary unique states | primary status | reference path nodes | reference complete | reference status |
|---:|---:|---|---:|---|---|
| 12 | 13 | PASS | 8,191 | yes | PASS |
| 15 | 16 | PASS | 65,535 | yes | PASS |
| 16 | 17 | PASS | 100,000 | no | HOLD |

The important result is not that depth 16 is a universal limit. It is that **the current independent path verifier has a demonstrable workload shape where exhaustive cross-checking becomes intractable long before visited-state exploration does**. Its existing fail-closed behavior is therefore necessary: budget exhaustion remains HOLD and can never silently become PASS.

## Operational consequence

- Use the reference path verifier as a bounded independent cross-check, not as a universal second engine for arbitrarily deep models.
- Treat path-node budget exhaustion as evidence that the comparison is incomplete, not evidence against the primary result.
- Prefer smaller models, smaller bounds, or a justified different verification method when path multiplicity dominates.
- Do not raise the budget merely to force PASS without an explicit resource/evidence reason.
- A future solver/model-checker comparison is justified only against a model whose semantics are already grounded and when this measured boundary blocks a useful verification question.

## Truth boundary

This probe measures only the repository's current two exploration strategies on one authored reconverging model. It does **not** establish general Python performance, memory ceilings, arbitrary AXM model tractability, solver performance, donor-runtime cost, or real-world safety.

No wall-clock benchmark is retained because host/load variance would turn a deterministic evidence artifact into environmental noise.

## Authority boundary

The tractability result recommends where verification should HOLD or change method. It grants no execution, merge, installation, device, network, promotion, or CANON authority.
