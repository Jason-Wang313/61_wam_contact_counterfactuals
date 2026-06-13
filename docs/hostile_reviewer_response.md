# Hostile Reviewer Response

Paper: 61 WAM Contact Counterfactuals

## Strongest Technical Threats

- Data-Efficient and Contact-Rich Manipulation Through Diffusion Augmentation and Vision-Language Models (2026)
- OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation (2026)
- Learning to Feel the Future: DreamTacVLA for Contact-Rich Manipulation (2025)
- ForceVLA: Enhancing VLA Models with a Force-aware MoE for Contact-rich Manipulation (2025)
- DexViTac: Collecting Human Visuo-Tactile-Kinematic Demonstrations for Contact-Rich Dexterous Manipulation (2026)
- Planning-Guided Diffusion Policy Learning for Generalizable Contact-Rich Bimanual Manipulation (2024)
- FAWAM: Force-Aware World Action Models for Closed-Loop Contact-Rich Manipulation (2026)

## ICLR Main Response

A hostile ICLR reviewer would no longer be correct to reject the paper for having only synthetic evidence. The v4 rebuild contains a real MuJoCo contact-pushing benchmark, paired hidden-physics tasks, implemented baselines, stress splits, ablations, and confidence intervals.

The reviewer would still be correct to reject the paper as an ICLR-main submission because the central mechanism is not decisively validated. Branch MPC mostly ties ensemble mean MPC, does not consistently beat robust worst-case MPC, and remains far from the oracle hidden-parameter planner in low-friction conditions.

## Honest Action

The paper is marked `STRONG_REVISE`. This keeps the real evidence and code, but prevents overclaiming submission readiness.

## What Would Be Needed To Revive

- Learned branch inference rather than a handcrafted branch library.
- Real robot or external manipulation benchmark experiments.
- Stronger tactile/contact baselines.
- Statistically significant gains over ensemble and robust MPC.
- Manual full-paper related-work audit.
- Qualitative rollout and failure analyses.
