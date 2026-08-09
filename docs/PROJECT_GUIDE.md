# Synrheon Project Guide — Plain English

This is the human-readable owner's manual for Synrheon. It explains what each important file owns, what is live now, what is only designed, and what the next experiment is actually trying to prove.

Always distinguish **current real behavior** from **planned responsibility**.

# The Mental Model

Synrheon is not trying to become intelligent by adding more hand-written rules for what to think next.

The direction is:

```text
KNOWLEDGE / EXPERIENCE
        ↓
CURRENT COGNITIVE STATE
        ↓
LEARNED COGNITIVE SKILL
        ↓
NEXT COGNITIVE STATE
        ↓
checkpoint
        ↓
repeat only if useful
```

In plain English:

> **We define the safe pieces and boundaries of cognition. Synrheon learns which mental move is useful next.**

A useful shorthand remains:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

# Current Real Flow

```text
YOU
 ↓
Development UI
 ↓
interfaces.py
 ↓
runtime.py
 ↓
time.py + experience.py + core.py
 ↓
state / trace
 ↓
Organism UI
```

The future learned thinking owner remains `cognition.py`, but it intentionally contains no hand-written thinking policy right now.

# Current Project Status

```text
Stage 0B — Observable Organism Harness       Verified
Stage 1  — Cognitive Substrate               Built / partially integrated
Stage 2  — Time + Experience                 Integrated foundation
Stage 1P — Trainable Cognitive Policy        Designed, not implemented
E011-A   — Controlled learning experiment    Fully preregistered, not implemented
E011-B   — Live cognition integration        Designed, not implemented
```

The previous lexical-match → relation-spread → fixed Top-K cognition experiment has been removed from production.

That means Chat currently records experience without pretending that a developer-selected graph heuristic is intelligence.

# What Synrheon Can Do Now

Synrheon can currently:
- run through the browser/runtime UI;
- start, pause, continue, and step the observable harness;
- record external Chat as `observed` experience;
- record Internal Thought injection as `injected` experience;
- maintain current-episode time, sequence, elapsed time, and previous/next links;
- hold explicit concepts;
- hold typed world relations;
- hold open-ended organism-relative relations;
- keep injected and self-learned organism relations separate;
- keep activation representation separate from stored knowledge;
- expose live state and trace;
- show the integrated stage and live backend-owned evidence in the **Organism** UI;
- reserve a real cognitive-growth surface for later backend learning metrics.

Synrheon currently **does not**:
- automatically decide which concepts should activate from text;
- choose cognitive actions through a trained model;
- perform checkpointed learned thought transitions;
- retrieve durable memory;
- reason recursively;
- generate natural-language answers;
- learn from live outcomes.

# What We Mean by “Train How to Think”

The long-term system may learn mental operations such as:

```text
focus
expand
retrieve
compare
check evidence
predict
revise
stop
```

But the first experiment should not try to teach all of those at once.

The next research question is much narrower:

> **Can Synrheon learn where to spend limited cognitive effort next, and can that learned process still work in completely new generated worlds?**

# E011-A — The First Actual Learning Experiment

E011-A is the controlled scientific test before we wire a learned model into the live organism.

It is deliberately small so we can tell whether learning actually happened.

## What one generated world looks like

Every task contains:

```text
10–14 anonymous nodes
1 visible starting node
1 hidden goal node
1 shortest route to the goal that is 3–5 edges long
2–4 distracting branches
sometimes 0–2 cross/back connections
10 mental actions maximum
```

The nodes do not have meaningful names like “dog,” “Daisy,” or “door.” They are opaque generated identities.

The goal is hidden. Synrheon must reveal the graph a little at a time.

## What Synrheon is allowed to do first

For E011-A v1 there are only two mental actions:

```text
EXPAND(target)
STOP
```

### EXPAND(target)

Synrheon chooses one currently available frontier node to inspect next.

That reveals the outgoing local structure from that node.

It costs one of the 10 available cognitive steps.

The software is allowed to tell Synrheon which targets are valid choices. The software is **not** allowed to pick which valid target is best.

### STOP

Synrheon ends the task.

If the goal has already been revealed, that is success.

If she stops before the goal is visible, that is a failure.

This also costs one cognitive step.

# Why Such a Simple First Experiment?

Because this lets us isolate the first thing we care about:

```text
several possible places to spend compute
        ↓
limited budget
        ↓
choose where to look next
        ↓
learn from many examples
        ↓
become better at choosing
        ↓
use that process on worlds never seen before
```

