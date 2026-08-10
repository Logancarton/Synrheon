**Synrheon** — from Greek *syn* (“together”) + *rheō* (“to flow”). Roughly: **“flows coming together.”**

# Synrheon

A research-driven recursive cognitive architecture for persistent artificial intelligence.

This repository is the canonical home for Synrheon.

## Current scientific branch

```text
experiment/external-retrieval-cascade
```

Historical synthetic branch:

```text
experiment/hippocampal-sparse-settling
```

Current continuation authority:

```text
docs/REV6_CONTINUATION_STATE.md
```

## Revision 6 thesis

Synrheon is investigating whether cognition over a very large knowledge field can remain broad and reversible while allocating deeper computation only where the current unresolved question requires it.

Current working flow:

```text
QUESTION / UNRESOLVED STATE
        ↓
legitimate broad candidate field
        ↓
select potentially discriminating context
        ↓
explicit context transition
        ↓
reversible contextual settling
        ↓
re-evaluate what remains unresolved
        ↓
optional deeper refinement / optional recurrence only if earned
        ↓
evidence sufficiency
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
```

The architecture is deliberately falsifiable. Mechanisms are removed or weakened when stronger evidence fails to support them.

## D6 — current strongest new development result

Revision 5 suspected that partial-context activation was being carried too strongly into later full context.

D6 isolated that transition on the frozen SciFact development partition.

Observed:

```text
93 development queries
92 transition-evaluable
reset control integrity: PASS
max reset activation difference: 2.220446049250313e-16
R_reset = 1.0
frozen verdict = MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

The supported lesson is narrow:

> **Settled activation is context-conditional state. Blindly carrying a state settled under partial context into materially changed context can create major path-dependent damage.**

This does not establish multi-taper necessity, residual refinement, recurrence necessity, final held-out superiority, or natural-language understanding.

## Current dual-track program

### Track A — Ground 0 science

```text
D6 complete
    ↓
MT-1 preregistration
    ↓
matched-compute multi-taper falsification
```

MT-1 asks whether more than one soft contextual settling stage materially outperforms one good soft stage after transition-state persistence is controlled.

Hard pruning losing is not sufficient evidence for multiple soft stages.

### Track B — representation architecture

```text
TD-0 stable token identity          Built
TD-1 multiple reversible senses     Built
TD-2 alias/morphology storage       Built
TD-3 exact surface segmentation     Next
TD-4 known/unknown acquisition      Later
TD-5 contextual sense learning      Later experiment
```

The Token Deck begins the path from raw language to stable internal representations.

Core separation:

```text
surface form != token identity != sense != concept/entity != episode
```

## Production-facing architecture already built

### Reversible candidate field

Owner:

```text
src/synrheon/contextual_search.py
```

Provides complete broad-field state, active/dormant regions, reversible checkpoints, restore/reopen, and explicit carry/reset/residual transition provenance.

### Token Deck

Owner:

```text
src/synrheon/token_deck.py
```

Provides stable token identity, observed forms/aliases, provenance, multiple candidate senses, optional concept links, non-inferential morphology storage, and reversible context-conditioned sense activation.

The Token Deck is stored in the live `CognitiveSubstrate`, but normal chat is not yet automatically segmented into token observations.

## What exists live

```text
observable runtime + development UI      Verified
computational time                       Integrated
ordered experience + provenance          Integrated
cognitive substrate                      Built
Token Deck TD-0/1/2                      Built
reversible candidate field               Built, not live-integrated
E011-A learned policy                    Historical controlled donor
Ground 0 contextual cognition            Not Integrated
durable memory                           Not Started
learned retrieval                        Not Started
recursive autonomous cognition           Not Started
```

## Development rule

Science:

```text
claim + falsifier
    ↓
preregister
    ↓
implement
    ↓
integrity/smoke
    ↓
allowed evidence run
    ↓
frozen interpretation
    ↓
simplify or earn next layer
```

Organism capabilities:

```text
build one capability
    ↓
give explicit stimuli
    ↓
inspect backend-owned state / trace
    ↓
fix the process, not the phrase
    ↓
add the failure as a regression test
    ↓
repeat with harder stimuli
```

The objective is not to make the original theory win. The objective is to discover which cognitive operations continue to deserve being built.

## Read first

```text
docs/REV6_CONTINUATION_STATE.md
docs/CURRENT_STAGE.md
docs/IMPLEMENTATION_STATUS.md
docs/ARCHITECTURE_PLAN.md
docs/TOKEN_DECK_ROADMAP.md
docs/PROJECT_GUIDE.md
docs/SIGNAL_FLOW.md
docs/SCAFFOLD.md
```

Agent workflow:

```text
AGENTS.md
agent/ARCHITECTURE_STEWARD.md
.agents/skills/synrheon-development-workflow/SKILL.md
```

Older theory and preregistration documents remain part of the scientific record and should not be silently rewritten after results are observed.
