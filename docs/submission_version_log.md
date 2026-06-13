# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Replaced the toy experiment with seven-seed synthetic metrics, stronger synthetic baselines, ablations, stress tests, and negative cases.
- Narrowed claims to synthetic diagnostic evidence.
- Recompiled canonical PDF at `C:/Users/wangz/Downloads/61.pdf`.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied the stricter ICLR-main-conference standard.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats were not recoverable from local artifacts.
- Recompiled the canonical PDF with `Submission-hardening version: v3`.
- Terminal decision: KILL_ARCHIVE.

## v4 - Real MuJoCo Rebuild

- Added concrete rebuild plan.
- Replaced synthetic scaffold with real MuJoCo contact-pushing benchmark.
- Added paired hidden-physics tasks, 5 seeds, 16 episodes per split/method, five stress splits, implemented baselines, ablations, paired statistics, and figures.
- Added checkpointed low-RAM runner with per-split worker pools.
- Rewrote paper and docs around the actual evidence.
- Terminal decision: STRONG_REVISE.
