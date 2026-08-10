# Synrheon Revision 6 Continuation State

**Authoritative continuation protocol for active research and architecture work**

Branch:

```text
experiment/external-retrieval-cascade
```

Historical synthetic branch:

```text
experiment/hippocampal-sparse-settling
```

Do not move scientific continuation back to the historical branch. Preserve it as evidence history.

## Revision 6 scientific state

Revision 5 ended with D6 as the immediate diagnostic gate. D6 has now been run on the frozen 93-query SciFact development partition.

Observed D6 facts:

```text
development queries:                 93
transition-evaluable queries:        92
reset control integrity:             PASS
max reset activation difference:     2.220446049250313e-16
reset recovery fraction R_reset:     1.0
frozen verdict:                      MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
reserved final split:                untouched by D6
```

The result supports a narrower architectural claim:

> A settled activation distribution is context-conditional state. Blindly carrying a state settled under partial or under-specified context into materially changed context can create strong path-dependent damage.

This does **not** establish that multiple soft contextual stages are necessary. It does **not** validate residual refinement. It does **not** restore static recurrence.

Condition E in D6 showed mixed query-level behavior and had no preregistered success threshold. Treat residual refinement as unresolved rather than as the default cure.

## Current evidence ledger

### Supported or strengthened

- Reversible suppression has strong synthetic evidence.
- A single full-context soft taper approximately preserves the SciFact BM25 development anchor.
- The BM25 top-100 field retains meaningful oracle headroom.
- D6 supports inappropriate carried activation as a major contributor to the partial-to-full transition failure on SciFact development.
- Explicit context-transition provenance and reset/reopen capability deserve a production-facing representation.
- E011-A remains historical controlled evidence that operation/target preferences can be learned across unseen and renamed synthetic worlds.

### Discounted / falsified in the current implementation

- EXT-1 C1/C2/C3 were not validated as originally hoped.
- The current four hand-designed lexical context channels are not established as useful residual discriminators.
- Current static recurrence harmed SciFact development ranking.
- Current commitment calibration is not established.
- HCT-2 does not establish external recurrence necessity because of identified synthetic confounds.
- Hard pruning losing does not establish multiple-soft-stage necessity.

### Open / untested

- Whether more than one soft contextual settling stage adds value after transition pathology is controlled.
- Question-guided contextual divergence with richer, genuinely discriminating context.
- Trajectory-relative recurrence.
- External value of reopening on a suitable changing-context task.
- Calibrated commitment beyond strong baselines.
- Token/sense representations as useful retrieval/context signals.

## Immediate scientific track — MT-1

D6 unlocks specification of **MT-1: Matched-Compute Multi-Taper Falsification**.

MT-1 must be preregistered before result-bearing implementation or data inspection changes its criteria.

Its central question is:

> After controlling the known transition-state persistence pathology, does more than one soft contextual settling stage materially outperform one good soft settling stage under matched computation?

The preregistration should include at least these conceptual controls:

```text
no-taper / retrieval anchor
single full-context soft settling
multiple soft stages with naive carry          # known-dangerous transition control
multiple soft stages with controlled reset
scrambled/reversed context-order control
matched-compute hard staged pruning
```

Recurrence should remain outside the primary MT-1 mechanism unless separately preregistered; MT-1 should isolate stage necessity rather than reintroduce a discounted operator.

Critical interpretation rule:

> Hard pruning losing is evidence about reversibility, not evidence that multiple soft stages are necessary.

If controlled multi-soft does not materially beat single-soft under the frozen matched-compute criterion, remove multiple-stage necessity from Ground 0.

Do not use the reserved final external split while designing or tuning MT-1.

## Parallel architecture track — Token Deck

The representation track may advance while MT-1 is designed, but it must not alter MT-1 inputs, channels, thresholds, or evaluation unless a later preregistration explicitly combines the tracks.

Current Token Deck state:

```text
TD-0 stable token identity                 BUILT
TD-1 multiple reversible senses            BUILT
TD-2 alias/morphology storage              BUILT (non-inferential)
TD-3 surface segmentation                  NEXT
TD-4 known/unknown acquisition             pending
TD-5 contextual sense disambiguation       pending experiment
TD-6 concept/entity bridge                 contract begun; behavior pending
TD-7 event/semantic-role composition       pending
TD-8 durable Token Deck                    pending
TD-9 candidate-source bridge               pending
TD-10 learned vocabulary growth            pending
```

Core invariant:

```text
surface form != token identity != sense != concept/entity != episode
```

D6's context lesson applies to sense state as an architectural invariant: context may change sense activation, but a weak alternative must not be silently deleted.

TD-3 should segment raw text into exact observable spans and preserve original offsets. It must not infer meaning, choose a sense, fabricate a concept, or call an LLM as a hidden authority.

## Build/test workflow

Synrheon now uses a repeating scientific-engineering loop rather than a stage-number march that protects an old architecture.

