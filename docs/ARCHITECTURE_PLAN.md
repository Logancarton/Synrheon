# Synrheon Architecture Plan

## Development Principle

Synrheon is developed bottom-up. Stage 0B established the verified running organism; later cognition must be exercised through that live path.

## Cognitive Dependency Order

```text
Stage 1  Cognitive Substrate
        ↓
Stage 2  Computational Time + Experience
        ↓
Stage 3  Memory + Sparse Activation
        ↓
Stage 4  Level 1 → Level 2 → Level 3 Retrieval
        ↓
Stage 5  Scratchpad + Recursive Cognition
        ↓
Stage 6  Problems + Trials + Solutions
        ↓
Stage 7  Learning + Cognitive Plasticity
        ↓
Stage 8  Consolidation + Abstraction
        ↓
Stage 9  Multi-Layer Training
        ↓
Stage 10 Continuous Autonomous Cognition
        ↓
Stage 11 External Intelligence + Tools
```

A narrow later-stage foundation may be pulled forward when an earlier stage fundamentally depends on it. This does not mark the later stage complete.

## Stage 0B — Observable Organism Harness

Verified development foundation:

```text
thin runtime
+
development UI
+
Start / Stimulus / Step / Continue / Pause
+
State / Trace observation
```

The UI controls and observes. Runtime sequences and routes. Neither owns cognition.

## Stage 1 — Cognitive Substrate

Create the minimum representations required for Synrheon to possess and transform internal state.

The substrate is intentionally layered:

```text
LAYER 1 — CONCEPT IDENTITY
What is this?

LAYER 2 — WORLD RELATIONS
How can things relate in general?

LAYER 3 — CURRENT SITUATION / ACTIVATION
What is active now?

LAYER 4 — ORGANISM RELATIONS
How does this relate to Synrheon?
```

### Layer 1 — Concept Identity

Concepts receive stable identities separate from display labels and later word/sense forms. Future learned language systems may map many expressions onto the same concept without making surface wording the concept itself.

### Layer 2 — World Relations

Typed relationships describe generic world structure, for example:

```text
Daisy IS_A dog
leash USED_FOR walk
dog HAS_PROPERTY fur
```

World relations preserve provenance, confidence, and later evidence lineage.

### Layer 3 — Current Situation / Activation

Current activation is separate from concept existence and stored relationship truth.

The first live activation mechanism now combines:

```text
known-concept stimulus seed
+
decayed current-round activation
+
normalized directed world-relation support
+
organism-relative salience on already-reached concepts
-
competition
        ↓
bounded Top-K sparse active region
```

This is the first real cognitive state transformation in the live organism. Its current hyperparameters are experimental and should later adapt rather than remain sacred constants.

### Layer 4 — Organism Relations

Generic semantic relevance is not enough to produce organism-specific sparse activation.

Synrheon represents how a concept relates to herself using **open-ended typed data**, not a fixed developer ontology.

Examples may include:

```text
protective_of
expects_help_from
reminds_me_of_home
trusted_source
```

These are examples only. New relation types must be representable without adding Python fields or editing an allowed-values list.

For each concept, two collections remain permanently separate:

```text
injected_relations
learned_relations
```

The injected collection records what Synrheon was explicitly told. The learned collection records organism-relative regularities accumulated from trusted experience.

In the first activation mechanism, relation names are not semantically interpreted. Their `strength × confidence` contributes generic salience only after that concept has already been reached by the current cue/world spread. This prevents unrelated personally important concepts from globally activating.

### Provenance

Initial broader provenance categories remain:

```text
injected
observed
inferred
learned
```

Injected information may bootstrap the organism but must never silently become self-learned.

### Explicit Self Learning

For one arbitrary learned organism relation type:

```text
learned_new
=
learned_old
+
(learning_rate × trust)
×
(observed_strength - learned_old)
```

The corresponding injected relation remains unchanged. Learned confidence and supporting experience-event IDs remain explicit outside future neural weights.

