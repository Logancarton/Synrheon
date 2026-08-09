**Synrheon** — from Greek *syn* (“together”) + *rheō* (“to flow”). Roughly: **“flows coming together.”**

# Synrheon: A Brain-Inspired Recursive Cognitive Architecture for Persistent Artificial Intelligence

This repository is the canonical home for Synrheon.

The current implementation priority is **Stage 1 — Trainable Cognition Pivot**. The verified runtime/UI, cognitive substrate, computational time, provenance, and ordered experience process remain in place, but the experimental hand-written lexical/spreading/Top-K thinking policy has been removed.

## Core Research Hypothesis

Synrheon should not primarily be trained to memorize `input → answer` mappings. It should increasingly learn **how to transform its own cognitive state**:

```text
experience / current state
        ↓
recognize what kind of cognitive work is needed
        ↓
choose a cognitive action
        ↓
perform one short transition
        ↓
checkpoint
        ↓
evaluate prediction / evidence / outcome
        ↓
choose the next action or stop
        ↓
assign credit and learn from what worked
```

The project therefore separates **knowledge** from **cognitive skill**. Concepts, experiences, relations, memory, tools, and outside information may supply what Synrheon knows. The trainable cognition system should learn what to **do with** that information.

## What We Intend to Train

The long-term trainable layers are:

```text
concept representations
organization / routing
cognitive-action selection
state-transition prediction
retrieval strategy
prediction / revision behavior
credit assignment
abstraction
```

Language is an input/output interface around cognition, not the definition of cognition itself.

## Immediate Proof Required

The first trainable experiment must demonstrate **transfer**, not answer memorization:

```text
train on unrelated knowledge worlds A / B / C
                    ↓
learn a cognitive process
                    ↓
evaluate on unseen world D
                    ↓
useful cognitive operations above baseline
```

Renaming concepts, changing surface wording, or withholding training-world answers must not destroy the learned strategy. If success depends on memorized names, relation labels, prompts, or answers, the experiment fails.

See `docs/PROJECT_GUIDE.md`, `docs/SIGNAL_FLOW.md`, `docs/ARCHITECTURE_PLAN.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/CURRENT_STAGE.md`, `docs/DECISIONS.md`, and `docs/EXPERIMENTS.md` for current implemented truth and the next experimental boundary.
