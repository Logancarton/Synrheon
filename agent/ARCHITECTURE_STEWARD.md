# Synrheon Architecture Steward

## Canonical repository and branch discipline

```text
Repository: Logancarton/Synrheon
Canonical:  https://github.com/Logancarton/Synrheon
Current scientific branch: experiment/external-retrieval-cascade
Historical synthetic branch: experiment/hippocampal-sparse-settling
```

Do not ask which repository Synrheon belongs in. Do not silently continue current science from `main` or the historical hippocampal branch. Preserve historical branches as evidence records.

## Primary development principle

Synrheon is now developed as a **scientific build/test organism** rather than as a fixed stage ladder.

The objective is not to implement the old Ground 0 diagram intact. The objective is to identify which cognitive operations survive falsification and make each surviving operation reusable by the organism.

Core loop:

```text
scientific question / architectural need
        ↓
smallest defensible invariant
        ↓
predeclared falsifier / preregistration when needed
        ↓
reusable implementation
        ↓
integrity + behavioral tests
        ↓
raw failure inspection
        ↓
scientific classification
        ↓
architecture shrinks or earns next layer
        ↓
project truth synchronized
```

## Startup sequence

Before material work, read and reconcile in this order:

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

Use older theory/preregistration documents for historical evidence and frozen experiment rules, not as the active continuation authority when Revision 6 supersedes them.

Then follow:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

Only after the affected ownership, scientific boundary, and signal path are understood should implementation begin.

## Revision 6 evidence boundary

D6 has been run on the frozen SciFact development partition.

Observed facts:

```text
93 development queries
92 transition-evaluable queries
reset control integrity: PASS
max reset activation difference: 2.220446049250313e-16
R_reset: 1.0
frozen verdict: MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
reserved final split: untouched by D6
```

Interpret narrowly:

> Settled activation is context-conditional. Naively carrying a state settled under partial context into materially changed context can create major path-dependent damage.

Do not upgrade this to:

- proof that multiple soft stages are necessary;
- proof that D6 residual refinement is correct;
- proof recurrence is necessary;
- final held-out retrieval superiority;
- natural-language understanding;
- biological equivalence.

Condition E was diagnostic and mixed; it had no preregistered pass threshold.

## Active dual-track program

### Track A — Ground 0 science

```text
D6 COMPLETE
    ↓
MT-1 PREREGISTRATION — immediate scientific task
    ↓
MT-1 matched-compute implementation
    ↓
integrity/smoke
    ↓
allowed development assay
    ↓
frozen interpretation
```

MT-1 asks whether more than one soft contextual settling stage materially improves over one good soft stage once the known transition pathology is controlled.

Hard pruning losing is not enough. Multi-stage necessity is supported only if controlled multi-soft materially outperforms single-soft under the frozen matched-compute criterion.

Keep recurrence outside the primary MT-1 mechanism unless separately preregistered.

### Track B — Representation architecture

```text
TD-0 stable token cards               BUILT
TD-1 reversible sense inventory       BUILT
TD-2 alias/morphology storage         BUILT
TD-3 exact surface segmentation       NEXT
TD-4 known/unknown acquisition        PENDING
TD-5 contextual sense learning        PENDING EXPERIMENT
```

The tracks may progress in parallel, but Token Deck improvements must not alter MT-1 conditions unless a future preregistration explicitly combines them.

## Architecture invariants currently earned

```text
suppressed != deleted
settled activation is context-conditional
winner != sufficient evidence
surface form != token identity != sense != concept/entity != episode
hidden experimental truth never enters production cognition
runtime sequences; cognition owners decide
UI observes; it does not calculate cognitive truth
```

Designed cognitive physics may enforce identities, complete-state preservation, provenance, checkpoint/restore/reopen, legal operation boundaries, resource ceilings, and trace contracts.

Learned or experimentally earned skill should increasingly determine what context matters, what representation is useful, which operation to choose, whether another stage is worth compute, when recurrence helps, and when evidence is sufficient.

## Broad-to-narrow review gate

For every proposed change, answer:

1. What capability or scientific claim is being advanced?
2. Is this scientific assay work, reusable architecture, live integration, or documentation?
3. What current evidence justifies the mechanism?
4. What would falsify or shrink the proposed mechanism?
5. What exact state enters and leaves the owner?
6. Which owner should decide the behavior?
7. What information is forbidden from that owner?
8. What baseline/control is needed?
9. What compute must be matched or explicitly accounted for?
10. What raw failures must be preserved?
11. What status can be claimed if the test passes?
12. What should be removed or simplified if it fails?

Do not begin with stimulus-specific patches, phrase rules, arbitrary score tweaks, scripted answers, hidden target selectors, benchmark truth, or UI-side cognition.

## Scientific workflow

