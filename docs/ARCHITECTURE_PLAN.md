# Synrheon Architecture Plan — Revision 5 Build/Test Program

## Current architectural thesis

Synrheon is no longer treating the historical HCT-2 pipeline as a production blueprint that must be integrated intact.

The current research question is narrower:

> Can a cognitive system keep broad alternatives recoverable while increasing contextual resolution only where the unresolved question earns more computation?

The current working flow is therefore:

```text
question / unresolved state
        ↓
legitimate broad candidate field
        ↓
select a potentially discriminating context operation
        ↓
reversible contextual state transition
        ↓
re-evaluate what remains unresolved
        ↓
optional deeper refinement or optional recurrence if evidence earns it
        ↓
evidence sufficiency
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
```

This is a research architecture, not a claim that every box is established or live.

## Evidence boundary

Current external-development evidence requires architectural restraint.

```text
reversible suppression
    strong synthetic support; external value still open

single full-context soft taper
    approximately preserves BM25 on SciFact development

multiple ordered context stages
    NOT established

current static recurrence
    discounted on SciFact development

current four hand-designed context channels
    insufficient residual signal on BM25 errors

current commitment calibration
    discounted

question-guided contextual divergence
    untested

trajectory-based recurrence
    untested
```

Historical HCT-1/HCT-2 results remain evidence records. They do not force production mechanisms that stronger external tests fail to support.

## Build/Test rule

Synrheon should now grow through a repeating loop:

```text
smallest defensible cognitive invariant
        ↓
build reusable production-facing primitive
        ↓
use that primitive in a falsifiable experiment
        ↓
negative result?
    yes → simplify / remove assumption
    no  → earn the next architectural layer
        ↓
only then integrate farther into the organism
```

This prevents a separate "research toy" and "production architecture" from drifting apart while also preventing an unvalidated experiment from becoming live cognition merely because code exists.

## Cognitive physics vs cognitive skill

### Designed cognitive physics may define

```text
candidate identity and complete-state representation
reversible suppression semantics
active vs dormant compute regions
checkpoint / restore / reopen mechanics
context-transition provenance
compute and safety ceilings
valid evidence / abstain / seek / reopen interfaces
observable trace boundaries
```

### Learned or experimentally earned cognitive skill should determine

```text
which candidate field to retrieve
which context matters
which context to evaluate next
how strongly to settle
whether multiple settling stages help
which region deserves more compute
whether recurrence adds useful information
when evidence is sufficient
when to seek evidence
when to reopen
when to stop
```

The design principle remains:

> **We code the cognitive physics. Synrheon must earn or learn the cognitive skill.**

## Architecture slice 1 — reversible candidate field

Status: **BUILT, NOT LIVE-INTEGRATED**

Owner:

```text
src/synrheon/contextual_search.py
```

The first production-facing primitive now implements:

```text
complete broad-field retrieval prior
complete current activation vector
active candidate region
dormant but recoverable candidate state
carry / reset / residual transition provenance
reversible checkpoints
restore
reactivate
reopen-all
```

Its central invariant is:

```text
suppressed != deleted
```

It rejects silent candidate deletion during soft state replacement. It contains no qrels, correct identity, semantic hierarchy, taper equation, recurrence rule, or commitment rule.

The primitive is exported through `cognition.py`, but `runtime.py` does not fabricate a candidate field merely to claim integration.

## Architecture slice 2 — transition isolation through D6

Status: **PREREGISTERED + BUILT; SCIFACT DEVELOPMENT RESULT NOT YET OBSERVED**

Scientific owners:

```text
docs/D6_PREREGISTRATION.md
experiments/d6_transition_persistence.py
tests/test_d6_transition_persistence.py
```

D6 uses the same reversible candidate-field contract to compare:

```text
A  BM25 anchor
B  one full-context soft taper
C  partial -> full with carried activation
D  partial -> full with reset
E  partial -> full with full-minus-partial residual evidence
```

No recurrence is allowed. No final split is accessible through the D6 interface.

The immediate purpose is not to improve performance. It is to determine whether carried settled state is a major cause of the existing sequential failure.

## Architecture slice 3 — multi-taper necessity

Status: **BLOCKED ON D6**

MT-1 will ask whether more than one context-settled soft taper actually earns a role after transition pathology is controlled.

Primary comparison:

```text
single soft
vs
multiple soft
vs
multiple soft + reset
vs
scrambled-order multiple soft
vs
matched-compute hard stages
```

Clock-driven Top-K may appear only as a negative control.

Frozen interpretation principle:

> **Hard pruning losing does not establish that multiple soft tapers are necessary.**

If multi-soft ~= single-soft while hard pruning loses reversal recovery, keep reversibility and remove multi-stage necessity from the architecture.

## What should be built now vs withheld

### Build now

Only mechanisms that remain useful under both positive and negative D6 outcomes:

```text
reversible candidate-state ownership
context-transition checkpoints
explicit provenance of carry / reset / residual operations
raw compute accounting
observable state boundaries
experiment-to-production compatible interfaces
```

