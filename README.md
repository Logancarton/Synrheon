**Synrheon** — from Greek *syn* (“together”) + *rheō* (“to flow”). Roughly: **“flows coming together.”**

# Synrheon

A brain-inspired recursive cognitive architecture for persistent artificial intelligence.

This repository is the canonical home for Synrheon.

## Ground 0 — Current Research Foundation

Synrheon now treats the experimentally reinforced HCT-1/HCT-2 result as **Ground 0**: the baseline cognitive process future architecture must implement, challenge, or improve.

Ground 0 is:

```text
VERY LARGE CANDIDATE / KNOWLEDGE FIELD
        ↓
learned context-dependent routing
        ↓
ordered reversible soft tapering
        ↓
SMALL SERIOUS-CANDIDATE FIELD
        ↓
state-dependent recurrent deliberation
        ↓
evidence / uncertainty state
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
```

Historical pathway reliability/resistance remains an optional learned modifier. Earlier assays found it promising, but HCT-2 showed it was not necessary in that task family.

The central principle is therefore:

> **Narrow softly, preserve reversibility, deliberate recurrently, and separate having a winner from having enough evidence to commit.**

## Why Ground 0 Changed the Architecture

Earlier experiments ruled out several attractive but brittle approaches:

```text
clock-driven progressive Top-K        failed
single global confidence gate         limited
stochastic winner consensus           false certainty
irreversible hard pruning             failed under context reversal
```

HCT-1 then showed that reversible soft narrowing could preserve correct candidates, uncertainty, and context-driven recovery while sharply reducing the field entering recurrence.

HCT-2 strengthened the theory:

```text
300 final held-out worlds
all frozen HCT-2 criteria passed
learned-order sparse good behavior      100%
correct-candidate survival              100%
unresolved commitment                     0%
context-reversal reactivation           100%
renaming retention                      100%
recurrent load vs no taper              3.125%
context evaluations vs generic soft     7.14%
learned-order efficiency gain           5.49%
```

The recurrence ablation was especially important: removing recurrence reduced good behavior to 45% even though the correct candidate survived tapering 100% of the time. Tapering and recurrence therefore performed distinct jobs in that family.

## Ground 0 Is Not Yet Live Production Cognition

The HCT work is controlled synthetic research. It is **not yet Integrated** into the running Synrheon organism.

The live repository still contains useful earlier foundations:

```text
observable runtime + UI
explicit cognitive substrate
computational time
ordered experience + provenance
first trainable operation/target policy from E011-A
```

E011-A remains evidence that a cognitive policy can learn transferable action preferences without memorizing opaque candidate identities. It should now be treated as a donor mechanism for learned routing, not as the complete cognitive architecture.

The old assumption that E011-B should simply wire the narrow E011-A policy directly into the organism is therefore under review. The next integration design should express Ground 0 cleanly through the real organism.

## Designed Cognitive Physics vs Learned Cognitive Skill

Synrheon should explicitly design only the reusable computational rules and boundaries:

```text
state / candidate representation
reversible suppression mechanics
recurrent update interface
compute ceilings
checkpoint / provenance structure
commit / abstain / reopen interfaces
validation / safety boundaries
```

Experience and training should increasingly determine:

```text
which context matters
which context to evaluate next
how strongly to taper
which region deserves compute
which cognitive operation / target to choose
when recurrence is useful
when evidence is enough
when to reopen broader context
```

A useful shorthand remains:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

## Scientific Sources of Truth

The consolidated scientific theory is:

```text
docs/CONTEXT_SETTLED_TAPERING_THEORY.md
```

The frozen HCT-2 preregistration is:

```text
docs/HCT2_PREREGISTRATION.md
```

Current implementation truth and architecture are summarized in:

```text
docs/PROJECT_GUIDE.md
docs/IMPLEMENTATION_STATUS.md
docs/ARCHITECTURE_PLAN.md
```
