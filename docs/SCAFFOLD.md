# Synrheon Scaffold

This is the compact structural map for the active repository.

Rule:

> **A planned capability does not earn a source file until real implementation exists.**

## Active Production Source

```text
src/synrheon/
├── __init__.py
├── __main__.py
├── state.py
├── cognition.py
├── policy.py
├── policy_learning.py
├── learning.py          # temporary E011-A compatibility export only
├── experience.py
├── temporal.py
├── runtime.py
└── dev_server.py
```

## Ownership

```text
state.py
    explicit organism/substrate state

cognition.py
    Ground 0 cognitive-cycle/checkpoint owner

policy.py
    retained E011-A trainable operation/target policy

policy_learning.py
    retained E011-A outcome-driven policy learning

learning.py
    temporary compatibility shim for frozen E011-A imports

experience.py
    ordered current-episode autobiographical experience

temporal.py
    episode/time/sequence coordinates

runtime.py
    thin sequencing only

dev_server.py
    local browser/API transport only
```

## Ground 0

```text
large candidate field
    ↓
learned routing
    ↓
ordered reversible taper
    ↓
small serious-candidate field
    ↓
state-dependent recurrence
    ↓
evidence / uncertainty
    ↓
commit | abstain | seek evidence | reopen
```

Ground 0 is research-backed but not yet live-integrated.

## Future Capabilities

Durable memory, retrieval, working-state/scratchpad cognition, problem/trial learning, consolidation, abstraction, and autonomy remain in `ARCHITECTURE_PLAN.md` until implementation begins.

Do not recreate empty placeholder modules for them.

## Scientific Separation

```text
src/synrheon/
    production state/process owners only

experiments/
    synthetic generators, hidden truth, scoring, falsification

tests/
    regression and scientific integrity checks

ui/
    observation and control only
```

Hidden experiment truth must never become production cognition input.

## Structural Rule

```text
one clear responsibility
        ↓
one understandable owner
        ↓
real complexity appears
        ↓
split only when justified
```
