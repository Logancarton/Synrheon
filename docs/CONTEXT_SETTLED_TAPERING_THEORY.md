# Context-Settled Tapering and Recurrent Inference — Ground 0

## Reversible contextual narrowing, recurrent deliberation, and evidence-gated commitment

**Synrheon Experimental Research Program**  
**Revision 4 — August 9, 2026**

## Abstract

Synrheon is testing a cognitive-process hypothesis for inference over a very large candidate or knowledge field. The current Ground 0 proposal is not to score everything once and permanently choose the highest value. Instead, a broad field is progressively narrowed through **soft, reversible contextual tapering**; a smaller set of serious alternatives then undergoes **state-dependent recurrent deliberation**; and a separate commitment process decides whether to commit, abstain, seek evidence, or reopen broader context.

The theory emerged through a sequence of failures and partial successes. Clock-driven Top-K pruning damaged relational inference. Confidence-only gating gave limited savings. Stochastic consensus overcommitted unresolved cases. HCT-1 then showed a strong synthetic advantage for reversible suppression over irreversible deletion under context reversal. HCT-2 extended the synthetic program to hierarchical context and produced apparently strong ordering, efficiency, abstention, reopening, and recurrence-ablation results.

A post-HCT code review materially changes how the HCT-2 results should be interpreted. The review identified six design properties that could inflate the stronger HCT conclusions: positional tie leakage, correctness-dependent structure in the synthetic relation graph, asymmetric memoization that made the generic control artificially expensive, a recurrent-cost ratio determined by configured constants rather than measured work, channel order entangled with the synthetic hierarchy, and weak self-authored baselines. These do **not** make the historical HCT measurements disappear. They mean that the strongest mechanistic interpretations—especially the HCT-2 recurrence ablation and the ordering/efficiency claims—must now be treated as **provisional synthetic evidence pending external validation**.

EXT-1 is the next confirmatory gate. It evaluates the same broad Ground 0 ideas on public BEIR retrieval data with published relevance judgments and a published BM25 anchor. Its design explicitly removes the six HCT vulnerabilities, measures rather than assumes feature cost, uses paired confidence intervals, and refuses to call any synthetic smoke run evidence.

The current theory should therefore be read as a research architecture with different evidence levels, not as a set of settled facts.

---

## 1. Ground 0 Research Question

The central question is:

> **Can a cognitive system reduce a very large field of possible knowledge or hypotheses without prematurely deleting alternatives that later context or recurrent interaction may make important?**

The current proposed process is:

```text
VERY LARGE CANDIDATE / KNOWLEDGE FIELD
        ↓
learned context / operation routing
        ↓
ordered reversible soft tapering
        ↓
TRACTABLE SERIOUS-CANDIDATE FIELD
        ↓
state-dependent recurrent deliberation
        ↓
evidence + uncertainty
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
```

Learned pathway resistance is no longer a required Ground 0 component. It remains an optional reliability mechanism that must earn its role separately.

---

## 2. Why the Process Is Split Into Separate Jobs

The architecture separates four functions that a one-shot scorer can collapse together:

1. **Routing** — what context or cognitive operation should be evaluated next?
2. **Tapering** — which candidates still deserve expensive computation?
3. **Recurrence** — how do surviving serious alternatives change one another's support?
4. **Commitment** — is the resulting evidence sufficient to act?

The core distinction is:

```text
suppressed ≠ deleted
winner ≠ knowledge
ranking ≠ commitment
```

A weak candidate may later become relevant. A stable winner may still be unsupported. A high-ranked option should therefore remain separable from the decision to assert it as known.

---

## 3. Experimental Development: What Failed First

The current theory was shaped at least as much by negative results as by successful ones.

### 3.1 Learned resistance

An early synthetic assay produced approximately:

```text
Equal resistance      10.0% accuracy
Learned resistance    94.5% accuracy
Renamed candidates    94.5% accuracy
```

This suggested that historical evidence reliability could transfer independently of candidate labels. HCT-2 later showed no behavioral loss when resistance was removed. Current status:

