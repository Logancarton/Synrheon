"""Compatibility exports for the frozen E011-A experiment.

Active E011 policy-learning ownership has moved to ``synrheon.policy_learning``.
New production work should import that module directly. This shim remains only so
the frozen historical experiment can still run without rewriting its scientific
implementation during an unrelated source-tree refactor.
"""

from synrheon.policy_learning import PolicyDecisionTrace, ReinforceLearner, load_recorded_learning_metrics

__all__ = ["PolicyDecisionTrace", "ReinforceLearner", "load_recorded_learning_metrics"]
