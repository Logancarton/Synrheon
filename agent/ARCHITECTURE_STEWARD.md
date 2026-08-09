# Synrheon Architecture Steward

## Canonical Repository

```text
https://github.com/Logancarton/Synrheon
```

Repository: `Logancarton/Synrheon`

Default branch: `main`

Do not ask the user which repository Synrheon belongs in.

When working locally, verify `origin` points to the canonical repository before pushing. If no origin exists and the tree is clearly Synrheon, add it. If origin points elsewhere, stop before push and report the mismatch.

# Primary Development Principle

Synrheon is developed bottom-up with explicit ownership, explicit state, controlled learning evidence, and observable live behavior.

Stage 0B — the runtime/UI organism — is **Verified**.

E011-A v1 — the first controlled trainable-cognition experiment — is now **Built** and its frozen five-seed Level-1 numeric gate passed.

That is genuine controlled cognitive evidence, but it is not live integration.

The active target is now **E011-B — Live Organism Integration**:

```text
recorded E011-A artifact
        ↓
legitimate live CognitiveState
        ↓
cognition.py
learned operation + target
        ↓
bounded checkpoint
        ↓
thin runtime sequencing
        ↓
OrganismState / trace
        ↓
Organism UI
```

The hidden E011 generator/scorer remains outside production cognition.

# Startup Sequence

Before material work, read and reconcile:

```text
README.md
docs/SCAFFOLD.md
docs/ARCHITECTURE_PLAN.md
docs/IMPLEMENTATION_STATUS.md
docs/CURRENT_STAGE.md
docs/EXPERIMENTS.md
docs/SIGNAL_FLOW.md
```

Read `docs/PROJECT_GUIDE.md` for the human-readable project map.

Then follow:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

Only after the affected ownership/signal path is understood should implementation begin.

# Status Vocabulary

Use:

- **Not Started** — no meaningful implementation exists.
- **Designed** — architecture/experiment contract is defined.
- **Built** — mechanism exists and works in isolation/controlled assay.
- **Integrated** — the live runtime reaches and uses it.
- **Verified** — intended live behavior was demonstrated through the running organism with relevant state/trace inspected.

Keep cognitive effect separate:

- **Infrastructure**
- **Supporting cognition**
- **Cognitive improvement**

A controlled E011-A result may be real cognitive improvement while remaining only `Built`.

# Broad-to-Narrow Review

For every proposed behavior or repair, identify:

1. **Cognitive objective** — what capability should Synrheon gain?
2. **Current bottleneck** — what mechanism prevents it?
3. **Affected signal path** — which state/owners/runtime/UI/learning paths are involved?
4. **Information boundary** — what may the mechanism know, and what must stay hidden?
5. **Correct owner** — where does the decision actually belong?
6. **Runtime role** — what should runtime only sequence/route?
7. **Failure modes** — what would create brittleness, hidden leakage, or duplicate authority?
8. **Evidence** — what controlled/live result would prove or falsify it?

Do not start with:

- stimulus-specific patches;
- phrase-specific rules;
- arbitrary score changes;
- scripted answers;
- test-only behavior;
- UI-side cognitive shortcuts;
- hand-written target selectors.

Prefer changes that improve the underlying process.

# E011-A Frozen Evidence Boundary

The recorded result is:

```text
data/e011a_v1_evidence.json
```

The controlled hidden harness is:

```text
experiments/e011a.py
```

Production policy/learning owners are:

```text
src/synrheon/cognition.py
src/synrheon/learning.py
```

Do not retune E011-A v1 against the already-inspected final seeds.

A material model/state/action/reward/generator change requires a new experiment version and fresh untouched final split.

The policy must never receive:

```text
unrevealed graph
hidden goal location
shortest path
shortest-path distance
on-solution-path truth
correct next action / target
future frontier
solver / scorer output
world seed as a clue
```

# E011-B Architecture Gate

E011-B must integrate the **learned policy**, not the benchmark environment.

Before coding, identify a legitimate live state source that can produce the policy-visible state without hidden benchmark truth.

Do not:

- import `experiments.e011a` into runtime;
- generate a hidden benchmark world in production;
- put model ranking logic in runtime;
- let UI choose targets;
- use a compatibility shim that hides a wrong owner;
- pretend static controlled metrics mean the policy is live.

E011-B must prove:

1. one exact recorded policy artifact loads;
2. live state reaches `cognition.py`;
3. `cognition.py` selects operation + target;
4. one bounded state transition/checkpoint occurs;
5. runtime only sequences;
6. state/trace expose the action/checkpoint;
7. UI can show the live mechanism separately from historical learning evidence;
8. malformed state fails safely;
9. unrelated state is not mutated;
10. hidden experiment truth never enters production cognition.

# Runtime Principle

`src/synrheon/runtime.py` is a thin active integration layer.

Runtime may:

- sequence owners;
- route typed handoffs;
- invoke live mechanisms;
- return outcomes/feedback;
- expose state/trace.

Runtime must not:

- own cognition;
- rank candidate actions/targets;
- duplicate memory/retrieval/learning;
- contain large experiment mechanisms;
- contain hidden solver truth.

# UI Principle

The UI is a microscope and behavioral lab.

It should show:

```text
what is integrated
+
what the integrated mechanism is doing now
+
backend-owned evidence of learning/generalization over time
```

Controlled E011-A metrics may appear as historical growth evidence.

They must remain clearly separate from E011-B live cognition status.

The UI must not choose actions or calculate the scientific pass gate.

# Tests

Prefer a small number of high-value behavioral tests proving:

- the intended owner is reached;
- valid input yields intended behavior;
- malformed/mismatched input fails safely;
- unrelated state is not mutated;
- feedback reaches the correct owner;
- no duplicate subsystem or hidden shortcut exists;
- live integration reaches the real runtime when `Integrated` is claimed.

Automated tests do not independently grant `Verified`.

# Documentation Synchronization

After meaningful work, update only affected truth:

- `docs/IMPLEMENTATION_STATUS.md`
- `docs/CURRENT_STAGE.md`
- `docs/ARCHITECTURE_PLAN.md`
- `docs/DECISIONS.md`
- `docs/EXPERIMENTS.md`
- `docs/SCAFFOLD.md`
- `docs/SIGNAL_FLOW.md`
- `docs/PROJECT_GUIDE.md`

Documentation must describe implemented/tested truth, not hoped-for cognition.

# Git Safety

Never use:

```powershell
git add .
git clean
git reset --hard
```

Prefer:

```powershell
git status --short -- Synrheon
git diff --check -- Synrheon
git diff -- Synrheon
```

Stage every changed file explicitly.

After relevant gates pass, create a focused reversible commit and push the active branch unless explicitly told not to.

# Completion Review

Before declaring a stage complete, confirm:

- behavior is in the correct owner;
- runtime remains thin;
- hidden experiment truth is quarantined;
- live path reaches the mechanism if integration is claimed;
- tests prove behavior, not structure only;
- UI remains observational;
- no parallel subsystem exists;
- no world-specific route was added;
- cognitive maturity is described accurately;
- docs match implemented truth.
