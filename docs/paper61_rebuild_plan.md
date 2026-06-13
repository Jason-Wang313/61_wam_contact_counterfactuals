# Paper 61 Rebuild Plan

Paper: `61_wam_contact_counterfactuals`

Active goal: rebuild this paper as a real ICLR-main-target submission if the evidence can honestly support that bar. If not, reach a terminal `STRONG_REVISE` or `KILL_ARCHIVE` decision with evidence.

## Starting Point

The current v3 paper is an ICLR main gate archive. It correctly says that the generated draft has only synthetic/template evidence. The rebuild treats that draft as disposable scaffolding.

## Salvageable Thesis

Contact-rich robot policies can fail when a single-future world/action model collapses plausible contact outcomes. A branch-structured world-action planner should preserve multiple contact-mode futures and choose actions by risk-sensitive value over those branches.

## Evidence Plan

Use real MuJoCo contact dynamics, not synthetic probability tables.

Primary benchmark:
- A planar contact-pushing MuJoCo benchmark with a cylindrical puck, a controlled pusher, Coulomb friction, mass variation, contact slip, and target-reaching objectives.
- Hidden physical branches vary object mass, surface friction, and contact/slip behavior.
- The policy gets limited observations and must choose diagnostic and delivery pushes.

Environment evidence:
- `robosuite` Panda `Lift` was verified to instantiate headlessly.
- Full experiments use direct MuJoCo because it allows controlled counterfactual branch rollouts and fast multi-seed stress tests.

## Methods and Baselines

Compare:
- `random_push`: random action baseline.
- `nominal_single_branch_mpc`: plans under one nominal contact model.
- `ensemble_mean_mpc`: averages predicted outcome over branch models.
- `robust_worst_case_mpc`: optimizes worst predicted branch outcome.
- `branch_counterfactual_mpc`: proposed method, uses a diagnostic push to update branch weights and then plans risk-sensitive delivery.
- `oracle_hidden_params`: upper bound with true hidden physical parameters.

## Ablations

For the proposed method:
- no diagnostic push.
- no branch reweighting.
- mean-risk instead of tail-risk.
- one branch only.
- reduced branch library.

## Stress Tests

Evaluate under:
- nominal hidden-parameter sampling.
- high friction shift.
- low friction shift.
- heavy object shift.
- light object shift.
- observation noise.
- pusher actuation noise.
- target pose shift.
- combined shift.

## Statistical Bar

Target:
- at least 5 random seeds.
- at least 40 episodes per seed per split for the main table.
- report mean, standard deviation, and 95% confidence intervals.
- include per-seed raw CSVs and aggregate tables.

## Paper Rewrite

If the experiment produces credible evidence:
- rewrite the paper around the MuJoCo benchmark.
- include method, benchmark, main table, ablation table, stress table, failure cases, hostile prior work, limitations, and reproducibility.

If evidence is promising but not enough for ICLR main:
- mark `STRONG_REVISE`.
- explain exactly what remains missing, likely public benchmark breadth, real robot validation, learned model training, and manual full-paper related work.

If the method fails against strong baselines:
- mark `KILL_ARCHIVE`.

## Terminal Criteria

`ICLR_MAIN_TARGET_READY` only if:
- real/high-fidelity MuJoCo evidence is strong and reproducible.
- branch method beats strong non-oracle baselines across stress tests.
- ablations isolate the mechanism.
- limitations are honest.
- code and paper are polished.
- GitHub is pushed and Downloads `61.pdf` is current.

Otherwise use `STRONG_REVISE` or `KILL_ARCHIVE` with evidence.
