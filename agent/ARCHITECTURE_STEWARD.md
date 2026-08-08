# Synrheon Architecture Steward

## Canonical Repository

Synrheon's canonical repository is:

```text
https://github.com/Logancarton/Synrheon
```

Repository full name:

```text
Logancarton/Synrheon
```

Default branch:

```text
main
```

Do not ask the user which repository Synrheon belongs in.

When working locally, verify the repository's `origin` points to the canonical Synrheon repository before pushing.

If no `origin` exists and the working tree is clearly the Synrheon project, add the canonical repository as `origin`.

If `origin` points to a different repository, stop before any push and report the mismatch rather than silently replacing it.

## Primary Development Principle

Synrheon is developed bottom-up, but the development organism must be observable from the beginning.

Before sophisticated cognition is built, establish a running Synrheon runtime and development UI that allow real behavior to be stimulated, stepped, observed, and inspected.

Automated tests are useful regression tools.

They are not sufficient proof that Synrheon actually behaves correctly.

A cognitive capability is not **Verified** merely because unit or integration tests pass. Verification requires observable behavior through the live Synrheon runtime, preferably through the development UI, with the relevant internal state or trace inspected.

The UI is a microscope for cognition.

It must not become the owner of cognition.

## Startup Sequence

Begin by reviewing `README.md` to understand Synrheon’s purpose, cognitive goals, core architectural principles, and development philosophy.

Then review `docs/SCAFFOLD.md` to understand repository structure, file ownership boundaries, and where different kinds of project truth belong. Reconcile it with the actual repository and update it if structure or ownership has materially changed.

Then review `docs/ARCHITECTURE_PLAN.md` against the current codebase and live behavior.

Then review `docs/IMPLEMENTATION_STATUS.md` and reconcile it with what is actually:
- designed
- built
- reachable through the live runtime
- observable in the UI
- verified through real organism behavior

Then review `docs/CURRENT_STAGE.md` so work remains focused on the active bottom-up layer.

When work touches runtime wiring or owner-to-owner handoffs, review `docs/SIGNAL_FLOW.md`.

`docs/PROJECT_GUIDE.md` is the human-facing plain-English code guide. Keep it synchronized when a file gains, loses, or changes a meaningful responsibility, class, function, command, UI control, or major internal section.

Finally, load and follow the canonical repo-local workflow:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

Only after these project truths are understood and synchronized should implementation begin.

## Status Vocabulary

Use these status levels:

- **Not Started** — no meaningful implementation exists.
- **Designed** — architecture or design is defined, but functional implementation does not yet exist.
- **Built** — the mechanism exists and works in isolation.
- **Integrated** — the live Synrheon runtime reaches and uses the mechanism.
- **Verified** — the intended behavior has been demonstrated through the running organism and its relevant state/trace has been inspected. Automated tests alone cannot grant this status.

Keep cognitive effect separate from implementation status:

- **Infrastructure** — enables development, observation, persistence, execution, or tooling but does not itself improve cognition.
- **Supporting cognition** — improves the conditions under which cognition works but does not yet demonstrate a smarter cognitive mechanism.
- **Cognitive improvement** — changes Synrheon’s actual reasoning, retrieval, learning, memory use, abstraction, prediction, or adaptive behavior.

## Broad-to-Narrow Review

For every proposed feature, behavior, or fix, identify:

1. **Cognitive objective** — What capability should Synrheon gain?
2. **Current bottleneck** — What underlying mechanism prevents that capability?
3. **Affected architecture** — Which owners, state, runtime, memory, retrieval, time, learning, UI observation, or signal paths are involved?
4. **Candidate mechanisms** — What reasonable architectural approaches could solve the bottleneck?
5. **System effects** — How would each approach affect the rest of Synrheon?
6. **Failure modes** — What brittleness, instability, duplicate authority, hidden coupling, or fixation could each approach introduce?
7. **Best owner** — Where should the mechanism actually belong?
8. **Live proof** — What real stimulus, runtime state transition, and UI/trace observation would prove the mechanism works?

Prefer changes that improve an underlying mechanism and therefore solve a class of problems.

Do not begin with:
- a stimulus-specific patch
- hardcoded phrase recognition
- a special-case route
- arbitrary score adjustment
- a scripted answer
- a test-only behavior
- a UI-side cognitive shortcut

unless the architecture itself genuinely requires it.

## UI-First / Live-Organism Rule

The first implementation priority is a minimal running organism with a development UI.

The early UI should make it possible to:

```text
start Synrheon
send a stimulus
think one step
continue thinking
pause
inspect current cognitive state
inspect active concepts / activation
inspect temporal state as it is added
inspect retrieval path as it is added
inspect scratchpad state as it is added
inspect problem / trial / outcome state as it is added
```

The UI may initially display empty or minimal panels before later mechanisms exist.

That is acceptable.

The purpose is to give every later cognitive stage a real observation surface.

When implementing a cognitive mechanism, wire it through the real runtime and make the relevant state observable rather than proving it only through a test fixture.

## Runtime Principle

`src/synrheon/runtime.py` is the thin live integration layer.

Runtime may:
- start the organism
- sequence cognitive owners
- route typed handoffs
- accept external stimuli
- trigger one cognitive step
- continue or pause recursion
- expose observable state to the UI
- return outcomes and feedback

Runtime must not:
- become the primary cognition owner
- duplicate memory, retrieval, learning, abstraction, autonomy, or problem-solving logic
- contain large cognitive mechanisms because integration is convenient

## Documentation Synchronization

After meaningful work:
- update `docs/IMPLEMENTATION_STATUS.md`
- update `docs/CURRENT_STAGE.md` when active-stage truth changes
- update `docs/ARCHITECTURE_PLAN.md` when intended architecture changes
- record durable architectural decisions in `docs/DECISIONS.md`
- record real experiment setup and observations in `docs/EXPERIMENTS.md`
- update `docs/SCAFFOLD.md` when repository structure, file placement, or ownership boundaries change
- update `docs/SIGNAL_FLOW.md` whenever the real runtime/UI/owner-to-owner signal path changes
- update `docs/PROJECT_GUIDE.md` whenever meaningful file responsibility or internal code structure changes, keeping explanations understandable to a non-programmer

Documentation must describe observed and implemented truth, not hoped-for behavior.

## Prompt Template Boundary

`docs/PROMPT_TEMPLATES.md` is a human-facing dispatch aid.

It may help the user choose a concise prompt for a type of work.

It is not project truth and does not override:
- this Architecture Steward
- `AGENTS.md`
- `.agents/skills/synrheon-development-workflow/SKILL.md`

Do not require the user to restate canonical workflow rules when a short goal-oriented prompt is sufficient.
