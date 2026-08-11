# HCT-2 Retrospective Audit — Order and Relation-Alignment Diagnostics

**Synrheon experimental research program**  
**Status: FROZEN AUDIT PROTOCOL before audit outputs are inspected**

## Classification

This is a **retrospective audit of the already-observed HCT-2 v1 synthetic result**. It is not a new confirmatory experiment and cannot upgrade HCT-2 evidence.

HCT-2 v1 remains frozen. This audit must not edit its generator, solver, historical final result, or preregistration.

The purpose is narrower: determine how much of two HCT-2 claims depended on the specific comparators and truth-shaped synthetic structure used by v1.

## Questions

### A — Was the learned context order genuinely exceptional?

HCT-2 compared the learned order with one fixed anonymous order. With four channels there are only 24 possible orders, so the complete order landscape can be measured directly.

Audit all 24 permutations using the **unchanged HCT-2 sparse taper and recurrent solver**.

Report for every order:

```text
order
semantic-depth order (diagnostic only)
good-behavior rate
correct-candidate final survival
mean context-feature evaluations
context-reversal suppression cases
context-reversal reactivation rate
```

Also report:

```text
HCT-2 learned order
original fixed order (0,1,2,3)
unsupervised selectivity order
rank of learned order by evaluation cost among orders with identical good behavior
number of orders with identical good behavior
best/worst/median evaluation cost across all 24 orders
```

No success threshold is attached. The landscape is descriptive because the original HCT-2 result is already known.

### B — Does supervised outcome learning add anything beyond channel selectivity?

Construct a comparison order without using `correct_index` or outcome labels.

For each training world, use the final available cue and calculate, for each channel, the fraction of candidates whose observed context token matches that cue. Average that fraction across training worlds. Channels with fewer matches are more selective.

```text
selectivity(channel) = mean_worlds( matching_candidates / candidate_count )
```

Order channels from lowest matching fraction to highest.

This is not proposed as cognition. It is a diagnostic comparator. If the supervised HCT-2 order is identical to a simple answer-independent selectivity order and offers no measurable advantage over it, the old language about learned semantic-depth recovery should be weakened accordingly.

### C — How dependent was recurrence on answer-aligned relation structure?

Keep the HCT-2 candidate evidence, cues, learned parameters, taper, recurrence width, recurrence cycles, and commitment rule unchanged. Compare the learned-order condition under three relation variants:

```text
ORIGINAL
    original HCT-2 excitation/inhibition graph

NO_RELATIONS
    same world with excitation/inhibition removed

SHIFTED_RELATIONS
    preserve every relation edge and weight but cyclically reassign every endpoint
    by a non-zero seed-determined candidate offset
```

`SHIFTED_RELATIONS` preserves graph topology, degree structure, edge count, and weight multiset while breaking the generator's intended alignment between relation structure and designated candidate roles.

Report:

```text
good-behavior rate
correct rate
commit rate
correct-candidate survival after taper
mean context-feature evaluations
```

No supportive threshold is attached. This audit asks how much the historical recurrence result changes when relation-to-answer alignment is removed; it does not claim that a shifted graph is a realistic world model.

## Important interpretation limits

The following are specification facts, not discoveries:

- hard deletion cannot reopen a deleted candidate when later computation is restricted to survivors;
- opaque renaming cannot alter a solver that never consumes candidate names;
- all 24 order permutations are exhaustively enumerable because HCT-2 has four channels.

The audit must not use those facts as evidence for HCT-2.

The original generator also remains synthetic and self-authored. Even if the learned order ranks first and recurrence degrades under shifted relations, that would only diagnose the historical HCT-2 result. It would not establish external cognitive benefit.

## Data boundary

Default audit evidence is the original HCT-2 development split:

```text
71000-71149
```

A quick smoke mode may use:

```text
71000-71049
```

The historical final split may be rerun only with an explicit `--historical-final` flag. Because its HCT-2 result has already been observed, such a rerun is **retrospective descriptive analysis**, not confirmatory evidence.

## Integrity requirements

The audit is invalid if it:

- changes HCT-2 v1 source behavior;
- changes learned HCT-2 gains, resistance, sparse gate, recurrence width/cycles, or commitment thresholds;
- uses hidden correct identity to construct the unsupervised selectivity order;
- changes candidate evidence or cues in the relation-alignment diagnostic;
- changes relation weights or topology in the shifted-relations condition rather than only relabeling endpoints;
- reports the audit as new confirmatory evidence.

## Advancement

After this audit, HCT-2 should be classified according to what remains defensible:

```text
SPECIFICATION / INVARIANCE
SYNTHETIC GENERATOR-COUPLED DEMONSTRATION
RETROSPECTIVE DIAGNOSTIC SUPPORT
OPEN / UNESTABLISHED
```

A later HCT-2 v2, if justified, must use a new generator family and a new untouched evaluation boundary.