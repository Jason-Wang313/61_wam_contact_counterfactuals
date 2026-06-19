# Paper 61 Development Log

Date: 2026-06-19

Purpose: record material method and evaluation changes made before the final protocol freeze. Development runs are not final evidence.

## 2026-06-19 Initial Expanded-Standard Changes

- Added CPU/RAM-light thread caps for BLAS-style libraries.
- Expanded the hidden-physics branch library to include very-low friction, light mass, and heavier mass regimes.
- Added stress splits for light objects, observation noise, actuation noise, target shift, contact offset mismatch, and adversarial low-friction/heavy-object shift.
- Added stronger comparison methods:
  - `domain_randomized_mpc`;
  - `adaptive_id_mpc`;
  - `robust_mean_hybrid_mpc`.
- Kept `branch_counterfactual_mpc` as the legacy v4 adaptive branch method for comparison.
- Added `branch_counterfactual_mpc_v5` as the new proposed method with an information-gain diagnostic action and conservative entropy-triggered fallback.
- Added ablations for no diagnostic push, no branch reweighting, mean-risk planning, no information-gain term, no conservative fallback, one branch only, and reduced branch library.
- Added posterior diagnostics:
  - final and mean posterior entropy;
  - final and mean near-true branch mass;
  - branch prediction error;
  - fallback activation count.
- Added isolated development output directories through `--output-subdir` so smoke/tuning runs do not overwrite frozen or legacy evidence.

Next step: run an isolated smoke test with one seed, one episode, and a small split/method subset to validate code paths before any larger development or frozen evaluation.

## 2026-06-19 Smoke-Test Cost Finding

- Isolated smoke command:
  - `python src/run_experiment.py --seeds 1 --episodes 1 --splits nominal low_friction combined_shift --methods branch_counterfactual_mpc_v5 adaptive_id_mpc robust_mean_hybrid_mpc oracle_hidden_params --skip-ablation --workers 1 --output-subdir dev_smoke_20260619`
- The run produced valid partial rows for all three splits, including posterior diagnostics, but the shell timed out before normal finalization.
- Diagnosis: the first v5 information-gain implementation was too expensive for CPU-only final evaluation.
- Cost-control changes made before protocol freeze:
  - reused one `MjData` buffer per physical-parameter model inside each process;
  - pruned the branch grid to a smaller curated set that still covers very-low friction, nominal, high friction, light, and heavy regimes;
  - reduced the candidate action stencil from 16 to 10 actions per planning decision.
- These changes are intended to preserve the scientific stress test while making final evaluation feasible on CPU with low RAM.

## 2026-06-19 Optimized Smoke Test

- Isolated smoke command:
  - `python src/run_experiment.py --seeds 1 --episodes 1 --splits nominal low_friction combined_shift --methods branch_counterfactual_mpc_v5 adaptive_id_mpc robust_mean_hybrid_mpc oracle_hidden_params --skip-ablation --workers 1 --output-subdir dev_smoke_fast_20260619`
- Result:
  - completed 12 rows;
  - elapsed time: approximately 42.5 seconds on one worker;
  - wrote complete raw, metric, seed, stress-curve, negative-case, and summary files under `results/dev_smoke_fast_20260619`.
- This smoke run validated the v5 method path, adaptive-ID baseline path, robust-hybrid baseline path, oracle path, posterior diagnostics, and isolated output routing.
- The final protocol was frozen after this smoke test in `docs/paper61_protocol_freeze_20260619.md`.

## 2026-06-19 Stale v4 Runner Interventions

- During the frozen v5 evaluation, stale v4 helper processes attempted to run:
  - `scripts/build_v4_paper.py`;
  - `scripts/run_v4_claim_audit.py`;
  - `experiments/v4_cached_evidence.py`.
- These were not part of the frozen v5 protocol and risked overwriting v5 manuscript/result artifacts.
- Only those stale v4 processes were stopped. The frozen v5 evaluation process `src/run_experiment.py --seeds 8 --episodes 20 --workers 2 --chunksize 2` and its worker processes were left running.
- Root cause found: old `codex-watchdog-daemon.py` processes from the 2026-06-16 continuation pass were still relaunching v4 commands. Those stale watchdog daemons were stopped after verifying they were not the frozen v5 evaluator.
- The first frozen v5 run exited after the nominal split with no stderr, leaving a valid `results/mujoco_contact_raw.partial.csv` containing 1,600 nominal rows.
- Recovery change: added `--resume` orchestration support to load partial CSV rows and skip completed splits/seeds. This does not change the method, branch library, metrics, splits, seeds, or decision rule.
