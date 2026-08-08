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

Create the minimum representations required for Synrheon to possess and later transform internal state.

The initial substrate is intentionally layered:

```text
LAYER 1 — CONCEPT IDENTITY
What is this?

LAYER 2 — WORLD RELATIONS
How can things relate in general?

LAYER 3 — CURRENT SITUATION / ACTIVATION
What is active now?

LAYER 4 — ORGANISM RELATION
What does this mean to Synrheon?
```

### Layer 1 — Concept Identity

Concepts receive stable identities separate from display labels and later word/sense forms. Future language systems may map many expressions onto the same concept without making the surface wording the concept itself.

### Layer 2 — World Relations

Typed relationships describe generic world structure, for example:

```text
Daisy IS_A dog
leash USED_FOR walk
dog HAS_PROPERTY fur
```

World relations preserve source/provenance, confidence, and later evidence lineage.

### Layer 3 — Current Situation / Activation

Current activation is separate from concept existence and stored relationship truth.

Future sparse activation should combine seeded context, weighted support, organism-relative relevance, decay, inhibition/competition, and bounded Top-K survival.

### Layer 4 — Organism Relation

Generic semantic relevance is not enough to produce organism-specific sparse activation.

Each concept may carry two permanently separate organism-relative representations:

```text
injected_self_vector
self_learned_vector
```

Both initially use:

```text
ownership
experience
social
goal
history
knowledge
trust
prediction
consequence
preference
uncertainty
```

The injected vector answers what Synrheon was explicitly told about how something relates to her.

The learned vector answers what Synrheon has accumulated from her own trusted experience.

They may both influence future activation, but they must remain separately inspectable.

### Provenance

Initial provenance categories:

```text
injected
observed
inferred
learned
```

Injected information may bootstrap the organism but must never silently become self-learned.

### Explicit Self Learning

Only the learned vector is updated by experience:

```text
learned_new
=
learned_old
+
(learning_rate × trust)
×
(observation - learned_old)
```

The injected vector remains unchanged. Learned confidence and supporting experience-event IDs remain explicit outside future neural weights.

### Stage 1 Activation Target

The next real cognitive mechanism should compute a bounded activation update conceptually like:

```text
next activation
=
world support
+
current context
+
injected self relevance
+
self-learned relevance
+
goal / recent relevance
-
competition
-
decay
```

followed by sparse selection.

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

The current episode thread is not durable memory.

## Stage 3 — Memory + Sparse Activation

Separate:

```text
memory exists
≠
memory strength
≠
current activation
```

World relations may provide broad possibilities while situation and organism-relative relevance strongly gate which small region survives.

## Stage 4 — Level 1 → Level 2 → Level 3 Retrieval

```text
LEVEL 1 — coarse orientation
      ↓
LEVEL 2 — relevant situation / episode / concept region
      ↓
LEVEL 3 — detailed evidence / relationships / reconstruction
```

Sparse activation should operate at each level.

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

Experience should modify useful associations, retrieval routes, cognitive-operation selection, prediction reliability, failed routes, variable-selection strategy, and self-learned relevance without rewriting provenance.

## Stage 8 — Consolidation + Abstraction

```text
raw events → episodes → patterns → concepts → abstractions
```

Higher layers must preserve lineage to lower-level evidence.

## Stage 9 — Multi-Layer Training

Potential targets include activation behavior, retrieval, prediction, route selection, semantic representation, and abstraction.

Neural training may absorb regularities, but explicit injected/self-learned vectors, experience, and provenance remain separately inspectable.

## Stage 10 — Continuous Autonomous Cognition

Synrheon should eventually produce:

```text
S(t) → S(t+1)
```

even when no new external input arrives.

## Stage 11 — External Intelligence + Tools

LLMs, vision, audio, web access, code execution, robotics, and other tools may expand Synrheon. They may own bounded neural cognition, but they must not erase Synrheon's explicit autobiographical sequence, provenance, self-relative state, or durable learning lineage.
