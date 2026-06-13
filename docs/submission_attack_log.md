# Submission Attack Log

Paper: 61 wam_contact_counterfactuals

This v4 pass rebuilds the paper with real MuJoCo evidence. The result is strong revise, not ICLR-main readiness.

## Rebuild Round 1

Attack: The previous evidence was synthetic/template-generated.

Verdict: Recovered.

Action: Replaced `src/run_experiment.py` with a real MuJoCo contact-pushing benchmark.

## Rebuild Round 2

Attack: Methods were not compared on paired tasks.

Verdict: Recovered.

Action: Each split/seed/episode now samples one hidden-physics task shared by every method.

## Rebuild Round 3

Attack: No implemented baselines.

Verdict: Partly recovered.

Action: Added random push, nominal single-branch MPC, ensemble mean MPC, robust worst-case MPC, and oracle hidden-parameter MPC.

## Rebuild Round 4

Attack: No stress testing.

Verdict: Recovered for simulation.

Action: Added nominal, low-friction, high-friction, heavy-object, and combined-shift splits.

## Rebuild Round 5

Attack: No uncertainty estimates.

Verdict: Recovered.

Action: Reported 95 percent confidence intervals over 80 episodes per split/method.

## Rebuild Round 6

Attack: No ablation.

Verdict: Recovered, but unfavorable.

Action: Combined-shift ablations show that reduced branch library and no-branch-reweighting variants are competitive with the proposed method. This weakens the mechanism claim.

## Rebuild Round 7

Attack: The proposed method must beat strong baselines, not just random or nominal MPC.

Verdict: Not recovered.

Action: Branch MPC ties ensemble mean MPC on multiple splits and does not consistently beat robust worst-case MPC.

## Rebuild Round 8

Attack: The method should adapt to low friction if branch counterfactuals are useful.

Verdict: Not recovered.

Action: Low-friction success is 0.113 +/- 0.070 for branch MPC versus 0.150 +/- 0.079 for robust MPC and 0.537 +/- 0.110 for oracle.

## Rebuild Round 9

Attack: High-fidelity simulation does not replace hardware or external benchmarks.

Verdict: Not recovered.

Action: Mark as a remaining blocker for ICLR main.

## Rebuild Round 10

Attack: Related work is still based mainly on local pool metadata.

Verdict: Not recovered.

Action: Keep hostile prior-work list and require manual full-paper synthesis before revival.

## Terminal Decision

Decision: STRONG_REVISE.

The paper is no longer a synthetic archive, but it is not submission ready.
