# Context-Settled Tapering and Learned-Resistance Recurrent Inference

## A revised hippocampal-inspired theory of staged contextual compression, learned cognitive routing, open-field recurrence, and evidence-gated commitment

**Synrheon Experimental Research Program**  
**August 9, 2026**

## Abstract

This paper develops a hippocampal-inspired inference theory in which a very large knowledge field is not collapsed in a single pruning step. Information instead passes through multiple soft contextual tapers. Each taper settles on a coherent context before forwarding a compressed but reversible representation to the next stage. Expensive state-dependent recurrent inference is then reserved for a much smaller field of serious competing hypotheses.

The theory retains the previously tested learned-resistance term, in which historically misleading evidence pathways acquire higher resistance and historically reliable pathways lower resistance. Existing Synrheon assays provide preliminary support for learned structural resistance and for state-dependent recurrence, while falsifying clock-driven progressive Top-K pruning in the tested relational family. Later confidence-gating and stochastic-consensus assays further showed that a stable winner is not sufficient evidence for truth or commitment.

The central revision in this version is that contextual tapering is no longer treated as a hand-authored routing policy. The mathematical taper operation may be designed cognitive physics, but contextual reliability, stage ordering, gain, and eventual selection of contextual operations should increasingly be learned from outcomes and transferred across candidate identities. The proposed architecture therefore separates four computational questions: what cognitive operation should occur, what broad knowledge should remain active, how serious alternatives interact recurrently, and whether the evidence is sufficient to commit.

The staged contextual-taper system remains a hypothesis. The new HCT-1 experiment is a direct full-system falsification assay using large nested candidate fields, transferable learned contextual weighting, reversible soft suppression, learned-resistance recurrence, calibrated abstention, context reversal, and matched hard/generic/no-taper controls.

---

## 1. Research Question and Thesis

The central thesis is that inference over a very large learned knowledge field may benefit from separating four functions that are often collapsed into one scoring process:

1. **Cognitive-operation selection** — deciding what kind of mental operation should occur next.
2. **Contextual tapering** — reducing irrelevant breadth without deleting recoverable alternatives.
3. **Relational deliberation** — allowing serious candidates to reinforce or suppress one another through recurrent state-dependent interaction.
4. **Commitment** — deciding whether evidence is sufficient to answer, abstain, seek information, or reopen broader context.

The earlier Synrheon formulation separated relational support from learned resistance. Relational support represents how strongly current evidence favors a candidate. Resistance represents how readily evidence from a pathway should influence settling based on historical outcome reliability.

The new claim is broader but still falsifiable: a learned contextual-routing layer may be able to reduce a very large candidate field before expensive recurrence while preserving the correct hypothesis, maintaining uncertainty when ambiguity is real, and reopening previously suppressed alternatives when context changes.

This is not a claim of hippocampal biological equivalence. It is a computational abstraction motivated by pattern separation, pattern completion, sparse competition, recurrent settling, and the experimental failures of premature hard collapse.

---

## 2. Biological and Computational Motivation

Hippocampal research distinguishes pattern separation, strongly associated with dentate gyrus and CA3 processing, from pattern completion associated with recurrent CA3 dynamics. Similar or degraded inputs can be transformed into separated representations and later reconstructed into coherent stored patterns. Sparse competition and winner-take-all dynamics have also been modeled in dentate-gyrus-inspired networks.

Synrheon borrows these functional motifs without claiming to reproduce hippocampal biophysics.

The computational motivation is simpler: a large cognitive system cannot afford to run expensive relational recurrence across all knowledge all the time. But hard early pruning is dangerous because an initially weak candidate may become correct after relational settling or new evidence. Therefore narrowing should be soft, contextual, reversible, and earned.

---

## 3. Tested Mathematical Core: Learned Resistance

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

A channel repeatedly stronger in wrong alternatives becomes harder to traverse. A channel repeatedly stronger in correct alternatives becomes easier. Candidate identity is not a learned parameter.

