# Context-Settled Tapering and Learned-Resistance Recurrent Inference

## A hippocampal-inspired theory of reversible contextual compression, learned pathway reliability, recurrent deliberation, and evidence-gated commitment

**Synrheon Experimental Research Program**  
**Revised August 9, 2026**

## Abstract

This paper develops and updates a hippocampal-inspired computational theory for inference over a very large learned knowledge field. The central proposal is that cognition should not collapse a large candidate field in one irreversible pruning step. Instead, broad activation should be narrowed through soft, reversible contextual tapering, after which a much smaller set of serious alternatives can undergo state-dependent recurrent deliberation. Commitment should occur only when evidence is sufficiently discriminating; otherwise the system should remain uncertain, seek additional evidence, or reopen broader context.

The theory did not emerge from a single successful experiment. Several earlier mechanisms failed or proved insufficient. A static recurrence assay showed little necessity for recurrence because a one-pass solution already achieved approximately 99% accuracy. A later state-dependent relational assay created a genuine need for recurrence: the one-pass scorer fell to 0%, fixed-width recurrent inference reached approximately 98%, and clock-driven progressive narrowing fell to approximately 25.5%. Confidence-gated narrowing either failed to activate or produced only modest savings. A stochastic-consensus approach then produced false certainty, committing on approximately 78% of deliberately unresolved worlds. These failures motivated a shift away from elapsed-time pruning, winner frequency, and single-step compression toward context-dependent, reversible narrowing and explicit abstention.

A learned-resistance mechanism also produced an important early result. In its original synthetic family, equal resistance produced approximately 10% accuracy while learned pathway resistance reached approximately 94.5% and retained that performance after opaque candidate renaming. This suggested that historical reliability could be attached to evidence pathways rather than candidate identity. HCT-2 later provided an important qualification: removing learned resistance did not reduce correct-or-abstain behavior in the HCT-2 family. Learned resistance therefore remains a promising, potentially task-dependent mechanism rather than a universally necessary component of the current architecture.

HCT-1 v1 was completed on 200 untouched held-out synthetic worlds with 256 opaque candidates each. The context-specific cascade achieved 100% correct-or-abstain behavior, 100% survival of the correct candidate into final recurrence, 0% commitment in deliberately unresolved worlds, 100% reactivation after context reversal, and 100% retention under candidate renaming. It reduced recurrent candidate processing from 2048 candidate-cycles per episode under no taper to 96, or 4.6875% of the full-field recurrent load. Hard Top-K pruning failed sharply under context reversal: the correct candidate was suppressed in 37 held-out reversal cases and reactivated in 0% of them. However, a simpler generic soft taper matched the cascade behaviorally while requiring substantially fewer taper evaluations. HCT-1 therefore supported reversible soft narrowing but did not establish that ordered context-specific stages were computationally useful.

HCT-2 v1 was designed and preregistered specifically to test that unresolved claim. It increased the field to 512 opaque candidates, introduced hierarchical conditional context and aliasing, scrambled the anonymous context-channel order, and compared learned-order sparse settling against generic soft tapering, fixed-order sparse tapering, hard Top-K, no taper, no-resistance, and no-recurrence controls. The untouched 300-world final split passed every frozen HCT-2 criterion. Learned-order sparse settling achieved 100% correct-or-abstain behavior, 100% correct-candidate survival, 0% commitment on unresolved worlds, 100% context-reversal reactivation, and 100% renaming retention. It used 128 recurrent candidate-cycles versus 4096 under no taper, or 3.125% of the full-field recurrent load. It used only 7.14% of the context-feature evaluations required by the strong generic-soft control while matching its behavior. The learned channel order recovered the hidden semantic-depth progression `0 -> 1 -> 2 -> 3` and used approximately 5.49% fewer context-feature evaluations than the same sparse mechanism in fixed anonymous order.

The HCT-2 ablations sharpen the theory further. Removing recurrence reduced correct-or-abstain behavior from 100% to 45%, despite the correct candidate surviving sparse tapering in 100% of episodes. This demonstrates that, in this family, tapering alone did not perform the decisive relational discrimination needed for appropriate commitment; recurrence contributed substantial computational work after narrowing. In contrast, removing learned resistance left correct-or-abstain behavior at 100%, so learned resistance was not necessary for HCT-2 performance. The strongest current evidence therefore favors **learned ordered reversible contextual narrowing + state-dependent recurrence + explicit abstention/reopening**, while treating learned resistance as a promising but task-dependent modifier whose necessity must be established separately.

This work remains controlled synthetic evidence only. It does not establish biological hippocampal equivalence, natural-language benefit, general intelligence, or superiority to contemporary machine-learning architectures.

---

## 1. Research Question and Current Thesis

The central question is:

> Can a cognitive system reduce a very large field of possible knowledge and hypotheses without prematurely deleting alternatives that later context or recurrent interaction may make important?

The current thesis separates four functions that are often collapsed into one scoring process:

