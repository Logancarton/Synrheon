# Context-Settled Tapering and Learned-Resistance Recurrent Inference

## A hippocampal-inspired theory of reversible contextual compression, learned pathway resistance, recurrent deliberation, and evidence-gated commitment

**Synrheon Experimental Research Program**  
**Revised August 9, 2026**

## Abstract

This paper develops and updates a hippocampal-inspired computational theory for inference over a very large learned knowledge field. The central proposal is that cognition should not collapse a large candidate field in one irreversible pruning step. Instead, broad activation should be narrowed through soft, reversible contextual tapering, after which a much smaller set of serious alternatives can undergo more expensive state-dependent recurrent deliberation. Commitment should occur only when evidence is sufficiently discriminating; otherwise the system should remain uncertain, seek additional evidence, or reopen broader context.

The theory did not emerge from a single successful experiment. Several earlier mechanisms were tested and failed or proved insufficient. A static recurrence assay showed almost no necessity for recurrence because a one-pass solution already achieved approximately 99% accuracy. A later state-dependent relational assay created a genuine need for recurrence: the one-pass scorer fell to 0%, fixed-width recurrent inference reached approximately 98%, and clock-driven progressive narrowing fell to approximately 25.5%. Confidence-gated narrowing either failed to activate or produced only modest savings. A stochastic-consensus approach then produced false certainty, committing on approximately 78% of deliberately unresolved worlds. These failures motivated a shift away from elapsed-time pruning, winner frequency, and single-step compression toward context-dependent, reversible narrowing.

A learned-resistance mechanism remains promising. In an earlier synthetic family, equal resistance produced approximately 10% accuracy while learned pathway resistance reached approximately 94.5%, retained after opaque candidate renaming. This suggests that outcome-driven pathway reliability can transfer independently of candidate labels in that restricted setting.

The first full contextual-taper experiment, HCT-1 v1, has now been completed on 200 untouched held-out synthetic worlds with 256 opaque candidates each. The context-specific cascade achieved 100% correct-or-abstain behavior, 100% survival of the correct candidate into final recurrence, 0% commitment in deliberately unresolved worlds, 100% reactivation after context reversal, and 100% retention under candidate renaming. It reduced recurrent candidate processing from 2048 candidate-cycles per episode under no taper to 96, or 4.6875% of the full-field recurrent load. Hard Top-K pruning failed sharply under context reversal: the correct candidate was suppressed in 37 held-out reversal cases and reactivated in 0% of them. The reversible cascade suppressed the correct candidate from the recurrent field in all 40 reversal worlds and recovered it in 100% after context changed.

However, HCT-1 also exposed an important limitation. A simpler generic soft taper achieved the same 100% correct-or-abstain behavior and 100% reactivation while requiring substantially fewer taper candidate-evaluations than the context-specific cascade. Therefore the strongest current evidence supports **reversible soft contextual narrowing over irreversible hard pruning**, not yet the stronger claim that multiple distinct ordered contextual taper stages are necessary or computationally superior.

HCT-2 has now been designed, implemented, and preregistered specifically to test that unresolved stronger claim. It increases the field to 512 opaque candidates, introduces hierarchical conditional context, deliberately scrambles anonymous context-channel order, adds alias competitors whose deeper context features can be misleading outside the correct broad basin, and compares a learned ordered sparse cascade against generic soft tapering, fixed-order sparse tapering, hard Top-K, no taper, no-resistance, and no-recurrence controls. Its primary claim is not that ordered tapering must be more accurate; it is that learned ordered conditional settling should preserve behavior while requiring substantially fewer context-feature evaluations than a strong simultaneous generic-soft control. Training and development splits are separated from a reserved 300-world final split, and quick runs are prevented from consuming final seeds. The HCT-2 final split has **not yet been evaluated** in this paper.

This work is controlled synthetic evidence only. It does not establish biological hippocampal equivalence, natural-language benefit, general intelligence, or superiority to contemporary machine-learning architectures.

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
    -> context-dependent soft narrowing
    -> small serious-candidate field
    -> recurrent interaction among serious alternatives
    -> evidence/stability assessment
    -> commit, abstain, seek evidence, or reopen
