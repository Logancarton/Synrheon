---
name: synrheon-development-workflow
description: Use proactively for Synrheon architecture, UI/runtime organism setup, cognitive implementation, repair, experimentation, live-behavior testing, stage work, learning, memory, retrieval, abstraction, autonomy, or documentation synchronization. Work broad-to-narrow, prove cognition through the running organism, and treat automated tests as regression support rather than the sole proof of behavior.
---

# Synrheon Development Workflow

This is the canonical repo-local execution workflow for Synrheon.

It owns the procedure for architecture review, implementation, live-organism proof, test support, cleanup, documentation synchronization, Git hygiene, commit, and push.

Tool-specific adapters may translate commands or invocation details, but they must not restate or override this workflow.

## Canonical Repository

Always treat the following repository as Synrheon's canonical destination:

```text
Repository: https://github.com/Logancarton/Synrheon
Full name:  Logancarton/Synrheon
Branch:     main
Clone:      https://github.com/Logancarton/Synrheon.git
```

Do not ask the user which repository to use.

Before pushing from a local checkout:
- verify `origin` points to the canonical repository
- if no origin exists and the working tree is clearly Synrheon, add the canonical repository as `origin`
- if origin points somewhere else, stop before push and report the mismatch

## Core Doctrine

Synrheon is not built by accumulating stimulus-specific fixes.

Use this development path:

```text
current project truth
        ↓
broad cognitive objective
        ↓
underlying bottleneck
        ↓
candidate mechanisms
        ↓
architecture decision
        ↓
correct owner
        ↓
pre-registered live experiment
        ↓
implementation
        ↓
real runtime wiring
        ↓
UI / trace observation
        ↓
outcome
        ↓
learning from success or failure
        ↓
documentation truth
```

The goal is not the smallest diff.

The goal is the smallest coherent architectural change that improves the organism without introducing duplicate authority.

## Live Organism Comes First

Synrheon should obtain a running runtime and development UI before sophisticated cognition is added.

The live UI/runtime is the primary cognitive laboratory.

Automated tests are supporting evidence and regression protection.

They are not sufficient proof that a cognitive capability works.

The first live organism should support, at minimum:

```text
Start
Send Stimulus
Think One Step
Continue
Pause
Inspect Current State
Inspect Trace
```

As later systems are built, the same UI should expose:
- active concepts / activation
- computational time
- event sequence
- memory state
- Level 1 → Level 2 → Level 3 retrieval
- scratchpad contents
- problem / trial / prediction / outcome
- learning updates
- consolidation / abstraction
- autonomous continuation

Do not place cognition in the UI to make a demonstration appear successful.

The UI observes and controls the organism.

The cognitive owners produce the behavior.

## Project Truth Owners

Read in this order before material work:

```text
README.md
        ↓
docs/SCAFFOLD.md
        ↓
docs/ARCHITECTURE_PLAN.md
        ↓
docs/IMPLEMENTATION_STATUS.md
        ↓
docs/CURRENT_STAGE.md
        ↓
affected production owners
        ↓
relevant tests / experiments
```

Also read:
- `docs/SIGNAL_FLOW.md` whenever runtime wiring, UI handoffs, cognitive-owner sequencing, feedback, or live signal paths are involved
- `docs/PROJECT_GUIDE.md` when changing a file's meaningful responsibility or internal structure so the human-readable guide can remain accurate
- `docs/DECISIONS.md` when prior architecture choices constrain the work
- `docs/EXPERIMENTS.md` when a hypothesis or prior live observation is relevant
- `docs/RESEARCH.md` only when outside mechanisms or donor ideas are being considered

Do not confuse research notes with implemented truth.

## Status Rules

Use:

```text
Not Started
Designed
Built
Integrated
Verified
```

Definitions:

- `Not Started`: no meaningful implementation.
- `Designed`: intended mechanism is defined.
- `Built`: implementation exists and works in isolation.
- `Integrated`: the real runtime reaches and uses it.
- `Verified`: the intended behavior has been demonstrated through the running organism and the relevant state/trace was inspected.

Automated tests alone cannot produce `Verified`.

Also classify cognitive effect separately:

```text
Infrastructure
Supporting cognition
Cognitive improvement
```

