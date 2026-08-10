---
name: synrheon-development-workflow
description: Use proactively for Synrheon research, architecture, Token Deck, cognition, memory, retrieval, experimentation, live integration, testing, UI/runtime work, documentation synchronization, Git commits, and scientific handoff. Preserve preregistration boundaries, separate evidence from implementation maturity, fix processes rather than examples, keep research and representation tracks independent until explicitly combined, and make every validated experiment leave behind reusable organism architecture where justified.
---

# Synrheon Development Workflow — Revision 6

Canonical repository:

```text
Repository: https://github.com/Logancarton/Synrheon
Full name:  Logancarton/Synrheon
Current scientific branch: experiment/external-retrieval-cascade
Historical synthetic branch: experiment/hippocampal-sparse-settling
```

Do not assume `main` is the current scientific continuation branch. Do not move current work back to the historical hippocampal branch.

## Source-of-truth order

Before material work, read in this order:

```text
README.md
docs/REV6_CONTINUATION_STATE.md
docs/CURRENT_STAGE.md
docs/IMPLEMENTATION_STATUS.md
docs/ARCHITECTURE_PLAN.md
docs/TOKEN_DECK_ROADMAP.md
docs/PROJECT_GUIDE.md
docs/SIGNAL_FLOW.md
docs/SCAFFOLD.md
```

Then inspect the relevant frozen preregistration/result record and affected source/test files.

Older Revision 4/5 theory, HCT, and E011 documents remain evidence history. They do not override Revision 6 current state.

## Current scientific truth

D6 has been run on SciFact development under the frozen protocol.

```text
development queries:              93
transition-evaluable:             92
reset integrity:                  PASS
max reset activation difference:  2.220446049250313e-16
R_reset:                          1.0
frozen verdict:                   MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

Supported interpretation:

> A settled activation distribution is context-conditional state. Blindly carrying a state settled under partial context into changed context can be a major source of path-dependent damage.

Do not infer from D6 that multi-taper processing is necessary, residual refinement is solved, recurrence is required, or external final superiority has been established.

## Active dual-track program

### Track A — scientific mechanism testing

Immediate boundary:

```text
D6 result preserved                                    DONE
    ↓
MT-1 v1 preregistration                                FROZEN, then DESIGN-INVALID
    ↓
CPN-1 equal-budget contextual pre-narrowing            FROZEN
    ↓
integrity + synthetic smoke
    ↓
allowed development assay
    ↓
frozen interpretation
```

MT-1 asks whether more than one soft contextual settling stage adds value over one good soft stage after transition-state persistence is controlled.

Hard pruning losing is not enough evidence for multiple stages. Recurrence should remain outside the primary MT-1 test unless separately preregistered.

### Track B — representation / organism construction

Current Token Deck state:

```text
TD-0 stable token cards               Built
TD-1 multiple reversible senses       Built
TD-2 alias/morphology storage         Built, non-inferential
TD-3 exact surface segmentation       Built + Integrated (td3-exact-surface-v1)
TD-4 known/unknown acquisition        Built + Integrated (td4-acquisition-routing-v1)
TD-5 contextual sense learning        Next; preregister before results
```

TD-3 owner is `src/synrheon/surface_segmentation.py`. It observes surface structure and
assigns no token, sense, or concept identity, so it can be replaced without invalidating
anything the Token Deck owns. Inspect it with `python3 -m synrheon segment "<text>"`,
`POST /api/segment`, or `state.stimuli[].segmentation`.

The representation track may advance while MT-1 is designed, but it may not change MT-1 inputs, feature channels, thresholds, data, or interpretation after the MT-1 boundary is frozen.

## Core doctrine

Use the same loop for the entire project:

```text
READ CURRENT TRUTH
        ↓
CLASSIFY THE WORK
        ↓
STATE CLAIM + FALSIFIER
        ↓
FREEZE SCIENTIFIC RULES WHEN NEEDED
        ↓
BUILD SMALLEST REUSABLE MECHANISM
        ↓
TEST IN LAYERS
        ↓
INSPECT RAW FAILURES
        ↓
CLASSIFY EVIDENCE
        ↓
SIMPLIFY OR EARN NEXT LAYER
        ↓
SYNC DOCS
        ↓
