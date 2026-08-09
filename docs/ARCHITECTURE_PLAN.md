# Synrheon Architecture Plan

## Development Principle

Synrheon is developed bottom-up. Stage 0B established the verified running organism; later cognition must be exercised through that live path.

The current architectural hypothesis is:

> **Do not primarily hand-code which cognitive path Synrheon should take. Build explicit state/process boundaries, then train the policy that chooses and evaluates short cognitive transitions.**

The goal is not to remove all designed structure. Synrheon still needs explicit representations, provenance, budgets, training boundaries, safe validation, and owner separation. The change is that useful cognitive routing should increasingly be **learned from outcomes**, not encoded as permanent domain rules.

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

The first trainable cognition slice should learn **how to perform cognitive work over explicit state** rather than memorize the world being used for training.

### Cognitive micro-cycle

The fundamental unit is one bounded transition:

```text
S(t)
 +
available cognitive operations
        ↓
policy selects a(t)
        ↓
execute one bounded cognitive operation
        ↓
S(t+1) checkpoint
        ↓
continue / redirect / stop
```

A checkpoint is an inspectable internal-state boundary. It is not a forced real-time delay.

### Initial cognitive operations

The first experiment may expose a small operation vocabulary:

```text
FOCUS
EXPAND
RETRIEVE
COMPARE
CHECK_SEQUENCE
CHECK_EVIDENCE
PREDICT
REVISE
STOP
```

These operations define **what kinds of mental work are possible**, not when they should be used. The sequencing policy should be learned.

The initial vocabulary is experimental. Later systems may learn finer operations, compose primitives, compress repeated action sequences into higher-level skills, or replace discrete actions with a continuous action representation.

### Parameterized cognitive actions

Action families must not hide the real cognitive choice in Python. A useful action representation should be able to include its target or scope:

```text
RETRIEVE(target, region, depth)
COMPARE(left, right, evidence_scope)
FOCUS(candidate_region)
EXPAND(candidate_path)
PREDICT(target_state_feature)
REVISE(belief_or_route)
```

The model should increasingly learn both the operation and what it should act upon. The first slice may deliberately constrain the parameter space, but the architecture must not require a developer-authored target selector to make the action meaningful.

### Trainable policy

The central policy is conceptually:

```text
P(cognitive_action | CognitiveState)
```

The policy input should describe the current cognitive problem/state, not leak the correct answer.

### Transition model

A second useful learned component predicts what a cognitive action is expected to accomplish:

```text
predicted S(t+1) = F(S(t), a(t))
```

The difference between predicted and observed next state becomes learning evidence rather than merely another score chosen by the developer.

### Expected cognitive value

A third conceptually distinct learned quantity is:

```text
V(S, a)
```

This estimates whether an available cognitive action is worth taking from the current state. A valid action may still be low-value because it is redundant, too expensive, or unlikely to reduce uncertainty.

Policy, transition prediction, and value may initially share a compact model, but the architecture should not collapse these questions into one opaque score.

### Training trace

Each trace should preserve:

```text
state_before
available_actions
selected_action
transition / short path
state_after
prediction
outcome
error / correction
credit
```

The training system must distinguish:

```text
path selected
≠
path useful
```

A route receives reinforcement only when later evidence supports its usefulness.

### Cognitive utility and cost

Correctness alone is not enough. A policy that retrieves, expands, and compares everything is not sparse cognition.

Evaluation should increasingly consider:

```text
task success / useful progress
-
compute cost
-
unnecessary steps
-
invalid or redundant actions
```

A hard maximum cognitive budget remains designed infrastructure. Within that ceiling, the learned policy should prefer efficient cognition. Exact utility weights remain experimental rather than permanent architecture constants.

## What Is Designed vs Learned

### Designed cognitive physics

Architecture may explicitly define:

```text
state schema
action interface
provenance
checkpoint recording
maximum cognitive budget
safe stopping ceiling
training-record schema
outcome / correction interfaces
parameter persistence
validation and failure behavior
```

### Learned cognitive skill

Training should increasingly own:

```text
attention / focus
concept organization
candidate-path ranking
cognitive-action selection
action targets / parameters
retrieval timing
comparison strategy
prediction strategy
revision strategy
route usefulness
credit assignment
stopping preference within the hard safety ceiling
```

This distinction should be reviewed whenever new cognition is proposed. A new production `if/then` rule that says **what thought to have** is a warning sign.

## Concept Training

Concepts are not merely words. The architecture should allow concept representations to become trainable while preserving explicit identities and provenance-bearing evidence outside neural weights.

Potential learned concept information includes:

```text
similarity
functional role
context compatibility
predictive usefulness
relation patterns
organism relevance
cross-modal grounding
```

Concept learning must not make the neural representation the sole authority for factual provenance.

## Organization / Routing Training

A separate training target should learn which regions of state are useful together.

Instead of hard-coding:

```text
relation X always spreads to target Y with gain Z
```

Synrheon should eventually learn:

```text
when this current state resembles prior useful situations,
which candidate region or transition deserves compute next?
```

This is where sparse cognition can emerge from learned route selection rather than a permanent spreading formula.

## Language Boundary

Language is not the cognition owner.

```text
text / observation
        ↓
perception / grounding
        ↓
concept/state representation
        ↓
trainable cognitive process
        ↓
state result
        ↓
optional language expression
```

Tokenization may be part of the input adapter. It should not dictate the thought process.

A future LLM may participate in perception, concept proposal, outside knowledge, simulation, or expression, but Synrheon's persistent state, provenance, cognitive-process traces, and learning effects remain explicit owners.

## Generated Curriculum Requirement