1. **Cognitive-operation selection** — deciding what kind of mental operation should occur next.
2. **Contextual tapering** — reducing irrelevant breadth while preserving recoverable alternatives.
3. **Relational deliberation** — allowing serious candidates to reinforce or suppress one another through recurrent state-dependent interaction.
4. **Commitment** — deciding whether evidence is sufficient to answer, abstain, seek information, or reopen broader context.

The working architecture is therefore not simply "choose the highest score." It is closer to:

```text
large activated field
    -> learned context-dependent soft narrowing
    -> small serious-candidate field
    -> recurrent interaction among serious alternatives
    -> evidence/stability assessment
    -> commit, abstain, seek evidence, or reopen
```

The word **soft** is essential. A candidate may be strongly suppressed without being erased. The word **contextual** is also important, but the HCT-2 result makes the strongest claim precise: ordered context did not increase final behavior over the strong soft controls in this synthetic family; it increased **evaluation efficiency while preserving behavior**.

---

## 2. Biological and Computational Motivation

Hippocampal research distinguishes pattern separation, strongly associated with dentate gyrus and CA3 processing, from pattern completion associated with recurrent CA3 dynamics. Similar or degraded inputs can be transformed into separated representations and later reconstructed into coherent stored patterns. Sparse competition and winner-take-all dynamics have also been modeled in dentate-gyrus-inspired networks.

Synrheon borrows these functional motifs without claiming to reproduce hippocampal biophysics.

The computational motivation is independent of the biological analogy. A large cognitive system cannot reasonably perform expensive relational recurrence across everything it knows on every inference step. Yet early hard pruning is dangerous because a weak candidate can become important after context changes or after support propagates through relations.

This creates a tension:

```text
Too broad for too long
    -> expensive deliberation

Too narrow too early
    -> brittle loss of recoverable alternatives
```

The theory attempts to occupy the middle ground: **sparse enough to deliberate, but reversible enough to reconsider.**

HCT-2 adds another refinement: if contextual features are conditional, the order in which they are evaluated may affect computational cost even when final behavior remains unchanged.

---

## 3. Mathematical Component I: Learned Pathway Resistance

For candidate `i` and evidence channel `j`, let `s_ij` denote support and `R_j` denote learned resistance.

Channel conductance is the inverse resistance normalized across channels:

```text
g_j = (1 / R_j) / mean_k(1 / R_k)
```

Effective support becomes:

```text
s'_ij = s_ij * g_j
```

After the correct outcome is revealed during training, channel resistance is updated by comparing correct support with the strongest wrong support:

```text
Delta R_j = eta * [max_(i != c)(s_ij) - s_cj]
R_j <- clamp(R_j + Delta R_j, R_min, R_max)
```

A pathway repeatedly stronger in wrong alternatives becomes harder to traverse. A pathway repeatedly stronger in correct alternatives becomes easier. Candidate identity is not itself a learned parameter.

### 3.1 Initial result

The first learned-resistance assay produced approximately:

```text
Equal-resistance baseline     10.0% accuracy
Learned resistance            94.5% accuracy
Renamed candidates            94.5% accuracy
Renaming retention           100.0%
```

This remains a promising result because the learned effect survived opaque candidate renaming. It supports a restricted proposition: **historical reliability can be attached to pathways or evidence channels rather than memorized candidate names.**

### 3.2 HCT-2 qualification: resistance was not necessary there

HCT-2 included a direct no-resistance ablation using the same learned-order sparse taper and recurrent solver. Removing learned resistance did not reduce correct-or-abstain behavior: both the full learned-order system and the no-resistance ablation achieved 100% good behavior, 100% survival, and 100% reversal reactivation.

The no-resistance condition even showed a slightly higher raw correct rate in the final aggregate, but that should not be overinterpreted because raw winner identity in deliberately unresolved worlds is not equivalent to knowledge; both systems appropriately abstained in those worlds.

The correct scientific interpretation is therefore:

```text
Learned resistance:
PROMISING IN EARLIER SYNTHETIC FAMILY
NOT NECESSARY FOR HCT-2 PERFORMANCE
TASK-DEPENDENT NECESSITY REMAINS OPEN
```

This result narrows the theory rather than invalidating it. Resistance should remain an optional learned reliability mechanism until future experiments show when it adds value beyond the other components.

---

## 4. Mathematical Component II: State-Dependent Recurrence

The recurrent deliberative idea is that candidate support is not fixed. Activation of one candidate changes the evidence landscape for others on the next cycle.

A generic form is:

```text
u_i^(t+1)
  = alpha * a_i^(t)
  + beta * sum_j[(W+_ji / R+_ji) * a_j^(t)]
  - mu   * sum_j[(W-_ji / R-_ji) * a_j^(t)]
  + gamma * I_i
```

where compatible candidates can excite one another, conflicting candidates can inhibit one another, and learned resistance may modify pathway influence when useful.

The important scientific distinction is between **recurrence that is actually necessary** and recurrence added to a task a one-pass scorer already solves.

### 4.1 Early evidence for recurrence

