# Cognitive Experiments

## Evidence Standard

The preferred experiment is a real stimulus applied through the running Synrheon organism.

Record stimulus/action, baseline, expected behavior, observed UI/runtime output, relevant internal state/trace, and interpretation.

Automated tests protect discovered behavior but are not enough to call cognition `Verified`.

## E000 — Stage 0B Connected Organism Transport

Hypothesis: browser-facing actions can cross into the real Python runtime, mutate Synrheon-owned state, and return observable state/trace without placing cognition in the UI/transport layer.

Observed result: the user ran the supported application and confirmed Start, Chat, Internal Thought, Step, Continue, Pause, Current State, and Trace through the real frontend/backend/runtime path.

Status: **Verified**

## E001 — World / Injected-Self / Learned-Self / Activation Separation

The initial Stage 1 substrate established separate world knowledge, organism-relative knowledge, learned organism-relative state, and activation representation.

Its first fixed 11-field self vector was later superseded by E001A.

Status: **Superseded representation; provenance separation retained.**

## E001A — Open-Ended Organism Relation Space

Hypothesis: Synrheon can preserve injected-versus-self-learned provenance without hard-coding a closed list of organism-relative dimensions.

Candidate result:
- arbitrary relation names were accepted as data
- injected and learned versions remained separate
- learned evidence lineage remained explicit
- world knowledge and current activation remained separate
- Stage 0B controls and ordered experience behavior remained intact

Status: **Built / integrated representation; human live verification still required for that bounded UI behavior.**

## E002 — Ordered Experience Thread

Hypothesis: every meaningful external or explicitly injected internal event can receive an episode coordinate and explicit before/after links without pretending current-episode experience is durable memory.

Expected result:
- Chat event is `origin = observed`
- Internal Thought injection is `origin = injected`
- sequence is monotonic
- previous/next links agree
- stimulus records link to experience event IDs
- new session starts a new episode
- no durable cross-process memory claim

Candidate automated result: current tests produced consistent observed/injected provenance, sequence, links, and stimulus-to-experience IDs.

Status: **Integrated; not durable memory.**

## E003 — Temporal Retrieval

Can Synrheon restrict retrieval to a time region such as earlier today without searching all lifetime memories?

Status: Future

## E004 — Hand-Written Sparse Chat Activation

Hypothesis tested: can Chat reach a state-changing cognition owner using generic lexical matching plus relation spreading, salience, inhibition, and Top-K selection without domain-specific phrase branches?

Historical candidate result:
- the live architecture was successfully wired from Chat/Internal Thought through runtime into `cognition.py`
- unrelated concept networks used the same algorithm
- fixed Top-K bounded the active region
- unknown cues failed safely
- world/organism knowledge was not rewritten

Important interpretation after review:

The experiment proved the **integration path**, but the actual decision policy still depended on developer-selected cognition mechanics:

```text
lexical matcher
fixed spread gain
fixed decay
fixed salience gain
fixed inhibition threshold
fixed Top-K
fixed recurrence count
```

Those mechanics are no longer considered the intended cognition architecture.

Production implementation status: **Removed / superseded by the trainable-cognition pivot.**

Historical Git evidence remains useful as a failure lesson: a mechanism can be generic across examples and still be too hand-designed to qualify as the long-term learned cognition policy.

## E005 — Three-Level Retrieval

Can Level 1 orientation narrow Level 2 candidates before Level 3 detailed retrieval?

Status: Future

## E006 — Problem / Trial Learning

After a failed trial, can Synrheon preserve why it failed and preferentially change the most likely causal variable?

Status: Future

## E007 — Route Learning

Can successful retrieval or reasoning trajectories become easier to select later without hardcoded stimulus rules?

Status: Future; likely absorbed into the trainable cognitive-policy direction.

## E008 — Recursive Thought

Can Synrheon solve a problem requiring several internal state transitions before producing an external response?

Status: Future

## E009 — Consolidation

Can repeated experiences produce a useful compressed representation while preserving evidence lineage?

Status: Future

## E010 — Autonomous Continuation

Can unresolved internal state produce useful S(t+1) without new external input while avoiding fixation?

Status: Future

## E011 — Train the Cognitive Process, Test Transfer

### Research Question

Can a small model learn **how to perform useful cognitive operations** on explicit state, then reuse that skill with knowledge it never trained on?

The experiment is intentionally not a natural-language question-answering benchmark. Natural-language fluency would make it too easy to mistake memorized language/world knowledge for learned cognition.

### Hypothesis

A small trainable cognitive policy can learn **which cognitive operation to perform next** from abstract cognitive state and transfer that process to an unseen knowledge world whose concepts and answers were never used during training.

