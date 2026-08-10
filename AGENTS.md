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

## Governing principle

> **Never modify the current organism to make an obsolete scientific hypothesis come true.**

A scientific experiment can run correctly and conclude that its hypothesis failed. That is a
successful experiment, not a defect. As Synrheon accumulates failed experiments this
distinction becomes more important, not less.

## Test taxonomy

A plain `python3 -m pytest` runs everything and **must be green**. Markers are for selection
and reporting; they are never permission for a test to fail.

```text
@pytest.mark.current      production architecture, invariants, live integration
                          failure = defect; blocks the stage

@pytest.mark.scientific   implementation/integrity of a current preregistered experiment
                          must pass; verifies the experiment runs correctly and its frozen
                          classifier behaves — NOT that its hypothesis is true

@pytest.mark.historical   reproduction of a superseded experiment's preserved result
                          passes when the recorded outcome is still reproduced,
                          including a recorded negative outcome
```

MT-1 and TD-5 belong to `scientific`. If MT-1 concludes that multi-stage settling provides
no advantage, MT-1 **succeeded** as an experiment even though the hypothesis failed, and no
test should turn red.

### When a test fails

```text
1. Identify its category: current architecture, current preregistered
   experiment, or historical evidence.

2. Never modify current production code merely to make a superseded
   scientific hypothesis pass.

3. For a historical reproduction, check whether the observed value still
   matches the preserved record in the test's module docstring. A changed
   value is the finding; a failed original threshold is not.

4. Only current regression/integrity failures block the stage.
```

Report results by category. `224 passed` with a category breakdown, never
`220 passed, 4 bugs remain`.

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
MT-1 preregistration FROZEN — docs/MT1_PREREGISTRATION.md
    ↓
matched-compute multi-taper falsification   ← implement next

REPRESENTATION TRACK
TD-0/1/2 Token Deck built
    ↓
TD-3 exact surface segmentation BUILT + INTEGRATED (td3-exact-surface-v1)
    ↓
TD-4 known/unknown routing BUILT + INTEGRATED (td4-acquisition-routing-v1)
    ↓
TD-5 contextual sense experiment            ← preregister next
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
surface_segmentation.py  TD-3 exact surface observation; owns no identity
acquisition_routing.py   TD-4 known/unknown routing; read-only
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

1. Implement MT-1 exactly against the frozen preregistration; do not move a threshold.
2. Drive TD-3/TD-4 with new stimuli, inspect the exact spans and routes, and convert any
   failure into a process-level regression test.
3. Preregister TD-5 before any result-bearing sense-learning implementation.
4. Keep observation identity-free: `acquire_route` is the only path to a token card, and it
   must be called explicitly.
5. Keep the tracks separate — MT-1 forbids Token Deck output in every condition.

Stimulus inspection paths:

```text
python3 -m synrheon segment "<text>"        TD-3 observation
python3 -m synrheon route "<text>"          TD-4 routing against an empty deck
POST /api/segment {"text": ...}
POST /api/acquisition {"text": ...}         TD-4 routing against the live deck
POST /api/acquire {"text": ..., "needs": [...]}   explicit acquisition
state.stimuli[].segmentation
state.stimuli[].acquisition
```