### Preliminary result

The initial learned-resistance assay produced approximately:

```text
Equal-resistance baseline     10.0% accuracy
Learned resistance            94.5% accuracy
Renamed candidates            94.5% accuracy
Renaming retention           100.0%
```

This supports a limited proposition: outcome-driven pathway reliability can transfer independently of candidate labels in the tested synthetic family.

It does not establish mathematical novelty or superiority to ordinary learned weights, attention, gating, or other conventional mechanisms.

---

## 4. Tested Mathematical Core: State-Dependent Recurrence

The current deliberative operator is:

```text
u_i^(t+1)
  = alpha * a_i^(t)
  + beta * sum_j[(W+_ji / R+_ji) * a_j^(t)]
  - mu   * sum_j[(W-_ji / R-_ji) * a_j^(t)]
  + gamma * I_i
```

Candidate activation at cycle `t` changes the evidence landscape at cycle `t+1`. Compatible candidates can reinforce one another and incompatible candidates can suppress one another.

The strongest mechanistic result to date was:

```text
One-pass initial scorer                  0%
State-dependent recurrent, fixed width  98%
Clock-driven progressive recurrence     25.5%
```

This supports state-dependent recurrence in the tested relational family and strongly discounts automatic cycle-driven pruning.

---

## 5. What Failed and Why It Matters

### 5.1 Clock-driven progressive Top-K

The original architecture narrowed the field because recurrent cycles elapsed. This was harmful. Useful candidates were removed before their relational support had time to circulate.

> **Elapsed computation is not evidence that a candidate should disappear.**

### 5.2 Confidence-gated narrowing

A later confidence/stability gate preserved accuracy but either failed to activate or produced only modest active-state savings. This suggested that a single global narrowing event may be the wrong abstraction for very large knowledge fields.

### 5.3 Stochastic consensus

Repeated perturbed recurrent trials produced false certainty in deliberately unresolved worlds. In the tested assay, unresolved-close worlds committed approximately 78% of the time, despite a requirement of at most 50%.

> **A stable or frequently repeated winner can reflect a stable structural bias rather than sufficient evidence.**

Winner frequency alone is therefore not a valid truth criterion.

---

## 6. Revised Theory: Cascaded Context-Settled Soft Tapering

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

The critical distinction is that `P^(s)` is not a hard deletion operator. Suppressed hypotheses remain recoverable.

Early stages may remain broad and high-temperature. Later stages may become more selective. Different taper stages may answer different contextual questions, such as relevance, semantic compatibility, temporal compatibility, goal relation, self relation, or relational coherence.

---

## 7. New Architectural Constraint: The Route Must Become Learned

The taper equations alone are not enough. If a developer permanently decides which context matters, what order the stages should run, what candidate region each stage should prefer, and how strongly each stage should narrow, then Synrheon has merely replaced one hand-written routing system with another.

The revised architecture therefore separates **designed cognitive physics** from **learned cognitive skill**.

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

The immediate HCT-1 experiment does not yet learn arbitrary semantic representations or a fully state-conditioned action policy. It uses anonymous context channels and asks whether reliability/order over those channels can be learned from training outcomes and transferred to unseen candidate identities. This is intentionally narrower than the long-term architecture.

---

## 8. Full Architecture Hypothesis

```text
VERY LARGE LEARNED KNOWLEDGE FIELD
        |
        v
learned cognitive-operation / context routing
        |
        v
context-settled soft taper 1
        |
        v
context-settled soft taper 2
        |
        v
additional context-specific tapers as needed
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

The four computational questions are:

```text
Policy:
What mental operation should I perform?

Taper:
What portion of the knowledge field should remain active?

Recurrence:
How do serious alternatives change one another's support?

