# Research Notes

Use this file for broad research questions, prior-art notes, donor ideas, and mechanisms worth investigating.

Do not treat research notes as implemented architectural truth.

## Current Research Direction

The primary question is no longer:

> How should Synrheon hand-code the right cognitive route?

It is:

> **What minimal state, actions, learning signals, and training tasks would let Synrheon learn a reusable cognitive process that transfers to unfamiliar knowledge?**

The research program should separate:

```text
knowledge representation
from
cognitive skill
```

and then test how much of cognition can become trainable without losing explicit state, provenance, memory lineage, or observability.

## Core Research Questions

### CognitiveState

- What information must be present in one checkpoint for useful action selection?
- Which state features should be symbolic, graph-based, vector-based, tensor-based, or hybrid?
- How can state describe uncertainty, evidence, focus, goal, recent sequence, and available resources without leaking the answer?
- How large can the active state become before sparse cognition is lost?

### Cognitive actions

- Is a small discrete vocabulary such as `FOCUS`, `EXPAND`, `RETRIEVE`, `COMPARE`, `PREDICT`, `REVISE`, and `STOP` enough for a first transfer experiment?
- Should actions remain discrete, become parameterized, or eventually become continuous learned operations?
- Can repeated successful action sequences be compressed into higher-level cognitive skills?
- How should a model decide that it has enough evidence to stop?

### Transition learning

- Should Synrheon learn only `P(action | state)`, or also predict `state_after | state_before, action`?
- Does explicit next-state prediction improve transfer and error correction?
- Which transition errors should alter the cognitive policy versus concept/world knowledge?

### Credit assignment

- How far backward should outcome credit propagate through a multi-step cognitive sequence?
- How do we avoid strengthening a path merely because it was chosen?
- How should partial success, uncertainty reduction, failed prediction, correction, and external feedback contribute to credit?
- How should Synrheon preserve failed routes as useful negative evidence without marking the participating memories false?

### Concept learning

- Can concept representations be trained for functional/predictive usefulness rather than word co-occurrence alone?
- How should surface word form, lemma, sense, entity, concept, image exemplar, action, and episode remain distinct?
- What makes a self-created concept useful enough to retain?
- Can concept quality be evaluated by prediction gain, compression, transfer, and reuse rather than frequency alone?

### Organization / sparse routing

- Can sparse activation emerge from a learned path-selection policy instead of a permanent spreading equation?
- Which generic capacity limits should remain fixed: compute budget, active-state size, maximum transitions, memory tiers?
- How should route usefulness differ from factual truth and relation confidence?
- How should current context, organism relevance, temporal relevance, and learned usefulness jointly influence routing without fixed semantic rules?

### Language boundary

- What is the lightest perception/grounding mechanism needed to map language into cognitive state without making language itself the thought process?
- Should early experiments bypass natural language entirely so transfer can be measured without pretrained linguistic knowledge contaminating the result?
- When an LLM is introduced, which bounded functions should it own: interpretation, concept proposal, outside knowledge, simulation, expression, correction?

### Transfer and evaluation

- How different must held-out worlds be before success counts as real process transfer?
- Which renaming/permutation tests best detect concept-identity shortcuts?
- How should topology and task composition change in the second transfer gate?
- What baseline is fair: random, untrained network, simple fixed heuristic, or all three?
- How many tasks/seeds are needed before improvement is unlikely to be luck?

### Time, memory, and retrieval

- How should computational time enter CognitiveState without forcing all reasoning to be temporal?
- Can the learned policy decide when Level 1 → 2 → 3 retrieval is worth the compute cost?
- How should memory existence, memory strength, current activation, and route usefulness remain mathematically separate?

### Recursive cognition and autonomy

- What stopping/anti-fixation mechanisms are needed before allowing stimulus-free continuation?
- Can uncertainty reduction or predicted information gain serve as a continuation signal?
- How can Synrheon avoid endless self-generated loops while still pursuing unresolved problems?

## Candidate Prior-Art Areas to Investigate

These are research leads, not donor code to copy:

- cognitive architectures with explicit state + operator selection, especially Soar;
- Neural Programmer-Interpreter and related learned program-selection systems;
- concept bottleneck / concept representation models;
- process supervision and reasoning-trace training;
- latent-reasoning approaches such as Quiet-STaR and Coconut;
- learned world models and planning systems such as MuZero and Dreamer;
- predictive representation learning such as JEPA-style approaches;
- reinforcement learning / actor-critic methods for multi-step credit assignment;
- graph neural networks and permutation-equivariant models for concept-name-invariant transfer;
- meta-learning / algorithmic reasoning benchmarks that test generalization to unseen structures.

The important question is not whether any donor system resembles Synrheon superficially. Mine mechanisms that can help answer:

> How can useful internal operations be learned while Synrheon preserves explicit organism state and provenance?

## Donor / Prior-Art Template

For each donor mechanism record:
- source;
- exact mechanism;
- useful equation or learning signal;
- what state/action boundary it assumes;
- what generalizes and what is task-specific;
- failure lesson;
- what Synrheon could learn from it;
- whether it would duplicate an existing owner;
- why the donor structure itself should or should not be copied.

## Experimental Discipline

Prefer tiny experiments capable of disproving the idea.

A compelling result should distinguish at least:

```text
memorized content
vs
memorized structural template
vs
partial process transfer
vs
reusable cognitive skill
```

Do not call training-world performance alone evidence of learned cognition.
