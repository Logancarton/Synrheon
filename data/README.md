# Synrheon Data

Keep durable and generated data visibly separate from production code.

Suggested future layout, created only when needed:

```text
data/
├── fixtures/
├── schemas/
├── runtime/       # ignored
├── checkpoints/   # ignored
└── cache/         # ignored
```

Do not create these directories until a live mechanism actually needs them.