If this does not work, adding memory, language, retrieval, autonomy, and more operations would only make the failure harder to understand.

# What Synrheon Is Allowed to See

The policy can see only what has legitimately been revealed so far:

```text
which cognitive step she is on
how many steps remain
revealed nodes
revealed connections
which nodes are still available to expand
which have already been expanded
known depth from the starting node
reveal order
whether a revealed node is the goal
available valid actions + targets
what she just did
```

# What Synrheon Must Never See

This is the anti-cheating wall:

```text
hidden nodes
hidden connections
where the goal actually is before it is revealed
the shortest solution route
distance from a candidate to the goal
“this node is on the correct route”
the correct next action
the correct next target
what will be revealed in the future
the experiment solver's answer
```

The experiment/scoring code can know those things because it has to judge performance.

The cognitive policy cannot.

If hidden answer information enters the policy, the experiment is invalid even if the score is excellent.

# Training and Test Worlds Are Frozen Before Coding

The world seeds are fixed now:

```text
Training worlds
1000–4999

Development validation worlds
5000–5999

Final untouched Level-1 worlds
10000–10999

Renaming/permutation control
same final worlds + permutation seeds 20000–20999

Future Level-2 structural worlds
30000–30999
```

Five model training seeds are also frozen:

```text
11
22
33
44
55
```

We report all five. We do not pick the one that happened to look best.

The final 10000–10999 worlds are **not allowed to become our practice test**.

If we inspect the final results and then change the model to improve those exact results, that becomes a new experiment version with a new untouched final set.

# What We Compare Against

We will compare Synrheon's trained policy with:

```text
random valid choices
same model before training
same model after training
brute-force / exhaustive exploration cost
```

That helps answer several different questions:

```text
Did training change anything?
Did it beat chance?
Did improvement survive unfamiliar worlds?
Did it survive renamed identities?
Did it become efficient, or just search everything?
```

# The First Numeric Gate Is Already Chosen

We are not going to wait for results and then decide what “good” means.

E011-A v1 requires all of these major conditions:

```text
At least 4 of 5 trained models improve training success
by at least 20 percentage points over their own untrained version.

Median success on untouched final worlds must be at least 70%.

Median final-world performance must beat BOTH random and untrained
by at least 20 percentage points.

At least 4 of 5 model runs must individually beat both baselines
by at least 15 percentage points.

Renaming the identities must retain at least 95% of performance,
with no more than a 5-point median drop.

Successful cognition should use no more than 80% of brute-force cost.

Average use of the 10-step budget must stay at or below 80%
while still meeting the success thresholds.
```

And regardless of numbers:
- no hidden answer leakage;
- no world-specific special cases;
- no Python code secretly picking the good target;
- all five model results are reported.

Those numbers belong to **E011-A v1**, not to Synrheon forever.

# Failure Is Already Categorized

If the experiment fails, we do not immediately patch the example.

We classify the failure:

```text
FAILED LEARNING
Training itself did not improve enough.

MEMORIZATION / OVERFIT
Training became good, unfamiliar worlds did not.

IDENTITY SHORTCUT
Renaming the same world destroyed performance.

STRUCTURAL OVERFIT
Identity transfer works, but later changed graph structure does not.

INEFFICIENT COGNITION
It succeeds mostly by searching nearly everything.

BAD STATE REPRESENTATION
The information given to the model is insufficient or misleading.

ANSWER LEAKAGE
The policy accidentally received information from the hidden solution.
```

That tells us **what kind of problem we actually have** before changing the architecture.

# When We Stop Tuning and Rethink the Design

We should revisit the experiment architecture instead of endlessly changing hyperparameters if:
- several small models learn the training worlds but repeatedly fail unfamiliar ones;
- renaming repeatedly breaks the policy;
- the only way to improve success is to spend almost the entire 10-step budget;
- the task is so easy or hard that trained and random behavior look nearly the same;
- success requires giving the model distance-to-goal, correct-route flags, or another hidden solver clue;
- the proposed “fix” is a special case for a certain world or target.

This is how we avoid another brittle patch cycle.

# Model Generations Will Have Identity

Every meaningful trained checkpoint should be traceable:

```text
model ID
parent model ID
experiment version
generator version
state/action version
training seed
world seed range
training configuration hash
number of episodes seen
checkpoint number
parameter checksum
Git commit
evaluation result
strongest generalization level
```

This means later we can actually say:

```text
Synrheon model v0
        ↓ training
v1
        ↓ training
v2
```

