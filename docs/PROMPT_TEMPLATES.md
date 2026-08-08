# Synrheon Prompt Templates

This is a human-facing prompt key for ChatGPT, Codex, Claude Code, or another coding agent.

These prompts are dispatch instructions, not workflow authority.

Canonical project rules remain:

```text
README.md
AGENTS.md
agent/ARCHITECTURE_STEWARD.md
.agents/skills/synrheon-development-workflow/SKILL.md
```

If a prompt conflicts with the canonical workflow, the canonical workflow wins.

---

# Prompt Variables

```text
{GOAL}               what you want accomplished
{OBSERVED_BEHAVIOR}  what Synrheon actually did
{EXPECTED_BEHAVIOR}  what you expected
{STIMULUS}           exact real test input/action
{CONSTRAINTS}        what must not change
{FILES}              known relevant files
{QUESTION}           architecture/research question
{STAGE}              current/proposed stage
```

You do not need to fill every variable.

---

# 1. Continue Current Work

```text
Continue Synrheon from the current documented state.

Read README.md, AGENTS.md, the Architecture Steward, the canonical Synrheon workflow, SCAFFOLD.md, ARCHITECTURE_PLAN.md, IMPLEMENTATION_STATUS.md, and CURRENT_STAGE.md.

Reconcile documentation with the actual repository and live behavior before changing anything.

Work only on the current eligible stage. Follow the canonical workflow, prove behavior through the running organism, update project truth, and commit/push verified work to https://github.com/Logancarton/Synrheon.
```

---

# 2. Architecture Review Only — No Coding

```text
Review Synrheon architecture for:

{QUESTION}

Do not write production code.

Work broad to narrow:
- define the cognitive objective
- identify the underlying bottleneck
- compare plausible mechanisms
- identify affected owners/dependencies
- identify failure modes
- determine what should remain trainable/adaptable later
- define the live experiment that would prove/falsify the mechanism

Update architecture documentation only where the review establishes new project truth.

Return the recommended architecture, unresolved decisions, and one next decision needed before implementation.
```

---

# 3. UI / Running Organism Foundation

Use while Stage 0B is active.

```text
Continue building Synrheon's observable running organism.

Priority: infrastructure, not cognitive sophistication.

Build/improve the thinnest coherent path that lets me:
- Start Synrheon
- Send a real stimulus
- Think One Step
- Continue
- Pause
- Inspect Current State
- Inspect Trace

Keep runtime thin and UI observational. Do not put cognition in runtime/UI just to make the demonstration work.

Run the organism and prove the controls/state path live. Automated tests are regression support, not primary proof.

Update project truth only where behavior actually changed. Commit/push verified work.
```

---

# 4. Implement a Bounded Cognitive Capability

```text
Implement this Synrheon capability:

{GOAL}

Before coding, review project truth and inspect the full affected live signal path.

Pre-register a real live-organism experiment:

Stimulus:
{STIMULUS}

Expected behavior:
{EXPECTED_BEHAVIOR}

Constraints:
{CONSTRAINTS}

Place behavior in the correct cognitive owner. Keep runtime thin and UI observational.

Wire it through the real runtime, expose relevant state/trace, run the same stimulus live, inspect actual behavior, then add the minimum high-value regression tests.

Do not patch the exact wording/stimulus.

Update docs to demonstrated truth, review the complete diff, run verification gates, then explicitly stage, commit, and push verified work.
```

---

# 5. Diagnose a Live Failure

```text
Synrheon failed this live test.

Stimulus:
{STIMULUS}

Observed behavior:
{OBSERVED_BEHAVIOR}

Expected behavior:
{EXPECTED_BEHAVIOR}

Do not patch this stimulus.

Reproduce the failure through the running organism first.

Trace:
input/internal trigger → runtime → owner(s) → state transition → memory/retrieval/scratchpad/problem-solving/learning where relevant → UI/trace → outcome.

Identify the broad architectural bottleneck and correct owner. Compare possible fixes before editing. Prefer the mechanism that solves the class of failure.

After repair, rerun the exact stimulus, inspect state/trace, test a small related variation for generality, then add only high-value regression tests.

Commit/push only if the live organism demonstrates the intended behavior.
```

---

# 6. Research a Mechanism Before Adoption

```text
Research this Synrheon architecture question:

{QUESTION}

Treat this as research, not implementation truth.

Understand current architecture/stage first. Compare candidate mechanisms based on:
- cognitive purpose
- mathematical behavior
- sparse-activation compatibility
- temporal compatibility
- memory/retrieval interaction
- trainability
- stability
- computational cost
- observability
- failure modes
- duplicate-authority risk

Separate:
1. established external facts
2. inference
3. speculative Synrheon ideas

Recommend: RESEARCH.md only, architectural candidate, or mature enough for a preregistered experiment.

Do not implement unless explicitly asked.
```