Automatic discovery of which relation type an experience implies is **not implemented yet**.

### Current Text-to-Concept Bootstrap

The first live path needs a bounded way for injected language to touch the substrate before a learned language system exists.

Current bridge:

```text
normalized text tokens
        ↓
existing concept ID / label phrase match
        ↓
concept activation seed
```

This is deliberately described as **lexical cueing**, not semantic understanding. No domain-specific phrase rules are allowed.

Later perception may use embeddings, a neural encoder, or an LLM-derived semantic representation to propose concept/sense activations, while the sparse activation owner remains in Synrheon cognition.

## Stage 2 — Computational Time + Experience

Give meaningful external and internal events a position in Synrheon's existence.

Initial temporal dimensions:

```text
absolute time
sequence number
relative / elapsed time
before / after relationships
episode membership
temporal context
day membership
recent trajectory
```

The first narrow foundation provides current episode ID, monotonic experience sequence, timestamp, elapsed episode time, previous/next event links, and observed vs injected provenance.

Each textual experience can now also point to an observable `CognitiveFrame` describing the activation consequence of that event.

The current episode thread is not durable memory.

## Stage 3 — Memory + Sparse Activation

Keep separate:

```text
memory exists
≠
memory strength
≠
current activation
```

### Sparse Activation — First Slice Integrated

The first sparse-activation slice is intentionally generic:

```text
seed
 ↓
recurrent spread
 ↓
personal salience gating
 ↓
inhibition
 ↓
Top-K winners
```

Outgoing fan-out is normalized so one source concept cannot produce unbounded total support merely because it has many outgoing edges.

The current mechanism respects directed world relations and does not enumerate organism-relation meanings.

### Durable Memory — Not Started

The live experience thread and activation frames still disappear when the Python process stops.

Durable memory must later persist evidence while keeping current activation separate.

## Stage 4 — Level 1 → Level 2 → Level 3 Retrieval

```text
LEVEL 1 — coarse orientation
      ↓
LEVEL 2 — relevant situation / episode / concept region
      ↓
LEVEL 3 — detailed evidence / relationships / reconstruction
```

Sparse activation should operate at each level rather than searching lifetime memory uniformly.

## Stage 5 — Scratchpad + Recursive Cognitive Loop

Initial RAM organization:

```text
CURRENT SITUATION — up to 3 condensed packages
LAST HOUR         — up to 2
LAST DAY          — up to 3
```

The scratchpad contains compressed active state and pointers into deeper memory.

## Stage 6 — Problems + Trials + Solutions

Preserve:

```text
problem → model → plan → prediction → trial → outcome
        → why → likely variable → revised plan → solution → lesson
```

Failed attempts remain remembered.

## Stage 7 — Learning + Cognitive Plasticity

Experience should modify useful associations, retrieval routes, cognitive-operation selection, prediction reliability, failed routes, variable-selection strategy, activation behavior, and organism-relative learned relations without rewriting provenance.

The current fixed activation hyperparameters are experimental starting values. Later learning may adapt them or replace them with learned policies if evidence supports that change.

## Stage 8 — Consolidation + Abstraction

```text
raw events → episodes → patterns → concepts → abstractions
```

Higher layers must preserve lineage to lower-level evidence.

## Stage 9 — Multi-Layer Training

Potential targets include activation behavior, retrieval, prediction, route selection, semantic representation, and abstraction.

Neural training may absorb regularities, but explicit injected/learned organism relations, experience, and provenance remain separately inspectable.

## Stage 10 — Continuous Autonomous Cognition

Synrheon should eventually produce:

```text
S(t) → S(t+1)
```

even when no new external input arrives.

The current Chat-triggered bounded recurrence is not autonomous continuation.

## Stage 11 — External Intelligence + Tools

LLMs, vision, audio, web access, code execution, robotics, and other tools may expand Synrheon. They may own bounded neural cognition, but they must not erase Synrheon's explicit autobiographical sequence, provenance, self-relative state, or durable learning lineage.