```text
PROMISING IN A SPECIFIC EARLY FAMILY
NOT REQUIRED IN HCT-2
OPTIONAL / TASK-DEPENDENT
```

### 3.2 First recurrence test

A one-pass system already reached about 99%, while recurrent inference reached about 100%.

```text
INCONCLUSIVE FOR RECURRENCE NECESSITY
```

### 3.3 State-dependent recurrence assay

A redesigned relational task produced approximately:

```text
One-pass initial scorer                  0%
Fixed-width state-dependent recurrence  98%
Clock-driven progressive recurrence     25.5%
```

This supported recurrence **inside that synthetic construction** and strongly argued against arbitrary time-driven pruning.

### 3.4 Confidence gating

The first gate barely or never fired. A later adaptive version preserved behavior but saved only about 7.61% of active state, below its preregistered 10% target.

```text
LIMITED
```

### 3.5 Stochastic consensus

Deliberately unresolved synthetic worlds were nevertheless committed about 78% of the time.

```text
FAILED
```

The important lesson was:

> **Repeated agreement is not sufficient evidence.**

This motivated explicit abstention and a separate commitment layer.

---

## 4. Evidence Summary — Revision 4 Status

The table below records the historical result **and the current evidentiary status after the HCT code review**.

| Mechanism / assay | Historical observation | Revision 4 interpretation |
|---|---|---|
| Learned resistance | ~10% baseline vs ~94.5% learned; rename retained | Promising but task-dependent; not necessary in HCT-2 |
| Static recurrence | ~99% one-pass vs ~100% recurrent | Recurrence necessity not established |
| Stateful recurrence | 0% one-pass vs ~98% recurrent | Synthetic support; external confirmation still needed |
| Clock-driven Top-K | ~25.5% in stateful assay | Failed; elapsed cycles are not evidence for deletion |
| Confidence gating | ~7.61% active-state saving vs 10% target | Limited |
| Stochastic consensus | ~78% commit on unresolved worlds | Failed as a commitment signal |
| HCT-1 reversible taper | Soft mechanisms recovered after reversal; hard Top-K did not | Strong synthetic evidence for reversibility |
| HCT-2 ordered taper | 100% good behavior; apparent 5.49% ordering advantage | **Provisional: order was entangled with synthetic hierarchy; EXT-1 pending** |
| HCT-2 context-evaluation cost | reported learned cascade ~7.14% of generic-soft evaluations | **Discounted as a clean efficiency result: generic control memoization was asymmetric; EXT-1 pending** |
| HCT-2 recurrent-load ratio | reported 3.125% of full-field candidate-cycles | Descriptive configured-width ratio, not measured compute evidence |
| HCT-2 no-recurrence ablation | 100% → 45% good behavior, with 100% candidate survival | **Internally striking but mechanistically exposed by answer-bearing relation graph; EXT-1 pending** |
| HCT-2 abstention/reopening | 0% unresolved commitment; 100% reversal recovery | Synthetic support; external C2/C3 now required |

This revision intentionally does **not** erase the HCT numbers. It changes what they are allowed to prove.

---

## 5. HCT-1: What Still Looks Valuable

HCT-1 used 256 opaque candidates and a 12-candidate recurrent field across 200 held-out synthetic worlds.

Historical aggregate results:

| Condition | Correct | Commit | Correct-or-abstain | Correct survival | Recurrent candidate-cycles | Reversal reactivation |
|---|---:|---:|---:|---:|---:|---:|
| No taper | 85.0% | 23.5% | 43.5% | 100.0% | 2048 | n/a |
| Hard Top-K | 63.5% | 71.5% | 77.5% | 79.5% | 96 | 0.0% |
| Generic soft | 84.5% | 80.0% | 100.0% | 100.0% | 96 | 100.0% |
| Context-specific cascade | 85.5% | 80.0% | 100.0% | 100.0% | 96 | 100.0% |

The strongest HCT-1 lesson remains qualitative:

> **Irreversible deletion is brittle when later context can change which candidate matters.**

The major limitation was already visible in HCT-1: generic soft tapering matched the context-specific cascade behaviorally while using fewer taper evaluations. HCT-1 therefore did not establish the necessity of multiple ordered context-specific stages.

