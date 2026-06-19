# 61 WAM Contact Counterfactuals

Submission-hardening version: v5 expanded frozen-protocol rebuild.

Terminal decision: STRONG_REVISE for ICLR main conference.

This repository contains a real CPU-only MuJoCo contact-pushing benchmark, branch-counterfactual MPC variants, strong MPC baselines, stress splits, ablations, posterior diagnostics, bootstrap/sign-flip paired statistics, generated LaTeX result tables, and a 25-page ICLR-style manuscript. The result is scientifically useful but not ICLR-main ready: Branch v5 improves low-friction behavior but does not consistently beat ensemble, adaptive-ID, robust worst-case, or robust-mean MPC, and ablations do not isolate the claimed mechanism.

## Evidence Summary

- Main frozen run: 8 seeds, 20 episodes per seed/split/method.
- Main rows: 17,600.
- Ablation rows: 1,440.
- Splits: nominal, low friction, high friction, heavy object, light object, observation noise, actuation noise, target shift, contact offset, combined shift, adversarial low-friction/heavy-object.
- Baselines: random push, nominal single-branch MPC, ensemble mean MPC, domain-randomized MPC, adaptive-ID MPC, robust worst-case MPC, robust-mean hybrid MPC, legacy branch MPC, oracle hidden-parameter MPC.
- Strong-baseline paired gate: failed, with positive Branch v5 success deltas in 18/55 strong-baseline comparisons.
- Ablation gate: failed, with Branch v5 winning/tieing only 1/8 removed-component ablations on success and distance.
- Terminal state: STRONG_REVISE, not submission ready.

## Reproduce

```powershell
python src\run_experiment.py --seeds 8 --episodes 20 --workers 2 --chunksize 2
python scripts\analyze_mujoco_results.py
python scripts\summarize_final_decision.py
```

If a long run exits after partial split output, resume without changing the frozen protocol:

```powershell
python src\run_experiment.py --seeds 8 --episodes 20 --workers 2 --chunksize 2 --resume
```

## Build PDF

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_submission_pdf.ps1
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/61.pdf`

PDF SHA256: `D9E85F35B6ABA1705C47A36944E59E6A195BD5830385869ECACC37ABC5FA4886`

GitHub: https://github.com/Jason-Wang313/61_wam_contact_counterfactuals
