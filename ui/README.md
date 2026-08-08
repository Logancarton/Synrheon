# Synrheon Development UI

The UI is Synrheon's development microscope and control surface. Stage 0B remains the verified frontend/backend/runtime foundation; Stage 1 adds observable substrate state without moving cognition into JavaScript.

Current views:

```text
Chat
Internal Thought
Knowledge
```

## Chat

Chat sends external user stimuli through the real Python boundary. Each accepted Chat stimulus also becomes an autobiographical `ExperienceEvent` with `origin = observed`, an episode-relative sequence number, and before/after linkage.

No fake conversational reply is generated.

## Internal Thought

Internal Thought sends explicit injections through `/api/thought`. Those events become `origin = injected`, not self-generated thought.

The view displays the ordered current-episode experience thread together with runtime trace, including experience sequence, provenance, previous/next links, and elapsed episode time.

This is an observable memory thread, not durable memory across process restart.

## Knowledge

The Knowledge tab provides explicit developer scaffolding for:

- concepts
- world relations
- injected organism/self relations

World knowledge, injected self state, self-learned state, and current activation are separate backend representations.

The Self Relation form writes only the **injected self vector**. There is intentionally no control that lets a developer directly label data as self-learned. The learned vector can only be changed by the learning mechanism when trusted experience evidence exists.

The current substrate JSON displays both injected and learned self sections so their separation remains inspectable.

## Controls

```text
Start
Think One Step
Continue
Pause
```

All controls call Python. JavaScript does not own organism state transitions.

## Inspector

The right-side inspector shows status, cycle, trace-event count, experience count, concept count, and the complete backend state snapshot.

## Boundary Rule

The UI controls, injects explicit scaffolding, and observes.

It must not own semantic interpretation, sparse activation, retrieval, durable memory, learning, abstraction, or problem solving.