```

The word **soft** is essential. A candidate may be strongly suppressed without being erased. The word **contextual** is also essential to the stronger theory, although HCT-1 did not yet show that distinct context-specific stages are superior to a simpler generic soft taper.

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

This is one of the more promising early results because the learned effect survived opaque candidate renaming. The test therefore supports a restricted proposition: **historical reliability can be attached to pathways or evidence channels rather than memorized candidate names.**

It does not establish mathematical novelty or superiority to conventional learned weights, attention, gating, mixture-of-experts routing, or other reliability-learning methods.

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

where compatible candidates can excite one another, conflicting candidates can inhibit one another, and learned resistance changes how readily pathways influence settling.

The important scientific distinction is between **recurrence that is actually necessary** and recurrence added to a task a one-pass scorer already solves.

---

## 5. Experimental Development: What Was Tried, What Failed, and What Changed

The experimental history is important because the current theory is partly defined by mechanisms that did **not** work.

### 5.1 Learned resistance: promising

The learned-resistance assay strongly outperformed equal resistance and transferred across candidate renaming in its synthetic family.

Status:

```text
PROMISING
```

What it suggests:

- reliability can be learned at the pathway/channel level;
- misleading channels can become harder to traverse;
- useful channels can become easier to traverse;
- the effect need not depend on candidate names.

What remains unresolved:

- whether the mechanism is better than ordinary learned weighting;
- whether it transfers to richer representations;
- whether resistance should be local, contextual, temporal, relational, or all of these.

### 5.2 First recurrence necessity test: insufficient

An early recurrence comparison did not provide meaningful evidence that recurrence was necessary. A one-pass solution achieved approximately 99% and the recurrent solution approximately 100%.

Status:

```text
INCONCLUSIVE FOR RECURRENCE NECESSITY
```

The lesson was methodological: if the task can already be solved from static evidence, recurrence cannot demonstrate its value.

This led to the design of a genuinely state-dependent relational problem in which later evidence depends on interactions among active candidates.

### 5.3 State-dependent recurrence: promising

The revised assay produced approximately:

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

This result was important because the recurrent process was no longer decorative. The state had to evolve for relational support to circulate.

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

This suggested that a single global narrowing event may be the wrong abstraction for a very large field. A system may need several smaller contextual settlements rather than one global confidence threshold.

### 5.6 Stochastic consensus: failed

The next idea was to run repeated perturbed recurrent trials and use consensus among trials as a confidence signal.

In deliberately unresolved worlds, the system committed approximately 78% of the time, exceeding the test requirement of at most 50%. The winning answer was often internally consistent but not sufficiently evidenced.

Status:

```text
FAILED
```

The lesson was:

> **Repeated agreement is not the same as evidence. A stable structural bias can repeatedly select the same answer.**

This failure directly motivated stronger abstention logic and the separation of **winner selection** from **commitment**.

### 5.7 Hard pruning under context reversal: failed

HCT-1 later provided the clearest direct failure of irreversible narrowing. In the final 200-world held-out set, hard Top-K suppressed the correct candidate in 37 context-reversal cases and recovered it in 0% of them.

Status:

```text
FAILED UNDER CONTEXT REVERSAL
```

This is stronger than a philosophical objection to hard pruning. It is a measured failure mode in the current synthetic family.

### 5.8 HCT-1 context specificity: behaviorally unresolved

HCT-1's learned context-specific cascade and the simpler generic soft taper both achieved 100% correct-or-abstain behavior and 100% context-reversal reactivation.

However, the generic soft taper used substantially fewer taper candidate-evaluations.

Status:

```text
REVERSIBLE SOFT NARROWING: PROMISING
MULTI-STAGE CONTEXT SPECIFICITY: NOT YET JUSTIFIED
```

This result prevented the theory from treating multiple ordered stages as established merely because the cascade worked. HCT-2 was created specifically to test whether ordered stages become useful when contextual information is hierarchical, aliased, and conditionally useful.

### 5.9 Experimental integrity hardening

During HCT-1 development, the inference firewall was hardened so that hidden correctness information used by the generator/scorer could not enter the recurrent solver. Explicit excitation and inhibition relations are materialized before inference, and the recurrent solver consumes those relations without consulting `correct_index`.

A later CLI defect caused nominal full command-line runs to pass the `argparse.Namespace` object as the `quick` argument, making both normal and `--quick` CLI runs execute the 50-world quick subset. This did **not** alter the experiment function itself. The discrepancy was detected by directly invoking `run_assay()`, the CLI was corrected to pass `args.quick`, a regression test was added, and the official full HCT-1 result was then run over all 200 intended held-out worlds.

HCT-2 adds a stronger safeguard: its `--quick` mode is restricted to a separate development range and cannot consume the reserved final split.

This implementation history is recorded because experimental tooling must be treated as part of scientific validity.

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

The phrase **within the basin** is now experimentally important. HCT-2 is designed so that a deeper context feature may be ambiguous or misleading when evaluated globally but useful after broader context has narrowed the active region. This is the first direct attempt to test the user's proposed principle that **each taper should settle on a like/coherent context before the next taper is applied.**

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

HCT-1 learned anonymous evidence resistance, contextual-stage ordering, and gains from training outcomes. HCT-2 strengthens this test by scrambling observed context-channel order and asking training to recover a useful ordered progression without receiving semantic-depth labels as the routing answer.

Neither HCT-1 nor HCT-2 learns arbitrary human semantic representations or a fully state-conditioned cognitive-operation policy. Those remain future steps.

---

## 8. HCT-1 v1: Predeclared Full-System Hypothesis

### HCT-1 — Learned Contextual Taper + Recurrent Deliberation

> **A transferable learned contextual-routing layer controlling multiple reversible soft taper stages will reduce a large nested candidate field before learned-resistance recurrent deliberation, while preserving final accuracy, retaining real ambiguity, and permitting context-driven reactivation better than matched hard pruning.**

Subclaims were:

- **HCT-1A — Transfer:** learned contextual reliability/order should transfer across opaque candidate renaming and unseen worlds.
- **HCT-1B — Survival:** the correct candidate should survive the cascade into expensive recurrence at a high rate.
- **HCT-1C — Recurrent compute:** substantially fewer candidates should enter expensive recurrence than under no taper.
- **HCT-1D — Reversibility:** suppressed candidates should be able to return when context changes; hard deletion should fail this case.
- **HCT-1E — Uncertainty:** genuinely unresolved worlds should remain mostly uncommitted.
- **HCT-1F — Context specificity:** a distinct context-specific cascade should be compared with a matched generic soft taper; if generic soft matches it, the stronger context-specific claim is weakened.
- **HCT-1G — Recurrence/resistance separability:** later ablations must test whether recurrence and learned resistance contribute independently.

### Frozen HCT-1 v1 interpretation gate

Before final interpretation, the following criteria were frozen:

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

The same learned parameters were used across held-out conditions:

```text
evidence_resistance:
[3.0,
 2.0725392061711534,
 1.1025813281666983,
 0.8107898768466211]