FOCUSED COMMIT
```

The project is not optimized to make the preferred theory win.

## Step 1 — preserve current work and identify branch

Before editing:

```bash
git status --short
git branch --show-current
git log -5 --oneline
```

Preserve unrelated dirty work. Never use destructive cleanup simply to make the worktree clean.

Avoid:

```text
git add .
git clean
git reset --hard
force push
```

## Step 2 — classify the requested work

Choose one primary mode:

```text
A. Scientific assay
B. Reusable architecture
C. Live integration / stimulus testing
D. Documentation / research handoff
```

A task may touch more than one mode, but identify the boundaries explicitly.

### Scientific assay

Requires hypothesis, controls, leakage boundary, metrics, success/failure interpretation, data boundary, and preregistration before result-bearing inspection when appropriate.

### Reusable architecture

Requires a clear owner, invariant, input/output contract, high-value tests, and restraint against embedding unvalidated cognitive skill as hard-coded logic.

### Live integration

Requires a legitimate upstream source, real runtime call path, observable backend state/trace, and human stimulus testing before `Verified` is claimed.

### Documentation

Must reflect actual scientific and implementation truth without rewriting historical preregistration after results.

## Step 3 — state the claim and falsifier

Before coding, answer:

1. What capability or mechanism is being tested/built?
2. What current evidence justifies it?
3. What result would make it smaller, optional, or wrong?
4. What baseline/control is needed?
5. Which information must remain unavailable?
6. Which owner decides and which owner only sequences?
7. What compute must be matched or measured?
8. What raw failures must remain inspectable?
9. What status may be claimed if it passes?
10. What architecture should be removed or simplified if it fails?

If these are unclear, resolve them before implementing result-bearing behavior.

## Step 4 — preregister scientific work before the result

For MT-1 or any comparable experiment, freeze before result inspection:

```text
hypothesis
conditions / baselines
candidate/data boundary
allowed features / context
forbidden information
matched-compute definition
primary metric(s)
paired uncertainty/statistics
success threshold
partial/inconclusive/failure rules
ablation(s)
random seeds / resampling rules
final-split policy
raw output requirements
```

Commit the preregistration separately before implementation/results whenever practical.

Do not change thresholds after seeing the result. A versioned amendment made before further result inspection must be explicit.

## Step 5 — build the smallest reusable mechanism

Prefer production-facing cognitive physics that remains useful under both positive and negative experiment outcomes.

Examples already justified:

```text
complete candidate-field identity
reversible suppression / dormant alternatives
checkpoint / restore / reopen
context-transition provenance
stable token identity
multiple recoverable senses
surface/sense/concept separation
provenance
```

Do not hard-code unearned skill such as:

```text
fixed semantic hierarchy
universal stage count
static recurrence as mandatory
answer-specific target selector
phrase-specific chat fixes
custom confidence threshold chosen after results
LLM output treated as truth
```

## Step 6 — enforce ownership

Current owners:

```text
state.py               organism/substrate state; contains TokenDeck
cognition.py           Ground 0 public cognitive contracts
contextual_search.py   reversible candidate field / transition state
token_deck.py          lexical/sense identity and reversible sense state
policy.py              historical E011-A donor policy
policy_learning.py     historical E011-A policy learning
experience.py          ordered current-episode experience + provenance
temporal.py            computational time / sequence
runtime.py             thin sequencing
dev_server.py          transport
experiments/           hidden truth / qrels / scientific scoring
ui/                    observation/control
```

Runtime must not become a parallel cognition, tokenizer, retrieval engine, memory system, or scientific scorer.

UI must not choose actions, senses, candidates, or scientific pass/fail status.

## Step 7 — keep hidden truth out of production cognition

Experiment harnesses may know qrels, hidden correct identities, generators, scorers, or labels for evaluation.

Production cognition must not receive answer-bearing truth that would not exist in real use.

If answer leakage occurs, the result is invalid regardless of score.

## Step 8 — test in layers

Use the lightest test that answers each question.

```text
unit/invariant tests
    ↓
integration/interface tests
    ↓
synthetic smoke (code-path only; never evidence)
    ↓
allowed scientific development/held-out assay
    ↓
live stimulus test if integrated
```

Do not equate passing pytest with cognitive verification.

## Test taxonomy and failure triage

A plain `python3 -m pytest` runs everything and **must be green**. Markers select and
report; they are never permission for a test to fail.

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

The repository separates experimental outcomes from software outcomes:

```text
experiment
    ↓
measure observations
    ↓
frozen classifier evaluates the hypothesis
    ↓
scientific verdict: SUPPORTED / DISCOUNTED / MIXED / INCONCLUSIVE
    ↓
software test verifies the classifier and the preserved result behave correctly
    ↓
pytest stays green
```

A preregistered hypothesis must never be encoded directly as a bare pytest assertion.
Encode the observation and the frozen threshold separately, so a failed hypothesis reads as
a recorded verdict rather than a red test.

When a test fails:

```text
1. Identify its category.
2. Never modify current production code merely to make a superseded
   scientific hypothesis pass.
3. For a historical reproduction, compare against the preserved record in
   the test's module docstring. A changed observation is the finding.
4. Only current regression/integrity failures block the stage.
```

> **Never modify the current organism to make an obsolete scientific hypothesis come true.**


## Step 9 — stimulus-test process, not phrases

For organism-facing work:

```text
build one capability
        ↓
give explicit stimulus
        ↓
inspect exact backend state / trace
        ↓
