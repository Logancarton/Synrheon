# R0-SR1D Amendment 1 — Evidence Classification Correction

**Applies to:** `R0_EXACT_MATCH_ENVELOPE.md` / `r0-exact-match-envelope-v1`  
**Status:** corrective amendment recorded after the first v1 run  
**Mechanism change:** none

## Correction

R0-SR1D v1 is a **SPECIFICATION / IMPLEMENTATION-INTEGRITY BASELINE**, not a scientific experiment and not evidence for the relational cognition hypothesis.

The frozen scorer is exact symbolic overlap:

```text
score(memory | cue, route) = exact overlap / cue-set size
```

The family-A world also fixes which concepts are unique, which are shared, and the deterministic `memory_id` tie-break. Consequently, the principal v1 outputs are closed-form consequences of the construction and scoring rule. Passing them verifies that the implementation obeys its specification. It does not establish that the mechanism generalizes, learns, or explains cognition.

## No scientific finding

```text
Evidence class:       SPECIFICATION
Scientific finding:   NONE
Engineering value:    frozen null/baseline behavior for future mechanisms
```

The original files and first run remain preserved for provenance. This amendment changes their interpretation, not their historical output.

## Zero-support correction

The v1 documentation described unmatched near-ID and alias conditions as falling to `32 / 128 = 0.25` "chance." That wording is incorrect.

When every candidate has zero support, all scores are tied. The frozen retriever then sorts by `memory_id` and returns the same deterministic first 32 IDs for every zero-support query.

Therefore:

```text
aggregate Hit@32 = 32 / 128 = 0.25
```

because 32 of the 128 possible targets happen to belong to that fixed returned prefix—not because the retriever samples randomly.

The correct name is:

```text
ZERO-SUPPORT DETERMINISTIC PREFIX BASELINE
```

Per-item behavior is deterministic: targets in the fixed prefix always hit; targets outside it always miss.

## Noise correction

The unbound-noise condition is also a specification property, not evidence of realistic noise robustness. Unbound concepts occur in no stored binding, so they contribute zero overlap to every candidate and the common cue denominator rescales all candidates equally. Ranking therefore cannot change.

The bound-wrong-detail condition is the more realistic competitive-noise baseline. Under the exact scorer, the competitor receives more exact overlap than the intended target and therefore wins by construction.

Neither behavior should be described as a discovered cognitive property.

## Identity cliff

Near-ID and unstored-alias conditions remain useful as **failure fixtures** for future learned/similarity mechanisms:

```text
same stored identity     -> exact support can exist
different unstored ID    -> zero exact support
```

But v1 does not experimentally discover that cliff; exact identity discontinuity is inherent in the scorer.

## Corrected executable report

Use:

```bash
python3 -m experiments.r0_exact_match_envelope_v2
```

The v2 reporting wrapper leaves the v1 scorer and generated world unchanged while:

- classifying the artifact as `SPECIFICATION`;
- reporting `scientific_finding: NONE`;
- renaming alias/near-ID aggregate rates as deterministic zero-support-prefix rates;
- explicitly measuring that all zero-support cues return one query-invariant field per route;
- preserving the v1 numbers as implementation baseline data.

## Advancement rule

Future work may use these values only as regression/null baselines. A scientific experiment must contain an outcome that is not fixed by the construction and scoring rule. Any learned-route experiment must continue to carry an identity-transfer/alias condition so that exact-ID success cannot substitute for relational generalization.
