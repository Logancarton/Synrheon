# Synrheon Project Guide — Plain English

This is the short human-readable owner's manual for Synrheon.

Always separate:

```text
Research evidence
Designed
Built
Integrated
Verified
```

A mechanism can be scientifically promising without being live in the organism.

# Ground 0

Ground 0 is the current experimentally reinforced cognitive process that future Synrheon architecture should implement, challenge, or improve.

```text
large candidate / knowledge field
        ↓
learned context routing
        ↓
ordered reversible soft tapering
        ↓
small serious-candidate field
        ↓
state-dependent recurrence
        ↓
evidence / uncertainty
        ↓
commit | abstain | seek evidence | reopen
```

Plain English:

1. Do not reason deeply over everything Synrheon knows.
2. Use context to progressively narrow what deserves serious attention.
3. Suppress weak candidates without permanently deleting them.
4. Let the remaining serious alternatives interact recurrently.
5. A first-place candidate is not automatically knowledge.
6. If evidence is inadequate, abstain or gather more evidence.
7. If context changes, reopen previously suppressed possibilities.

Learned pathway resistance remains optional. Earlier assays found it useful, but HCT-2 showed it was not required in that task family.

The full scientific record lives in `CONTEXT_SETTLED_TAPERING_THEORY.md`.

# Why We Believe Ground 0 Is Worth Building

Several earlier ideas failed or were insufficient:

```text
clock-driven Top-K narrowing       failed badly
confidence-only narrowing          limited savings
stochastic consensus               false certainty
hard deletion                      failed under reversal
```

HCT-1 then showed that reversible soft narrowing could preserve uncertainty and restore candidates when context changed.

HCT-2 tested the stronger ordered-context idea on 300 final held-out worlds and passed every frozen criterion.

Key HCT-2 result:

```text
learned-order good behavior          100%
correct-candidate survival           100%
unresolved commitment                  0%
reversal reactivation                100%
renaming retention                   100%
recurrent load vs full field         3.125%
context evaluation vs generic soft   7.14%
learned-order efficiency advantage   5.49%
```

The recurrence ablation was especially valuable:

```text
correct candidate survived tapering  100%
good behavior without recurrence      45%
```

So tapering preserved the useful field, while recurrence performed important downstream relational work.

# What Exists in the Live Organism

Current live foundations remain:

```text
observable runtime + development UI     Verified
cognitive substrate                     Built
computational time                      Integrated
ordered experience + provenance         Integrated
```

Current live flow:

```text
Chat / injected developer thought
        ↓
runtime
        ↓
time + ordered experience
        ↓
organism state / trace
        ↓
UI
```

Ground 0 cognition is **not yet live-integrated**.

# What E011-A Still Contributes

E011-A predates Ground 0 but remains useful evidence.

It showed that a small policy could learn which valid cognitive action/target to choose from visible state and transfer that preference across unseen and renamed worlds.

Its first actions were only:

```text
EXPAND(target)
STOP
```

That is not the full Ground 0 process. The important reusable lesson is:

> **The architecture may expose valid cognitive operations, while training learns which operation and target are useful.**

E011-A should therefore be treated as a donor mechanism for learned cognitive routing, not as the final cognition design.

# What Changes Next

The old immediate plan was to wire the narrow E011-A policy directly into the live runtime as E011-B.

Ground 0 changes that assumption.

Before direct integration, the live cognition design should be reconciled with the reinforced process:

```text
live CognitiveState
        ↓
represent broad candidate field
        ↓
learned context/order decision
        ↓
reversible sparse taper
        ↓
small recurrent field
        ↓
state-dependent recurrent step(s)
        ↓
commit / abstain / reopen checkpoint
        ↓
runtime sequences result
        ↓
OrganismState / trace / UI
```

The exact integration should stay small and observable. We should not import the entire synthetic experiment harness into production.

# Designed Cognitive Physics

Production code may define generic rules and safe boundaries such as:

```text
state schema
candidate representation
valid cognitive operations
reversible suppression interface
recurrent transition interface
hard compute ceiling
checkpoint representation
provenance
commit / abstain / reopen interfaces
```

# Learned Cognitive Skill

Training should increasingly determine:

```text
what context matters
what context to inspect next
how strongly to taper
which candidate region deserves compute
which operation + target to choose
when further recurrence is useful
when evidence is sufficient
when broader context should reopen
```

The rule remains:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

# Important Owners

`src/synrheon/core.py`  
Stores explicit organism state, concepts, relations, and activation representation.

`src/synrheon/cognition.py`  
Owns trainable cognitive choices. Current implementation contains the earlier E011-A policy surface; future Ground 0 cognition belongs here or in clearly separated cognitive owners, not in runtime/UI.

`src/synrheon/learning.py`  
Owns outcome-driven learning of cognitive skill.

`src/synrheon/time.py`  
Owns computational time and event coordinates.

`src/synrheon/experience.py`  
Owns the current ordered experience thread and provenance.

`src/synrheon/runtime.py`  
Traffic controller only. It sequences cognition but must not secretly decide the cognitive answer or route.

`src/synrheon/interfaces.py`  
Browser/API transport only.

`ui/`  
Development microscope. It displays backend-owned state and evidence; it does not perform cognition.

`experiments/`  
Scientific laboratory. Hidden truth/scorers may exist here for controlled experiments but must not leak into production cognition.

# Scientific Guardrails

1. Do not tune frozen final results after inspection and keep the same experiment name.
2. Hidden correct identity must remain outside inference.
3. Renaming/permutation should continue to test identity shortcuts.
4. A mechanism that fails an ablation should lose theoretical status rather than be protected.
5. Ground 0 may be revised if stronger experiments contradict it.
6. Do not call Ground 0 Integrated until the real live organism uses it.

# Files to Read First

For most work:

```text
README.md
PROJECT_GUIDE.md
IMPLEMENTATION_STATUS.md
ARCHITECTURE_PLAN.md
```

For scientific reasoning:

```text
CONTEXT_SETTLED_TAPERING_THEORY.md
HCT2_PREREGISTRATION.md
```