---

## 6. HCT-2 Historical Result

HCT-2 increased the field to 512 candidates, used four hierarchical context depths, a 16-candidate recurrent field, and 300 final synthetic worlds.

Historical aggregate results:

| Condition | Correct | Commit | Good behavior | Survival | Recurrent candidate-cycles | Context evaluations | Reversal recovery |
|---|---:|---:|---:|---:|---:|---:|---:|
| No taper | 50.0% | 28.0% | 48.0% | 100.0% | 4096 | 0 | n/a |
| Hard Top-K | 70.67% | 60.33% | 80.0% | 80.0% | 128 | 2060.8 | 0.0% |
| Generic soft | 90.33% | 80.0% | 100.0% | 100.0% | 128 | 19660.8 | 100.0% |
| Fixed-order sparse | 90.33% | 80.0% | 100.0% | 100.0% | 128 | 1485.78 | 100.0% |
| Learned-order sparse | 90.33% | 80.0% | 100.0% | 100.0% | 128 | 1404.26 | 100.0% |
| No resistance | 91.33% | 80.0% | 100.0% | 100.0% | 128 | 1404.26 | 100.0% |
| No recurrence | 85.0% | 25.0% | 45.0% | 100.0% | 0 | 1404.26 | 81.67% |

Those measurements remain part of the research record. Revision 4 changes the interpretation because later code review found that several controls and synthetic structures were not independent enough to support the strongest causal claims.

---

## 7. The Six HCT-2 Vulnerabilities Found in Review

### 7.1 Positional tie leakage

The correct synthetic candidate occupied a privileged index and stable sorting could resolve equal scores toward that position.

EXT-1 instead derives relevance from external qrels and breaks score ties by document id.

### 7.2 Answer-bearing relation graph

The HCT-2 relation construction included correctness-dependent excitation. That means a recurrent solver could receive structural information correlated directly with the hidden answer.

This matters most for the apparent recurrence ablation.

EXT-1 builds document/document relations only from rare-term overlap. Its regression suite requires the relation field to remain unchanged when every qrel is removed.

### 7.3 Asymmetric memoization

The HCT-2 generic-soft control repeatedly evaluated feature values that were invariant across cycles. Those repeated evaluations were counted as cost, producing much of the apparent 7.14% efficiency advantage.

EXT-1 gives every condition its own `FeatureMeter` and charges cache misses only.

### 7.4 Configured rather than measured recurrent cost

The 3.125% HCT-2 recurrent-load figure is mathematically:

```text
16 candidates × 8 cycles
------------------------
512 candidates × 8 cycles
```

That is a useful description of field width, but it cannot by itself establish a computational efficiency advantage.

EXT-1 counts actual feature cache misses and separately records measured nanoseconds.

### 7.5 Channel order entangled with synthetic hierarchy

The HCT-2 order result was not independent enough from the generator's branching/depth construction to establish discovery of a general semantic hierarchy.

EXT-1 instead learns order from **discriminative utility per unit of measured development cost**.

### 7.6 Weak self-authored baselines

Synthetic controls can unintentionally make the tested mechanism look better simply because the whole world family was designed around that mechanism.

EXT-1 uses BM25 with a published BEIR anchor and a fully evaluated cached rerank control.

---

## 8. Current Mathematical Hypothesis

Ground 0 still proposes a reversible taper interface.

For candidate `i`, taper stage `s`, and internal stage cycle `t`, a generic representation is:

```text
z_i^(s,t)
  = gamma_s I_i^(s)
  + sum_j W_ij^(s) a_j^(s,t)
  - lambda_s D_i^(s,t)

a_i^(s,t+1) = softmax(z_i^(s,t) / tau_s)
```

A stage may settle when:

```text
||a^(s,t+1) - a^(s,t)||_1 < epsilon_s
```

The next stage receives a soft projection rather than hard deletion:

```text
I^(s+1) = P^(s) a^(s,*)
```

The architectural invariant is more important than this exact equation:

```text
low activation may become dormant
but dormant state remains recoverable
```