taper_order:
[2, 3, 1, 0]

taper_gains:
[0.7215276074720123,
 1.0119617823169562,
 1.1462560526105259,
 1.1202545576005059]
```

Candidate names were opaque and then regenerated under a rename condition to test identity independence.

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

### 10.2 Unresolved worlds

For the context-specific cascade:

```text
unresolved_close episodes: 40
commit rate:               0.0%
good behavior:           100.0%
```

The internal winner still matched the hidden answer in 27.5% of unresolved cases, but the system correctly declined to commit because the evidence was intentionally insufficient.

This distinction matters:

```text
winner != knowledge
```

A candidate can rank first without the system having enough evidence to act as if it knows.

### 10.3 Context reversal

Hard Top-K:

```text
40 reversal worlds
37 cases where correct candidate was initially excluded
0.0% reactivation
2.5% final correct rate
0.0% good behavior
```

Context-specific reversible cascade:

```text
40 reversal worlds
40 cases where correct candidate was initially outside the recurrent field
100.0% reactivation after late context
100.0% final correct rate
100.0% good behavior
```

Generic soft taper also achieved 100% reactivation.

This is currently the strongest direct evidence for the **reversibility** principle. Hard pruning did exactly what the theory predicted it would do poorly: once a candidate was deleted, changed context could not restore it.

### 10.4 Recurrent-field reduction

No taper performed recurrence over all 256 candidates for 8 cycles:

```text
256 * 8 = 2048 recurrent candidate-cycles
```

The taper conditions performed recurrence over 12 candidates for 8 cycles:

```text
12 * 8 = 96 recurrent candidate-cycles
```

Therefore:

```text
96 / 2048 = 0.046875
```

The cascade used **4.6875% of the full-field recurrent candidate-cycle load**.

This is evidence for recurrent-field reduction only. It is **not** evidence of lower total wall-clock cost because taper operations themselves also consume computation.

### 10.5 Candidate renaming

All aggregate results were preserved exactly under candidate renaming. The cascade's behavior retention was 100%.

This indicates that the tested mechanism depends on generated evidence/context/relation structure rather than opaque candidate labels.

---

## 11. What HCT-1 Supports

Within this synthetic experimental family, the following claims are now reasonably supported:

### 11.1 Soft reversible narrowing is substantially safer than hard deletion under changing context

This is the clearest result. Hard Top-K could not restore excluded candidates. Both soft methods could.

### 11.2 A large field can be reduced before expensive recurrence without losing the correct candidate in the tested worlds

The cascade retained the correct candidate into final recurrence in 100% of the 200 held-out worlds while reducing recurrence from 256 candidates to 12.

### 11.3 Commitment must remain distinct from ranking

The unresolved worlds demonstrate that a first-place candidate should not automatically produce an answer. The system can have a winner and still abstain.

### 11.4 Learned routing parameters can transfer across candidate identity

The learned resistance/order/gain parameters remained effective after opaque candidate renaming.

### 11.5 Context change should be allowed to reopen a broader field

The reversal results support a computational architecture in which earlier suppression is provisional rather than permanent.

---

## 12. What HCT-1 Does Not Yet Support

The following stronger claims remain unestablished.

### 12.1 Multiple distinct context-specific taper stages are not yet shown to be necessary

The generic soft control achieved:

```text
100% good behavior
100% correct-candidate survival
100% reversal reactivation
96 recurrent candidate-cycles
```

These matched the cascade on the primary behavioral outcomes.

The context-specific cascade therefore did **not** demonstrate a behavioral advantage over generic soft tapering in HCT-1 v1.

### 12.2 The cascade is not yet computationally superior overall

Average taper candidate-evaluations were:

```text
Generic soft taper            1228.8
Context-specific cascade      4915.2
```

The cascade required roughly four times as many taper candidate-evaluations in this implementation.

Therefore the current evidence does not justify a claim that the full cascade is cheaper overall. HCT-2 directly addresses this by allowing later context stages to evaluate only the currently eligible sparse field rather than all candidates at every stage.

### 12.3 HCT-1 does not establish semantic cognition

The contextual dimensions are anonymous synthetic channels, not learned human-like concepts such as time, self, goals, relationships, causality, or semantics.

### 12.4 HCT-1 does not yet isolate recurrence from static reweighting

HCT-2 includes explicit no-resistance and no-recurrence ablations. These are mechanistic probes rather than primary gates: if removing recurrence or resistance leaves behavior unchanged, the interpretation of those components must be weakened rather than protected post hoc.

---

## 13. Current Theory Status

The research program can now be summarized as follows.

### Discounted or failed mechanisms

```text
automatic clock-driven progressive Top-K
single global confidence gate as sufficient solution
stochastic winner consensus as evidence of truth
irreversible hard deletion under changing context
```

### Promising mechanisms

```text
outcome-learned pathway resistance
state-dependent recurrence when the task truly requires interaction
soft reversible suppression
separate commitment/abstention logic
context-driven reopening
identity-independent structural transfer
```

### Promising but not yet uniquely justified

```text
multiple ordered context-specific taper stages
learned stage ordering as a computational advantage
```

The strongest current formulation of the theory is therefore narrower than the original aspiration:

> **A large candidate field should be narrowed softly and reversibly before expensive relational deliberation, and commitment should depend on discriminating evidence rather than simply on the existence or repetition of a winner.**

A stronger statement—that cognition benefits specifically from several ordered contextual settling stages—remains under active test in HCT-2.

---

## 14. HCT-2: Frozen Ordered Conditional Context Experiment

HCT-2 is no longer merely a proposed next step. Its design, implementation, tests, and interpretation gate are now frozen before final held-out evaluation.

### 14.1 Why HCT-2 exists

HCT-1 established that reversible soft narrowing can preserve behavior and recover from changed context, but it did **not** establish that multiple distinct ordered stages are needed. Generic soft tapering matched the cascade behaviorally and used fewer taper evaluations.

HCT-2 therefore tests a narrower and more demanding claim:

> **Does a learned order of context-specific settling become computationally useful when context channels are hierarchically aliased and later context is cheaper or safer to evaluate only after earlier context has narrowed the active field?**

The primary HCT-2 claim is an **efficiency-with-preserved-behavior** claim, not an accuracy-superiority claim.

### 14.2 HCT-2 hypothesis

> **A learned ordering of reversible sparse context stages will preserve high correct-or-abstain behavior and correct-candidate survival in hierarchically aliased worlds while using substantially fewer context-feature evaluations than a strong simultaneous learned generic-soft control. The learned order should also be more evaluation-efficient than the same sparse mechanism run in fixed anonymous channel order.**

The hypothesis is weakened if generic soft matches behavior at similar context-evaluation cost, if learned ordering provides no measurable efficiency benefit over fixed order, if correct candidates fail to survive sparse settling, or if reversibility is lost.

### 14.3 Larger and harder candidate field

HCT-2 uses:

```text
512 opaque candidates per world
16-candidate recurrent width
8 recurrent cycles
4 hierarchical context depths
```

Each candidate has a four-level latent context path. Deeper observed context tokens are encoded through prefix-specific deterministic codebooks. The same deep token can therefore occur under different broad contexts.

This means a deep feature can be locally meaningful but globally ambiguous.

### 14.4 Anonymous context channels are scrambled

The learner is not presented with context channels in semantic-depth order.

Frozen mapping:

```text
channel 0 -> semantic depth 2
channel 1 -> semantic depth 0
channel 2 -> semantic depth 3
channel 3 -> semantic depth 1
```

The learner must derive a useful processing order from training outcomes. Development calibration indicates that the learned order recovers semantic depth progression `0 -> 1 -> 2 -> 3`, but this development observation is **not** a final HCT-2 result.

### 14.5 Conditional aliasing

HCT-2 creates wrong-broad-context candidates that share deeper raw context tokens with the correct path. Therefore simply averaging all context globally may spend computation evaluating features whose interpretation is ambiguous outside the proper broad basin.

The proposed sparse mechanism instead asks:

```text
settle broad context
    -> mark a narrower high-activation field as eligible
    -> evaluate the next context stage mainly within that field
    -> continue narrowing conditionally
