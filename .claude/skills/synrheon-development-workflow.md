---
name: synrheon-development-workflow
description: Use proactively for Synrheon architecture, runtime/UI organism setup, cognition, memory, retrieval, learning, experimentation, repair, and stage work. Load the shared repo-local Synrheon workflow before acting; do not maintain a separate Claude version of its rules.
tools: Read, Edit, Write, Grep, Glob, Bash
model: sonnet
---

# Claude Code Adapter for Synrheon

## Canonical Repository

Synrheon's canonical repository is:

```text
https://github.com/Logancarton/Synrheon
```

Repository:

```text
Logancarton/Synrheon
```

Default branch:

```text
main
```

Do not ask the user which repository Synrheon belongs in.

## Canonical Authority

Before taking material action:

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Read `agent/ARCHITECTURE_STEWARD.md`.
4. Read the canonical workflow completely:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

5. Follow that workflow without restating, weakening, or replacing its rules.

The repo-local canonical workflow:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

is the single shared workflow authority.

This Claude file exists only to:
- make Claude Code discover the workflow
- translate the workflow into Claude Code's available tools
- preserve Claude-specific local artifacts when necessary

Do not maintain a separate Claude version of:
- Synrheon architecture
- stage order
- live-organism verification
- testing requirements
- documentation rules
- Git hygiene
- commit / push policy
- cognitive ownership boundaries

If this adapter conflicts with the canonical workflow, the canonical workflow wins and this adapter should be corrected.

## Current Development Priority

Synrheon is being built bottom-up, but the first implementation priority is the observable organism foundation:

```text
thin runtime
      +
development UI
      +
Start
      +
Send Stimulus
      +
Think One Step
      +
Continue
      +
Pause
      +
State / Trace Inspection
      ↓
RUNNING TEST ORGANISM
```

The UI is a microscope and control surface.

It must not become a cognition owner.

Automated tests are regression support.

They do not replace live-organism verification.

## Claude Tool Translation

Use Claude Code tools to implement the canonical workflow as faithfully as possible:

```text
Read / Grep / Glob
    → inspect repository truth, owners, signal paths, tests, and docs

Edit / Write
    → make bounded architecture-approved changes

Bash
    → run Git inspection, runtime, UI/server commands, tests,
      compilation, verification, and Git hygiene
```

If a required canonical workflow action cannot be performed with available Claude Code capabilities, stop and report the missing capability rather than silently weakening the workflow.

## Local Claude Artifacts

Preserve Claude-specific local artifacts that are not part of Synrheon production behavior.

Do not stage incidental Claude scheduler, cache, session, or local-state files unless the user explicitly requests them or they are intentionally part of repository configuration.
