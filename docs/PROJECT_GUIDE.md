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

A mechanism can be scientifically reinforced without being live in the organism.

# Ground 0

Ground 0 is the current experimentally reinforced cognitive process future Synrheon architecture should implement, challenge, or improve.

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

Plain English: narrow what deserves serious attention without deleting alternatives, let the serious alternatives interact, and do not confuse a first-place candidate with enough evidence to commit.

Learned pathway resistance remains optional. Earlier assays found it useful, but HCT-2 showed it was not required in that task family.

The full scientific record lives in `CONTEXT_SETTLED_TAPERING_THEORY.md`.

# Why Ground 0 Is Worth Building

Earlier mechanisms provided useful negative evidence:

```text
clock-driven Top-K narrowing       failed badly
confidence-only narrowing          limited savings
stochastic consensus               false certainty
hard deletion                      failed under reversal
```

HCT-1 showed reversible soft narrowing could preserve uncertainty and restore candidates after context changed.

HCT-2 then passed every frozen criterion on 300 final held-out worlds. Its learned-order sparse system preserved 100% good behavior, 100% candidate survival, 0% unresolved commitment, 100% reversal reactivation, and 100% renaming retention while using 3.125% of full-field recurrent candidate-cycles and about 7.14% of generic-soft context evaluations.

The recurrence ablation was especially important:

```text
correct candidate survived tapering  100%
good behavior without recurrence      45%
```

So tapering preserved the useful field while recurrence performed important downstream relational work.

# What Exists Live

```text
observable runtime + development UI     Verified
cognitive substrate / organism state    Built
computational time                      Integrated
ordered experience + provenance         Integrated
E011-A trainable action policy          Built experimentally
Ground 0 cognition                      Designed / research-backed, not Integrated
```

Current live flow:

```text
Chat / injected developer thought
        ↓
dev_server.py
        ↓
runtime.py
        ↓
temporal.py + experience.py
        ↓
state.py
        ↓
UI
```

# What E011-A Still Contributes

E011-A showed that a small policy could learn which valid cognitive action/target to choose from visible state and transfer that preference across unseen and renamed worlds.

Its action set was only:

```text
EXPAND(target)
STOP
```

That is not the full Ground 0 process. Its reusable lesson is that architecture may expose valid operations while training learns which operation and target are useful.

The E011 implementation now lives in `policy.py` and `policy_learning.py`. `cognition.py` is reserved for the broader Ground 0 process.

# Source Ownership

`src/synrheon/state.py`  
Explicit organism state, concepts, relations, activation, stimuli, and trace records.

`src/synrheon/cognition.py`  
Ground 0 cognitive-cycle contract. It defines observable phase/disposition checkpoints without importing synthetic hidden truth.

`src/synrheon/policy.py`  
Retained E011-A trainable operation/target policy primitives.

`src/synrheon/policy_learning.py`  
Outcome-driven updates for the retained E011-A policy and recorded policy evidence loading.

`src/synrheon/temporal.py`  
Computational time, episode position, sequence, and elapsed-time coordinates.

`src/synrheon/experience.py`  
Current ordered autobiographical experience thread and provenance.

`src/synrheon/runtime.py`  
Traffic controller only. It sequences owners; it must not decide the cognitive answer or route.

`src/synrheon/dev_server.py`  
Local browser/API transport only.

`ui/`  
Development microscope. It displays backend-owned state and evidence; it does not perform cognition.

`experiments/`  
Scientific laboratory. Hidden truth/scorers may exist here for controlled experiments but must never leak into production cognition.

# Why Future Source Files Were Removed

Files for durable memory, retrieval, scratchpad, problem solving, consolidation, abstraction, and autonomy previously contained only roadmap docstrings. They were removed from `src/`.

Those capabilities remain in the architecture plan, but a source file should now appear only when real implementation earns an owner.

```text
planned capability ≠ implemented source module
```

# Next Integration Direction

The old assumption was to wire the narrow E011-A policy directly into the runtime. Ground 0 changes that.

The next live cognition slice should preserve the essential separation:

```text
legitimate live state
        ↓
broad candidate field
        ↓
learned routing / reversible taper checkpoint
        ↓
small serious-candidate field
        ↓
state-dependent recurrent checkpoint(s)
        ↓
evidence assessment
        ↓
commit | abstain | seek evidence | reopen
        ↓
runtime → state / trace → UI
```

The exact implementation should stay small and observable. Do not copy the synthetic HCT generator/scorer into production.

# Scientific Guardrails

1. Do not tune frozen final results after inspection and keep the same experiment name.
2. Hidden correct identity must remain outside inference.
3. Renaming/permutation should continue to test identity shortcuts.
4. A mechanism that fails an ablation should lose theoretical status rather than be protected.
5. Ground 0 may be revised if stronger experiments contradict it.
6. Do not call Ground 0 Integrated until the real live organism uses it.

# Files to Read First

For implementation:

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