and know exactly what changed.

# The UI Can Then Show Real Development

The Organism UI should eventually receive backend-owned records like:

```text
model version
training episode
training performance
unseen-world performance
renamed-world performance
cognitive efficiency
strongest demonstrated generalization level
```

That gives you a real development history instead of a fake “smartness” number.

The UI already has a growth surface, but it correctly says **Not measured** until a backend learning owner produces real data.

# E011-B — When the Learned Policy Becomes Part of Synrheon

Even if E011-A works, the model is not yet integrated into the organism.

Then we perform E011-B:

```text
real CognitiveState
        ↓
cognition.py
        ↓
learned operation + target
        ↓
bounded state transition
        ↓
checkpoint
        ↓
runtime.py only sequences
        ↓
OrganismState / trace
        ↓
Organism UI
```

The hidden experiment answer/scorer never belongs in that live path.

Only after the runtime really reaches the learned policy can we call it **Integrated**.

Only after you run the organism and we inspect the behavior can we call the intended live behavior **Verified**.

# One Cognitive Micro-Cycle

The broader architecture remains:

```text
S0 — current state
 ↓
see valid operations + targets
 ↓
choose one learned mental action
 ↓
perform one bounded transition
 ↓
S1 — checkpoint
 ↓
learn from later outcome / continue / stop
```

The checkpoint is not a literal pause in seconds. It is an observable state boundary.

# The Training Record

The current trace contract is:

```text
state_before
available_actions_and_targets
selected_action
state_after
predicted_state_after
expected_value
observed_outcome
compute_cost
error_or_correction
credit_assignment
alternative_action_estimates
```

Some of the future-facing fields may initially be empty during E011-A v1. Keeping the slots prevents us from later confusing “the model chose it” with “the action actually deserved credit.”

Very important:

```text
selected path ≠ good path
```

# Root / Workflow Files

`README.md` — why Synrheon exists and the current research direction.

`AGENTS.md` — front door for coding agents.

`agent/ARCHITECTURE_STEWARD.md` — broad-to-narrow development, correct ownership, live-organism proof, thin runtime, honest status.

`.agents/skills/synrheon-development-workflow/SKILL.md` — canonical implementation workflow.

`pyproject.toml` — Python project/test configuration.

`.gitignore` — generated/local files Git should ignore.

# Project-Truth Documents

`docs/SCAFFOLD.md` — repository map and owner boundaries.

`docs/PROJECT_GUIDE.md` — this plain-English owner's manual.

`docs/SIGNAL_FLOW.md` — how information actually moves now and how the planned trainable loop should move.

`docs/ARCHITECTURE_PLAN.md` — intended dependency order and future mechanisms.

`docs/IMPLEMENTATION_STATUS.md` — what is Not Started, Designed, Built, Integrated, or Verified.

`docs/CURRENT_STAGE.md` — current development boundary and immediate success criteria.

`docs/DECISIONS.md` — durable architecture choices.

`docs/EXPERIMENTS.md` — preregistered and observed experiments, including the full E011-A numeric/seed contract.

`docs/RESEARCH.md` — research ideas and prior-art leads, not implementation truth.

`docs/PROMPT_TEMPLATES.md` — human-facing dispatch prompts.

# Actual Python Organism

## `src/synrheon/core.py`

**Plain English:** owns basic explicit state, not the thinking strategy.

### `Concept`

One stable concept identity:

```text
concept_id
label
optional future world_vector
```

A concept should eventually be richer than a word. Neural representations may later learn similarity, function, context, prediction usefulness, and cross-modal grounding while the explicit concept identity remains available.

### `WorldRelation`

A stored relationship between known concepts, for example:

```text
daisy IS_A dog
```

The relation is data. Storing it does not mean production cognition automatically follows it.

### `OrganismRelation`

An open-ended relationship between Synrheon and a concept.

Important fields:

```text
relation_type
strength
confidence
origin
evidence_event_ids
```

`relation_type` remains free data rather than a fixed Python ontology.

### `SelfRelation`

Keeps injected and learned organism relations separate.

What Synrheon was explicitly told cannot silently become what she learned herself.

### `ActivationState`

A container for current activation values.

Important: **it is representation only.** Core does not decide which concepts should win.

### `CognitiveSubstrate`

Owns concepts, world relations, organism relations, and activation representation.

It validates stored state but does not choose cognitive routes.

### `learn_self_relation()`

A narrow provenance-preserving storage update for one learned organism relation. It does not decide what thought path to follow and is not the cognitive policy.