The primary E011 curriculum should come from a deterministic seeded world/task generator rather than a small hand-written set of examples.

A generator may define experiment rules and retain hidden ground truth for scoring while exposing only legitimate task state to the cognitive policy.

Generated variation should include:

```text
concept identities
relation identities / encodings
graph topology
task targets
starting focus
irrelevant distractors
required cognitive-step count
```

Hand-authored worlds remain useful for debugging and human interpretation, but cannot be the main evidence for general cognitive skill.

## Required Transfer Experiment

The first model experiment must test **process transfer** rather than answer accuracy alone.

```text
worlds A / B / C
       ↓
learn process
       ↓
unseen world D
       ↓
useful cognitive-action sequence
```

### Anti-memorization controls

At minimum:

```text
held-out concept identities
randomized / opaque concept names
concept-name permutation evaluation
no correct answer embedded in policy features
no production world-specific branches
untrained/random baseline
```

A stronger second evaluation should vary graph/world topology so success cannot come from memorizing one structural template.

### Generalization ladder

Claims should name the strongest demonstrated level:

```text
Level 0 — Training memorization
same training worlds/tasks

Level 1 — Identity transfer
new or renamed concepts with comparable structure

Level 2 — Structural transfer
new concepts + changed topology / relation arrangement

Level 3 — Compositional transfer
new knowledge + new structure + novel combinations of cognitive demands
```

Passing Level 1 does not imply Level 2 or 3.

### Counterfactual credit direction

The learning trace should preserve the alternatives available at a checkpoint so later credit assignment can distinguish:

```text
action correlated with success
from
action likely contributed to success
```

Counterfactual estimates may initially be approximate or deferred, but the architecture should allow comparison of chosen actions against plausible alternatives rather than reinforcing whatever happened during a successful episode.

### Meaningful pass condition

The experiment is promising only if the learned policy:

```text
improves with training
+
beats baseline on unseen content
+
survives concept renaming
+
performs useful multi-step action sequences
+
produces inspectable checkpoints
+
uses cognitive resources more economically than exhaustive search
```

If it only becomes better at the training worlds, it learned content or shortcuts rather than a reusable cognitive skill.

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

Future temporal state should also expose:

```text
before / after
relative recency
episode boundaries
day membership
elapsed intervals
recent trajectory
```

without requiring cognition to search all prior experience uniformly.

## Stage 3 — Durable Memory + Learned Sparse Routing

Keep separate:

```text
memory exists
≠
memory strength
≠
current activation
≠
route usefulness
```

Sparse routing should increasingly emerge from learned cognitive policy/state-transition behavior rather than a permanent developer-selected graph propagation formula.

The architecture may still use mathematical constraints such as bounded compute, normalization, capacity limits, and explicit memory tiers, but those constraints must not secretly encode domain-specific reasoning paths.

## Stage 4 — Level 1 → Level 2 → Level 3 Retrieval

```text
LEVEL 1 — coarse orientation
      ↓
LEVEL 2 — relevant situation / episode / concept region
      ↓
LEVEL 3 — detailed evidence / relationships / reconstruction
```

Retrieval becomes a cognitive operation the learned policy can choose when useful.

The levels constrain search cost; they should not dictate the answer.

## Stage 5 — Scratchpad + Recursive Cognitive Loop

Initial RAM organization remains:

```text
CURRENT SITUATION — up to 3 condensed packages
LAST HOUR         — up to 2
LAST DAY          — up to 3
```

The scratchpad should expose state to the learned policy and support short checkpointed transitions rather than a monolithic hidden thought chain.

Repeated useful micro-cycles may eventually become compressed cognitive skills.

## Stage 6 — Problems + Trials + Solutions

Preserve:

```text
problem → model → plan → prediction → trial → outcome
        → why → likely variable → revised plan → solution → lesson
```

Failed attempts remain evidence. A selected path must not be reinforced merely because it was selected.

## Stage 7 — Learning + Cognitive Plasticity

Learning should modify cognitive-action selection, route usefulness, prediction reliability, failure attribution, memory access, and organism-relative learned state based on outcomes and credit assignment.

Generic loop:

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
policy / transition model changes
```

Different learning rates may eventually apply across timescales:

```text
immediate activation / working state
short-term route adaptation
episode-level usefulness
longer consolidation / abstraction
strategic neural training
```

## Stage 8 — Consolidation + Abstraction

```text
raw events → episodes → patterns → concepts → abstractions
```

Higher layers must preserve lineage to lower-level evidence.

A repeated successful cognitive sequence may also become a reusable higher-level cognitive skill, but compression must preserve the ability to inspect its evidence and failure conditions.

## Stage 9 — Multi-Layer Training

Potential trainable targets include:

```text
concept representation
organization / routing
cognitive-action policy
state-transition prediction
expected cognitive value
retrieval strategy
prediction / revision
route usefulness
credit assignment
abstraction
```

The central goal is not to train a bigger answer memorizer. It is to improve transformations of internal cognitive state.

## Stage 10 — Continuous Autonomous Cognition

Synrheon should eventually produce useful:

```text
S(t) → action → S(t+1)
```

without requiring new external input, while retaining checkpoints, stopping conditions, resource budgets, and anti-fixation controls.

Autonomy should not be added until the cognitive policy can demonstrate useful bounded transitions under direct stimulation.

## Stage 11 — External Intelligence + Tools

LLMs, vision, audio, web access, code execution, robotics, and other tools may contribute perception, knowledge, simulation, or expression.

They must not erase Synrheon's explicit autobiographical sequence, provenance, self-relative state, or learned cognitive-process lineage.
