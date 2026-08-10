# D6 Result — Transition Persistence Diagnostic

**Status: completed on SciFact development**  
**Evidence level: external development evidence, not final held-out confirmation**

Frozen protocol:

```text
docs/D6_PREREGISTRATION.md
```

Implementation:

```text
experiments/d6_transition_persistence.py
```

## Observed run

The frozen D6 run was executed on the SciFact development partition after the D6 tests passed locally.

Known result summary from the preserved run output:

```text
development queries:                 93
transition-evaluable queries:        92
reset control integrity:             true
max reset activation diff vs B:      2.220446049250313e-16
reset recovery fraction R_reset:     1.0
split:                               development
synthetic:                           false
frozen verdict:                      MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

The run scope explicitly states:

```text
Development-only transition isolation.
No recurrence.
No final split.
No post-hoc threshold changes permitted.
```

## Frozen interpretation

The preregistered major-support category required the carried-state damage to be reproduced, reset to improve over carry, the paired reset effect to exclude zero on the positive side, and `R_reset >= 0.50`.

The implemented frozen classifier returned:

```text
MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

Therefore the current supported development-level diagnosis is:

> Inappropriate persistence of a state settled under partial context is a major contributor to the measured partial-to-full transition failure in the current SciFact development implementation.

## Architectural consequence

Do not treat a settled activation state as context-free accumulated evidence.

Future context transitions must make the transition mode explicit and test/learn when to:

```text
carry
reset / re-anchor
transform / use residual evidence
reopen
```

D6 does **not** imply that reset is universally correct. It establishes that blind carry is unsafe in the tested transition.

## What D6 does not establish

D6 does not establish:

- that multiple soft contextual stages outperform one soft stage;
- that residual refinement is correct;
- that recurrence should return;
- that the current four channels are useful contextual signals;
- that the reserved final external split would reproduce the result;
- that Synrheon outperforms modern retrieval or language models.

Condition E was exploratory/diagnostic and had no preregistered success threshold. Its query-level behavior was mixed, so do not promote it to the default production transition rule.

## Next scientific gate

D6 unlocks specification of:

```text
MT-1 — Matched-Compute Multi-Taper Falsification
```

MT-1 must be preregistered before result-bearing implementation or threshold selection. Its purpose is to determine whether more than one soft contextual settling stage earns a role after the known carried-state pathology is controlled.

## Raw-output note

The user-run export preserved per-query D6 outcomes and the final diagnostic fields. This repository summary records only values available from that preserved output excerpt. Do not invent missing exact paired-delta or bootstrap-bound values. If a complete raw D6 JSON artifact is later added, treat that artifact as the authoritative numerical record and keep this summary synchronized with it.
