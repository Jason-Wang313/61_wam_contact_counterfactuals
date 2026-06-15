# Paper 61 Terminal Audit

Date: 2026-06-15

Paper: `61_wam_contact_counterfactuals`

Decision: `STRONG_REVISE`

ICLR-main ready: no

## Commands Executed

- `python -m py_compile src\run_experiment.py scripts\analyze_mujoco_results.py`
- `python scripts\analyze_mujoco_results.py`
- CSV finite/schema audit over `results/mujoco_contact_raw.csv`, `results/mujoco_contact_metrics.csv`, `results/mujoco_contact_pairwise.csv`, `results/mujoco_contact_ablation.csv`, `results/mujoco_contact_seed_metrics.csv`, and `results/negative_cases.csv`
- `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` in `paper`
- `Copy-Item paper\main.pdf C:\Users\wangz\Downloads\61.pdf -Force`

## Verified Evidence

- Real MuJoCo contact-pushing benchmark is implemented in `src/run_experiment.py`.
- Main evidence contains 2,400 paired rows: 5 stress splits, 5 seeds, 16 episodes per seed/split/method, and 6 methods.
- Ablation evidence contains 480 rows on the combined-shift split.
- Baselines include random push, nominal single-branch MPC, ensemble mean MPC, robust worst-case MPC, and oracle hidden-parameter MPC.
- Analysis regenerates paired statistics and figures from the checked-in CSV outputs.
- The rebuilt PDF is `C:/Users/wangz/Downloads/61.pdf`.
- `C:/Users/wangz/Desktop/61.pdf` is absent.

## Blocking Results

The proposed branch counterfactual MPC is not a clear ICLR-main result:

- Against ensemble mean MPC, branch MPC ties on nominal, low-friction, high-friction, and heavy-object splits, and loses on combined shift.
- Against robust worst-case MPC, branch MPC wins on nominal/heavy-object but loses on low-friction/high-friction and is statistically indistinguishable on combined shift.
- Low-friction success remains far below the oracle hidden-parameter planner: branch `0.113 +/- 0.070`, robust `0.150 +/- 0.079`, oracle `0.537 +/- 0.110`.
- Combined-shift ablations do not isolate the claimed mechanism: reduced branch library and no-branch-reweighting variants are competitive with or better than the proposed method on success.

## Gate Decision

This paper satisfies the local evidence-package requirements for a serious `STRONG_REVISE`: high-fidelity simulator evidence, paired baselines, ablations, stress splits, uncertainty, hostile prior-work pressure, limitations, reproducible code, rebuilt PDF, and public repository.

It does not satisfy the ICLR-main-ready bar because the central method is not decisively better than strong non-oracle baselines and the ablations do not validate branch reweighting as the decisive mechanism.

Required revival work:

- learned branch inference rather than handcrafted branches;
- public manipulation benchmark or robot validation;
- stronger tactile/contact policy baselines;
- statistically significant wins over ensemble and robust MPC;
- manual full-paper related-work synthesis and qualitative failure analysis.
