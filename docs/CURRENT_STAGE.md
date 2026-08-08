# Current Stage

## Active Stage

**Stage 0B — Observable Organism Harness**

## Current Goal

Create the first running Synrheon development organism before implementing deeper cognitive stages.

The organism should provide a thin runtime and a development UI capable of:

```text
Start
Send Stimulus
Think One Step
Continue
Pause
Inspect Current State
Inspect Trace
```

The first version does not need sophisticated cognition.

Its purpose is to establish the live observation and testing path that every later cognitive mechanism will use.

## Why This Comes First

Automated pass/fail tests can prove that code paths behave as asserted while still failing to demonstrate that Synrheon functions coherently as one organism.

The live runtime/UI therefore becomes the primary laboratory.

Later cognitive stages should be tested by:

```text
real stimulus
    ↓
live runtime
    ↓
actual owner state change
    ↓
observable UI / trace
    ↓
real outcome
```

Automated tests preserve contracts after the real behavior is understood.

## Architecture Boundary

This stage is **Infrastructure**.

It should not be described as cognitive improvement.

The UI observes and controls Synrheon.

The runtime sequences owners.

Neither should become the primary owner of cognition.

## Exit Condition

Stage 0B is complete when a developer can start Synrheon, apply a stimulus, advance cognition one step at a time or continuously, pause it, and inspect the organism's current state and trace through the supported development surface.

Verification must include actually running the organism, not only tests.
