# Paper 61 Terminal Evidence

Decision: STRONG_REVISE.

ICLR main ready: no.

Submission-hardening version: v4 real MuJoCo rebuild.

## What Changed

- Replaced the synthetic scaffold with a real MuJoCo contact-pushing benchmark.
- Added paired hidden-physics tasks across methods.
- Added 5 seeds, 16 episodes per split/method, five stress splits, and 480 combined-shift ablation episodes.
- Added implemented baselines: random push, nominal single-branch MPC, ensemble mean MPC, robust worst-case MPC, and oracle hidden-parameter MPC.
- Added paired statistics and figures.

## Main Evidence

Branch MPC success rates:
- nominal: 0.688 +/- 0.102
- low_friction: 0.113 +/- 0.070
- high_friction: 0.850 +/- 0.079
- heavy_object: 0.588 +/- 0.109
- combined_shift: 0.312 +/- 0.102

The proposed method beats random and usually beats nominal single-branch MPC. It is approximately tied with ensemble mean MPC and does not consistently beat robust worst-case MPC. The oracle hidden-parameter gap is large on low friction and heavy object splits.

## Ablation Evidence

On combined shift, branch_counterfactual_mpc reaches 0.312 success and 0.1006 m final distance. Reduced branch library and no-branch-reweighting are competitive or better on success, so the mechanism is not isolated strongly enough for an ICLR-main claim.

## Terminal Reason

The paper now has real high-fidelity evidence, but the claimed mechanism is not decisively validated. The correct terminal state is STRONG_REVISE, not ICLR_MAIN_READY and not synthetic KILL_ARCHIVE.