---

# 7. Review Repository Without Changes

```text
Review the current Synrheon repository without making changes.

Read project purpose, scaffold, architecture plan, implementation status, current stage, decisions, canonical workflow, source owners, tests, and live entry path.

Check for:
- documentation drift
- duplicate ownership
- premature files/folders
- cognition leaking into runtime/UI
- Integrated/Verified claims without live proof
- dead/unreachable code
- architecture/implementation mismatch
- unnecessary complexity
- missing observation surfaces
- likely next bottleneck

Return:
1. current state
2. highest-value concern
3. whether it affects cognition or infrastructure
4. one recommended next action

Do not edit, commit, or push.
```

---

# 8. Reconcile Documentation

```text
Reconcile Synrheon's documentation with the actual repository and live organism.

Review README.md and docs/SCAFFOLD.md, PROJECT_GUIDE.md, SIGNAL_FLOW.md, ARCHITECTURE_PLAN.md, IMPLEMENTATION_STATUS.md, CURRENT_STAGE.md, DECISIONS.md, EXPERIMENTS.md, and RESEARCH.md.

Inspect source/runtime/UI behavior before changing status claims.

Correct stale, contradictory, duplicated, or overstated documentation.

Do not mark something Verified based only on tests.

If a documentation conflict reveals a real implementation defect, stop and report it rather than silently broadening the task.
```

---

# 9. Decide What Comes Next

```text
Determine Synrheon's next bottom-up development target.

Do not code.

Review the live organism, current stage, architecture plan, implementation status, decisions, experiments, and unresolved research.

Identify:
- what foundation is genuinely available
- weakest next dependency
- later systems depending on it
- whether work is Infrastructure, Supporting cognition, or Cognitive improvement
- broad experiment establishing success

Update CURRENT_STAGE.md / ARCHITECTURE_PLAN.md only if the next target is clear.

Return one recommended next task, not a long future sequence.
```

---

# 10. Create a New Cognitive Experiment

```text
Design a falsifiable Synrheon live-organism experiment for:

{GOAL}

Do not implement yet.

Define:
- hypothesis
- current baseline
- real stimulus/action
- expected state transition
- state/trace that must be observable
- expected outward behavior
- what must remain unchanged
- failure condition
- what different outcomes would imply architecturally

Prefer a test that distinguishes competing mechanisms rather than simple pass/fail.
```

---

# 11. Clean Up File / Folder Structure

```text
Review Synrheon's repository structure for unnecessary complexity.

Use docs/SCAFFOLD.md as the intended guide but verify against the actual repository.

Prefer:
one clear responsibility → one understandable file → split only when real complexity requires it.

Identify unnecessary folders, placeholders with no purpose, duplicate docs, unclear ownership, and misplaced files.

Do not reorganize merely for aesthetics. Update SCAFFOLD.md after approved structural changes.
```

---

# 12. Minimal Prompt

```text
Continue Synrheon from current project truth using the Architecture Steward and canonical development workflow.

Goal:
{GOAL}

Use live-organism behavior as primary evidence, keep runtime thin and UI observational, update documentation honestly, and commit/push only verified work.
```

---

# 13. Pull Latest Synrheon Changes

```powershell
cd C:\Users\Logan\Desktop\Synrheon
git pull --ff-only origin main
```

If Git reports local changes/divergence/conflict, stop and inspect instead of forcing the pull.

Never use `git reset --hard` as routine cleanup.

---

# 14. Review and Commit Synrheon Changes

```powershell
cd C:\Users\Logan\Desktop\Synrheon

git status --short
git diff --check
git diff

git add <file1>
git add <file2>
git add <file3>

git status --short
git diff --cached

git commit -m "Your commit message here"
```

Use explicit paths. Do not use `git add .` or `git add -A`.

---

# 15. Push Synrheon Changes

First upstream push:

```powershell
git push -u origin main
```

Normal future push:

```powershell
git push
```

Canonical repo:

```text
https://github.com/Logancarton/Synrheon.git
```

Do not force-push unless explicitly directed for a specific reason.

---

# 16. Full Safe Manual Git Sequence

```powershell
cd C:\Users\Logan\Desktop\Synrheon

git pull --ff-only origin main

git status --short
git diff --check
git diff

git add <file1>
git add <file2>
git add <file3>

git status --short
git diff --cached

git commit -m "Your commit message here"

git push
```

