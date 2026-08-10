# Current Stage — Revision 6

## Active boundary

Synrheon is now in a **dual-track build/test stage**:

```text
TRACK A — Ground 0 science
D6 COMPLETE
    ↓
MT-1 PREREGISTRATION FROZEN — docs/MT1_PREREGISTRATION.md
    ↓
MT-1 IMPLEMENTATION — immediate scientific boundary

TRACK B — Representation architecture
TD-0/1/2 BUILT
    ↓
TD-3 EXACT SURFACE SEGMENTATION BUILT + INTEGRATED
    ↓
TD-4 KNOWN/UNKNOWN ROUTING BUILT + INTEGRATED
    ↓
TD-5 CONTEXTUAL SENSE EXPERIMENT — immediate boundary; preregister first
```

The old direct E011-B integration path is not the active priority. E011-A remains donor evidence for learned operation selection, not the current architecture target.

## Scientific state

D6 ran on the frozen 93-query SciFact development partition.

Observed:

```text
transition-evaluable queries:        92 / 93
reset control integrity:             PASS
max reset activation difference:     2.220446049250313e-16
R_reset:                             1.0
frozen verdict:                      MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
reserved final split:                untouched by D6
```

Current supported lesson:

> Settled activation is context-conditional. Carrying an already-settled partial-context state blindly into changed context can create major path-dependent damage.

This does not establish multiple contextual settling stages, residual refinement, recurrence necessity, or final held-out superiority.

## Ground 0 working form

```text
question / unresolved need
        ↓
legitimate broad candidate field
        ↓
select potentially discriminating context
        ↓
explicit context transition
    carry | reset/re-anchor | residual/transform | reopen
        ↓
reversible contextual settling
        ↓
re-evaluate unresolved state
        ↓
optional deeper refinement or optional recurrence only if earned
        ↓
evidence sufficiency
        ↓
commit | abstain | seek evidence | reopen
```

Multiple stages and recurrence are hypotheses, not guaranteed production components.

## Immediate scientific task — implement frozen MT-1

The preregistration is frozen at `docs/MT1_PREREGISTRATION.md`. Conditions, metric,
compute rule, thresholds, and data boundary may no longer move except through an explicit
versioned amendment recorded before further results.

Frozen conditions:

```text
M0 retrieval anchor                          BM25 top-100, no taper
M1 single full-context soft                  primary baseline
M2 multi-soft, naive carry                   D6 pathology control
M3 multi-soft, reset + retained narrowing    primary treatment
M4 multi-soft, full reset                    wasted-stage sanity control
M5 reversed stage order                      order control
M6 matched-compute hard staged pruning       reversibility control
```

Frozen primary decision:

```text
MULTI_STAGE_SUPPORTED requires all of:
  n >= 30
  (M3 - M1) >= 0.010 nDCG@10
  95% paired CI lower bound > 0
  E(M3) <= 1.10 * E(M1)
```

The essential thing D6 left open, and MT-1 closes: D6's staged conditions spent roughly
twice the feature budget of its single-stage condition, so D6 could show that *carrying*
is harmful but not whether *staging* is worth its cost.

Hard pruning losing is not evidence that multi-soft is necessary. Multi-soft must materially beat single-soft under the frozen matched-compute rule to earn a permanent architectural role.

Recurrence and Token Deck output are excluded from every MT-1 condition.

## Immediate architecture task — preregister TD-5

TD-3 and TD-4 are built and integrated:

```text
raw text
   ↓
exact surface spans + character offsets     (gap-free; exact reconstruction enforced)
   ↓
normalized lookup forms                     (lexical spans only)
   ↓
known/unknown routing + acquisition need    (read-only; evidence recorded)
   ↓
explicit acquisition -> token identity      (never automatic)
   ↓
contextual sense disambiguation             ← TD-5, next
```

Frozen versions `td3-exact-surface-v1` and `td4-acquisition-routing-v1`. Neither creates
identity on its own, so both can be replaced without invalidating anything the deck owns.

Stimulus inspection paths now available:

```text
python3 -m synrheon segment "<text>"        TD-3 observation
python3 -m synrheon route "<text>"          TD-4 routing against an empty deck
POST /api/segment {"text": ...}
POST /api/acquisition {"text": ...}         TD-4 routing against the live deck
POST /api/acquire {"text": ..., "needs": [...]}   explicit acquisition; the only mutation
StimulusRecord.segmentation / .acquisition in the live state snapshot
```

TD-5 is the first serious language-learning experiment, so it is preregistered like MT-1
rather than built like TD-3/TD-4. Required before results: held-out contexts, ambiguous
cases where abstention is correct, context reversals, preservation of initially suppressed
senses, a simple frequency/default-sense baseline, no answer identity in routing, and raw
per-case failures. A learned disambiguator must output support *over* the sense inventory
without overwriting it.

Still missing before TD-5 can run: a sense-annotated data source, and a frozen decision
about which contexts are held out.

## Current live status

```text
observable runtime/UI                    Verified
computational time                       Integrated
ordered experience + provenance          Integrated
cognitive substrate                      Built
TokenDeck in substrate                   Built; still not auto-fed with identity
reversible candidate field               Built; not live-integrated
Ground 0 contextual cognition            Not Integrated
MT-1 mechanism                           Not Started; preregistration frozen
TD-3 segmenter                           Built + Integrated; awaiting stimulus verification
TD-4 acquisition router                  Built + Integrated; awaiting stimulus verification
TD-5 sense disambiguation                Not Started; preregistration next
Durable memory / learned retrieval       Not Started
```

Observation is integrated without identity on purpose: a live stimulus is segmented and
routed, and both records are attached to the stimulus, but no token card is created, so
`cognitive_substrate` is unchanged by chat. `acquire_route` is the only path from
observation to identity, and nothing calls it automatically.

## Development method

For every new organism capability:

```text
build one capability
    ↓
run explicit stimuli
    ↓
inspect backend-owned state / trace
    ↓
locate failed process
    ↓
fix process, not example
    ↓
add failure as regression test
    ↓
advance one layer
```

For every result-bearing scientific claim:

```text
hypothesis + falsifier
    ↓
preregistration
    ↓
implementation
    ↓
integrity/smoke
    ↓
allowed evidence run
    ↓
frozen interpretation
    ↓
architecture shrinks or earns next layer
```

## Completion gates for this stage

The current stage advances when both immediate boundaries are resolved independently:

### Scientific gate

- [x] MT-1 preregistration exists and is frozen before results;
- [ ] implementation obeys the frozen information/compute boundary;
- [ ] allowed development result is classified without post-hoc threshold movement.

### Representation gate

- [x] TD-3 exact segmentation exists in the correct owner;
- [x] exact text and offsets are preserved;
- [x] adversarial surface tests pass;
- [x] live/observable stimulus path added without fabricating meaning;
- [x] TD-4 routes known/unknown with recorded evidence and acquires nothing implicitly;
- [ ] observed failures from human stimulus testing become process-level regression tests.

The two tracks may later converge through token/sense/event representation -> memory/retrieval -> legitimate broad candidate fields, but they remain scientifically separate today.