A recurrent serious-candidate stage may then update support as a function of the current candidate state and candidate-to-candidate relations. The exact recurrence operator is **not currently considered externally validated**.

---

## 9. Designed Cognitive Physics vs Learned Cognitive Skill

Ground 0 continues to separate what developers define from what the organism should learn.

### Designed cognitive physics may define

```text
state and candidate schemas
valid cognitive operations
reversible suppression semantics
recurrent-transition interface
compute/safety ceilings
provenance
checkpoint formats
commit / abstain / seek / reopen interfaces
```

### Learned cognitive skill should increasingly determine

```text
which context matters
which context to evaluate next
stage ordering
stage gain / selectivity
candidate-region preference
when recurrence is worth more compute
when evidence is sufficient
when to seek evidence
when to reopen
when to stop
```

The principle remains:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

But mechanisms should only remain in Ground 0 if they continue to earn their role under stronger controls.

---

## 10. EXT-1: First External Falsification Gate

EXT-1 asks:

> **Does reversible ordered tapering plus recurrent deliberation earn its cost on a public benchmark against published baselines, under answer-independent relations and symmetric cost accounting?**

Primary dataset: **BEIR SciFact**.  
Secondary preregistered dataset: **BEIR NFCorpus**.

EXT-1 tests three independent claims.

### C1 — Staged narrowing

Can the learned reversible cascade beat BM25, remain close to a full cached rerank, and use substantially fewer measured feature evaluations?

### C2 — Reopening

When an under-specified cue suppresses the relevant document, can retained dormant state recover it more often than hard deletion?

The candidate field is retrieved from the full query for both conditions; only starting activation is misled. This intentionally isolates the taper from the retriever.

### C3 — Commitment

Does explicit abstention improve precision relative to forced argmax while also abstaining appropriately when the candidate field contains no relevant document?

The complete frozen protocol is in:

```text
docs/EXT1_PREREGISTRATION.md
```

Synthetic smoke runs are explicitly barred from producing an evidence verdict.

---

## 11. Current Mechanistic Status

### 11.1 Reversible soft suppression

```text
STATUS:
STRONG SYNTHETIC SUPPORT
EXTERNAL TEST PENDING EXT-1 C2
```

HCT-1 and HCT-2 repeatedly showed a difference between soft reversible suppression and hard deletion under constructed context reversal. EXT-1 asks whether that distinction earns value on external retrieval data.

### 11.2 Learned context ordering

```text
STATUS:
HCT-2 HISTORICAL EFFICIENCY RESULT
CLEAN CAUSAL INTERPRETATION NOT ESTABLISHED
EXT-1 C1 PENDING
```

The HCT-2 5.49% figure remains a historical observation, but the order was not sufficiently independent from the synthetic hierarchy.

### 11.3 Efficiency

```text
STATUS:
HCT-2 REPORTED LARGE SAVINGS
ORIGINAL GENERIC CONTROL COST WAS INFLATED BY RECOMPUTATION
MEASURED EXTERNAL COST PENDING EXT-1 C1
```

Neither the old 7.14% context-evaluation ratio nor the configured 3.125% recurrent-load ratio should now be presented as proof of real computational advantage.

### 11.4 Recurrence ablation — pending EXT-1

The HCT-2 no-recurrence ablation remains one of the most striking internal observations:

```text
with recurrence:       100% good behavior
without recurrence:     45% good behavior
correct survival:      100% in both
```

Before the code review, this was interpreted as strong evidence that tapering preserved the candidate while recurrence performed essential downstream relational work.

That interpretation is now **provisional**. HCT-2's candidate relation graph contained correctness-dependent structure, so the recurrent stage was not isolated from hidden-answer information strongly enough to support a clean causal claim.

The revised statement is:

> **HCT-2 observed a large recurrence ablation effect inside its synthetic family, but EXT-1 must determine whether answer-independent recurrence contributes value on external data.**

EXT-1 constructs relations from document/document overlap without qrels and directly includes `learned_order_no_recurrence` as a matched downstream ablation.

```text
STATUS:
HCT-2 INTERNAL EFFECT: LARGE
MECHANISTIC INTERPRETATION: PENDING EXT-1
```

