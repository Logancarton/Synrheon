# Synrheon Architecture Plan — Revision 6

## Current thesis

Synrheon is being developed as a **question-guided, context-conditional cognitive architecture** with explicit state, provenance, reversible alternatives, and progressively learned cognitive skill.

The architecture is not a frozen diagram. Every major mechanism must continue to earn its place through controlled falsification.

The current working flow is:

```text
question / unresolved state
        ↓
legitimate broad candidate field
        ↓
select a potentially discriminating context operation
        ↓
explicit context transition
    carry | reset/re-anchor | residual/transform | reopen
        ↓
reversible contextual settling
        ↓
re-evaluate what remains unresolved
        ↓
optional deeper refinement or optional recurrence if evidence earns it
        ↓
evidence sufficiency
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
```

The new Revision 6 addition is important:

> **A settled activation distribution is context-conditional state, not permanently accumulated evidence.**

D6 supports this on SciFact development: reset recovered the measured transition damage under the frozen protocol (`R_reset = 1.0`) while the reset control reproduced the one-pass full-context state to floating-point precision.

## Evidence boundary

Current external-development evidence supports restraint.

```text
single full-context soft taper
    approximately preserves BM25

partial -> full naive carried activation
    major transition pathology supported by D6

controlled reset/re-anchor
    justified as an explicit transition operation

multiple contextual soft stages
    still NOT established

current static recurrence
    discounted on SciFact development

current four hand-designed lexical channels
    insufficient residual discrimination

current commitment calibration
    discounted

question-guided contextual divergence
    still untested as a complete mechanism
```

D6 does not prove the full architecture. It sharpens one state-transition rule.

## Development philosophy

Synrheon should grow through a repeatable build/test loop:

```text
smallest defensible invariant
        ↓
build reusable production-facing primitive
        ↓
preregister/falsify the cognitive skill around it
        ↓
negative result?
    yes -> simplify architecture
    no  -> earn next layer
        ↓
integrate only when legitimate upstream data exists
```

This prevents research code and production architecture from diverging while also preventing unvalidated mechanisms from being declared live simply because code exists.

## Cognitive physics vs cognitive skill

### Designed cognitive physics may define

```text
stable identities and representation boundaries
complete-state preservation
reversible suppression semantics
active vs dormant regions
checkpoint / restore / reopen
context-transition provenance
legal operation interfaces
compute / safety ceilings
observable trace boundaries
provenance and evidence lineage
```

### Learned or experimentally earned cognitive skill should determine

```text
which candidate field to retrieve
which context matters
which context to evaluate next
which context-transition mode is appropriate
how strongly to settle
whether another settling stage is useful
which region deserves more compute
whether recurrence adds new information
when evidence is sufficient
when to seek evidence
when to reopen
when to stop
```

The design rule remains:

> **We code the cognitive physics. Synrheon must earn or learn the cognitive skill.**

## Architecture slice 1 — reversible candidate field

Status: **Built, not live-integrated**

Owner:

```text
src/synrheon/contextual_search.py
```

Current mechanics:

```text
complete broad-field retrieval prior
complete activation vector
active candidate region
dormant but recoverable candidates
carry / reset / residual transition provenance
reversible checkpoints
restore
reactivate
reopen-all
```

Core invariant:

```text
suppressed != deleted
```

The candidate field contains no qrels, hidden target identity, hard-coded semantic hierarchy, recurrence rule, or commitment policy.

## Architecture slice 2 — D6 context-transition isolation

Status: **Completed external-development diagnostic**

Owners:

```text
docs/D6_PREREGISTRATION.md
experiments/d6_transition_persistence.py
tests/test_d6_transition_persistence.py
```

Observed:

```text
93 development queries
92 transition-evaluable
reset integrity PASS
max reset activation diff 2.220446049250313e-16
R_reset = 1.0
verdict = MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

Architectural consequence:

```text
previous settled state
    is not automatically