The first recurrence necessity test was weak because one-pass inference already reached approximately 99% accuracy. A redesigned state-dependent assay later produced:

```text
One-pass initial scorer                  0%
State-dependent recurrent, fixed width  98%
Clock-driven progressive recurrence     25.5%
```

This was the first strong indication that recurrence can matter when candidate interactions genuinely change the later evidence state.

### 4.2 HCT-2 ablation: recurrence became mechanistically necessary

HCT-2 provides a cleaner component-level result. The learned-order sparse mechanism with recurrence achieved:

```text
good behavior:                    100%
correct candidate survival:       100%
reversal reactivation:            100%
```

The matched no-recurrence ablation achieved:

```text
good behavior:                     45%
correct candidate survival:       100%
reversal reactivation:          81.67%
```

This is highly informative. The tapering mechanism still preserved the correct candidate in every episode, yet behavior collapsed when recurrent interaction was removed. Therefore the taper was not simply solving the task before recurrence began.

The most defensible interpretation is:

> **Sparse contextual tapering preserved the relevant hypothesis; recurrence supplied the relational discrimination and settling needed to convert that preserved field into appropriate commitment behavior.**

The distinction matters because it separates two computational jobs:

```text
Taper:
Which alternatives remain serious enough to consider?

Recurrence:
How do those serious alternatives change one another's support,
and is the resulting state discriminating enough to act?
```

Within HCT-2, recurrence is therefore not decorative. It contributes measurable function after narrowing.

---

## 5. Experimental Development: What Was Tried, What Failed, and What Changed

The experimental history is important because the current theory is partly defined by mechanisms that did **not** work.

### 5.1 Learned resistance: promising, but now qualified

The learned-resistance assay strongly outperformed equal resistance and transferred across candidate renaming in its original synthetic family.

Status:

```text
PROMISING
BUT NOT UNIVERSALLY NECESSARY
```

HCT-2 showed that the full task could retain 100% correct-or-abstain behavior without learned resistance. Future work should therefore test **when** resistance adds value rather than assuming it is always necessary.

### 5.2 First recurrence necessity test: insufficient

An early recurrence comparison did not provide meaningful evidence that recurrence was necessary. A one-pass solution achieved approximately 99% and the recurrent solution approximately 100%.

Status:

```text
INCONCLUSIVE FOR RECURRENCE NECESSITY
```

The lesson was methodological: if the task can already be solved from static evidence, recurrence cannot demonstrate its value.

### 5.3 State-dependent recurrence: promising

The revised relational assay produced approximately:

```text
One-pass initial scorer                  0%
State-dependent recurrent, fixed width  98%
Clock-driven progressive recurrence     25.5%
```

Status:

```text
PROMISING FOR STATE-DEPENDENT RECURRENCE
FAILED FOR CLOCK-DRIVEN PROGRESSIVE NARROWING
```

### 5.4 Clock-driven progressive Top-K: failed

The original narrowing mechanism reduced the field because recurrent cycles elapsed. Candidates disappeared simply because computation had advanced.

That performed poorly in the state-dependent recurrence assay.

The principle extracted from this failure is:

> **Elapsed computation is not evidence that a candidate should disappear.**

A taper should occur because the state has settled, evidence has discriminated, context has become coherent, or a learned policy predicts that narrowing is appropriate—not because an arbitrary number of cycles passed.

### 5.5 Confidence/stability gating: limited

A later confidence gate attempted to narrow only when the current state appeared sufficiently stable. The first version effectively did not fire. A more adaptive version preserved behavior but saved only about 7.61% of active state, below the predeclared 10% target.

Status:

```text
LIMITED / DID NOT JUSTIFY THE MECHANISM AS DESIGNED
```

This suggested that a single global narrowing event may be the wrong abstraction for a very large field.

### 5.6 Stochastic consensus: failed

Repeated perturbed recurrent trials were tested as a confidence signal. In deliberately unresolved worlds, the system committed approximately 78% of the time, exceeding the test requirement of at most 50%.

Status:

```text
FAILED
```

The lesson was:

> **Repeated agreement is not the same as evidence. A stable structural bias can repeatedly select the same answer.**

This directly motivated stronger abstention logic and the separation of **winner selection** from **commitment**.

### 5.7 Hard pruning under context reversal: failed

HCT-1 provided the clearest direct failure of irreversible narrowing. In the final 200-world held-out set, hard Top-K suppressed the correct candidate in 37 context-reversal cases and recovered it in 0% of them.

HCT-2 reproduced the same failure in a harder family: hard Top-K suppressed the correct candidate in all 60 context-reversal worlds and reactivated it in 0% of them.

Status:

```text
FAILED UNDER CONTEXT REVERSAL
REPLICATED ACROSS HCT-1 AND HCT-2 FAMILIES
```

### 5.8 HCT-1 context specificity: behaviorally unresolved

HCT-1's learned context-specific cascade and the simpler generic soft taper both achieved 100% correct-or-abstain behavior and 100% context-reversal reactivation. The generic soft taper also used substantially fewer taper evaluations.

