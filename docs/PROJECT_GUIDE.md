# Synrheon Project Guide — Plain English

This is the human-readable owner's manual for Synrheon. It explains what actually exists, what each important file owns, and what the next live step is.

Always separate:

```text
Designed
Built
Integrated
Verified
```

# The Mental Model

Synrheon is not being built by adding more hard-written rules for what thought should happen next.

The direction is:

```text
explicit state
    ↓
trainable cognitive policy
    ↓
choose one useful operation + target
    ↓
bounded state change
    ↓
checkpoint
    ↓
learn from what happened
```

A useful shorthand is:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

# Where The Project Stands Now

```text
Stage 0B   Observable runtime + UI          Verified
Stage 1    Cognitive substrate              Built
Stage 2    Time + ordered experience        Integrated
E011-A     First trainable cognition assay  Built; Level-1 numeric gate passed
E011-B     Live policy integration          Not built yet
```

The important change is that `cognition.py` is no longer empty.

Synrheon now has a small trainable cognitive policy that was trained and tested in a controlled generated environment.

That policy is **not yet being called by Chat or the live runtime**.

# What E011-A Actually Learned

The first problem was deliberately simple and anonymous.

Each generated world contains:

```text
10–14 anonymous nodes
1 visible start
1 hidden goal
1 shortest route 3–5 edges long
2–4 distracting branches
sometimes cross/back connections
10 cognitive actions maximum
```

Synrheon is allowed only:

```text
EXPAND(target)
STOP
```

`EXPAND(target)` means: choose one currently visible frontier node and spend one cognitive step revealing its local outgoing structure.

`STOP` means: end the episode. It succeeds only after the goal has actually become visible.

The software may tell the model which actions/targets are valid.

The software does **not** tell it which valid target is best.

# What The Policy Is Allowed To See

Only already-revealed information:

```text
current checkpoint
remaining budget
revealed nodes
revealed edges
known depth from start
which nodes are expanded
which nodes remain frontier candidates
reveal order
whether a revealed node is the goal
available valid actions + targets
previous action summary
```

# What The Policy Is Never Allowed To See

```text
hidden nodes
hidden edges
hidden goal location
shortest route
shortest-path distance
correct-route flags
correct next action
correct next target
future frontier
solver/scorer output
world seed as a clue
```

This is the anti-cheating wall.

# The Controlled Result

The evidence is saved in:

```text
data/e011a_v1_evidence.json
```

Five frozen model seeds were trained and evaluated.

Recorded result:

```text
training success, median          81.0%
held-out unseen-world success     79.8%
random-valid baseline              6.1%
matched untrained, median          0.0%
renamed-world success             79.8%
renaming retention               100.0%
mean budget use                   78.02%
success cost / brute force        57.18%
```

The policy also succeeded on unseen tasks whose shortest route required 3, 4, and 5 edges.

That means the first controlled result supports:

```text
Level 1 — identity / instance transfer
```

It does **not** yet prove:

```text
Level 2 changed-structure transfer
Level 3 compositional transfer
language understanding
durable memory
full reasoning
autonomy
```

# Why Renaming Matters

The node names are anonymous handles only.

They are deliberately not part of the learned feature vector.

So when the same held-out worlds were independently renamed, performance remained:

```text
79.8% → 79.8%
```

That is evidence the policy did not simply memorize node names.

# What The Model Appears To Have Learned

The model does not learn the hidden route directly.

It learns a preference over visible cognitive-state features such as:

```text
candidate depth
candidate recency
current frontier size
remaining compute budget
checkpoint progress
whether STOP is being considered after a revealed goal
```

Training changes the weights controlling those preferences from almost-useless initial behavior into a much more effective bounded-search policy.

# File-by-File Ownership

## `src/synrheon/cognition.py`

**Plain English:** the owner of the first trainable thinking choice.

Current important pieces:

### `RevealedNode`

One policy-visible region/candidate.

Stores only legitimate revealed facts:

```text
opaque handle
depth
expanded?
reveal order
frontier?
is goal? only after reveal
```

### `CognitiveAction`

One operation plus its target.

Current E011-A actions:

```text
EXPAND(target)
STOP
```

It validates that EXPAND has a target and STOP does not.

### `CognitiveState`

One explicit checkpoint presented to the policy.

Contains:

```text
checkpoint index
remaining budget
hard budget
revealed nodes
revealed edges
previous action
```

It cannot contain the hidden experiment answer because those fields do not exist in this representation.

### `LinearCognitivePolicy`

The first small trainable policy.

It:

```text
receives CognitiveState
    ↓
enumerates valid actions
    ↓
builds visible-state feature vectors
    ↓
scores every valid operation + target
    ↓
chooses one
```

The target handle is used to execute the choice, but the handle string itself is not a learned feature.

The policy can serialize/load its weights and calculate a parameter checksum.

