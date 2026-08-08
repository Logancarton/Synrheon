# Current Stage

## Active Stage

**Stage 0B — Observable Organism Harness**

## Current Goal

Finish verification of the first connected Synrheon development organism before Stage 1 cognition begins.

The repository now contains the intended Stage 0B product shell:

```text
Chat
Internal Thought
Start
Think One Step
Continue
Pause
Current State
Trace
```

The implemented path is:

```text
browser
 ↓
HTTP boundary
 ↓
thin runtime
 ↓
Synrheon-owned session state
 ↓
state change + trace
 ↓
browser
```

Chat input and injected internal thought use distinct runtime channels.

## What Stage 0B Does Not Claim

Stage 0B is **Infrastructure**.

It does not implement:

- semantic understanding
- language response generation
- durable memory
- retrieval
- learning
- abstraction
- problem solving
- autonomous cognition

`Continue` only advances the observable harness cycle until future cognitive owners exist.

## Remaining Exit Condition

Before Stage 0B becomes `Verified`, run the application through the supported local entrypoint and inspect it in the browser:

```powershell
.\scripts\synrheon.ps1 run
```

Verify that:

- the browser opens the Synrheon development application
- Start creates a real session
- Chat sends an external stimulus
- Internal Thought injects a distinct internal stimulus
- Think One Step increments exactly once
- Continue advances cycles
- Pause stops further cycle advancement
- state and trace visibly match those actions

Automated regression tests protect the path but do not replace this live-browser observation.