valid prior for changed context
```

The architecture therefore needs explicit transition semantics rather than invisible cumulative carry.

Condition E residual refinement remains unresolved. Do not promote `full - partial` residualization to production truth merely because D6 isolated carry damage.

## Architecture slice 3 — MT-1 multi-stage necessity

Status: **Preregistration frozen at `docs/MT1_PREREGISTRATION.md`; implementation next**

Central question:

> Once transition-state persistence is controlled, does more than one soft contextual settling stage add material value over one good soft stage under matched computation?

Frozen conditions:

```text
M0 retrieval/no-taper anchor
M1 single full-context soft                  primary baseline
M2 multi-soft with naive carry               known pathology control
M3 multi-soft, reset + retained narrowing    primary treatment
M4 multi-soft with full reset                wasted-stage sanity control
M5 reversed context order
M6 matched-compute hard staged pruning
```

The compute unit is one candidate x channel feature evaluation. `MULTI_STAGE_SUPPORTED`
requires `n >= 30`, `M3 - M1 >= 0.010` nDCG@10, a positive 95% paired bootstrap lower
bound, and `E(M3) <= 1.10 * E(M1)`. These may move only through an explicit versioned
amendment recorded before further results.

Critical rule:

> **Hard pruning losing does not establish multi-soft necessity.**

If controlled multi-soft ~= single-soft under the frozen criterion, remove multiple-stage necessity from the architecture while preserving reversibility and explicit transition control.

Recurrence stays outside the primary MT-1 mechanism unless separately preregistered.

## Architecture slice 4 — Token Deck representation

Status: **TD-0/1/2/3/4 Built; TD-5 next (preregister first)**

Owners:

```text
src/synrheon/token_deck.py            identity
src/synrheon/surface_segmentation.py  observation
src/synrheon/acquisition_routing.py   known/unknown routing
```

Stored inside:

```text
CognitiveSubstrate.token_deck
```

Core invariant:

```text
surface form != token identity != sense != concept/entity != episode
```

Current implementation owns:

```text
stable token IDs
observed surface forms / explicit aliases
provenance
open-ended morphology metadata
multiple candidate senses
optional concept links
context-conditioned reversible sense activation
sense checkpoints / restore / reopen
```

The Token Deck does not own truth, world relations, memory truth, natural-language generation, or Ground 0 commitment.

D6's context lesson applies here as a representational invariant: one context may suppress a sense, but that sense remains available when context changes.

## TD-3 — exact surface segmentation

Status: **Built + Integrated** as `td3-exact-surface-v1`.

```text
raw input
    ↓
exact surface spans
    ↓
character offsets
    ↓
normalized lookup forms
```

Two invariants are enforced at construction, not merely tested: every character belongs to
exactly one span, and the spans rejoin into the exact original string. Offsets always index
the original text, never a normalized form.

TD-3 preserves the exact original text and remains replaceable without invalidating stable
token/sense identity, because it assigns no identity at all.

TD-3 must not:

```text
choose meaning
choose part of speech as truth
select a sense
create a concept/entity
ask an LLM for an answer
collapse punctuation/offset provenance
```

Its only joining rule is positional: a punctuation or symbol character joins a lexical span
when, and only when, lexical characters flank it on both sides. Every absorbed mark is
recorded with its offset, so a later stage can re-split without the segmenter guessing that
a span is an abbreviation, an address, or a URL.

Regression coverage includes punctuation, contractions, possessives, hyphenation,
decimals/currency, times, quotes, symbols, names, case variants, whitespace and layout,
compatibility normalization, invisible characters, emoji, and reconstruction from offsets.

## TD-4 — known/unknown acquisition boundary

Status: **Built + Integrated** as `td4-acquisition-routing-v1`.

Routing is read-only. `acquire_route` is the only path from an observed span to a token
card, and nothing on the live path calls it, so observing language never silently becomes
identity.

Each route carries every mechanical signal observed for the span, including signals that
did not decide the proposed need, so a learned router can later be compared against this
one on identical observations.

Where orthography does not isolate a class the router abstains with `unresolved` rather
than guessing: sentence-initial capitals and all-capital forms both fall here. Acquiring a
routed name creates identity and **no sense** — deciding what a token can mean is TD-5.

After stable segmentation:

```text
surface span
   ↓
known token?
 ┌───────┴───────┐
yes              no
 ↓                ↓
retrieve       classify acquisition need
senses            ↓
             name/entity?
             morphology/variant?
             ordinary unknown word?
             number/symbol/code?
