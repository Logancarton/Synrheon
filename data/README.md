# Synrheon Data

Keep durable/generated experiment evidence visibly separate from production cognition.

Current files:

```text
data/tiny_world.json
    human-readable debug / UI fixture only
    never E011 training data
    never E011 transfer evidence

data/e011a_v1_evidence.json
    immutable controlled E011-A v1 five-seed result summary
    includes model lineage, parameter checksums, learned weights, baselines,
    transfer/renaming results, cognitive-cost evidence, and the frozen numeric gate
```

The E011 generator/scorer itself lives outside production cognition in
`experiments/e011a.py`. Hidden generated-world truth must never be read by
`src/synrheon/cognition.py`.

Suggested future layout, created only when needed:

```text
data/
├── fixtures/
├── schemas/
├── runtime/       # ignored
├── checkpoints/   # ignored
└── cache/         # ignored
```

Do not create deeper directories until a live mechanism actually needs them.
