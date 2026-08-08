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
- injected organism relations

World knowledge, injected organism state, self-learned organism state, and current activation are separate backend representations.

The Self Relation form uses a free-text **Relation type** field. The UI does not provide a fixed dropdown or an allowed ontology. A relation such as `protective_of` can be injected without changing production code.

The form writes only the injected organism-relation collection. There is intentionally no control that lets a developer directly label data as self-learned. Learned organism relations can only be changed by the learning mechanism when trusted experience evidence exists.

The substrate JSON displays injected and learned relation collections separately so their provenance remains inspectable.

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

It must not own semantic interpretation, relation discovery, sparse activation, retrieval, durable memory, learning, abstraction, or problem solving.