### `OrganismState`

Top-level live state containing:
- session status/cycle;
- stimuli;
- trace;
- computational time;
- ordered experience thread;
- cognitive substrate.

## `src/synrheon/cognition.py`

**Plain English:** home for the trainable thinking policy.

Right now it deliberately contains **no production thinking algorithm**.

E011-A should place the learned policy/state/action mechanism here or at the cleanest existing cognition-owned boundary, not in runtime or UI.

## `src/synrheon/learning.py`

**Plain English:** intended owner for learning from whether cognition actually helped.

Expected responsibilities include:

```text
prediction vs outcome
error / correction
credit assignment
policy update
transition-model update
route-usefulness learning
```

The controlled experiment scorer can know hidden generated truth, but hidden answer truth must not become a general production learning dependency.

## `src/synrheon/time.py`

Owns when an experience occurs and where it sits in the current episode.

## `src/synrheon/experience.py`

Owns the current autobiographical event thread.

This is not durable memory across restart.

## `src/synrheon/runtime.py`

**Plain English:** thin traffic controller.

For Chat/Internal Thought it currently records time, ordered experience, stimulus, state, and trace.

When learned cognition is integrated in E011-B, runtime may sequence:

```text
state → cognition owner → checkpoint → next owner
```

but runtime must not choose the cognitive action or preferred target itself.

## `src/synrheon/interfaces.py`

Browser/API transport only.

Current endpoints remain:

```text
GET  /
GET  /api/state
GET  /health
POST /api/start
POST /api/pause
POST /api/continue
POST /api/step
POST /api/stimulus
POST /api/thought
POST /api/concept
POST /api/world-relation
POST /api/self-relation
```

# UI

## `ui/index.html`

The current development views are:

```text
Organism
Chat
Internal Thought
Knowledge
```

### Organism

Shows backend-owned current evidence rather than static stage paint:
- runtime/cycle/experience/concept/relation/activation counts;
- actual current experience thread;
- actual concepts and world relations;
- injected vs learned organism-relative relations;
- activation state;
- stage-specific live evidence;
- reserved cognitive-growth metrics when a backend learning owner exists.

### Chat

Shows external text accepted as ordered observed experience.

It intentionally does **not** invent a cognitive answer while learned cognition is absent.

### Internal Thought

Shows ordered experience and runtime trace. Explicit injections remain marked as injected.

Later it may show explicit cognitive checkpoints, not hidden chain-of-thought prose.

### Knowledge

Allows manual developer scaffolding for concepts, world relations, and injected organism relations.

### Inspector

Shows status, cycle, trace, experience, concept count, activation state, and complete backend state.

# Tests

## `tests/test_scaffold.py`

Current tests protect the observable runtime, provenance, experience order, open-ended organism relations, and the absence of the removed hand-written cognition policy.

The next E011-A tests should prove:
- generated splits are deterministic and disjoint;
- hidden truth cannot enter policy-visible state;
- action semantics and the 10-step budget are exact;
- model parameters change through training;
- untouched held-out transfer beats the preregistered baselines;
- renaming does not destroy performance;
- multi-step behavior is real;
- cost is measured;
- failures are classified without special-case production branches.

E011-B tests later prove the real runtime reaches the same learned owner while runtime stays thin.

# Developer Scripts

On Windows PowerShell:

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

On macOS, use `pwsh` for the PowerShell helper when PowerShell is installed, or invoke the underlying Python commands directly where appropriate.

# Current Information Flow

```text
Chat / Internal Thought
          ↓
     interfaces.py
          ↓
      runtime.py
       /       \
      ↓         ↓
 time.py   experience.py
      \         /
       OrganismState
            ↓
      snapshot / trace
            ↓
      Organism UI
```

Knowledge injection separately reaches `core.py` through runtime.

`cognition.py` remains intentionally uninvoked until a genuine trainable policy exists.

# Planned E011-A Controlled Flow

```text
generated hidden world
     │            \
     │             → hidden scorer / training truth
     ↓
revealed state only
     ↓
CognitiveState
     ↓
learned policy
     ↓
EXPAND(target) / STOP
     ↓
next revealed state
     ↓
training/evaluation record
```

# Planned E011-B Live Flow

```text
live state
   ↓
cognition.py
   ↓
learned action + target
   ↓
checkpoint
   ↓
runtime sequences only
   ↓
OrganismState / trace
   ↓
UI
```

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain what each owner does, what goes in/out, what state it owns, what calls it, what is live, and what is still planned.