identify failed owner / transition / representation
        ↓
fix process
        ↓
add regression test from failure
        ↓
retry with harder / adversarial stimulus
```

Never solve a failed stimulus with a phrase-specific rule if the underlying process is wrong.

For TD-3, test punctuation, contractions, possessives, hyphens, quotes, numbers, symbols, case variants, names, and exact character offsets. Meaning inference is explicitly out of scope for TD-3.

## Step 10 — Token Deck discipline

Core invariant:

```text
surface form != token identity != sense != concept/entity != episode
```

A token card may retain multiple senses. Context may alter activation among senses, but alternatives must remain recoverable.

External dictionary/parser/LLM assistance may later propose morphology, senses, concepts, or structure, but each proposal must preserve source provenance and remain distinguishable from Synrheon-learned or user-confirmed information.

Unknown names/entities must not automatically be treated like dictionary words.

## Step 11 — D6 lesson for future state transitions

Do not assume previous settled activation should always become the prior for the next context.

Every context transition should make the mode explicit:

```text
carry
reset / re-anchor
residual / transformed update
reopen
```

The correct mode is a cognitive skill to learn/test later; the architecture should preserve enough provenance/state to support alternatives.

## Step 12 — MT-1 discipline

MT-1 must test stage necessity, not bundle multiple new ideas.

Conceptual conditions should include:

```text
retrieval/no-taper anchor
single full-context soft
multi-soft with naive carry       # pathology control
multi-soft with controlled reset
scrambled/reversed order
matched-compute hard staged pruning
```

Do not reintroduce recurrence, richer Token Deck features, or new context channels into the primary MT-1 comparison unless the preregistration explicitly makes them part of the test before results.

## Step 13 — evidence classification

Use explicit labels:

```text
Supported
Partially supported
Discounted / falsified
Inconclusive
Untested
```

And separately use implementation maturity:

```text
Not Started
Designed
Built
Integrated
Verified
```

A development-set positive finding is not confirmatory held-out evidence. A scientific result may be meaningful while the implementation remains only `Built`.

## Step 14 — negative results change architecture

When a frozen test fails:

1. preserve the failure;
2. diagnose with the smallest justified follow-up;
3. remove or weaken the unsupported architectural claim;
4. do not lower the threshold simply to retain the mechanism;
5. do not hide the result behind a new aggregate score.

This is how EXT-1 led to EXT-2 and D6.

## Step 15 — synchronize project truth

Current authority order:

```text
docs/REV6_CONTINUATION_STATE.md
docs/CURRENT_STAGE.md
docs/IMPLEMENTATION_STATUS.md
docs/ARCHITECTURE_PLAN.md
docs/TOKEN_DECK_ROADMAP.md
relevant frozen preregistration/result docs
docs/PROJECT_GUIDE.md
docs/SIGNAL_FLOW.md
docs/SCAFFOLD.md
```

Update only affected truth. Preserve historical theory/preregistration documents as chronology.

## Step 16 — repository verification

Run relevant focused tests first, then broader gates as appropriate:

```bash
python3 -m pytest -q <focused tests>
python3 -m pytest -q                 # everything; must be green
python3 -m pytest -q -m current      # production architecture and invariants
python3 -m pytest -q -m scientific   # current experiment implementation/integrity
python3 -m pytest -q -m historical   # reproduction of preserved historical results
python3 -m compileall -q src tests experiments
git diff --check
git status --short
git diff
```

On src-layout machines where the package is not installed editable, use the project's environment/setup or explicit `PYTHONPATH="$PWD/src"` for direct module execution rather than changing scientific code to work around import setup.

## Step 17 — commit chronology

Prefer focused, reversible chronology:

```text
preregistration commit
implementation commit
test/integrity commit
result record commit
theory/status update commit
```

Do not amend a preregistration after observing results merely to make it match the outcome.

## Definition of done

A bounded change is complete only when:

- [ ] current Revision 6 truth and active branch were checked;
- [ ] work mode was identified;
- [ ] claim and falsifier were explicit;
- [ ] scientific criteria were frozen before result inspection when required;
- [ ] hidden-answer boundaries were preserved;
- [ ] mechanism lives in the correct owner;
- [ ] no phrase/world-specific patch was introduced;
- [ ] tests target meaningful invariants/behavior;
- [ ] raw failures remain inspectable;
- [ ] evidence was classified without overclaiming;
- [ ] implementation maturity was classified separately;
- [ ] runtime/UI boundaries remain clean;
- [ ] parallel research/representation tracks were not accidentally mixed;
- [ ] documentation authority files match current truth;
- [ ] relevant verification commands pass;
- [ ] intended files are committed/pushed without disturbing unrelated work.

The governing rule is:

> **Fix the process, preserve the failure, freeze the science before the result, and build only mechanisms that continue to earn a place in the organism.**