Status:

```text
REVERSIBLE SOFT NARROWING: PROMISING
MULTI-STAGE CONTEXT SPECIFICITY: NOT YET JUSTIFIED
```

This result directly motivated HCT-2.

### 5.9 HCT-2 ordered sparse context: reinforced as an efficiency mechanism

HCT-2 increased the field to 512 candidates, made deeper context tokens conditionally ambiguous, scrambled context-channel order, and allowed sparse stages to evaluate only currently eligible candidates while preserving dormant candidates for reopening.

The learned-order sparse mechanism matched generic soft tapering at 100% correct-or-abstain behavior, but required only about 7.14% of generic soft's context-feature evaluations. It also used about 5.49% fewer context-feature evaluations than the same sparse mechanism run in fixed anonymous channel order.

Status:

```text
REINFORCED AS AN EFFICIENCY-WITH-PRESERVED-BEHAVIOR RESULT
```

The result does **not** show that learned order is necessary for correctness in this family, because fixed-order sparse also achieved 100% good behavior. It shows that the learned order reduced contextual evaluation cost while preserving behavior.

### 5.10 HCT-2 recurrence ablation: strongly supportive

Removing recurrence reduced good behavior to 45% despite 100% correct-candidate survival through tapering.

Status:

```text
STRONGLY SUPPORTIVE OF RECURRENT DELIBERATION
IN THIS TASK FAMILY
```

### 5.11 HCT-2 resistance ablation: no added behavioral value in this family

Removing learned resistance did not reduce good behavior, survival, or reversal recovery.

Status:

```text
NO NECESSITY DEMONSTRATED IN HCT-2
```

This means the full theory should not treat resistance as required merely because it succeeded in earlier assays.

### 5.12 Experimental integrity hardening

During HCT-1 development, the inference firewall was hardened so that hidden correctness information used by the generator/scorer could not enter the recurrent solver. Explicit excitation and inhibition relations are materialized before inference, and the recurrent solver consumes those relations without consulting `correct_index`.

A later CLI defect caused nominal full command-line runs to execute the 50-world quick subset. The discrepancy was detected, the CLI was corrected, a regression test was added, and the official HCT-1 result was rerun over all 200 intended held-out worlds.

HCT-2 added a stronger safeguard: `--quick` was restricted to development seeds and could not consume the reserved final split. The final 300-world split was then run only after the design and gate were frozen.

This implementation history is recorded because experimental tooling is part of scientific validity.

---

## 6. Revised Theory: Context-Settled Soft Tapering

For taper stage `s` and internal settling cycle `t`:

```text
z_i^(s,t)
  = gamma_s * I_i^(s)
  + sum_j W_ij^(s) * a_j^(s,t)
  - lambda_s * D_i^(s,t)

a_i^(s,t+1) = softmax(z_i^(s,t) / tau_s)
```

A stage is settled when:

```text
||a^(s,t+1) - a^(s,t)||_1 < epsilon_s
```

After settling, the next stage receives a soft contextual projection:

```text
I^(s+1) = P^(s) * a^(s,*)
```

The critical distinction is that `P^(s)` is not a hard deletion operator. Suppressed hypotheses remain available for reactivation.

The stronger version of the theory proposes that different stages may settle on different contextual dimensions, for example:

```text
semantic context
    -> temporal context within the semantic basin
    -> goal context within the semantic+temporal basin
    -> self/social/relational context within that narrower basin
```

HCT-2 supplies the first direct evidence that the order can carry computational value when later features are conditionally meaningful. The learner recovered the hidden semantic-depth progression and reduced context-feature evaluations relative to fixed anonymous order while preserving identical final behavior.

The claim should remain narrow:

> **Ordered context settling can improve evaluation efficiency in hierarchically conditional fields. HCT-2 does not show that ordered settling is required for correct behavior in every field.**

---

## 7. Designed Cognitive Physics vs Learned Cognitive Skill

The taper equations alone are not enough. If a developer permanently decides which context matters, what order stages should run, what candidate region each stage should prefer, and how strongly each stage should narrow, then the architecture merely replaces one brittle routing system with another.

The theory therefore separates **designed cognitive physics** from **learned cognitive skill**.

### Designed cognitive physics may define

```text
state representation
taper operation
soft projection
reversible suppression
maximum compute budget
recurrent update form
checkpoint representation
commit / abstain / reopen interfaces
safe bounds
```

### Learned cognitive skill should increasingly determine

```text
which contextual operation is useful
context-channel reliability
stage ordering
stage gain / selectivity
candidate-region preference
when to taper
when to deliberate recurrently
when to seek evidence
when to reopen broader context
when to stop
```

HCT-2 strengthens the learned-skill side of the theory because the observed channels were deliberately scrambled. Training recovered a useful semantic-depth order without receiving the desired order as the inference answer.

Neither HCT-1 nor HCT-2 learns arbitrary human semantic representations or a fully state-conditioned cognitive-operation policy. Those remain future steps.

---

## 8. HCT-1 v1: Predeclared Full-System Hypothesis