```

Dormant candidates are suppressed, not deleted. Context reversal can reopen from the broad field.

### 14.6 HCT-2 conditions

Seven conditions are frozen:

```text
1. no_taper
2. hard_topk
3. generic_soft
4. fixed_order_sparse
5. learned_order_sparse
6. learned_order_no_resistance
7. learned_order_no_recurrence
```

**No taper** runs recurrence over all 512 candidates.

**Hard Top-K** scores the broad field, retains only 16 candidates, and permanently excludes the rest for that episode. Context reversal may rescore only retained candidates.

**Generic soft** uses all learned context gains simultaneously across the full field for repeated settling cycles. It is deliberately a strong control.

**Fixed-order sparse** uses the same reversible sparse mechanism and learned gains as the proposed model, but processes anonymous channels in fixed numerical order `(0, 1, 2, 3)`.

**Learned-order sparse** is the primary proposed mechanism. It uses the learned channel order and reversible sparse eligibility.

**Learned-order no resistance** removes learned evidence resistance to test whether resistance contributes independently.

**Learned-order no recurrence** replaces recurrent deliberation with a non-recurrent downstream decision to test whether recurrence contributes independently.

The no-resistance and no-recurrence conditions are mechanistic ablations. They are not forced to fail by the primary HCT-2 gate.

### 14.7 HCT-2 data firewall

Frozen splits:

```text
Training:     70000-70499   (500 worlds)
Development:  71000-71149   (150 worlds)
Quick dev:    71000-71049    (50 worlds)
Final:        72000-72299   (300 worlds, reserved)
```

The final split is not used for:

```text
quick runs
parameter selection
development tuning
gate selection
regression tests
```

The CLI explicitly separates development quick mode from the final run so the final split cannot be accidentally consumed by `--quick`.

At the time of this revision, the HCT-2 final 300-world split remains **untouched**.

### 14.8 Frozen HCT-2 interpretation gate

Before any final HCT-2 evaluation, the following primary criteria are frozen:

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
```