```

Dictionary, parser, or LLM assistance may later propose candidates with provenance. External proposals are not truth and must remain distinguishable from user-confirmed, observed, inferred, or Synrheon-learned structure.

## TD-5 — contextual sense learning

This should be a real experiment, not hand-written disambiguation.

Required scientific behavior should include:

```text
held-out contexts
ambiguous cases where abstention is correct
context reversal
preservation/reactivation of initially suppressed senses
simple frequency/default-sense baseline
no answer identity in routing
```

The output should be support over senses, not destructive rewriting of the sense inventory.

## Candidate-source dependency

The live organism cannot use Ground 0 contextual search legitimately until it can obtain a broad candidate field without planted answer identity.

The evolving intended path is:

```text
raw stimulus
   ↓
Token Deck / surface-sense representation
   ↓
concept/entity/event representation
   ↓
durable memory
   ↓
retrieval / candidate source
   ↓
opaque candidate IDs + provenance + initial support
   ↓
ReversibleCandidateField
```

Do not fabricate a candidate field merely to make contextual search appear Integrated.

## Question and unresolved-state controller

The future cognitive controller needs explicit representation of:

```text
current question
currently available evidence
what remains unresolved
candidate disagreements relevant to that unresolved portion
possible next context operations
expected information gain / cost
transition history / provenance
```

Do not hard-code semantic, temporal, identity, causal, social, or goal dimensions as a universal stage ladder. They may become available operations if later data show they are useful.

## Recurrence boundary

Recurrence is optional.

Static lexical similarity was not sufficient on SciFact development. A future recurrence operator must earn its role with question-relative relations such as:

```text
complementarity
contradiction / support
causal dependence
temporal sequence
trajectory compatibility
missing-aspect coverage
```

A matched no-recurrence condition is mandatory for a recurrence claim.

## Commitment boundary

Architectural separation remains:

```text
winner != sufficient evidence
```

But the current external commitment signal is discounted. A future commitment owner should be evaluated against strong calibration/confidence baselines and may consume provenance, unresolved alternatives, evidence quality, and task-specific risk.

Valid dispositions remain conceptual interfaces:

```text
COMMIT
ABSTAIN
SEEK EVIDENCE
REOPEN
CONTINUE DELIBERATION
```

## Relationship to E011-A

E011-A remains historical controlled evidence that an operation/target policy can learn transferable preferences from visible state without memorizing opaque identity.

Owners:

```text
policy.py
policy_learning.py
```

Treat E011-A as a donor mechanism. Do not directly force its narrow `EXPAND/STOP` contract into Ground 0 or Token Deck unless a new state/action experiment justifies that reuse.

## Current production ownership

```text
state.py               organism/world state; contains TokenDeck
cognition.py           public Ground 0 contracts / cognitive boundary
contextual_search.py   reversible candidate field / transition checkpoints
token_deck.py          token/sense identity and reversible sense state
policy.py              retained E011-A donor policy
policy_learning.py     retained E011-A learning
experience.py          ordered current-episode experience + provenance
temporal.py            computational time + sequence
runtime.py             thin sequencing only
dev_server.py          transport only
experiments/           falsification assays, qrels, hidden scoring
ui/                    observation/control only
```

## Live integration sequence

Integration should proceed only as legitimate dependencies appear:

```text
1. Token Deck representation                         TD-0/1/2 Built
2. exact segmentation                                TD-3 Built + Integrated
3. known/unknown acquisition                         TD-4 Built + Integrated
4. contextual sense learning                         TD-5 Next; preregister first
5. concept/entity/event representation               later
6. durable memory                                    later
7. legitimate retrieval/candidate source             later
8. ReversibleCandidateField live handoff              later
9. question-guided context controller                later
10. optional recurrence if earned                    later
11. commitment calibration if earned                 later
12. broader recursive/autonomous cognition           later
```

In parallel, MT-1 continues the scientific mechanism track without using Token Deck changes to alter its frozen comparison.

## Scientific rule

Every major result-bearing mechanism should declare before evidence inspection:

```text
hypothesis
baseline/control
information boundary
matched compute where relevant
primary metric
uncertainty/statistical method
success threshold
partial/inconclusive/failure interpretation
ablation
identity/leakage safeguards
held-out policy
raw failure output
```

Negative and unexpected results are research assets. Change the theory before changing a frozen threshold.

## Governing objective

> **Build increasingly rich cognition, but only one falsifiable layer at a time. Preserve alternatives, provenance, failures, and scientific chronology so that every surviving mechanism becomes a trustworthy part of the organism rather than another brittle patch.**
