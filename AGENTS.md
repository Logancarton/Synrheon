# Synrheon Agent Entry Point

Canonical repository:

```text
https://github.com/Logancarton/Synrheon
```

Current scientific continuation branch:

```text
experiment/external-retrieval-cascade
```

Historical synthetic branch:

```text
experiment/hippocampal-sparse-settling
```

Do not silently move scientific work back to `main` or to the historical hippocampal branch.

## Read first

Before material work, read in this order:

```text
README.md
docs/REV6_CONTINUATION_STATE.md
docs/CURRENT_STAGE.md
docs/IMPLEMENTATION_STATUS.md
docs/ARCHITECTURE_PLAN.md
docs/TOKEN_DECK_ROADMAP.md
agent/ARCHITECTURE_STEWARD.md
.agents/skills/synrheon-development-workflow/SKILL.md
```

Then inspect the relevant frozen preregistration/result documents and receiving source owners.

Older Revision 4/5 theory and E011/HCT material remains historical evidence. It must not override Revision 6 continuation state when documents conflict.

## Current project state

D6 is complete on the frozen SciFact development partition:

```text
93 development queries
92 transition-evaluable
reset integrity: PASS
R_reset = 1.0
verdict = MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

The supported architectural lesson is narrow:

> Settled activation is context-conditional state; blindly carrying a state settled under partial context into materially changed context can cause strong path-dependent damage.

D6 does **not** establish multi-taper necessity, residual refinement, recurrence necessity, natural-language understanding, or final held-out superiority.

## Active work is dual-track

```text
SCIENTIFIC TRACK
D6 complete
    ↓
MT-1 preregistration
    ↓
matched-compute multi-taper falsification

REPRESENTATION TRACK
TD-0/1/2 Token Deck built
    ↓
TD-3 exact surface segmentation
    ↓
TD-4 known/unknown routing
    ↓
TD-5 contextual sense experiment
```

Keep the tracks separate until an experiment explicitly preregisters their integration.

Token Deck work must not be used to rescue or reinterpret MT-1 after results are seen.

## Development doctrine

Use this loop:

```text
read current truth
    ↓
state claim + falsifier
    ↓
preregister when scientific
    ↓
build smallest reusable mechanism
    ↓
test integrity / behavior
    ↓
inspect raw failures
    ↓
classify evidence honestly
    ↓
fix the process, not the example
    ↓
update project truth
    ↓
focused commit
```

Never loosen a frozen threshold after seeing a result. Never hide a negative result. Never add phrase-specific or benchmark-answer-specific patches.

## Architecture invariants currently earned

```text
suppressed != deleted
settled state is context-conditional
winner != sufficient evidence
hidden truth never enters production cognition
runtime sequences; it does not own cognition
UI observes; it does not decide
surface form != token identity != sense != concept/entity != episode
```

## Current production owners

```text
state.py               organism/substrate state; contains TokenDeck
cognition.py           Ground 0 public contracts / cognitive boundary
contextual_search.py   reversible candidate field / transition checkpoints
token_deck.py          stable token/sense identity and reversible sense state
policy.py              retained E011-A donor policy
policy_learning.py     retained E011-A learning
experience.py          ordered experience + provenance
temporal.py            computational time / sequence
runtime.py             thin sequencing only
dev_server.py          transport only
experiments/           scientific assays / qrels / hidden scoring
ui/                    observation and control only
```

## Status discipline

Keep scientific evidence separate from implementation maturity.

Evidence:

```text
historical synthetic
external development
confirmatory held-out
supported / partial / discounted / inconclusive / untested
```

Maturity:

```text
Not Started / Designed / Built / Integrated / Verified
```

Automated tests can support `Built` or `Integrated`; they do not independently grant `Verified`.

## Immediate priorities

1. Preserve D6 as completed development evidence.
2. Freeze MT-1 before implementing result-bearing changes.
3. Verify Token Deck TD-0/1/2 locally.
4. Build TD-3 exact segmentation without meaning inference.
5. Continue stimulus-test development by inspecting backend-owned state and converting failures into process-level regression tests.
