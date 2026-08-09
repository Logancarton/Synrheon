"""Non-production E011-A generated-world training and scoring harness.

This module owns hidden generated graph truth and scoring. Production cognition in
``synrheon.cognition`` receives only revealed ``CognitiveState`` snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
import random
from statistics import mean, median
from typing import Iterable, Sequence

from synrheon.cognition import CognitiveAction, CognitiveState, LinearCognitivePolicy, RevealedNode
from synrheon.learning import PolicyDecisionTrace, ReinforceLearner

EXPERIMENT_ID = "E011-A"
GENERATOR_VERSION = "e011a-v1"
STATE_CONTRACT_VERSION = "e011a-state-v1"
ACTION_CONTRACT_VERSION = "e011a-actions-v1"
HARD_ACTION_BUDGET = 10
TRAIN_SEEDS = range(1000, 5000)
DEVELOPMENT_SEEDS = range(5000, 6000)
FINAL_SEEDS = range(10000, 11000)
MODEL_SEEDS = (11, 22, 33, 44, 55)


@dataclass(frozen=True, slots=True)
class GeneratedWorld:
    seed: int
    start: str
    goal: str
    adjacency: dict[str, tuple[str, ...]]
    shortest_path: tuple[str, ...]
    handles: tuple[str, ...]

    @property
    def shortest_path_edges(self) -> int:
        return len(self.shortest_path) - 1

    @property
    def exhaustive_cost(self) -> int:
        return len(self.handles) + 1


@dataclass(frozen=True, slots=True)
class EpisodeResult:
    success: bool
    total_actions: int
    expand_count: int
    stop_count: int
    premature_stop_count: int
    invalid_action_count: int
    invalid_target_count: int
    stale_target_count: int
    budget_exhausted: bool
    exhaustive_cost: int
    shortest_path_edges: int


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    episodes: int
    success_rate: float
    mean_actions: float
    median_actions: float
    mean_success_actions: float
    median_success_actions: float
    budget_exhaustion_rate: float
    premature_stop_rate: float
    mean_budget_fraction: float
    mean_success_exhaustive_ratio: float
    depth_success: dict[int, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "episodes": self.episodes,
            "success_rate": self.success_rate,
            "mean_actions": self.mean_actions,
            "median_actions": self.median_actions,
            "mean_success_actions": self.mean_success_actions,
            "median_success_actions": self.median_success_actions,
            "budget_exhaustion_rate": self.budget_exhaustion_rate,
            "premature_stop_rate": self.premature_stop_rate,
            "mean_budget_fraction": self.mean_budget_fraction,
            "mean_success_exhaustive_ratio": self.mean_success_exhaustive_ratio,
            "depth_success": dict(self.depth_success),
        }


class PartialGraphEpisode:
    """Revealed-state environment; hidden truth remains inside this harness."""

    def __init__(self, world: GeneratedWorld) -> None:
        self.world = world
        self.revealed: set[str] = {world.start}
        self.expanded: set[str] = set()
        self.reveal_order: dict[str, int] = {world.start: 0}
        self.revealed_edges: set[tuple[str, str]] = set()
        self.action_count = 0
        self.previous_action: CognitiveAction | None = None
        self.terminated = False
        self.success = False
        self.premature_stop_count = 0
        self.invalid_action_count = 0
        self.invalid_target_count = 0
        self.stale_target_count = 0
        self.expand_count = 0
        self.stop_count = 0

    def state(self) -> CognitiveState:
        depths = self._known_depths()
        nodes = tuple(
            RevealedNode(
                handle=handle,
                depth=depths.get(handle, HARD_ACTION_BUDGET),
                expanded=handle in self.expanded,
                reveal_order=self.reveal_order[handle],
                frontier=handle not in self.expanded,
                is_goal=handle == self.world.goal,
            )
            for handle in sorted(self.revealed, key=lambda item: self.reveal_order[item])
        )
        return CognitiveState(
            checkpoint_index=self.action_count,
            remaining_budget=HARD_ACTION_BUDGET - self.action_count,
            hard_budget=HARD_ACTION_BUDGET,
            nodes=nodes,
            revealed_edges=tuple(sorted(self.revealed_edges)),
            previous_action=self.previous_action,
        )

    def apply(self, action: CognitiveAction) -> tuple[float, str]:
        if self.terminated:
            raise RuntimeError("Episode already terminated.")
        if self.action_count >= HARD_ACTION_BUDGET:
            raise RuntimeError("Action budget already exhausted.")

        self.action_count += 1
        self.previous_action = action
        reward = -0.025
        outcome = "step"

        if action.operation == "STOP":
            self.stop_count += 1
            self.terminated = True
            if self.world.goal in self.revealed:
                self.success = True
                reward += 1.5
                outcome = "success_stop"
            else:
                self.premature_stop_count += 1
                reward -= 1.0
                outcome = "premature_stop"
            return reward, outcome

        if action.operation != "EXPAND":
            self.invalid_action_count += 1
            reward -= 1.0
            outcome = "invalid_action"
            return reward, outcome

        target = action.target
        if target is None or target not in self.revealed:
            self.invalid_target_count += 1
            reward -= 1.0
            outcome = "invalid_target"
            return reward, outcome
        if target in self.expanded:
            self.stale_target_count += 1
            reward -= 0.5
            outcome = "stale_target"
            return reward, outcome

        self.expand_count += 1
        self.expanded.add(target)
        newly_revealed = 0
        goal_newly_revealed = False
        for child in self.world.adjacency[target]:
            self.revealed_edges.add((target, child))
            if child not in self.revealed:
                self.revealed.add(child)
                self.reveal_order[child] = len(self.reveal_order)
                newly_revealed += 1
                if child == self.world.goal:
                    goal_newly_revealed = True

        if newly_revealed:
            reward += 0.015
        if goal_newly_revealed:
            reward += 1.0
            outcome = "goal_revealed"
        elif newly_revealed:
            outcome = "structure_revealed"
        else:
            reward -= 0.02
            outcome = "dead_end"

        if self.action_count >= HARD_ACTION_BUDGET and not self.terminated:
            self.terminated = True
            reward -= 0.5
            outcome = "budget_exhausted"
        return reward, outcome

    def result(self) -> EpisodeResult:
        return EpisodeResult(
            success=self.success,
            total_actions=self.action_count,
            expand_count=self.expand_count,
            stop_count=self.stop_count,
            premature_stop_count=self.premature_stop_count,
            invalid_action_count=self.invalid_action_count,
            invalid_target_count=self.invalid_target_count,
            stale_target_count=self.stale_target_count,
            budget_exhausted=self.terminated and not self.success and self.action_count >= HARD_ACTION_BUDGET,
            exhaustive_cost=self.world.exhaustive_cost,
            shortest_path_edges=self.world.shortest_path_edges,
        )

    def _known_depths(self) -> dict[str, int]:
        depths = {self.world.start: 0}
        queue = [self.world.start]
        while queue:
            source = queue.pop(0)
            for edge_source, target in self.revealed_edges:
                if edge_source != source or target in depths:
                    continue
                depths[target] = depths[source] + 1
                queue.append(target)
        return depths


def _opaque_handles(count: int, seed: int, permutation_seed: int | None) -> tuple[str, ...]:
    rng = random.Random(seed if permutation_seed is None else permutation_seed)
    tokens = [f"n{index:02d}" for index in range(count)]
    rng.shuffle(tokens)
    return tuple(tokens)


def generate_world(seed: int, *, permutation_seed: int | None = None) -> GeneratedWorld:
    """Generate a deterministic hidden graph satisfying the frozen E011-A v1 family."""

    rng = random.Random(seed)
    node_count = rng.randint(10, 14)
    path_edges = rng.randint(3, 5)
    branch_count = rng.randint(2, 4)
    handles = _opaque_handles(node_count, seed + 9973, permutation_seed)

    start = handles[0]
    path_nodes = list(handles[: path_edges + 1])
    goal = path_nodes[-1]
    adjacency: dict[str, list[str]] = {handle: [] for handle in handles}
    for source, target in zip(path_nodes, path_nodes[1:]):
        adjacency[source].append(target)

    unused = list(handles[path_edges + 1 :])
    anchors = [path_nodes[index] for index in range(min(path_edges, 3))]
    for branch_index in range(branch_count):
        if not unused:
            break
        anchor = anchors[branch_index % len(anchors)]
        first = unused.pop(0)
        adjacency[anchor].append(first)
        cursor = first
        desired_extra = rng.randint(0, 2)
        for _ in range(desired_extra):
            if not unused:
                break
            child = unused.pop(0)
            adjacency[cursor].append(child)
            cursor = child

    distractor_nodes = [handle for handle in handles if handle not in path_nodes]
    while unused:
        child = unused.pop(0)
        anchor = rng.choice(distractor_nodes[:-1] or [start])
        if child == anchor:
            anchor = start
        adjacency[anchor].append(child)

    cross_count = rng.randint(0, 2)
    depth_hint = {node: index for index, node in enumerate(path_nodes)}
    depth_hint.update({node: path_edges + 1 for node in distractor_nodes})
    non_goal = [handle for handle in handles if handle != goal]
    added = 0
    attempts = 0
    while added < cross_count and attempts < 40:
        attempts += 1
        source = rng.choice(distractor_nodes or non_goal)
        target = rng.choice(non_goal)
        if source == target or target in adjacency[source]:
            continue
        if target == goal:
            continue
        if depth_hint.get(target, 0) > depth_hint.get(source, path_edges + 1):
            continue
        adjacency[source].append(target)
        added += 1

    for children in adjacency.values():
        rng.shuffle(children)

    return GeneratedWorld(
        seed=seed,
        start=start,
        goal=goal,
        adjacency={key: tuple(value) for key, value in adjacency.items()},
        shortest_path=tuple(path_nodes),
        handles=handles,
    )


def run_episode(
    world: GeneratedWorld,
    policy: LinearCognitivePolicy,
    *,
    rng: random.Random,
    greedy: bool,
    learner: ReinforceLearner | None = None,
) -> EpisodeResult:
    environment = PartialGraphEpisode(world)
    decisions: list[PolicyDecisionTrace] = []
    rewards: list[float] = []

    while not environment.terminated:
        state = environment.state()
        action, evaluations, selected_index = policy.choose(
            state,
            rng=rng,
            greedy=greedy,
            temperature=1.0,
        )
        reward, _ = environment.apply(action)
        decisions.append(PolicyDecisionTrace(evaluations, selected_index))
        rewards.append(reward)

    if learner is not None:
        learner.update_episode(decisions, rewards)
    return environment.result()


def run_random_episode(world: GeneratedWorld, *, rng: random.Random) -> EpisodeResult:
    environment = PartialGraphEpisode(world)
    policy = LinearCognitivePolicy(seed=0, weights=[0.0] * 9)
    while not environment.terminated:
        state = environment.state()
        actions = policy.valid_actions(state)
        environment.apply(rng.choice(actions))
    return environment.result()


def train_policy(
    model_seed: int,
    *,
    training_seeds: Iterable[int] = TRAIN_SEEDS,
    epochs: int = 2,
) -> tuple[LinearCognitivePolicy, int, str]:
    policy = LinearCognitivePolicy(seed=model_seed)
    initial_checksum = policy.parameter_checksum()
    learner = ReinforceLearner(policy)
    seed_list = list(training_seeds)
    shuffle_rng = random.Random(model_seed * 1009)
    action_rng = random.Random(model_seed * 9176 + 3)
    episodes = 0
    for _ in range(epochs):
        shuffle_rng.shuffle(seed_list)
        for world_seed in seed_list:
            run_episode(
                generate_world(world_seed),
                policy,
                rng=action_rng,
                greedy=False,
                learner=learner,
            )
            episodes += 1
    return policy, episodes, initial_checksum


def evaluate_policy(
    policy: LinearCognitivePolicy,
    world_seeds: Iterable[int],
    *,
    permutation_seeds: Iterable[int] | None = None,
) -> tuple[EvaluationSummary, list[EpisodeResult]]:
    seeds = list(world_seeds)
    permutations = list(permutation_seeds) if permutation_seeds is not None else [None] * len(seeds)
    if len(seeds) != len(permutations):
        raise ValueError("World and permutation seed counts must match.")
    results = [
        run_episode(
            generate_world(seed, permutation_seed=permutation),
            policy,
            rng=random.Random(seed + policy.initialization_seed),
            greedy=True,
        )
        for seed, permutation in zip(seeds, permutations)
    ]
    return summarize(results), results


def evaluate_random(world_seeds: Iterable[int]) -> EvaluationSummary:
    results = [
        run_random_episode(generate_world(seed), rng=random.Random(seed * 31 + 7))
        for seed in world_seeds
    ]
    return summarize(results)


def summarize(results: Sequence[EpisodeResult]) -> EvaluationSummary:
    if not results:
        raise ValueError("At least one episode result is required.")
    successes = [item for item in results if item.success]
    by_depth: dict[int, list[EpisodeResult]] = {}
    for item in results:
        by_depth.setdefault(item.shortest_path_edges, []).append(item)
    return EvaluationSummary(
        episodes=len(results),
        success_rate=mean(1.0 if item.success else 0.0 for item in results),
        mean_actions=mean(item.total_actions for item in results),
        median_actions=float(median(item.total_actions for item in results)),
        mean_success_actions=mean(item.total_actions for item in successes) if successes else 0.0,
        median_success_actions=float(median(item.total_actions for item in successes)) if successes else 0.0,
        budget_exhaustion_rate=mean(1.0 if item.budget_exhausted else 0.0 for item in results),
        premature_stop_rate=mean(1.0 if item.premature_stop_count else 0.0 for item in results),
        mean_budget_fraction=mean(item.total_actions / HARD_ACTION_BUDGET for item in results),
        mean_success_exhaustive_ratio=(
            mean(item.total_actions / item.exhaustive_cost for item in successes) if successes else 1.0
        ),
        depth_success={
            depth: mean(1.0 if item.success else 0.0 for item in group)
            for depth, group in sorted(by_depth.items())
        },
    )


def full_assay(*, quick: bool = False) -> dict[str, object]:
    train_range = range(1000, 1400) if quick else TRAIN_SEEDS
    eval_range = range(10000, 10200) if quick else FINAL_SEEDS
    rename_range = range(20000, 20200) if quick else range(20000, 21000)
    random_summary = evaluate_random(eval_range)
    runs: list[dict[str, object]] = []

    for model_seed in MODEL_SEEDS:
        untrained = LinearCognitivePolicy(seed=model_seed)
        untrained_summary, _ = evaluate_policy(untrained, eval_range)
        untrained_training_summary, _ = evaluate_policy(untrained, train_range)
        trained, episodes_seen, initial_checksum = train_policy(
            model_seed,
            training_seeds=train_range,
            epochs=2,
        )
        trained_training_summary, _ = evaluate_policy(trained, train_range)
        trained_summary, _ = evaluate_policy(trained, eval_range)
        renamed_summary, _ = evaluate_policy(
            trained,
            eval_range,
            permutation_seeds=rename_range,
        )
        runs.append(
            {
                "model_seed": model_seed,
                "episodes_seen": episodes_seen,
                "initial_checksum": initial_checksum,
                "trained_checksum": trained.parameter_checksum(),
                "training_untrained": untrained_training_summary.to_dict(),
                "training_trained": trained_training_summary.to_dict(),
                "untrained": untrained_summary.to_dict(),
                "trained": trained_summary.to_dict(),
                "renamed": renamed_summary.to_dict(),
                "weights": trained.to_dict()["weights"],
            }
        )

    return {
        "experiment_id": EXPERIMENT_ID,
        "generator_version": GENERATOR_VERSION,
        "state_contract_version": STATE_CONTRACT_VERSION,
        "action_contract_version": ACTION_CONTRACT_VERSION,
        "quick": quick,
        "random_valid": random_summary.to_dict(),
        "runs": runs,
    }


def assess_pass_gate(report: dict[str, object]) -> dict[str, object]:
    """Evaluate the frozen E011-A v1 numerical gate without changing thresholds."""

    runs = report["runs"]
    if not isinstance(runs, list) or len(runs) != 5:
        raise ValueError("E011-A pass assessment requires all five frozen model seeds.")
    random_valid = report["random_valid"]
    assert isinstance(random_valid, dict)
    random_success = float(random_valid["success_rate"])
    held = [float(run["trained"]["success_rate"]) for run in runs]
    untrained = [float(run["untrained"]["success_rate"]) for run in runs]
    renamed = [float(run["renamed"]["success_rate"]) for run in runs]
    training_gains = [
        float(run["training_trained"]["success_rate"])
        - float(run["training_untrained"]["success_rate"])
        for run in runs
    ]
    checksums_changed = all(run["initial_checksum"] != run["trained_checksum"] for run in runs)
    four_training = sum(gain >= 0.20 for gain in training_gains) >= 4
    med_held = float(median(held))
    med_untrained = float(median(untrained))
    final_margin = med_held - max(random_success, med_untrained)
    four_individual = sum(
        held_value - random_success >= 0.15 and held_value - untrained_value >= 0.15
        for held_value, untrained_value in zip(held, untrained)
    ) >= 4
    paired_drops = [held_value - renamed_value for held_value, renamed_value in zip(held, renamed)]
    rename_retention = float(median(renamed)) / med_held if med_held else 0.0
    rename_drop = float(median(paired_drops))
    depth_coverage = all(
        all(
            float(
                run["trained"]["depth_success"].get(
                    str(depth), run["trained"]["depth_success"].get(depth, 0.0)
                )
            )
            > 0
            for depth in (3, 4, 5)
        )
        for run in runs
    )
    efficiency = all(
        float(run["trained"]["mean_success_exhaustive_ratio"]) <= 0.80 for run in runs
    )
    budget = all(float(run["trained"]["mean_budget_fraction"]) <= 0.80 for run in runs)
    checks = {
        "parameters_changed": checksums_changed,
        "four_of_five_training_gain_ge_20pp": four_training,
        "median_held_out_ge_70pct": med_held >= 0.70,
        "median_margin_ge_20pp_over_both_baselines": final_margin >= 0.20,
        "four_of_five_individual_margin_ge_15pp": four_individual,
        "renaming_retains_95pct_and_drop_le_5pp": rename_retention >= 0.95 and rename_drop <= 0.05,
        "depths_3_4_5_have_success": depth_coverage,
        "successful_cost_le_80pct_exhaustive": efficiency,
        "mean_budget_use_le_80pct": budget,
    }
    return {
        "passed_numeric_gate": all(checks.values()),
        "checks": checks,
        "median_held_out_success": med_held,
        "random_valid_success": random_success,
        "median_untrained_success": med_untrained,
        "median_renamed_success": float(median(renamed)),
        "median_renaming_retention": rename_retention,
        "median_renaming_absolute_drop": rename_drop,
        "training_gains": training_gains,
    }


def learning_metrics(report: dict[str, object]) -> dict[str, object]:
    """Build the backend-owned summary consumed by the Organism UI later."""

    gate = report.get("gate")
    if not isinstance(gate, dict):
        gate = assess_pass_gate(report)
    runs = report["runs"]
    assert isinstance(runs, list)
    training = float(median(float(run["training_trained"]["success_rate"]) for run in runs))
    held = float(median(float(run["trained"]["success_rate"]) for run in runs))
    renamed = float(median(float(run["renamed"]["success_rate"]) for run in runs))
    exhaustive_ratio = float(
        median(float(run["trained"]["mean_success_exhaustive_ratio"]) for run in runs)
    )
    return {
        "model_version": "e011a-linear-softmax-v1/five-seed-assay",
        "training_episode": int(median(int(run["episodes_seen"]) for run in runs)),
        "training_success": training,
        "held_out_success": held,
        "renamed_success": renamed,
        "cognitive_efficiency": max(0.0, 1.0 - exhaustive_ratio),
        "strongest_generalization_level": "Level 1",
        "verdict": (
            "E011-A v1 numeric gate passed"
            if gate.get("passed_numeric_gate")
            else "E011-A v1 numeric gate failed"
        ),
        "detail": "Controlled generated-world evidence only; E011-B live organism integration is separate.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the controlled E011-A process-transfer assay.")
    parser.add_argument("--quick", action="store_true", help="Run a small regression-sized assay.")
    arguments = parser.parse_args()
    report = full_assay(quick=arguments.quick)
    report["gate"] = assess_pass_gate(report)
    report["learning_metrics"] = learning_metrics(report)
    print(json.dumps(report, indent=2, sort_keys=True))
