# Synrheon Development UI

The UI is Synrheon's development microscope and control surface. Stage 0B remains the verified frontend/backend/runtime foundation; Stage 1 now adds observable substrate state without moving cognition into JavaScript.

Current views:

```text
Chat
Internal Thought
Knowledge
```

## Chat

Chat sends external user stimuli through the real Python boundary. Each accepted Chat stimulus now also becomes an autobiographical `ExperienceEvent` with `origin = observed`, an episode-relative sequence number, and before/after linkage.

No fake conversational reply is generated.

## Internal Thought

Internal Thought sends explicit injections through `/api/thought`. Those events become `origin = injected`, not self-generated thought.

The view now displays the ordered current-episode experience thread together with runtime trace so the developer can inspect:

- experience sequence
- observed vs injected provenance
- previous/next event linkage
- elapsed episode time
- runtime trace

This is an observable memory thread, not durable memory across process restart.

## Knowledge

The Knowledge tab provides explicit developer injection for the first Stage 1 substrate:

- concepts
- world relations
- organism/self relations

World and self relations are stored separately. Injected self relations remain marked `origin = injected`; they are not relabeled as learned.

The current substrate snapshot is visible in the same tab.

## Controls

```text
Start
Think One Step
Continue
Pause
```

All controls call Python. JavaScript does not own the organism state transition.

## Inspector

The right-side inspector shows status, cycle, trace-event count, experience count, concept count, and the complete backend state snapshot.

## Boundary Rule

The UI controls, injects explicit developer scaffolding, and observes.

It must not own semantic interpretation, sparse activation, retrieval, durable memory, learning, abstraction, or problem solving.