These criteria must not be loosened after inspecting final results.

### 14.9 What would count as strong HCT-2 evidence

The strongest HCT-2 result would not merely be higher accuracy. It would show that the learned ordered sparse mechanism:

```text
preserves correct-or-abstain behavior
preserves the correct candidate
retains genuine uncertainty
recovers after context reversal
transfers under candidate renaming
uses much less context evaluation than generic simultaneous tapering
uses less evaluation than the same sparse mechanism in the wrong/fixed order
continues to reduce expensive recurrence
```

That would be direct evidence that **order itself carries computational value** when context is conditional.

### 14.10 What would weaken the theory

If generic soft again matches behavior and requires similar or less total context work, the stronger multi-stage claim should be weakened.

If fixed order performs as efficiently as learned order, the claim that learning the context sequence matters should be weakened.

If no-recurrence performs equivalently, the recurrent interpretation should be weakened.

If no-resistance performs equivalently, the resistance interpretation should be weakened.

If hard Top-K handles reversal as well as reversible tapering in the new worlds, the claimed need for reopening would be weakened.

HCT-2 is therefore designed so that several parts of the current theory can fail independently.

---

## 15. Long-Term Architecture Hypothesis

The broader Synrheon architecture remains:

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
learned-resistance state-dependent recurrence
        |
        v