This prevents a large amount of engineering work from being misrepresented as smarter cognition.

# Standard Workflow

## 0. Confirm project and preserve current work

Before editing:
- confirm the worktree is Synrheon
- record current branch and HEAD
- inspect `git status --short`
- inspect recent history
- preserve unrelated or pre-existing dirty work
- never use destructive cleanup to make the tree appear clean

If the local repository does not have the canonical GitHub remote, handle it according to the Canonical Repository section above.

## 1. Read current project truth

Read:
- `README.md`
- `docs/SCAFFOLD.md`
- `docs/ARCHITECTURE_PLAN.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/CURRENT_STAGE.md`

Then inspect only the production owners and tests relevant to the active work.

Update documentation first if the written architecture clearly disagrees with reality.

## 2. Run the architecture gate

Before choosing code, state:

1. What capability are we trying to create?
2. Why is it the correct bottom-up capability to address now?
3. What broad bottleneck prevents it?
4. What candidate mechanisms could solve it?
5. What later systems will depend on this choice?
6. What owner or coordinated set of owners should hold it?
7. What could go wrong?
8. What live observation would prove or falsify it?

If these cannot be answered coherently, do not code yet.

## 3. Pre-register the live experiment

Before editing, define:

```text
real stimulus or action
baseline live behavior
expected post-change behavior
internal state / trace to inspect
what must remain unchanged
what result means failure
```

Prefer a real UI/runtime stimulus over a synthetic test-only call whenever the organism can already run.

Do not move the success criteria after seeing the result.

## 4. Observe the baseline in the running organism

When a runnable organism exists:
- start Synrheon through the supported entry point
- use the UI or runtime control surface
- apply the pre-registered stimulus
- inspect the visible output
- inspect relevant internal state / trace
- record what actually happened

If the organism cannot yet run, the active work should generally remain focused on the observable runtime/UI foundation unless the user explicitly directs otherwise.

## 5. Inspect the full affected signal path

Before implementation, inspect:

```text
input / internal trigger
        ↓
runtime sequencing
        ↓
correct cognitive owner
        ↓
state transition
        ↓
observable trace / UI
        ↓
outcome / feedback
```

When later systems exist, also trace any relevant:
- memory access
- retrieval cascade
- scratchpad mutation
- prediction
- problem-solving state
- learning effect
- consolidation effect

Do not solve a local symptom before finding the correct owner.

## 6. Evaluate candidate mechanisms

Compare reasonable approaches before coding.

Consider:
- cognitive generality
- mathematical adaptability
- sparse activation compatibility
- temporal compatibility
- future trainability
- memory / retrieval interaction
- failure containment
- computational cost
- interpretability / observability
- risk of duplicate authority

Use prior Sonara code, papers, repositories, or other systems as research evidence when useful.

Do not transplant old package structures or authority boundaries merely because they already exist.

## 7. Implement in the correct owner

Prefer the existing owner when it can cleanly hold the mechanism.

Create a new production file only when no existing owner can represent the responsibility coherently.

Keep the early codebase understandable:
- one major cognitive owner per file
- split into packages only when real complexity justifies it
- keep runtime thin
- keep UI observational
- keep tests outside production

Do not add:
- phrase-specific cognition
- fake success flags
- test-only production branches
- scripted answers
- parallel planners
- parallel memory stores
- duplicate learning paths
- UI-side cognitive logic

## 8. Wire through the live runtime and UI

A cognitive mechanism is not Integrated until the real runtime reaches it.

When the mechanism changes internal state, expose the relevant observation through the development UI or trace when practical.

The desired path is:

```text
mechanism
   ↓
correct owner state changes
   ↓
runtime reaches owner
   ↓
UI / trace exposes result
   ↓
real stimulus demonstrates behavior
```

## 9. Run the live organism before declaring success

Run the same pre-registered stimulus again.

Inspect:
- visible behavior
- current state
- state transition
- relevant trace
- unexpected mutation
- whether the mechanism generalized beyond a test fixture

If the result differs from expectation, diagnose the organism before changing the acceptance criterion.

## 10. Add the minimum high-value automated tests

After or alongside live proof, add tests that preserve the discovered contract.

