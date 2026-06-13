# Reproducibility Checklist

## What Reproduces

- [x] `python src/run_experiment.py --seeds 5 --episodes 16 --workers 4 --chunksize 4`
- [x] `python scripts/analyze_mujoco_results.py`
- [x] `results/mujoco_contact_raw.csv`
- [x] `results/mujoco_contact_metrics.csv`
- [x] `results/mujoco_contact_seed_metrics.csv`
- [x] `results/mujoco_contact_ablation.csv`
- [x] `results/mujoco_contact_pairwise.csv`
- [x] `figures/mujoco_success_by_split.png`
- [x] `figures/mujoco_final_distance_by_split.png`
- [x] `figures/mujoco_ablation_distance.png`
- [x] `paper/main.tex`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/61.pdf`

## What Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] External benchmark results.
- [ ] Learned WAM checkpoints.
- [ ] Learned branch-inference model.
- [ ] Human/manual full-paper related-work annotations.

This is reproducible as a real MuJoCo strong-revise paper, not as an ICLR-main-ready robotics system.