### 11.5 Learned resistance

```text
STATUS:
OPTIONAL / TASK-DEPENDENT
```

Its early result remains interesting, but HCT-2 did not require it. EXT-1 does not need resistance to rescue Ground 0.

### 11.6 Commitment / abstention

```text
STATUS:
SYNTHETIC SUPPORT
EXTERNAL CALIBRATION PENDING EXT-1 C3
```

The principle that `winner != knowledge` remains architecturally important, but the value of the current commitment mechanism must transfer outside synthetic unresolved worlds.

---

## 12. Current Ground 0 After the Review

The current architecture remains a hypothesis worth testing:

```text
large field
    ↓
learned routing
    ↓
reversible contextual taper
    ↓
serious-candidate field
    ↓
state-dependent recurrence       ← provisional pending external ablation
    ↓
evidence / uncertainty
    ↓
commit | abstain | seek | reopen
```

What changed in Revision 4 is the **confidence level**, not the goal.

### Most defensible current principles

```text
Do not delete alternatives merely because they are currently weak.
Do not use elapsed cycles as evidence for pruning.
Keep ranking separate from commitment.
Measure compute rather than infer it from configured widths.
Use controls that receive equal information and equal caching opportunities.
Keep hidden truth entirely outside inference structures.
Require mechanisms to transfer outside worlds designed around them.
```

### Claims now explicitly pending EXT-1

```text
reversible tapering has real external recovery value
ordered tapering earns measured external compute savings
learned order contributes beyond fixed order
answer-independent recurrence materially improves external behavior
explicit abstention improves external calibration
```

---

## 13. Scientific Boundaries

HCT-1 and HCT-2 are controlled synthetic experiments. Their results do not establish:

- biological hippocampal equivalence;
- a new mathematical law;
- natural-language understanding;
- semantic representation learning;
- general intelligence;
- superiority to transformers, attention, mixture-of-experts, dense retrieval, late-interaction retrieval, or associative-memory systems;
- end-to-end wall-clock superiority;
- production integration.

EXT-1, even if successful, would remain narrow: one external retrieval setting using four hand-designed feature channels.

The purpose of EXT-1 is not to prove Synrheon generally. It is to determine whether the central process survives its **first test outside a world written around itself**.

---

## 14. Continuation Protocol

Repository:

```text
Logancarton/Synrheon
```

Historical synthetic research branch:

```text
experiment/hippocampal-sparse-settling
```

Current external-validation branch:

```text
experiment/external-retrieval-cascade
```

Primary EXT-1 files:

```text
experiments/external_retrieval_cascade.py
tests/test_external_retrieval_cascade.py
docs/EXT1_PREREGISTRATION.md
```

Required order:

```text
1. freeze implementation + preregistration
2. run integrity tests
3. run synthetic smoke check — NOT EVIDENCE
4. run SciFact development split only
5. inspect mechanics, baseline anchor, and test integrity
6. freeze any pre-final correction as a new version if material
7. run untouched SciFact final split once
8. interpret C1 / C2 / C3 independently
9. do not tune EXT-1 after final inspection
```

If SciFact provides fewer than 30 paired C2 suppression cases, C2 is inconclusive under EXT-1. NFCorpus was declared secondary before the primary final run and may provide an additional external test, but it must not be used to retroactively turn a failed SciFact criterion into a pass.

HCT-3 synthetic generalization is no longer the immediate next scientific gate. **EXT-1 comes first.** What should be tested after EXT-1 depends on what survives.

---

## 15. Research Principle

The program should prefer a mechanism that survives hostile testing over a beautiful theory protected by its own benchmark.

A negative EXT-1 result is useful evidence. If C1 fails, simplify the efficiency claim. If C2 fails, reconsider whether reopening provides value outside constructed reversal worlds. If C3 fails, redesign commitment rather than lowering the threshold. If recurrence adds no value once the relation graph is answer-independent, remove or constrain the recurrence claim.

The objective is not to make Ground 0 win.

> **The objective is to discover which parts of Ground 0 continue to deserve being built.**
