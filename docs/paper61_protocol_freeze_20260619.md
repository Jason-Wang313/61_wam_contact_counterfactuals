# Paper 61 Protocol Freeze

Date: 2026-06-19

Status: frozen before final v5 evaluation.

This document freezes the final Paper 61 expanded-standard evaluation. After this point, no method constants, branch library entries, stress splits, metrics, or reporting gates may be changed based on final results. Only documented bug fixes are allowed, and any bug fix requires rerunning the affected final suite from scratch.

## Compute Constraints

- CPU-only.
- Keep RAM light.
- Thread caps:
  - `OMP_NUM_THREADS=1`;
  - `OPENBLAS_NUM_THREADS=1`;
  - `MKL_NUM_THREADS=1`;
  - `NUMEXPR_NUM_THREADS=1`.
- Final runner workers: `2`.
- Final runner chunksize: `2`.
- MuJoCo models and data buffers may be cached within each worker process.

## Final Main Suite

Seeds: `8`

Episodes per seed/split/method: `20`

Splits:

- `nominal`;
- `low_friction`;
- `high_friction`;
- `heavy_object`;
- `light_object`;
- `observation_noise`;
- `actuation_noise`;
- `target_shift`;
- `contact_offset`;
- `combined_shift`;
- `adversarial_low_friction_heavy`.

Methods:

- `random_push`;
- `nominal_single_branch_mpc`;
- `ensemble_mean_mpc`;
- `domain_randomized_mpc`;
- `adaptive_id_mpc`;
- `robust_worst_case_mpc`;
- `robust_mean_hybrid_mpc`;
- `branch_counterfactual_mpc`;
- `branch_counterfactual_mpc_v5`;
- `oracle_hidden_params`.

Main rows: `8 * 20 * 11 * 10 = 17,600`.

## Final Ablation Suite

Seeds: `8`

Episodes per seed/method on `combined_shift`: `20`

Ablation methods:

- `branch_counterfactual_mpc_v5`;
- `branch_counterfactual_mpc`;
- `no_diagnostic_push`;
- `no_branch_reweighting`;
- `mean_risk_instead_of_tail`;
- `no_information_gain_term`;
- `no_conservative_fallback`;
- `one_branch_only`;
- `reduced_branch_library`.

Ablation rows: `8 * 20 * 9 = 1,440`.

## Frozen Command

```powershell
python src\run_experiment.py --seeds 8 --episodes 20 --workers 2 --chunksize 2
python scripts\analyze_mujoco_results.py
```

## Metrics

Primary:

- success rate;
- final distance;
- normalized progress.

Paired primary comparisons:

- proposed `branch_counterfactual_mpc_v5` versus every non-oracle baseline;
- proposed versus oracle as an upper-bound gap.

Diagnostics:

- final posterior entropy;
- mean posterior entropy;
- final near-true branch mass;
- mean near-true branch mass;
- branch prediction error;
- fallback activation count.

Statistical reporting:

- 95% normal-approximation confidence intervals;
- bootstrap confidence intervals for paired success and distance deltas;
- sign-flip paired p-values;
- per-seed summaries;
- oracle regret tables.

## Frozen Decision Rule

Set `ICLR_MAIN_TARGET_READY` only if all of the following are true:

- final v5 results are reproducible from the frozen command;
- `branch_counterfactual_mpc_v5` clearly beats ensemble, domain-randomized, adaptive-ID, robust worst-case, and robust-mean hybrid baselines on the predefined primary splits or supports a sharply narrower claim;
- ablations show that diagnostic information gain, posterior reweighting, and fallback behavior materially contribute;
- low-friction and adversarial shifts are either improved or honestly bounded by the identifiability theory;
- the 25+ page manuscript reports all predefined results, including ties and failures;
- citations are clickable and displayed with bright boxes;
- final `C:/Users/wangz/Downloads/61.pdf` is 25+ pages and matches `paper/main.pdf`;
- no numbered Paper 61 PDF is placed on the visible Desktop.

Otherwise:

- use `STRONG_REVISE` if the result is useful but not ICLR-main-ready;
- use `KILL_ARCHIVE` if the final evidence invalidates the central contribution.
