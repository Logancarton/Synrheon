# Synrheon Development UI

The UI is Synrheon's development microscope and control surface. Stage 0B remains the verified frontend/backend/runtime foundation.

The previous hand-written sparse-activation experiment has been removed from production. The UI remains in place so the next trainable cognitive policy can be observed through the same live organism surface.

Current views:

```text
Chat
Internal Thought
Knowledge
```

## Chat

Chat sends external user stimuli through the real Python boundary. Each accepted stimulus becomes an autobiographical `ExperienceEvent(origin="observed")` with sequence/time/provenance.

There is intentionally no fake cognitive activation card and no fake conversational reply while the trainable policy is absent.

## Internal Thought

Internal Thought sends explicit injections through `/api/thought`. Those events remain `origin = injected`, not self-generated thought.

The view displays:
- ordered current-episode experience thread
- runtime trace

A future trainable cognitive policy may add explicit learned state-transition/checkpoint observations here, but JavaScript will not own them.

## Knowledge

The Knowledge tab provides explicit developer scaffolding for:
- concepts
- world relations
- injected organism relations

World knowledge, injected organism state, self-learned organism state, and activation representation remain separate backend state.

The Self Relation form uses a free-text **Relation type** field. The UI does not impose a fixed ontology. It writes only injected organism relations; there is no control that directly manufactures self-learned state.

## Controls

```text
Start
Think One Step
Continue
Pause
```

All controls call Python. `Think One Step` and `Continue` still advance the observable harness cycle only; they do not yet invoke a trainable cognitive policy or autonomous cognition.

## Inspector

The inspector shows status, cycle, trace-event count, experience count, concept count, current activation representation, and the complete backend state snapshot.

## Boundary Rule

The UI controls, injects explicit scaffolding, and observes.

It must not own lexical/semantic interpretation, cognitive-action selection, retrieval, durable memory, learning, abstraction, problem solving, or response generation.
