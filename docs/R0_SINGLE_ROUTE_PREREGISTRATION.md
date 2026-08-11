# R0-SR1 Preregistration — Single-Route Partial-Cue Access Baseline

**Synrheon relational cognition track**  
**Status: FROZEN before the first assay run**

## Question

Before asking Synrheon to discover or combine multiple latent relationship channels, can one isolated route reliably make an encoded memory reachable from a partial cue under a fixed candidate-field budget?

R0-SR1 is an **instrument and baseline test**, not evidence that latent multi-route cognition works.

It deliberately supplies the route index to the isolated retriever so that one route can be tested at a time. A later experiment must remove that oracle isolation and learn route/channel assignment from visible structure.

## Why this comes first

The larger R0 hypothesis is about memory access through multiple learned relational routes. A multi-route result is uninterpretable if the underlying harness cannot first show all of the following:

```text
one stored route can retrieve its memory
partial information broadens rather than silently deletes
structural ambiguity can consume a fixed field
missing evidence does not receive hidden target help
one route cannot borrow evidence from another route
```

This baseline therefore tests route access before channel emergence, coincidence, composition, learned resistance, or recollapse.

## Frozen scope

Use a deterministic synthetic mechanism world with:

```text
memories:                     128
hidden generator route slots: 4
route group sizes:             8, 16, 32, 64
fixed candidate field:         32
route signature:               anchor concept + detail concept
concept IDs:                   opaque
memory IDs:                    opaque
learning:                      none
multi-route merge:             none
coincidence:                   none
composition:                   none
recurrence:                    none
least-resistance learning:     none
natural language:              none
```

The four route slots are hidden generator structure. Human semantic labels such as temporal, social, causal, or spatial are not used.

R0-SR1 uses only a **family-A mechanism generator**. It does not claim A/B/C structural transfer. Future generator families B and C must differ structurally rather than merely by seed or renamed IDs.

## Representation

Each stored memory `m` has one binding in each route slot `k`:

```text
binding(m, k) = {anchor(m, k), detail(m, k)}
```

Within a route slot:

- `detail(m, k)` is unique to that memory;
- `anchor(m, k)` is shared by a group of memories;
- group size controls ambiguity/interference;
- route slots use disjoint opaque concept identities.

The isolated single-route retriever receives:

```text
cue concept IDs
route index k
fixed field size 32
```

It does **not** receive the target memory ID.

The target label is held by the experiment only for scoring after retrieval.

## Frozen single-route scoring rule

For candidate memory `m`, route `k`, and cue concept set `C`:

```text
score(m | C, k) = |C ∩ binding(m, k)| / |C|
```

If the cue is empty, the score is zero.

Candidates are sorted by descending score and then by opaque memory ID for deterministic tie handling. The returned field is exactly the first 32 memories.

This is intentionally simple. R0-SR1 is checking the access instrument, not proposing this overlap rule as Synrheon's final relational cognition.

## Conditions

Every memory is probed in every route slot.

### F — full route cue

Cue contains the target memory's route anchor and unique route detail.

```text
{correct anchor, correct detail}
```

Purpose: verify that a complete single route can identify its stored memory without target leakage.

### P — partial route cue

Cue contains only the shared route anchor.

```text
{correct anchor}
```

Purpose: verify broad partial-cue access under controlled structural ambiguity.

Expected aggregate `Hit@32` is determined entirely by route group size:

```text
group size  8 -> 1.00
group size 16 -> 1.00
group size 32 -> 1.00
group size 64 -> 0.50
```

The 64-member route is deliberately wider than the field. A fixed 32-memory field therefore forces ambiguity/interference to evict half of the equally supported targets across the complete probe set.

### N — noisy route cue

Cue contains the correct anchor plus a detail concept belonging to a memory outside the target's anchor group.

```text
{correct anchor, foreign detail}
```

Purpose: expose competition without changing the field budget. This condition is diagnostic; no supportive threshold is attached to its exact value in R0-SR1.

### M — missing route cue

Cue contains one opaque concept that is not bound to any memory in the tested route.

Purpose: negative control for hidden target leakage.

Because every candidate receives zero support and every memory is used exactly once as a target, aggregate `Hit@32` must equal field capacity by chance:

```text
32 / 128 = 0.25
```

### W — wrong-route cue

Use the target's cue concepts from another route slot while retrieval is restricted to route `k`.

Purpose: verify route isolation. Since concept identities are disjoint across route slots, the tested route receives no matching evidence.

Aggregate `Hit@32` must therefore also equal:

```text
0.25
```

## Primary integrity metrics

For every route report:

```text
full Top1
full Hit@32
partial Hit@32
noisy Hit@32
missing Hit@32
wrong-route Hit@32
```

Also report the fixed field size and route group size.

## Frozen integrity verdict

`SINGLE_ROUTE_INSTRUMENT_VALID` requires all of the following for every route:

```text
full Top1 = 1.00
full Hit@32 = 1.00
partial Hit@32 = min(1.00, 32 / route_group_size)
missing Hit@32 = 0.25
wrong-route Hit@32 = 0.25
every returned field contains exactly 32 memories
```

If any condition fails, the harness is invalid and must be fixed before multi-route work begins.

The noisy condition is preserved for diagnosis but does not change the frozen validity verdict.

## What a valid result means

A valid R0-SR1 result establishes only that:

```text
single-route binding is represented correctly
partial cues create measurable ambiguity
fixed field capacity converts ambiguity into retrieval loss
missing/wrong-route evidence receives no target assistance
routes are isolated cleanly enough for later controlled comparisons
```

It does **not** establish:

- that multiple routes outperform one route;
- that latent channels can emerge;
- that K=4 is optimal;
- that channels will avoid collapse;
- that coincidence detection is useful;
- that learned relationship composition is useful;
- that least-resistance propagation is useful;
- that the mechanism transfers outside its generator;
- that the mechanism is natural-language cognition.

## Hidden-information firewall

The retriever may use only:

```text
stored route bindings
cue concepts
isolated route index
fixed field size
```

It may not use:

```text
target memory ID
probe condition label
future multi-route information
human semantic relation labels
correct-answer metadata
```

The route index is an explicit oracle isolation variable in R0-SR1 and must not be mistaken for learned channel identity.

## Seeds and determinism

The world generator uses an explicit seed. Opaque identifiers and route partitions must be deterministic for a given seed.

Integrity tests may use more than one seed, but no seed may be selected because it produces a preferred scientific outcome.

## Next gate

Only after R0-SR1 is valid should the next step test a **single learned route/channel** on the same access problem.

The intended progression is:

```text
R0-SR1  explicit isolated route integrity
    ↓
R0-SR2  one learned channel, partial-cue objective
    ↓
R0-MR1  K=4 latent channels, no coincidence/composition
    ↓
family B development diagnosis
    ↓
freeze
    ↓
family C structural-transfer verdict
```

R0-MR1 must not inherit the oracle route index as a model input.
