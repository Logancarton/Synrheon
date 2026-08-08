# Synrheon Architecture Plan

## Development Principle

Synrheon is developed bottom-up.

There are two different orders that must not be confused:

1. **Development foundation** — observation/runtime harness needed to test real behavior.
2. **Cognitive dependency order** — substrate and later mechanisms that build on it.

Stage 0B established the verified running organism. Later cognition must be exercised through that live path.

## Development Foundation

```text
architecture stewardship
        ↓
observable runtime + development UI
        ↓
running test organism
        ↓
cognitive substrate
        ↓
deeper cognition
```

### Stage 0A — Architecture Stewardship

Protect architectural coherence while Synrheon is designed and built.

### Stage 0B — Observable Organism Harness

Verified foundation:

```text
thin runtime
+
development UI
+
Start
+
Send Stimulus
+
Think One Step
+
Continue
+
Pause
+
Inspect State
+
Inspect Trace
```

The UI is an observation/control surface, not a cognitive owner.

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

A narrow Stage 2 sequencing foundation may be implemented while Stage 1 remains active because time is foundational to the substrate. That does not mark the whole later stage complete.

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

Concepts receive stable identities separate from display labels and later word/sense forms.

Future language systems may map many expressions onto the same concept without making the surface wording the concept itself.

### Layer 2 — World Relations

Typed relationships describe generic world structure.

Examples:

```text
Daisy IS_A dog
leash USED_FOR walk
dog HAS_PROPERTY fur
```

World relations preserve provenance and confidence.

### Layer 3 — Current Situation / Activation

Current activation is separate from concept existence and stored relationship strength.

Future sparse activation should combine:
- seeded stimulus/context
- weighted incoming support
- decay
- inhibition / competition
- bounded Top-K survival

No stored fact should disappear merely because it is not currently active.

### Layer 4 — Organism Relation

Generic semantic relevance is not enough to create organism-specific sparse activation.

Each concept may carry a separate organism-relative vector:

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

This layer answers:

```text
What does this concept mean to Synrheon,
given Synrheon's own experience and current state?
```

It remains distinct from generic world truth.

### Provenance

Initial relation provenance:

```text
injected
observed
inferred
learned
```

Injected information may bootstrap the organism but must not be silently reclassified as self-learned.

### Explicit Self Learning

The first proposed online self-vector update is:

```text
s_new = s_old + (learning_rate × trust) × (observation - s_old)
```

The explicit vector keeps evidence-event lineage even if future neural training learns a broader pattern.

### Stage 1 Activation Target

The next live cognitive mechanism should compute a bounded activation update conceptually like:

```text
next activation
=
world support
+
current context
+
organism-relative relevance
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

The first narrow foundation provides:
- current episode ID
- monotonic experience sequence
- timestamp
- elapsed episode time
- previous/next event links
- observed vs injected provenance

The current episode thread is not durable memory.

## Stage 3 — Memory + Sparse Activation

Separate:
- existence in memory
- durable memory strength
- current activation

Only a small relevant region should normally activate.

World relations may provide broad possibilities, while situation and organism-relative relevance should strongly gate which region survives.

## Stage 4 — Level 1 → Level 2 → Level 3 Retrieval

Normal retrieval cascade:

```text
LEVEL 1
coarse orientation
      ↓
LEVEL 2
relevant situation / episode / concept region
      ↓
LEVEL 3
detailed relationships / reconstruction
```

Sparse activation should operate at each level.

## Stage 5 — Scratchpad + Recursive Cognitive Loop

Initial RAM organization:

```text
CURRENT SITUATION
up to 3 condensed packages

LAST HOUR
up to 2 condensed packages

LAST DAY
up to 3 condensed packages
```

The scratchpad should contain compressed active state and pointers into deeper memory.

## Stage 6 — Problems + Trials + Solutions

Preserve:

```text
problem
↓
current model
↓
plan
↓
prediction
↓
trial
↓
outcome
↓
failure / success
↓
why
↓
highest-probability variable to change
↓
new plan
↓
solution
↓
lesson
```

Failed attempts remain remembered.

## Stage 7 — Learning + Cognitive Plasticity

Experience should modify:
- useful associations
- retrieval routes
- cognitive operation selection
- prediction reliability
- failed problem-solving routes
- variable-selection strategy
- organism-relative relevance

## Stage 8 — Consolidation + Abstraction

Progressively condense:

```text
raw events
    ↓
episodes
    ↓
patterns
    ↓
concepts
    ↓
abstractions
```

Higher layers must preserve lineage to lower-level evidence.

## Stage 9 — Multi-Layer Training

Train different aspects at different timescales.

Potential targets:
- activation behavior
- retrieval behavior
- prediction
- route selection
- semantic representation
- abstraction

Neural training may absorb regularities, but explicit experience/provenance remains separately inspectable.

## Stage 10 — Continuous Autonomous Cognition

Synrheon should eventually produce:

```text
S(t) → S(t+1)
```

even when no new external input arrives.

## Stage 11 — External Intelligence + Tools

LLMs, vision, audio, web access, code execution, robotics, and other tools may expand Synrheon.

They may own bounded neural cognition, but they should not erase Synrheon's explicit autobiographical sequence, provenance, self-relative knowledge, or durable learning lineage.