Commitment:
Do I know enough to act?
```

---

## 9. New Falsifiable Hypothesis: HCT-1

### HCT-1 — Learned Contextual Taper + Recurrent Deliberation

> **A transferable learned contextual-routing layer controlling multiple reversible soft taper stages will reduce a large nested candidate field before learned-resistance recurrent deliberation, while preserving final accuracy, retaining real ambiguity, and permitting context-driven reactivation better than matched hard pruning.**

The hypothesis is explicitly discounted if a simpler matched mechanism performs as well or better.

### HCT-1A — Transfer

Learned context reliability/order should transfer across opaque candidate renaming and unseen generated worlds.

### HCT-1B — Survival

The correct candidate should survive the contextual cascade into expensive recurrence at a high rate, including misleading-early cases.

### HCT-1C — Expensive recurrent compute

The cascade should send substantially fewer candidates into expensive recurrent deliberation than no-taper full-field recurrence.

This is intentionally **not** the same as claiming lower total wall-clock compute. HCT-1 v1 separately reports taper candidate-evaluations and recurrent candidate-cycles. A total compute claim requires a justified cost model for the two operations.

### HCT-1D — Reversibility

When later evidence changes the contextual basin, a candidate suppressed by the initial context should be able to re-enter. A hard Top-K control should fail this case whenever the candidate was deleted.

### HCT-1E — Uncertainty

Genuinely unresolved-close worlds should usually remain uncommitted rather than being forced into an answer.

### HCT-1F — Context specificity

A cascade using distinct learned contextual functions should be compared against a matched generic soft taper. If the generic control equals or exceeds the context-specific cascade on behavior and reactivation, the stronger context-specific claim is weakened.

### HCT-1G — Recurrence and resistance remain separable

Downstream recurrence and learned evidence resistance must remain separately ablatable. If the full-system gain can be reproduced by simple static reweighting, the recurrent/resistance interpretation is weakened.

---

## 10. HCT-1 v1 Full-System Experiment

The first HCT-1 assay uses synthetic worlds containing **256 opaque candidates** organized into nested context families. The recurrent field is capped at 12 serious candidates after tapering.

World regimes include:

```text
clear context
misleading early evidence
persistent close competitors
genuinely unresolved close calls
context reversal after initial suppression
```

### Information firewall

The generator is allowed to know hidden truth in order to create a scoreable synthetic world. Before held-out inference begins it materializes:

```text
opaque candidates
anonymous evidence channels
context-path features
explicit excitation relations
explicit inhibition relations
current context cue
```

Held-out inference receives those generated structures. The recurrent solver consumes the explicit relation field and does **not** consult `correct_index` when updating activations.

The hidden correct index may be used only for:

```text
training outcome updates after an episode
post-inference scoring
reactivation/survival measurement
```

Held-out inference must not receive:

```text
correct candidate identity as a feature
correct route
hidden answer index as a routing signal
future context reversal before it occurs
solver output
candidate name embedding
world seed as a predictive feature
```

Candidate names can be regenerated independently without changing evidence, context, or relation structure.

### Matched controls

```text
1. no taper + full-field recurrence
2. hard global Top-K + identical downstream recurrence
3. generic soft taper + identical downstream recurrence
4. learned context-specific cascaded soft tapers + identical downstream recurrence
```

Later versions should separately ablate learned resistance and recurrence.

### Measurements

```text
final correct rate
correct-or-abstain behavior
commit rate
unresolved-world commitment rate
correct-candidate survival into recurrence
recurrent candidate-cycles
taper candidate-evaluations
post-taper active proxy
context-reversal suppression cases
reactivation success after context reversal
candidate-renaming retention
per-world-type results
```

The experiment deliberately keeps **recurrent candidate-cycles** separate from **taper candidate-evaluations**. HCT-1 v1 only claims that the taper can reduce the field entering expensive recurrence. It does not claim total compute superiority without a calibrated cost model.

---

## 11. Predeclared HCT-1 v1 Interpretation Gate

The HCT-1 v1 mechanism is **reinforced** only if all of the following hold on untouched held-out worlds:

1. context-specific cascade correct-or-abstain behavior is at least 85%;
2. correct-candidate survival into final recurrence is at least 90%;
3. unresolved-close commitment rate is at most 25%;
4. at least 5 held-out context-reversal worlds actually suppress the correct candidate from the initial recurrent field, so reactivation is genuinely exercised;
5. context-reversal reactivation succeeds in at least 75% of those suppressed cases;
6. hard Top-K reactivation is at least 20 percentage points worse than reversible contextual tapering on suppressed reversal cases;
7. context-specific cascade recurrent candidate-cycle cost is at most 50% of no-taper full-field recurrent candidate-cycle cost;
8. candidate renaming retains at least 97% of context-specific cascade behavior;
9. the generic soft control does not beat the context-specific cascade by more than 3 percentage points on correct-or-abstain behavior;
10. no candidate identity or hidden answer signal enters held-out routing or recurrent state updates.

If the reversal mechanism is not exercised enough to satisfy criterion 4, the assay is **inconclusive**, not reinforced.

If any other frozen criterion fails, the corresponding part of HCT-1 is discounted. Thresholds must not be lowered after inspecting the held-out result. A material mechanism change creates a new experiment version and should receive a new untouched held-out split.

---

## 12. Scientific Boundary

The current Synrheon evidence does **not** establish:

- a biological hippocampal mechanism;
- a new mathematical law;
- superiority to transformers, attention, mixture-of-experts, associative-memory, learned-retrieval, or modern routing systems;
- general reasoning;
- natural-language benefit;
- learned semantic representations;
- autonomous cognition;
- production integration of the hippocampal-inspired branch.

The current evidence supports a narrower research direction: learned pathway resistance can transfer structural reliability in a synthetic family, state-dependent recurrence can matter when candidate interactions change later evidence, and automatic hard narrowing can destroy useful support.

HCT-1 asks whether a learned, reversible contextual front end can make that recurrent mechanism more tractable without recreating brittle hand-written routing.

---

## 13. Experimental Sequence and Continuation Protocol

Repository: `Logancarton/Synrheon`  
Research branch: `experiment/hippocampal-sparse-settling`

Existing sequence:

```text
experiments/hippocampal_settling.py
experiments/hippocampal_learning.py
experiments/hippocampal_equivalence.py
experiments/hippocampal_stateful_recurrence.py
experiments/hippocampal_confidence_gated.py
experiments/hippocampal_consensus_trials.py
```

HCT-1 implementation:

```text
experiments/hippocampal_contextual_taper_full_system.py
tests/test_hippocampal_contextual_taper_full_system.py
```

The failed stochastic-consensus threshold should not be tuned further as the default next step. The next scientific target is the HCT-1 full-system contextual-taper falsification assay.

---

## References

Bakker, A., Kirwan, C. B., Miller, M., & Stark, C. E. L. (2008). Pattern separation in the human hippocampal CA3 and dentate gyrus. *Science, 319*(5870), 1640-1642. https://doi.org/10.1126/science.1152882

Myers, C. E., & Scharfman, H. E. (2011). Pattern separation in the dentate gyrus: A role for the CA3 backprojection. *Hippocampus, 21*(11), 1190-1215. https://doi.org/10.1002/hipo.20828

Neunuebel, J. P., & Knierim, J. J. (2014). CA3 retrieves coherent representations from degraded input: Direct evidence for CA3 pattern completion and dentate gyrus pattern separation. *Neuron, 81*(2), 416-427. https://doi.org/10.1016/j.neuron.2013.11.017

Nolan, C. R., Wyeth, G., Milford, M., & Wiles, J. (2011). The race to learn: Spike timing and STDP can coordinate learning and recall in CA3. *Hippocampus, 21*, 647-660. https://doi.org/10.1002/hipo.20777

Kim, S.-Y., & Lim, W. (2021). Dynamical origin for winner-take-all competition in a biological network of the hippocampal dentate gyrus. arXiv:2105.06057.

Synrheon experimental source: the hippocampal experiment modules on branch `experiment/hippocampal-sparse-settling`.