Prefer a small number of tests proving:
- valid behavior
- safe malformed / mismatched behavior
- correct owner state change
- live runtime reachability when feasible
- unrelated state remains unchanged
- feedback reaches the correct learning owner when relevant

Do not create large batteries of object-construction, getter, or duplicate wording tests.

Passing tests do not replace the live experiment.

## 11. Diagnose failed work rather than patching around it

If the live proof fails:
- trace the actual state transition
- identify whether the failure is architecture, wiring, representation, runtime sequencing, or observation
- repair the same mechanism only when the architecture still appears sound
- do not add a special-case stimulus patch to make the experiment pass

If the mechanism itself is disproven:
- remove the failed production path
- remove implementation-specific tests that no longer represent a real contract
- preserve useful experimental evidence in `docs/EXPERIMENTS.md`
- update architecture / decisions honestly
- leave no partial behavior represented as Integrated or Verified

A failed experiment is useful evidence.

## 12. Run verification gates

After live behavior is correct:
- run focused tests
- run the full active test suite when the change affects broad cognition/runtime/state
- compile
- run `git diff --check`
- inspect the complete Synrheon diff
- inspect `git status --short`
- run the live organism again if any cleanup or integration change occurred after the prior live proof

The most important gate remains the actual organism behavior.

## 13. Synchronize project truth

Update only what changed:

- `docs/ARCHITECTURE_PLAN.md` — intended architecture
- `docs/IMPLEMENTATION_STATUS.md` — implemented/live/verified truth
- `docs/CURRENT_STAGE.md` — active work and immediate next boundary
- `docs/DECISIONS.md` — durable architectural decisions
- `docs/EXPERIMENTS.md` — preregistered stimulus, observation, failure/success, interpretation
- `docs/RESEARCH.md` — research evidence that is not yet adopted architecture
- `docs/SCAFFOLD.md` — repository structure and ownership map
- `docs/SIGNAL_FLOW.md` — current real signal path plus clearly labeled planned flow
- `docs/PROJECT_GUIDE.md` — plain-English explanation of files and meaningful classes/functions/sections for a non-programmer

Do not let documentation claim cognition that the UI/runtime has not demonstrated.

## 14. Review the whole change as one organism

Before completion, confirm:
- behavior is in the correct owner
- runtime remains thin
- UI remains observational
- the real path reaches the mechanism
- no duplicate subsystem exists
- tests preserve behavior rather than manufacture it
- documentation matches reality
- cognitive effect is described honestly
- no unrelated files are included

## 15. Commit and push verified work

After the relevant gates pass:
- stage each intended file explicitly
- never use `git add .` or `git add -A`
- create a focused reversible commit
- push the active branch to the canonical Synrheon repository

Do not:
- force push
- amend without explicit direction
- rewrite history
- commit failed or partial work as complete
- include unrelated files

# Definition of Done

A bounded Synrheon change is complete only when:

- [ ] Current project truth was read first.
- [ ] The architecture gate identified the real bottleneck and owner.
- [ ] A live experiment was defined before implementation.
- [ ] Baseline behavior was observed through the running organism when available.
- [ ] Implementation lives in the correct cognitive owner.
- [ ] Runtime wiring reaches it.
- [ ] UI/trace makes the relevant state observable when practical.
- [ ] The same real stimulus was used after implementation.
- [ ] The observed organism behavior matches the intended mechanism.
- [ ] High-value automated tests protect the resulting contract.
- [ ] Full relevant tests and compilation pass.
- [ ] `git diff --check` passes.
- [ ] Complete diff and status were reviewed.
- [ ] Documentation states implemented truth.
- [ ] Implementation status is not overstated.
- [ ] Cognitive effect is classified honestly.
- [ ] Completed verified work is committed and pushed to `Logancarton/Synrheon`.

# Current Priority

Until the observable organism exists, prioritize:

```text
minimal runtime
      +
development UI
      +
step / continue / pause controls
      +
state / trace visibility
      ↓
RUNNING TEST ORGANISM
```

Only then should deeper cognitive stages be evaluated primarily through that live organism.

This foundation is infrastructure, not cognition.

Its value is that every later cognitive mechanism can be tested as actual behavior rather than inferred from pass/fail assertions.