### HCT-1 — Learned Contextual Taper + Recurrent Deliberation

> **A transferable learned contextual-routing layer controlling multiple reversible soft taper stages will reduce a large nested candidate field before recurrent deliberation, while preserving final accuracy, retaining real ambiguity, and permitting context-driven reactivation better than matched hard pruning.**

Subclaims were:

- **HCT-1A — Transfer:** learned contextual reliability/order should transfer across opaque candidate renaming and unseen worlds.
- **HCT-1B — Survival:** the correct candidate should survive the cascade into expensive recurrence at a high rate.
- **HCT-1C — Recurrent compute:** substantially fewer candidates should enter expensive recurrence than under no taper.
- **HCT-1D — Reversibility:** suppressed candidates should be able to return when context changes; hard deletion should fail this case.
- **HCT-1E — Uncertainty:** genuinely unresolved worlds should remain mostly uncommitted.
- **HCT-1F — Context specificity:** a distinct context-specific cascade should be compared with a matched generic soft taper.
- **HCT-1G — Recurrence/resistance separability:** later ablations must test whether recurrence and learned resistance contribute independently.

### Frozen HCT-1 v1 interpretation gate

```text
cascade good behavior >= 0.85
correct-candidate survival >= 0.90
unresolved commit rate <= 0.25
at least 5 true reversal-suppression cases
cascade reactivation >= 0.75
hard reactivation disadvantage >= 0.20
cascade recurrent candidate-cycle fraction <= 0.50 of no taper
candidate-renaming retention >= 0.97
generic-soft advantage over cascade <= 0.03
hidden answer identity must not enter held-out inference
```

The thresholds were not changed after observing the final result.

---

## 9. HCT-1 v1 Experimental Design

The final HCT-1 assay used:

```text
256 opaque candidates per world
12-candidate recurrent width after tapering
8 recurrent cycles
500 training worlds: seeds 60000-60499
200 final held-out worlds: seeds 62000-62199
40 held-out worlds per world type
```

World types:

```text
clear_context
misleading_early
persistent_close
unresolved_close
context_reversal
```

Matched conditions:

```text
1. no taper + full-field recurrence
2. hard global Top-K + identical downstream recurrence
3. generic soft taper + identical downstream recurrence
4. learned context-specific reversible cascade + identical downstream recurrence
```

---

## 10. HCT-1 v1 Final 200-World Results

### 10.1 Aggregate held-out behavior

| Condition | Correct | Commit | Correct-or-abstain behavior | Correct entered recurrence | Recurrent candidate-cycles | Taper candidate-evaluations | Reversal reactivation |
|---|---:|---:|---:|---:|---:|---:|---:|
| No taper | 85.0% | 23.5% | 43.5% | 100.0% | 2048 | 0 | n/a |
| Hard Top-K | 63.5% | 71.5% | 77.5% | 79.5% | 96 | 258.4 | 0.0% |
| Generic soft | 84.5% | 80.0% | 100.0% | 100.0% | 96 | 1228.8 | 100.0% |
| Context-specific cascade | 85.5% | 80.0% | 100.0% | 100.0% | 96 | 4915.2 | 100.0% |

The formal frozen HCT-1 gate was passed in every category.

### 10.2 Interpretation

HCT-1 established three important points within its family:

1. reversible soft narrowing survived context reversal while hard deletion did not;
2. the full field could be reduced drastically before recurrence without losing the correct candidate;
3. winner identity had to remain separate from commitment in unresolved worlds.

But HCT-1 did **not** establish that a multi-stage context-specific cascade was preferable to generic soft narrowing because generic soft matched behavior and used fewer taper evaluations.

---

## 11. HCT-2 v1: Frozen Ordered Conditional Context Experiment

### 11.1 Why HCT-2 exists

HCT-2 directly tests the unresolved HCT-1 question:

> **Does a learned order of context-specific settling become computationally useful when context channels are hierarchically aliased and later context is cheaper or safer to evaluate only after earlier context has narrowed the active field?**

The primary HCT-2 claim is an **efficiency-with-preserved-behavior** claim, not an accuracy-superiority claim.

### 11.2 Experimental structure

HCT-2 uses:

```text
512 opaque candidates per world
16-candidate recurrent width
8 recurrent cycles
4 hierarchical context depths
500 training worlds:     70000-70499
150 development worlds:  71000-71149
300 final worlds:        72000-72299
```

Observed context channels are scrambled:

```text
channel 0 -> semantic depth 2
channel 1 -> semantic depth 0
channel 2 -> semantic depth 3
channel 3 -> semantic depth 1
```

The learner is not handed the desired order.

World types:

```text
clear_hierarchy
alias_conflict
misleading_deep
unresolved_branch
context_reversal
```

Conditions:

```text
1. no_taper
2. hard_topk
3. generic_soft
4. fixed_order_sparse
5. learned_order_sparse
6. learned_order_no_resistance
7. learned_order_no_recurrence
```

### 11.3 Frozen HCT-2 interpretation gate

