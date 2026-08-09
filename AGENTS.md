# Synrheon Agent Entry Point

Canonical repository:

```text
https://github.com/Logancarton/Synrheon
```

Start by reading `README.md`.

Then read:

```text
agent/ARCHITECTURE_STEWARD.md
```

Then load and follow the canonical workflow:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

Before material implementation, review and reconcile:

```text
docs/SCAFFOLD.md
docs/ARCHITECTURE_PLAN.md
docs/IMPLEMENTATION_STATUS.md
docs/CURRENT_STAGE.md
docs/EXPERIMENTS.md
docs/SIGNAL_FLOW.md
```

Synrheon is developed broad-to-narrow and bottom-up.

Stage 0B — the observable runtime/UI organism — already exists and is **Verified**.

The current implementation priority is:

```text
E011-A v1 controlled process-transfer assay
        ↓
implement the frozen generated task / CognitiveState / EXPAND(target)+STOP policy
        ↓
run the preregistered training + untouched transfer gates
        ↓
classify success/failure honestly
        ↓
only then E011-B live cognition integration
        ↓
cognition.py → thin runtime → state/trace → Organism UI
```

Do not broaden E011-A, change its hidden-information firewall, tune against final held-out seeds, add solver-derived features, or insert a hand-written preferred-target selector to make the experiment pass.

A controlled E011-A result is experimental evidence, not `Integrated`. E011-B is required before the live organism may claim integration.

Automated tests support the work but do not replace live-organism proof once E011-B begins.
