# Synrheon Architecture Plan

## Development Principle

Synrheon is developed bottom-up. Stage 0B established the verified running organism; later cognition must be exercised through that live path.

The current architectural hypothesis is now stronger:

> **Do not primarily hand-code which cognitive path Synrheon should take. Build explicit state/process boundaries, then train the policy that chooses and evaluates short cognitive transitions.**

## Cognitive Dependency Order

```text
Stage 1   Cognitive Substrate
          + Trainable Cognitive-State / Action Policy
        ↓
Stage 2   Computational Time + Experience
        ↓
Stage 3   Durable Memory + Learned Sparse Routing
        ↓
Stage 4   Level 1 → Level 2 → Level 3 Retrieval
        ↓
Stage 5   Scratchpad + Recursive Cognition
        ↓
Stage 6   Problems + Trials + Solutions
        ↓
Stage 7   Learning + Cognitive Plasticity / Credit Assignment
        ↓
Stage 8   Consolidation + Abstraction
        ↓
Stage 9   Multi-Layer Training
        ↓
Stage 10  Continuous Autonomous Cognition
        ↓
Stage 11  External Intelligence + Tools
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

Keep the minimum explicit representations required for learned cognition:

```text
Concept identity
World relations
Open-ended organism relations
Current activation representation
Provenance
Current-process experience
```

World and organism-relative information remain separate. Injected and self-learned organism relations remain separately inspectable.

### Activation Is State, Not Policy

`ActivationState` may hold whatever concepts a future learned cognitive policy activates, but production code should not prescribe the final routing policy through fixed lexical matching, fixed edge-spreading gains, fixed decay, fixed inhibition, fixed Top-K, or fixed recurrence counts.

Those experimental heuristics were removed after demonstrating the live wiring.

## Stage 1P — Trainable Cognitive Policy

The next experimental vertical slice should learn **how to think** over knowledge rather than memorize the knowledge itself.

A training unit should look conceptually like:

```text
state before
+
available cognitive actions
        ↓
select action
        ↓
short transition / path
        ↓
checkpoint
        ↓
state after
        ↓
prediction / outcome / error
        ↓
credit assignment
```

Initial cognitive actions may be represented generically, but their usefulness and sequencing should be learned rather than bound to stimulus phrases.

Candidate operations may include functions such as focus, expand, retrieve, compare, check evidence, check sequence, predict, revise, and stop. These are an experimental action vocabulary, not world knowledge or answer rules.

### Required Transfer Experiment

Training must use multiple small unrelated knowledge worlds, then evaluate on a held-out world whose concept names and relationships were never used in training.

```text
worlds A / B / C
       ↓
learn process
       ↓
unseen world D
       ↓
useful cognitive-action sequence
```

Success means transfer exceeds an untrained/random baseline and does not collapse when concept names are changed.

## Stage 2 — Computational Time + Experience

Meaningful external and injected internal events already receive:

```text
absolute timestamp
monotonic sequence
episode ID
elapsed episode time
previous / next links
observed vs injected provenance
```

The current thread is process-local, not durable memory.

These events should become evidence and training context for later cognitive transitions.

## Stage 3 — Durable Memory + Learned Sparse Routing

Keep separate:

```text
memory exists
≠
memory strength
≠
current activation
```

Sparse routing should increasingly emerge from learned cognitive policy/state transition behavior rather than a permanent developer-selected graph propagation formula.

The architecture may still use mathematical constraints such as bounded compute, normalization, or capacity limits, but those constraints must not secretly encode domain-specific reasoning paths.

## Stage 4 — Level 1 → Level 2 → Level 3 Retrieval

```text
LEVEL 1 — coarse orientation
      ↓
LEVEL 2 — relevant situation / episode / concept region
      ↓
LEVEL 3 — detailed evidence / relationships / reconstruction
```

Retrieval becomes a cognitive operation the learned policy can choose when useful.

## Stage 5 — Scratchpad + Recursive Cognitive Loop

Initial RAM organization remains:

```text
CURRENT SITUATION — up to 3 condensed packages
LAST HOUR         — up to 2
LAST DAY          — up to 3
```

The scratchpad should expose state to the learned policy and support short checkpointed transitions rather than a monolithic hidden thought chain.

## Stage 6 — Problems + Trials + Solutions

Preserve:

```text
problem → model → plan → prediction → trial → outcome
        → why → likely variable → revised plan → solution → lesson
```

Failed attempts remain evidence. A selected path must not be reinforced merely because it was selected.

## Stage 7 — Learning + Cognitive Plasticity

Learning should modify cognitive-action selection, route usefulness, prediction reliability, failure attribution, memory access, and organism-relative learned state based on outcomes and credit assignment.

A generic update loop is:

```text
prediction
 ↓
actual outcome
 ↓
error
 ↓
which transition/action contributed?
 ↓
credit / blame
 ↓
policy changes
```

## Stage 8 — Consolidation + Abstraction

```text
raw events → episodes → patterns → concepts → abstractions
```

Higher layers must preserve lineage to lower-level evidence.

## Stage 9 — Multi-Layer Training

Potential trainable targets include:

```text
concept representation
cognitive-action policy
state-transition prediction
retrieval strategy
prediction
route usefulness
abstraction
```

The central goal is not to train a bigger answer memorizer. It is to improve transformations of internal cognitive state.

## Stage 10 — Continuous Autonomous Cognition

Synrheon should eventually produce useful:

```text
S(t) → action → S(t+1)
```

without requiring new external input, while retaining checkpoints, stopping conditions, and anti-fixation controls.

## Stage 11 — External Intelligence + Tools

LLMs, vision, audio, web access, code execution, robotics, and other tools may contribute perception, knowledge, simulation, or expression.

They must not erase Synrheon's explicit autobiographical sequence, provenance, self-relative state, or learned cognitive-process lineage.
