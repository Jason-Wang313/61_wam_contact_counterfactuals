# Novelty Boundary Map

## Crowded Territory
- Bigger data/model scaling.
- New benchmark only.
- Generic active learning or uncertainty.
- Combining a planner with a learned policy without a new state/action object.

## Claimed Boundary
Wam contact counterfactuals keeps action-critical alternatives explicit until a physical observation collapses them.

## What Would Falsify The Claim
If observed-only baselines match the adverse-mode coverage and closed-loop success of the proposed branch-aware mechanism, the paper should be revised or killed.

## v4 Outcome
The v4 MuJoCo rebuild partially triggers this falsification condition. Branch MPC beats random and usually improves over nominal single-branch MPC, but ensemble mean MPC matches it on several splits and robust worst-case MPC remains competitive. The novelty boundary is therefore not strong enough for ICLR main without a learned branch mechanism or stronger empirical separation.