evidence + uncertainty accumulation
        |
        +--> COMMIT
        +--> ABSTAIN
        +--> SEEK DISCRIMINATING EVIDENCE
        +--> REOPEN BROADER CONTEXT
```

The four computational questions remain:

```text
Policy:
What mental operation should I perform?

Taper:
What portion of the knowledge field should remain strongly active?

Recurrence:
How do serious alternatives change one another's support?

Commitment:
Do I know enough to act?
```

The long-term goal is not to hand-code these answers. The architecture should expose learnable operations and allow experience to shape which operations are selected, which pathways resist activation, which context is useful, what order context should be applied, when narrowing is justified, and when prior suppression should be reopened.

---

## 16. Scientific Boundary

The current Synrheon evidence does **not** establish:

- biological hippocampal equivalence;
- a new mathematical law;
- superiority to transformers, attention, mixture-of-experts, associative-memory, learned-retrieval, or modern routing systems;
- general reasoning;
- natural-language benefit;
- learned semantic representations;
- autonomous cognition;
- production integration of the hippocampal-inspired branch;
- lower total compute than simpler soft-routing systems;
- necessity of multiple context-specific taper stages;
- a final HCT-2 result.

The current evidence supports a narrower experimental direction: learned pathway resistance can transfer structural reliability in a synthetic family; state-dependent recurrence can matter when candidate interactions genuinely change later evidence; hard pruning can destroy recoverable alternatives; reversible soft narrowing can preserve those alternatives while substantially shrinking the field entering recurrence; and uncertainty should remain explicit rather than being converted automatically into commitment.

HCT-2 is the current attempt to determine whether **ordered conditional context settling** adds a measurable computational advantage beyond generic reversible soft narrowing.

---

## 17. Experimental Sequence and Continuation Protocol

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

HCT-2 status:

```text
DESIGNED
IMPLEMENTED
PREREGISTERED
DEVELOPMENT-CALIBRATED
FINAL 300-WORLD SPLIT NOT YET RUN
```

Scientific interpretation before HCT-2 final evaluation:

```text
Strongest supported claim:
reversible soft narrowing > irreversible hard pruning under context change

Current open claim:
learned ordered conditional sparse settling > simpler generic soft taper
on efficiency while preserving behavior
```

The next scientific action is the untouched HCT-2 final assay. Its result should be interpreted against the frozen gate without post-hoc threshold changes.

---

## References

Bakker, A., Kirwan, C. B., Miller, M., & Stark, C. E. L. (2008). Pattern separation in the human hippocampal CA3 and dentate gyrus. *Science, 319*(5870), 1640-1642. https://doi.org/10.1126/science.1152882

Myers, C. E., & Scharfman, H. E. (2011). Pattern separation in the dentate gyrus: A role for the CA3 backprojection. *Hippocampus, 21*(11), 1190-1215. https://doi.org/10.1002/hipo.20828

Neunuebel, J. P., & Knierim, J. J. (2014). CA3 retrieves coherent representations from degraded input: Direct evidence for CA3 pattern completion and dentate gyrus pattern separation. *Neuron, 81*(2), 416-427. https://doi.org/10.1016/j.neuron.2013.11.017

Nolan, C. R., Wyeth, G., Milford, M., & Wiles, J. (2011). The race to learn: Spike timing and STDP can coordinate learning and recall in CA3. *Hippocampus, 21*, 647-660. https://doi.org/10.1002/hipo.20777

Kim, S.-Y., & Lim, W. (2021). Dynamical origin for winner-take-all competition in a biological network of the hippocampal dentate gyrus. arXiv:2105.06057.

Synrheon experimental source: hippocampal experiment modules, tests, and preregistration documents on branch `experiment/hippocampal-sparse-settling`.