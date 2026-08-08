# Synrheon Development UI

The UI is Synrheon's development microscope and control surface.

Stage 0B now provides a connected modern application with two main views:

```text
Chat
Internal Thought
```

## Chat

Chat sends external user stimuli through:

```text
browser
 ↓
POST /api/stimulus
 ↓
interfaces.py
 ↓
runtime.py
 ↓
Synrheon-owned state
```

Stage 0B does not generate fake replies.

## Internal Thought

This tab displays observable runtime trace and explicit thought injections.

Injected thoughts travel through a distinct `/api/thought` boundary so they are not confused with user chat.

Later cognitive owners can publish structured internal state here, including activation, retrieval, scratchpad, predictions, uncertainty, learning, and autonomous thought.

## Controls

```text
Start
Think One Step
Continue
Pause
```

All controls call Python. JavaScript does not own the organism state transition.

## Inspector

The right-side inspector shows:

- status
- cycle
- event count
- input count
- complete current state snapshot

The browser polls the backend so continued runtime cycles remain visible.

## Boundary Rule

The UI controls and observes.

It must not own cognitive interpretation, memory, retrieval, learning, abstraction, or problem solving.