```text
learned-order good behavior >= 0.90
learned-order final survival >= 0.95
unresolved commit rate <= 0.20
at least 10 genuine reversal-suppression cases
learned-order reactivation >= 0.80
hard reactivation disadvantage >= 0.30
learned-order recurrent cost <= 0.10 of no taper
renaming retention >= 0.97
generic behavior advantage over learned order <= 0.03
learned-order context-evaluation fraction <= 0.50 of generic soft
learned-order efficiency advantage over fixed order >= 0.03
learned hierarchical order must recover semantic depth progression
```

These criteria were frozen before the final split was run.

---

## 12. HCT-2 v1 Final 300-World Results

HCT-2 passed every frozen criterion.

### 12.1 Aggregate comparison

| Condition | Correct | Commit | Good behavior | Correct survival | Recurrent cycles | Context evaluations | Reversal reactivation |
|---|---:|---:|---:|---:|---:|---:|---:|
| No taper | 50.0% | 28.0% | 48.0% | 100.0% | 4096 | 0 | n/a |
| Hard Top-K | 70.67% | 60.33% | 80.0% | 80.0% | 128 | 2060.8 | 0.0% |
| Generic soft | 90.33% | 80.0% | 100.0% | 100.0% | 128 | 19660.8 | 100.0% |
| Fixed-order sparse | 90.33% | 80.0% | 100.0% | 100.0% | 128 | 1485.78 | 100.0% |
| Learned-order sparse | 90.33% | 80.0% | 100.0% | 100.0% | 128 | 1404.26 | 100.0% |
| Learned-order no resistance | 91.33% | 80.0% | 100.0% | 100.0% | 128 | 1404.26 | 100.0% |
| Learned-order no recurrence | 85.0% | 25.0% | 45.0% | 100.0% | 0 | 1404.26 | 81.67% |

### 12.2 Ordered sparse settling versus generic soft

The learned-order sparse system matched generic soft on the primary behavioral outcomes:

```text
good behavior:          100% vs 100%
survival:               100% vs 100%
reversal reactivation:  100% vs 100%
```

But context-feature evaluations were:

```text
Generic soft:            19660.8
Learned-order sparse:     1404.26
```

Therefore:

```text
1404.26 / 19660.8 = 0.071424...
```

The learned-order sparse system used approximately **7.14%** of generic soft's context-feature evaluations, or roughly one-fourteenth as many, while preserving identical correct-or-abstain behavior.

This directly addresses the main weakness exposed by HCT-1.

### 12.3 Learned order versus fixed sparse order

Fixed-order sparse also achieved 100% good behavior, so the learned order was not required for behavioral correctness in this family.

However:

```text
Fixed-order sparse evaluations:    1485.78
Learned-order sparse evaluations:  1404.26
```

The learned order produced an approximately **5.49% evaluation-efficiency advantage**.

The learner also recovered the hidden semantic-depth sequence:

```text
0 -> 1 -> 2 -> 3
```

despite receiving context channels in scrambled anonymous order.

This is the first direct evidence in the program that **learned context order carries measurable computational value** under hierarchical conditional context.

### 12.4 Recurrent-field reduction

No taper:

```text
512 candidates * 8 cycles = 4096 recurrent candidate-cycles
```

Learned-order sparse:

```text
16 candidates * 8 cycles = 128 recurrent candidate-cycles
```

Therefore:

```text
128 / 4096 = 0.03125
```

The sparse system used **3.125% of the full-field recurrent candidate-cycle load**.

As before, recurrent candidate-cycles and context-feature evaluations are reported separately. This is not yet a wall-clock superiority claim.

### 12.5 Context reversal

Hard Top-K:

```text
60 reversal worlds
60 initial suppressions
0% reactivation
```

Learned-order sparse:

```text
60 reversal worlds
60 initial suppressions
100% reactivation
```

The reversible-suppression result from HCT-1 therefore replicated in a second, larger and structurally different synthetic family.

### 12.6 Unresolved worlds

The learned-order sparse system committed in 0% of the 60 unresolved-branch worlds and achieved 100% good behavior there.

Again:

```text
winner != knowledge
```

The system can retain an internal ranking while correctly refusing to convert insufficient evidence into commitment.

---

## 13. HCT-2 Ablations: What Each Component Actually Contributed

The HCT-2 ablations are among the most scientifically valuable results because they separate components that the full-system score alone cannot distinguish.

### 13.1 Removing recurrence: major functional loss

The no-recurrence condition retained the correct candidate through tapering in 100% of episodes. Yet good behavior fell from 100% to 45%.

Aggregate comparison:

```text
Full learned-order sparse:
  correct rate             90.33%
  commit rate              80.0%
  good behavior           100.0%
  correct survival        100.0%
  reversal reactivation   100.0%

No recurrence:
  correct rate             85.0%
  commit rate              25.0%
  good behavior            45.0%
  correct survival        100.0%
  reversal reactivation    81.67%
```

The crucial observation is that **survival remained perfect while appropriate behavior collapsed**.