Stop if pull, verification, or repository state reveals a problem.

---

# 17. First Synrheon Commit

Use only when the remote is empty and this scaffold is the first commit.

```powershell
cd C:\Users\Logan\Desktop\Synrheon

git status --short
git diff --check

git add .agents
git add .claude
git add .gitignore
git add AGENTS.md
git add README.md
git add agent
git add data
git add docs
git add pyproject.toml
git add scripts
git add src
git add tests
git add ui

git status --short
git diff --cached

git commit -m "Initialize Synrheon scaffold"
git push -u origin main
```

Before committing, confirm no accidental root duplicates/local-only files are staged.

---

# 18. Update My Plain-English Project Guide / Signal Flow

```text
Update Synrheon's human-readable project documentation.

Review the actual current repository and live behavior first.

Update:
- docs/PROJECT_GUIDE.md
- docs/SIGNAL_FLOW.md
- docs/SCAFFOLD.md only if structure/ownership changed

For PROJECT_GUIDE.md:
- explain every changed file in ordinary language
- explain each meaningful class/function/command/UI control/major section
- state inputs/outputs/ownership/call relationships
- distinguish current implemented behavior from planned responsibility
- write for a non-programmer

For SIGNAL_FLOW.md:
- update CURRENT REAL FLOW only for wiring that actually exists
- keep future architecture under PLANNED / INTENDED FLOW
- show owner-to-owner handoffs/feedback clearly

Do not change production behavior merely to make docs simpler.
```

---

# 19. Finish Chat Thread / Create Next-Thread Handoff

```text
Finish this Synrheon chat thread and prepare a complete handoff for a fresh chat.

Do not begin new implementation work.

First reconcile the conversation with the current repository and project truth, including relevant docs, Git branch/HEAD/status, files changed, live runtime/UI behavior observed, and tests/verification actually run.

Update repository documentation only where this thread established new truth not yet recorded.

Then create a self-contained handoff that a new ChatGPT/Codex/Claude session can continue from without reading this thread.

Include:
1. PROJECT — relevant purpose, canonical repo, branch/commit when known
2. CURRENT STATE — active stage; Designed/Built/Integrated/Verified truth; cognitive-effect classification
3. WHAT WAS ACCOMPLISHED — decisions, files, mechanisms, wiring, live behavior, tests/checks, commits/pushes
4. IMPORTANT DECISIONS/CONSTRAINTS — ownership boundaries, rejected approaches, user preferences
5. LIVE ORGANISM EVIDENCE — exact stimuli/actions, observed vs expected behavior, state/trace, unverified parts
6. UNRESOLVED GAPS — bugs, uncertainties, failures, partial work, doc conflicts, risks
7. NEXT ACTION — exactly one immediate action with exact commands or one precise task prompt
8. FILES TO READ FIRST — smallest resume set
9. COPY-PASTE NEXT-THREAD PROMPT — complete prompt that assumes no access to this conversation

Distinguish observed fact from inference/plan. Do not claim tests/live behavior not actually run. Do not omit failed attempts that affect the next decision. Do not start the next task after the handoff.
```

---

# Prompt Selection Key

```text
Keep building
→ Continue Current Work

Think before coding
→ Architecture Review Only

Get UI/runtime working
→ UI / Running Organism Foundation

Build a known capability
→ Implement a Bounded Cognitive Capability

Synrheon did something wrong
→ Diagnose a Live Failure

Study a mechanism
→ Research a Mechanism Before Adoption

Independent audit
→ Review Repository Without Changes

Docs are stale
→ Reconcile Documentation

Stage just finished
→ Decide What Comes Next

Design a better test
→ Create a New Cognitive Experiment

Repository feels messy
→ Clean Up File / Folder Structure

Pull newest GitHub changes
→ Pull Latest Synrheon Changes

Manually review/commit
→ Review and Commit Synrheon Changes

Manually push
→ Push Synrheon Changes

One pull → commit → push sequence
→ Full Safe Manual Git Sequence

Update plain-English guide / signal flow
→ Update My Plain-English Project Guide / Signal Flow

End this chat/start a new one
→ Finish Chat Thread / Create Next-Thread Handoff

Shortest instruction
→ Minimal Prompt
```

---

# Important Prompt Rule

Keep prompts focused on what the repository cannot know:

```text
what you want
what you observed
what you expected
what must not change
```

Do not repeat the entire Synrheon workflow inside every prompt. The repository already owns the workflow.