### First-Phase Scope

Keep the first slice deliberately narrow:

```text
small explicit knowledge world
+
small CognitiveState
+
small cognitive-action vocabulary
+
one action per checkpoint
+
trainable action policy
+
outcome / credit signal
```

Do not add an LLM, response generator, durable memory system, autonomous loop, or large neural architecture merely to make the demo look intelligent.

### Initial Cognitive Actions

Candidate first action set:

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

The experiment may begin with a smaller subset if that creates a cleaner causal test. These actions are cognitive operations, not answer labels.

### Core Training Unit

```text
state_before
available_actions
selected_action
short_transition_or_path
checkpoint
state_after
prediction
observed_outcome
error_or_correction
credit_assignment
```

A path is not rewarded merely because it was selected. Credit must depend on outcome, correction, prediction error, or another explicit usefulness signal.

### CognitiveState Requirements

The first state representation should expose only information that is legitimately available at that checkpoint, such as:

```text
current focus / active region
available local structure
current goal or unresolved condition
retrieved evidence already present
sequence position where relevant
uncertainty / confidence features
remaining compute budget
```

It must not contain the correct next action, final answer, hidden target identity, or a world-specific shortcut.

### Training Worlds

Use at least three tiny worlds with different content.

Example requirement:

```text
World A — arbitrary objects / relations
World B — unrelated arbitrary objects / relations
World C — unrelated arbitrary objects / relations
```

The important feature is not the topic. The worlds should require comparable **cognitive work** while using different knowledge.

Names should be opaque, randomized, or permuted where practical so semantic familiarity cannot solve the task.

### Held-Out World

World D must contain:
- concept identities never used in training;
- no answer text seen during training;
- no production branch that names the world;
- a task requiring the same general cognitive abilities;
- enough structural difference that success is not a trivial copied trace.

The first evaluation may preserve some abstract task structure so transfer is measurable. A stronger second evaluation should change topology and task composition as well.

### Required Renaming Test

For at least one evaluation world:

```text
same underlying world / task
        ↓
randomly permute every concept name / identity presented to the policy
        ↓
run again
```

Material performance collapse is evidence that the policy relied on identity shortcuts instead of reusable process.

### Baselines

At minimum compare against:
- random action selection;
- same model before training;
- a simple non-learning heuristic only if it can remain outside production cognition and does not contaminate the policy.

### Measurements

Record at least:

```text
training loss or policy objective
training-world task success
held-out-world task success
random / untrained baseline success
renamed-world success
mean cognitive steps to resolution
invalid / wasted cognitive actions
percentage of tasks requiring successful multi-step sequences
```

For any stochastic experiment, use enough repeated episodes/seeds that a single lucky run cannot be presented as success.

### Pass Criteria

The experiment is promising only if all of the following are true:

1. model parameters actually change through training;
2. decision quality or task success improves on training worlds;
3. held-out world performance exceeds the untrained/random baseline by a meaningful margin;
4. renaming concepts does not materially destroy the learned strategy;
5. at least some held-out tasks require and receive a useful **multi-step cognitive-action sequence**, not one lucky action;
6. success cannot be explained by memorized answer text, concept identities, relation names, or production world-specific branches;
7. each cognitive action produces an inspectable checkpoint;
8. state/action/outcome/error/credit traces remain inspectable;
9. the learned policy can be invoked through the real Synrheon runtime boundary without moving cognition into runtime or UI;
10. unrelated persistent world/organism state is not silently mutated by policy inference.

### Stronger Follow-Up Gate

If the first transfer test passes, the next test should vary more than names:

```text
new concepts
+
new relation arrangement / topology
+
new task composition
+
same underlying cognitive skills
```

This is a stronger test of learning **how** rather than memorizing a structural template.

### Failure Criteria

The experiment fails if:
- performance collapses on unseen or renamed identities despite equivalent cognitive demands;
- the implementation embeds task answers or special-case routes;
- selected paths are reinforced without outcome evidence;
- runtime becomes the cognition owner;
- the model merely reproduces training traces rather than adapting its operation sequence to current state;
- the policy receives leaked answer/target features;
- a single-step shortcut solves nearly every task that was supposed to test multi-step cognition;
- training-world improvement does not transfer above baseline.

### Interpretation Rules

If training performance rises but held-out performance does not, classify the result as **task memorization / overfitting**, not cognitive improvement.

If held-out performance survives concept renaming but fails on changed topology, classify the result as **partial process transfer** and design the next experiment around structural generalization.

If the model transfers across unseen content and altered structure while choosing useful multi-step operations, that is the first meaningful evidence that Synrheon is learning a reusable cognitive process.

### Current Status

**Pre-registered; implementation not started.**