For result-bearing experimental changes:

```text
question
  ↓
preregister hypothesis + controls + metrics + success/failure rules
  ↓
commit preregistration before result inspection
  ↓
implement mechanism without changing frozen criteria
  ↓
integrity tests
  ↓
synthetic smoke = code-path check only
  ↓
allowed development/held-out run
  ↓
apply frozen classifier
  ↓
record raw results + failures
  ↓
update evidence ledger
```

Never retune a frozen threshold after seeing the result. Never relabel a smoke run as evidence. If a development set has been repeatedly inspected, treat it as tuning/diagnostic data rather than final confirmation.

## Stimulus-test architecture workflow

For organism-facing capabilities:

```text
build one capability
        ↓
feed explicit stimuli
        ↓
inspect exact backend-owned state / trace
        ↓
locate the failed process/owner
        ↓
fix the process, not the sample phrase
        ↓
add regression test
        ↓
repeat with harder stimuli
```

A UI should make the integrated stage observable, but it must not fabricate the cognitive result.

## Token Deck rules

Current owner:

```text
src/synrheon/token_deck.py
```

Core separation:

```text
raw text
  ↓
surface span
  ↓
stable token identity
  ↓
possible senses
  ↓
optional concept/entity links
  ↓
event / memory representation later
```

TD-3 segmentation must preserve exact text and offsets. It must not choose meaning, infer a correct sense, fabricate a concept, or use an LLM as an invisible authority.

External dictionaries/parsers/LLMs may later propose evidence with provenance. Proposal is not truth.

## Current production ownership

```text
state.py               explicit organism/substrate state; contains TokenDeck
cognition.py           Ground 0 public contracts / cognitive boundary
contextual_search.py   reversible candidate field + transition checkpoints
token_deck.py          stable token/sense identity + reversible sense state
policy.py              retained E011-A donor policy
policy_learning.py     retained E011-A learning
experience.py          ordered current-episode experience + provenance
temporal.py            time/sequence coordinates
runtime.py             thin sequencing only
dev_server.py          local transport only
experiments/           scientific harnesses, qrels, hidden evaluation/scoring
ui/                    observation and control only
```

Do not fabricate a candidate field merely to claim contextual search is Integrated. The live organism needs a legitimate candidate source from representation/memory/retrieval first.

## Status vocabulary

Keep two dimensions separate.

Scientific evidence:

```text
Historical synthetic evidence
External development evidence
Confirmatory held-out evidence
Supported
Partially supported
Discounted / falsified
Inconclusive
Untested
```

Implementation maturity:

```text
Not Started
Designed
Built
Integrated
Verified
```

`Built` means implementation exists and passes the relevant isolated/controlled gates. `Integrated` means the real runtime reaches it. `Verified` requires intended live behavior observed through the running organism with relevant state/trace.

Automated tests do not independently grant `Verified`.

## Runtime principle

`runtime.py` may sequence owners, route typed handoffs, invoke bounded operations, record observable trace, and return outcomes.

It must not own candidate ranking, sense selection, context selection, memory truth, learned policy weights, or commitment decisions.

## UI principle

The UI is a microscope and behavioral laboratory. It should show:

```text
what is really integrated
what the mechanism is doing now
what internal state changed
what evidence/uncertainty remains
what historical learning/scientific evidence exists
```

Keep historical scientific evidence visibly separate from current live behavior.

## Tests

Prefer high-value tests that prove invariants and process boundaries:

- stable identity reuse;
- no silent deletion of alternatives;
- context reversal/reopen behavior;
- exact transition reset independence;
- malformed input fails safely;
- hidden truth cannot reach inference owners;
- unrelated state is not mutated;
- live call path reaches the true owner when integration is claimed;
- regressions are built from observed failures, not cosmetic constructor coverage.

## Documentation synchronization

After meaningful work, update only affected current truth. Revision 6 authority order is:

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

Do not silently rewrite historical preregistrations after results are observed.

## Git safety

Preserve unrelated dirty work. Never use destructive cleanup to make the repository look clean.

Avoid:

```text
git add .
git clean
git reset --hard
force-push / history rewrite
```

Stage intended files explicitly. After relevant gates pass, make focused reversible commits and push the active branch unless explicitly told not to.

## Completion review

Before declaring a bounded change complete, confirm:

- active branch and current scientific authority were checked;
- claim and falsifier were explicit;
- preregistration preceded result-bearing experimentation when needed;
- implementation is in the correct owner;
- no hidden truth or benchmark shortcut entered cognition;
- runtime remains thin;
- UI remains observational;
- raw failures were preserved;
- evidence status and implementation maturity are not conflated;
- negative results simplify rather than trigger post-hoc tuning;
- docs match actual current truth;
- intended files were committed without disturbing unrelated work.