## `src/synrheon/learning.py`

**Plain English:** the first owner that changes the cognitive policy because of outcomes.

### `PolicyDecisionTrace`

Keeps the candidates and which one was selected for a learning step.

### `ReinforceLearner`

Uses discounted outcome/cost evidence to adjust the policy weights.

Conceptually:

```text
choice
 ↓
what happened afterward?
 ↓
success / failure / wasted compute
 ↓
credit or blame
 ↓
weights change
 ↓
future choices change
```

It does not receive the hidden shortest path or hidden goal location.

## `experiments/e011a.py`

**Plain English:** the controlled scientific laboratory, not production cognition.

It owns:

```text
generated hidden graph worlds
hidden goal/route truth
revealed-state environment
training episodes
random baseline
untrained baseline
trained evaluation
renaming evaluation
cognitive-cost scoring
frozen pass-gate calculation
```

This file is intentionally outside `src/synrheon` so hidden experiment truth cannot quietly become production cognition.

## `data/e011a_v1_evidence.json`

**Plain English:** the receipt for the experiment.

It records:

```text
all five model seeds
model IDs
parent IDs
parameter checksums
learned weights
training results
held-out results
renaming results
cognitive cost
training configuration
source commit
frozen gate outcome
```

## `tests/test_e011_trainable_cognition.py`

Protects the most important scientific contracts:

```text
opaque identity is not a policy feature
generator stays inside frozen size/depth family
action/target validation works
quick five-seed assay learns + transfers + survives renaming
```

# The Existing Live Organism

## `src/synrheon/core.py`

Owns explicit organism state:

```text
Concept
WorldRelation
OrganismRelation
SelfRelation
ActivationState
CognitiveSubstrate
OrganismState
```

It stores/validates state. It does not decide which cognitive route to take.

## `src/synrheon/time.py`

Owns event sequence, absolute time, elapsed episode time, and episode identity.

## `src/synrheon/experience.py`

Owns the current ordered autobiographical event thread.

External Chat is `observed`.

Internal Thought injection is `injected`.

This is not durable memory across restart.

## `src/synrheon/runtime.py`

**Plain English:** traffic controller.

Current live flow is still:

```text
Chat / Internal Thought
        ↓
runtime
        ↓
time + experience
        ↓
state / trace
        ↓
UI
```

The runtime does **not** call the new E011-A policy yet.

That is the next stage, E011-B.

Runtime may sequence cognition later, but it must not choose the cognitive action or target itself.

## `src/synrheon/interfaces.py`

Browser/API transport only.

It translates UI requests into runtime calls.

It does not interpret the stimulus or make cognitive decisions.

# The UI

`ui/index.html` is Synrheon's development microscope.

Current major surfaces:

```text
Organism
Chat
Internal Thought
Knowledge
```

The Organism surface can show what is live and backend-owned state.

The next E011-B work should expose:

```text
which trained artifact is loaded
current live CognitiveState
selected learned operation + target
resulting checkpoint
backend-owned E011-A growth evidence
```

The UI must display those things, not calculate them itself.

# What Is Not Integrated Yet

Even though E011-A passed, this is still true:

```text
Chat does not invoke the learned policy
Think One Step does not invoke the learned policy
Continue does not invoke the learned policy
OrganismState has no live learned-policy checkpoint yet
UI does not yet show a live learned action
```

So the correct status is:

```text
Built experimentally
NOT Integrated
NOT live-Verified
```

# The Next Stage — E011-B

The next correct path is:

```text
recorded trained artifact
        ↓
legitimate live CognitiveState
        ↓
cognition.py
        ↓
learned operation + target
        ↓
bounded transition
        ↓
checkpoint
        ↓
runtime sequences it
        ↓
OrganismState / trace
        ↓
UI
```

The hidden E011 generator/scorer does not belong in that production path.

# Broader Future Architecture

The long-term system still separates:

```text
P(a | S)
What should I do next?

F(S,a) → predicted S'
What do I think this action will change?

V(S,a)
How useful do I expect this action to be?
```

E011-A implemented only the first policy slice.

Future work still includes:

```text
transition prediction
expected cognitive value
counterfactual credit
Level 2 structural transfer
concept organization
language grounding
durable memory
retrieval
scratchpad / recursive cognition
problem trials and revision
consolidation / abstraction
autonomy
```

# Important Guardrail

The final E011-A held-out seeds have already been inspected.

Do not change the model/generator/state/action/reward specifically to improve those same final results and still call it `e011a-v1`.

A material change requires a new experiment revision and fresh untouched final worlds.

# Useful Commands

Run the normal organism using the existing helper.

Run a small E011 scientific regression:

```text
python -m experiments.e011a --quick
```

Run the complete frozen assay:

```text
python -m experiments.e011a
```

The full assay is controlled experiment work, not live runtime verification.
