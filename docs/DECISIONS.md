# Architectural Decisions

Keep durable architectural choices here until this file becomes large enough to justify separate ADR files.

## D001 — Bottom-Up Development

Synrheon will be developed from substrate upward rather than by patching individual conversational failures.

## D002 — Strict Initial Retrieval Cascade

Normal retrieval begins with:

```text
Level 1 → Level 2 → Level 3
```

Additional levels may be added later only if evidence supports them.

## D003 — Limited Temporal Scratchpad

The initial scratchpad uses:
- current situation: up to 3 condensed packages
- last hour: up to 2
- last day: up to 3

The scratchpad is RAM-like working state, not a full-day memory store.

## D004 — Time Is Foundational

Meaningful external and internal events receive temporal position and sequence information.

## D005 — Memory Existence, Strength, and Activation Are Separate

A memory may exist durably without being currently active.

## D006 — Failed Reasoning Does Not Make Participating Memories False

Synrheon should learn route usefulness and failure attribution separately from factual memory truth.

## D007 — External LLMs May Participate but Do Not Own Persistent Cognition

LLMs may help with interpretation, semantic inference, language, and outside knowledge while Synrheon owns persistent state, autobiographical sequence, memory lineage, and durable learning effects.

## D008 — Major Cognitive Owners Begin as Files, Not Packages

Start with a small number of high-context source files.

Split a file into a package only when the implementation demonstrates multiple independent owners or the file becomes meaningfully difficult to understand.

## D009 — Live Organism Before Deep Cognition

Before Stage 1 cognitive mechanisms are treated as the primary implementation target, establish a running Synrheon runtime and development UI.

The live organism is the primary testing laboratory.

Automated tests are regression support and cannot by themselves grant `Verified` status.

## D010 — UI Is an Observation and Control Surface

The development UI may stimulate, step, continue, pause, inject explicit developer scaffolding, and inspect Synrheon.

It must not own cognitive interpretation, retrieval, memory, learning, abstraction, or problem-solving behavior.

## D011 — Canonical Repository

Synrheon's canonical repository is:

```text
https://github.com/Logancarton/Synrheon
```

Agents should use this repository without asking the user to provide it again.

## D012 — World Knowledge and Organism Knowledge Stay Separate

Generic world relationships and Synrheon-relative relationships are different state.

Example:

```text
Daisy IS_A dog
```

is world knowledge, while organism-relative relations describe what Daisy means to Synrheon.

The two may later influence the same learned cognitive state, but one must not overwrite or silently become the other.

## D013 — Injected, Observed, Inferred, and Learned Provenance Is Preserved

Knowledge and experience must retain how they entered the organism.

Initial provenance categories are:

```text
injected
observed
inferred
learned
```

Injected developer scaffolding must never be relabeled as self-learned merely because it is stored or later used.

If neural training later absorbs a pattern, the explicit source/evidence representation remains outside model weights.

## D014 — Organism Relations Are Open-Ended Data, Not a Fixed Cognitive Ontology

Synrheon must not be limited to a hard-coded list of ways that something can matter to her.

Organism-relative relation types are stored as data. A relation type not known when the software was written must be representable without changing production code.

For each concept, injected and self-learned organism relations remain permanently separate collections:

```text
injected_relations
≠
learned_relations
```

Injected developer scaffolding may write only `injected_relations`.

Experience-based learning may create or update only `learned_relations`.

The existing learned-relation update is a narrow provenance-preserving storage mechanism, not a thinking policy.

## D015 — Experience Thread Is Ordered but Is Not Yet Durable Memory

Meaningful current-process events receive:
- episode ID
- monotonic experience sequence
- absolute timestamp
- elapsed episode time
- previous/next event links
- observed vs injected provenance

This creates an autobiographical thread for live cognition.

It does not become durable memory until a later memory owner persists and retrieves it across process restart.

## D016 — The First Hand-Written Sparse Activation Policy Was Experimental and Is Retired

A temporary experiment used:

```text
lexical concept matching
fixed graph spreading
fixed decay / salience gains
fixed inhibition
fixed Top-K
fixed recurrence rounds
```

It proved that the live Chat/runtime path could reach a state-changing cognition owner and expose the result in the UI.

It did **not** prove that those developer-selected mechanics were the correct long-term cognition policy.

That production logic has been removed. Historical experiment evidence may remain in Git history/docs, but future agents must not treat the retired heuristic as current architecture.

## D017 — Train the Cognitive Process Instead of Hand-Coding Cognitive Routes

Synrheon's next core hypothesis is that the system should learn **how to transform cognitive state** rather than primarily memorize input→output mappings or follow developer-authored reasoning routes.

The preferred training unit is:

```text
state before
candidate cognitive actions
selected action
short transition / path
checkpoint
state after
prediction
outcome
error
credit
```

The architecture may define general process boundaries, representations, safety constraints, compute limits, and learning mechanics.

It should not encode world-specific answers, stimulus-specific branches, or permanent rules saying which relation/path to follow for a given phrase.

A selected path is not automatically rewarded. Learning should depend on outcome, correction, prediction error, or other evidence that the transition was useful.

The required research test is **transfer**:

```text
train on unrelated knowledge worlds A/B/C
        ↓
learn cognitive-action policy
        ↓
evaluate on unseen world D
```

If the policy only works because it remembers concept names, relation labels, exact prompts, or answers from training, the experiment fails.

## D018 — Language Is an Interface Around Cognition, Not the Thought Process Itself

Text tokenization, language encoding, and natural-language generation are perception/expression concerns.

The intended flow is:

```text
language / observation
        ↓
perception / grounding
        ↓
CognitiveState
        ↓
trainable cognitive process
        ↓
state result
        ↓
optional language expression
```

A future language model may contribute interpretation, concept proposal, outside knowledge, simulation, or expression. It must not become the sole owner of Synrheon's persistent state, provenance, memory lineage, or learned cognitive-process history.

## D019 — One Cognitive Micro-Cycle Produces One Observable Checkpoint

The default unit of trainable cognition is a bounded state transition rather than one monolithic hidden reasoning pass.

Conceptually:

```text
S(t)
 ↓ choose cognitive action
bounded operation
 ↓
S(t+1) checkpoint
```

A checkpoint is computational state, not a required wall-clock delay.

This boundary exists so Synrheon can:
- inspect uncertainty before continuing;
- redirect when evidence changes;
- preserve sequence and provenance;
- assign credit to individual cognitive transitions;
- stop under a hard compute budget;
- later compress repeated successful transition sequences into reusable cognitive skills.

## D020 — Separate Cognitive Physics From Learned Cognitive Skill

Synrheon may hard-code the **rules of the nervous system**, but should increasingly learn the **connections and useful thought routes**.

Architecture may explicitly define:

```text
state schema
action interface
provenance
checkpoint format
hard compute / safety budget
training-record format
outcome / correction interface
validation and persistence
```

Training should increasingly determine:

```text
attention / focus
concept organization
path ranking
cognitive-action selection
retrieval timing
comparison strategy
prediction / revision behavior
route usefulness
credit assignment
stopping preference within the hard ceiling
```

A production rule that says what thought to have for a particular phrase, relation name, concept, or answer pattern is presumed suspect unless the rule is truly a generic invariant and cannot reasonably be learned.

## D021 — Knowledge Transfer Is the Primary Test of Cognitive Skill

A model that performs well only on the knowledge it was trained with has not demonstrated reusable cognition.

The first trainable-policy experiments must therefore use anti-memorization controls such as:

```text
held-out concept identities
opaque / randomized names
renaming or permutation tests
no correct answer embedded in policy features
untrained or random baseline
no world-specific production branches
```

Later evaluations should also vary world topology and task composition.

The key question is:

> **Can Synrheon use a learned thinking process on knowledge it did not learn that process from?**

## D022 — Training Worlds and Tasks Must Be Generated, Not Hand-Curated as the Main Curriculum

E011 should use a deterministic seeded generator capable of producing many small knowledge worlds and tasks from abstract templates.

The generator may define the **rules of an experiment** and know the ground-truth solution path for scoring, but production cognition must never receive that hidden solution.

The curriculum should vary at least:

```text
concept identities
relation identities / encodings
graph topology
task targets
starting focus
irrelevant distractors
required cognitive-step count
```

Developer-authored examples may be used for debugging and human inspection, but they are not sufficient evidence of learned cognition because they can accidentally encode the developer's assumptions.

## D023 — Cognitive Actions Are Operation + Target, Not Merely Action Labels

A discrete action name such as `RETRIEVE` or `COMPARE` is only the operation family.

A useful cognitive action may also need parameters describing what the operation acts on, for example:

```text
RETRIEVE(target, region, depth)
COMPARE(left, right, evidence_scope)
FOCUS(candidate_region)
EXPAND(candidate_path)
PREDICT(target_state_feature)
REVISE(belief_or_route)
```

The model should increasingly learn both:

```text
which operation?
+
what should it operate on?
```

Python must not secretly choose the meaningful target after the model selects only a generic verb, because that would move the real cognitive decision back into hand-written code.

The first E011 slice may use a deliberately small parameter space, but the representation must not prevent later parameterized actions.

## D024 — Separate Policy, Transition Prediction, and Expected Cognitive Value

The architecture distinguishes three learnable questions:

```text
POLICY
P(a | S)
Which cognitive action should I take?

TRANSITION MODEL
F(S, a) → predicted S'
What do I expect this action to change?

VALUE
V(S, a)
How useful do I expect this action to be from here?
```

These functions may initially share a small model or be implemented incrementally, but the concepts must remain distinct.

Expected value matters because an action can be valid yet not worth its computational cost in the current state.

## D025 — Cognitive Utility Includes Resource Cost

A cognition policy is not successful merely because it eventually reaches the correct outcome after exploring everything.

Training and evaluation should eventually account for both task success and cognitive cost, conceptually:

```text
utility
=
task success / progress
-
compute cost
-
unnecessary cognitive steps
-
invalid or redundant actions
```

The exact coefficients are experimental and must not become arbitrary permanent constants without evidence.

A hard maximum budget remains infrastructure. Within that ceiling, the learned policy should prefer useful, economical cognition over exhaustive search.

## D026 — Credit Assignment Must Consider Alternatives and Generalization Level

Observed success does not prove that the selected action caused the success.

Training should preserve enough information to estimate or later learn from alternatives available at each checkpoint:

```text
state
├─ chosen action
├─ other available actions
├─ predicted consequences
└─ later outcome
```

Counterfactual estimates may be approximate, learned, sampled, or introduced in a later E011 phase, but the architecture must not equate correlation with causal credit.

Generalization claims use four levels:

```text
Level 0 — Training memorization
same training worlds/tasks

Level 1 — Identity transfer
new/renamed concepts with comparable structure

Level 2 — Structural transfer
new concepts + changed topology / relation arrangement

Level 3 — Compositional transfer
new knowledge + new structure + novel combinations of cognitive demands
```

Passing one level does not imply the next. Documentation and status claims must name the strongest demonstrated level rather than using the broad phrase “learned how to think” without qualification.