That means contextual tapering successfully preserved the relevant candidate but did not, by itself, create enough relational discrimination to support appropriate commitment.

The recurrence stage therefore appears to perform a distinct downstream function:

```text
Taper preserves a good search field.
Recurrence resolves interactions inside that field.
Commitment reads the resulting evidence state.
```

This materially strengthens the state-dependent recurrence component of the theory.

### 13.2 Removing learned resistance: no behavioral loss

The no-resistance ablation achieved:

```text
correct rate             91.33%
commit rate              80.0%
good behavior           100.0%
correct survival        100.0%
reversal reactivation   100.0%
```

This matched the full learned-resistance system on every primary behavioral outcome.

The slightly higher raw correct rate should not be interpreted as evidence that resistance is harmful, because the difference is largely compatible with winner variation inside deliberately unresolved cases where both systems appropriately abstain.

The correct interpretation is narrower:

> **HCT-2 did not demonstrate a need for learned resistance.**

This matters because it prevents the architecture from preserving an attractive mechanism merely because earlier experiments supported it. Learned resistance should remain separately testable and should earn its place by adding value in tasks where evidence-source reliability genuinely varies across history or context.

### 13.3 Component status after HCT-2

```text
Reversible sparse contextual tapering:
STRONGLY SUPPORTED IN HCT-1/HCT-2 FAMILIES

Learned context ordering:
SUPPORTED AS AN EFFICIENCY ADVANTAGE IN HCT-2

State-dependent recurrence:
STRONGLY SUPPORTED BY HCT-2 ABLATION

Explicit abstention / commitment separation:
SUPPORTED BY UNRESOLVED-WORLD BEHAVIOR

Context-driven reopening:
SUPPORTED ACROSS HCT-1 AND HCT-2 REVERSAL TESTS

Learned resistance:
PROMISING FROM EARLIER ASSAYS
NOT NECESSARY IN HCT-2
REQUIRES TASK-SPECIFIC JUSTIFICATION
```

---

## 14. Current Theory Status After HCT-2

The strongest current formulation of the theory is now:

> **A large candidate field can be narrowed through learned, reversible contextual settling before recurrent relational deliberation. In hierarchically conditional fields, learning the order of contextual settling can reduce evaluation cost while preserving behavior. Recurrence then performs a distinct and necessary downstream role in resolving interactions among the surviving serious alternatives, while commitment remains separate from winner ranking and can abstain when evidence is insufficient.**

This is stronger and more specific than the post-HCT-1 formulation.

### Discounted or failed mechanisms

```text
automatic clock-driven progressive Top-K
single global confidence gate as sufficient solution
stochastic winner consensus as evidence of truth
irreversible hard deletion under changing context
```

### Repeatedly supported mechanisms

```text
soft reversible suppression
context-driven reopening
explicit commitment/abstention separation
state-dependent recurrence when relational interaction matters
identity-independent structural transfer
```

### Newly strengthened by HCT-2

```text
sparse conditional context evaluation
learned context ordering as an efficiency mechanism
recurrence as functionally distinct from tapering
```

### Still conditional / unresolved

```text
learned resistance as a generally necessary mechanism
semantic interpretation of context channels
generalization beyond synthetic task families
real wall-clock compute advantage
fully learned state-conditioned cognitive-operation policy
```

---

## 15. Long-Term Architecture Hypothesis

The broader Synrheon architecture should now be written with learned resistance as optional rather than assumed universal:

```text
VERY LARGE LEARNED KNOWLEDGE FIELD
        |
        v
learned cognitive-operation / context routing
        |
        v
one or more reversible soft contextual settlements
        |
        v
TRACTABLE SERIOUS-CANDIDATE FIELD
        |
        v
state-dependent recurrent deliberation
        |
        +--> optional learned pathway reliability / resistance
        |
        v
evidence + uncertainty accumulation
        |
        +--> COMMIT
        +--> ABSTAIN
        +--> SEEK DISCRIMINATING EVIDENCE
        +--> REOPEN BROADER CONTEXT
```

The computational questions are:

```text
Policy:
What mental operation should I perform?

Taper:
What portion of the knowledge field should remain strongly active?

Order:
Which contextual dimension should be evaluated next?

Recurrence:
How do serious alternatives change one another's support?

Reliability:
Should some evidence pathways be trusted more or less from learned history?

Commitment:
Do I know enough to act?
```

The long-term goal is not to hand-code these answers. The architecture should expose learnable operations and allow experience to shape which operations are selected, which context is useful, what order context should be applied, when recurrence is needed, when source reliability should matter, when narrowing is justified, and when prior suppression should be reopened.

---

## 16. What HCT-2 Does and Does Not Prove

### HCT-2 supports, within its synthetic family