```text
1. READ CURRENT TRUTH
   REV6_CONTINUATION_STATE -> CURRENT_STAGE -> IMPLEMENTATION_STATUS

2. CLASSIFY THE WORK
   scientific assay | reusable architecture | live integration | documentation

3. STATE THE CLAIM
   what should improve or what invariant should hold?

4. STATE THE FALSIFIER
   what result would make the mechanism smaller, optional, or wrong?

5. FREEZE WHEN SCIENTIFIC
   preregister data boundary, controls, metrics, thresholds, ablations, leakage rules

6. BUILD THE SMALLEST REUSABLE MECHANISM
   production-facing primitive when justified; experiment-specific truth stays in experiments/

7. TEST IN LAYERS
   unit/integrity -> synthetic smoke (not evidence) -> controlled/dev assay -> live stimulus test when integrated

8. INSPECT RAW FAILURES
   preserve per-case failures; do not average away unexpected behavior

9. CLASSIFY EVIDENCE
   supported | partially supported | discounted/falsified | inconclusive | untested

10. CHANGE THE THEORY BEFORE THE THRESHOLD
    a negative result simplifies architecture; it does not trigger post-hoc threshold loosening

11. UPDATE PROJECT TRUTH
    CURRENT_STAGE, IMPLEMENTATION_STATUS, ARCHITECTURE_PLAN, relevant roadmap/result docs

12. COMMIT FOCUSED WORK
    preserve history and keep scientific preregistration/results chronologically distinct
```

## Stimulus-test development rule

For organism-facing capabilities, use increasingly detailed stimulus tests while preserving process-level fixes:

```text
build one capability
        ↓
run explicit stimuli
        ↓
inspect backend-owned internal state / trace
        ↓
locate the failed owner or transition
        ↓
fix the process, not the example
        ↓
add the failure as a regression test
        ↓
move one level deeper
```

Do not add phrase-specific answer patches, hidden correct-target rules, or UI-side cognition.

## Status vocabulary

Keep scientific evidence and implementation maturity separate.

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

A mechanism may have external-development evidence and still be only `Built`. Automated tests do not grant `Verified`.

## Current production owners

```text
state.py               organism/substrate state; contains TokenDeck
cognition.py           Ground 0 public contracts / cognitive boundary
contextual_search.py   reversible candidate field and context-transition checkpoints
token_deck.py          stable lexical/sense identity and reversible sense state
policy.py              retained E011-A operation/target donor mechanism
policy_learning.py     retained E011-A policy learning
experience.py          ordered current-episode experience + provenance
temporal.py            computational time / sequence
runtime.py             thin sequencing only
dev_server.py          browser/API transport only
experiments/           scientific assays, qrels, hidden evaluation truth, scoring
ui/                    observation/control only
```

## Integration boundary

Do not fabricate a broad candidate field merely to make Ground 0 look live.

The eventual production path should be earned incrementally:

```text
raw stimulus
   ↓
surface segmentation / Token Deck
   ↓
sense + concept/entity + event representation
   ↓
durable memory / legitimate retrieval
   ↓
broad ReversibleCandidateField
   ↓
question-guided contextual cognition
   ↓
evidence sufficiency
   ↓
commit | abstain | seek evidence | reopen
   ↓
runtime sequencing -> state/trace -> UI
```

The Token Deck is not cognition by itself. Ground 0 is not natural-language understanding by itself. Integration occurs only when legitimate owners and data sources exist.

## Documentation authority order

For future work, use this order when documents disagree:

```text
1. docs/REV6_CONTINUATION_STATE.md
2. docs/CURRENT_STAGE.md
3. docs/IMPLEMENTATION_STATUS.md
4. docs/ARCHITECTURE_PLAN.md
5. docs/TOKEN_DECK_ROADMAP.md
6. frozen preregistration/result documents for the experiment being discussed
7. docs/PROJECT_GUIDE.md / docs/SIGNAL_FLOW.md / docs/SCAFFOLD.md
8. older Revision 5 / Revision 4 theory and historical experiment documents
```

Older documents remain evidence history; do not silently rewrite historical preregistrations after seeing results.

## Immediate next actions

```text
SCIENTIFIC TRACK
1. record D6 as completed external-development evidence
2. write/freeze MT-1 preregistration
3. implement MT-1 only after the preregistration boundary exists
4. run integrity/smoke tests
5. run the allowed development assay
6. classify under frozen criteria

REPRESENTATION TRACK
1. verify current TD-0/1/2 tests locally
2. implement TD-3 exact surface segmentation
3. expose segmentation state for stimulus inspection
4. add adversarial punctuation/contraction/name/number tests
5. proceed to TD-4 known/unknown routing only after TD-3 is stable
```

The objective remains: **discover which cognitive operations deserve to survive, and make every surviving experiment leave behind a reusable piece of the organism.**