### Withhold until evidence earns them

```text
fixed multi-level context hierarchy
production multi-taper controller
production recurrence operator
learned recurrence resistance as a universal mechanism
hard-coded semantic context routes
custom commitment thresholds
live autonomous Ground 0 loop
```

This is deliberate. Building these now would optimize implementation toward the preferred theory before MT-1 has had a chance to falsify it.

## Next legitimate production dependency — candidate source

The live organism cannot use contextual search until it has a legitimate broad candidate field.

Today the live system has concepts, relations, current activation storage, ordered experience, provenance, and computational time, but it does not yet have durable memory or learned retrieval.

Therefore the next production dependency is not "turn on tapering." It is to establish a candidate-source interface that can eventually receive candidates from memory/retrieval without knowing the correct answer.

Required contract:

```text
question / current cognitive need
        ↓
candidate source
        ↓
opaque candidate IDs + provenance + initial support
        ↓
ReversibleCandidateField
```

The interface may be built before a sophisticated retriever exists, but production tests must use legitimate visible state rather than planted correct identity.

## Question and unresolved-state controller

Revision 5 proposes that context resolution should be controlled by what remains unanswered rather than by a universal stage count.

Future architecture therefore needs an explicit representation of:

```text
current question
currently available evidence
what remains unresolved
candidate disagreements relevant to that unresolved portion
possible next context operations
expected information gain / cost
```

This owner is **not yet built** because D6/MT-1 may change what a transition should preserve. Do not hard-code an ontology of semantic, temporal, identity, causal, or social levels as a mandatory sequence.

Those may become available context operations; they should not become a universal ladder by assumption.

## Recurrence boundary

Recurrence is now optional, not part of the guaranteed funnel.

A future recurrence owner must earn its role by operating on a question-relative relation such as:

```text
complementary evidence
contradiction / support
causal dependence
temporal sequence
trajectory compatibility
missing-aspect coverage
```

Generic static lexical similarity is not enough evidence for production recurrence.

A recurrence experiment must compare against a matched no-recurrence condition and measure whether recurrence reduces unresolved uncertainty or improves external behavior enough to justify its cost.

## Commitment boundary

The architectural separation remains valuable:

```text
winner != knowledge
```

But the current commitment signal is not externally established.

Production commitment should eventually consume explicit evidence sufficiency, provenance, unresolved alternatives, and calibration evidence. Until a mechanism passes external tests, the architecture should preserve the actions without pretending the policy is solved:

```text
COMMIT
ABSTAIN
SEEK EVIDENCE
REOPEN
CONTINUE DELIBERATION
```

## Relationship to E011-A

E011-A remains evidence that an operation/target policy can learn transferable preferences from visible state without memorizing candidate identity.

Owners:

```text
policy.py
policy_learning.py
```

Its role is donor evidence for learned cognitive routing. It is not the Ground 0 architecture and should not be directly wired into contextual search until the state/action contract being learned is justified.

## Production ownership

```text
state.py
    explicit organism/world state

cognition.py
    public Ground 0 contracts and cognitive boundary

contextual_search.py
    reversible candidate field and context-transition checkpoints

policy.py
    retained trainable operation/target policy primitives

policy_learning.py
    outcome-driven policy updates

experience.py
    ordered current-episode experience + provenance

temporal.py
    computational time and sequence

runtime.py
    thin sequencing only

dev_server.py
    browser/API transport only

experiments/
    falsification assays, external qrels, hidden evaluation truth, scientific scoring
```

Hidden evaluation truth must never cross from `experiments/` into production cognition.

## Live integration sequence

Do not integrate an entire presumed architecture at once.

The current dependency order is:

```text
1. reversible candidate field                         BUILT
2. D6 transition isolation                            BUILT / NOT YET RUN
3. interpret D6                                       PENDING
4. MT-1 multi-taper falsification                     BLOCKED
5. legitimate production candidate-source contract    NEXT BUILDABLE DEPENDENCY
6. question / unresolved-state representation         PENDING EVIDENCE
7. learned context-operation selection                PENDING SIGNAL
8. optional recurrence                                MUST EARN ROLE
9. evidence sufficiency / commitment calibration      MUST EARN ROLE
10. runtime + UI integration of earned mechanisms     LATER
```

Durable memory, retrieval, scratchpad cognition, problem/trial learning, consolidation, abstraction, and autonomy should receive implementation owners only when real code and a clear responsibility exist.

## Scientific development rule

Every major mechanism must declare before evidence inspection:

```text
hypothesis
strong baseline
matched information access
matched compute where relevant
success threshold
failure interpretation
ablation
identity / leakage safeguards
held-out boundary
raw metrics
```

Negative and unexpected results are research assets. Do not lower a threshold or add a patch merely to preserve the preferred architecture.

The objective is not to build the historical Ground 0 diagram.

> **The objective is to discover which cognitive operations continue to deserve a place in Synrheon, and build only those operations strongly enough that the organism and the experiments can share them.**