- learned-order sparse tapering can preserve 100% correct-or-abstain behavior while using far fewer context evaluations than a strong generic-soft control;
- learned stage ordering can provide measurable efficiency benefit over fixed stage order;
- correct candidates can survive aggressive sparse narrowing without being permanently deleted;
- context reversal can reactivate previously suppressed candidates when suppression is reversible;
- hard Top-K remains brittle under context reversal;
- recurrence contributes substantial downstream function beyond tapering;
- unresolved cases can retain a winner without forcing commitment;
- the learned structure transfers across opaque candidate renaming.

### HCT-2 does not establish

- biological hippocampal equivalence;
- a new mathematical law;
- superiority to transformers, attention, mixture-of-experts, associative-memory, learned-retrieval, or modern routing systems;
- natural-language benefit;
- learned semantic representations;
- autonomous cognition;
- production integration of the hippocampal-inspired branch;
- lower total wall-clock compute without a calibrated cost model;
- that ordered settling is necessary for correctness in all tasks;
- that learned resistance is generally necessary;
- generalization to substantially different world generators or real knowledge distributions.

The resistance ablation is especially important to this boundary. The theory should not become a bundle in which every historically promising mechanism is treated as necessary. Components must continue to earn their place independently.

---

## 17. Next Falsifiable Question: HCT-3

The next experiment should not merely make HCT-2 larger. It should attack **generality**.

The central question should be:

> **Does the same learned ordered reversible taper + recurrent deliberation mechanism continue to discover useful context order and preserve appropriate behavior when the structure of the problem changes substantially?**

A strong HCT-3 should vary factors that HCT-2 held fixed, for example:

```text
number of context levels
candidate count
branching factor
channel scrambling
context noise
context missingness
relation topology
excitation/inhibition density
reversal depth
relative evidence reliability
```

The mechanism should not be redesigned separately for each family.

Important HCT-3 controls should include:

```text
generic soft
fixed-order sparse
learned-order sparse
no recurrence
learned resistance on/off where reliability is manipulated
hard deletion
```

The learned-resistance component should receive a particularly fair test by including worlds in which evidence-channel reliability changes systematically across history or context. If resistance then produces a reproducible advantage, its role becomes clearer. If it again does nothing, the theory should simplify further.

The strongest next evidence would therefore be **transfer of the computational principle across different structural families**, not merely another perfect score on one generator.

---

## 18. Experimental Sequence and Continuation Protocol

Repository: `Logancarton/Synrheon`  
Research branch: `experiment/hippocampal-sparse-settling`

Experimental sequence:

```text
experiments/hippocampal_settling.py
experiments/hippocampal_learning.py
experiments/hippocampal_equivalence.py
experiments/hippocampal_stateful_recurrence.py
experiments/hippocampal_confidence_gated.py
experiments/hippocampal_consensus_trials.py
experiments/hippocampal_contextual_taper_full_system.py
experiments/hippocampal_ordered_context.py
```

HCT-1 tests:

```text
tests/test_hippocampal_contextual_taper_full_system.py
```

HCT-2 tests:

```text
tests/test_hippocampal_ordered_context.py
```

HCT-2 preregistration:

```text
docs/HCT2_PREREGISTRATION.md
```

HCT-1 v1 status:

```text
COMPLETE
200 final held-out worlds
all frozen HCT-1 gates passed
formal verdict: REINFORCED within the synthetic experimental family
```

HCT-2 v1 status:

```text
COMPLETE
300 final held-out worlds
all frozen HCT-2 gates passed
formal verdict: REINFORCED within the synthetic ordered-context family
```

Current strongest mechanistic interpretation:

```text
learned reversible contextual tapering
    + learned ordering when context is conditional
    + state-dependent recurrence
    + explicit abstention / reopening

are jointly promising.

Learned resistance remains optional pending stronger task-specific evidence.
```

The next scientific action should be a frozen HCT-3 generalization assay rather than post-hoc modification of HCT-2.

---

## References

Bakker, A., Kirwan, C. B., Miller, M., & Stark, C. E. L. (2008). Pattern separation in the human hippocampal CA3 and dentate gyrus. *Science, 319*(5870), 1640-1642. https://doi.org/10.1126/science.1152882

Myers, C. E., & Scharfman, H. E. (2011). Pattern separation in the dentate gyrus: A role for the CA3 backprojection. *Hippocampus, 21*(11), 1190-1215. https://doi.org/10.1002/hipo.20828

Neunuebel, J. P., & Knierim, J. J. (2014). CA3 retrieves coherent representations from degraded input: Direct evidence for CA3 pattern completion and dentate gyrus pattern separation. *Neuron, 81*(2), 416-427. https://doi.org/10.1016/j.neuron.2013.11.017

Nolan, C. R., Wyeth, G., Milford, M., & Wiles, J. (2011). The race to learn: Spike timing and STDP can coordinate learning and recall in CA3. *Hippocampus, 21*, 647-660. https://doi.org/10.1002/hipo.20777

Kim, S.-Y., & Lim, W. (2021). Dynamical origin for winner-take-all competition in a biological network of the hippocampal dentate gyrus. arXiv:2105.06057.

Synrheon experimental source: hippocampal experiment modules, tests, and preregistration documents on branch `experiment/hippocampal-sparse-settling`.