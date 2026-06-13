# 61 WAM Contact Counterfactuals

Submission-hardening version: v4 real MuJoCo rebuild.

Terminal decision: STRONG_REVISE for ICLR main conference.

This repository now contains a real MuJoCo contact-pushing benchmark, paired baselines, stress splits, ablations, uncertainty summaries, and generated figures. The result is not ICLR-main ready: adaptive branch MPC beats random and nominal MPC in several regimes, but it does not clearly dominate ensemble or robust MPC and the low-friction/oracle gap remains large.

## Evidence Summary

- Main run: 5 seeds, 16 episodes per seed/split/method.
- Splits: nominal, low friction, high friction, heavy object, combined shift.
- Baselines: random push, nominal single-branch MPC, ensemble mean MPC, robust worst-case MPC, oracle hidden-parameter MPC.
- Ablations: no diagnostic push, no branch reweighting, mean-risk variant, one-branch-only, reduced branch library.
- Terminal state: strong revise, not submission ready.

## Reproduce

```powershell
python src\run_experiment.py --seeds 5 --episodes 16 --workers 4 --chunksize 4
python scripts\analyze_mujoco_results.py
```

## Build PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/61.pdf`

GitHub: https://github.com/Jason-Wang313/61_wam_contact_counterfactuals
