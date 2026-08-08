# Synrheon Development UI

The UI is Synrheon's development microscope and control surface. Stage 0B remains the verified frontend/backend/runtime foundation; the current Stage 1 candidate now exposes real sparse cognitive activation without moving cognition into JavaScript.

Current views:

```text
Chat
Internal Thought
Knowledge
```

## Chat

Chat sends external user stimuli through the real Python boundary. Each accepted stimulus becomes an autobiographical `ExperienceEvent(origin="observed")` and is then routed by runtime into `cognition.py`.

Chat now displays a **Cognitive activation** card after each message:
- matched known concept cue(s)
- bounded sparse active winners and activation values
- an explicit unmatched state when no known concept cue exists

No fake conversational reply is generated. The visible result is the organism's actual activation state.

## Internal Thought

Internal Thought sends explicit injections through `/api/thought`. Those events remain `origin = injected`, not self-generated thought.

The view displays:
- ordered current-episode experience thread
- cognitive activation frames
- recent world/organism activation contributions
- runtime trace

This is inspectable state-transition evidence, not hidden chain-of-thought and not durable memory across process restart.

## Knowledge

The Knowledge tab provides explicit developer scaffolding for:
- concepts
- world relations
- injected organism relations

World knowledge, injected organism state, self-learned organism state, and current activation are separate backend representations.

The Self Relation form uses a free-text **Relation type** field. The UI does not impose a fixed ontology. It writes only injected organism relations; there is no control that directly manufactures self-learned state.

## Controls

```text
Start
Think One Step
Continue
Pause
```

All controls call Python. `Think One Step` and `Continue` still advance the harness cycle only; they do not yet produce stimulus-free autonomous cognition.

## Inspector

The inspector shows status, cycle, trace-event count, experience count, concept count, **active concept count**, and the complete backend state snapshot.

## Boundary Rule

The UI controls, injects explicit scaffolding, and observes.

It must not own lexical/semantic interpretation, sparse activation, relation discovery, retrieval, durable memory, learning, abstraction, problem solving, or response generation.
