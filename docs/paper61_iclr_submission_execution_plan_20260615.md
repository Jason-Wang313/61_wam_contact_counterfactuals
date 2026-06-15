# Paper 61 ICLR-Main Execution Plan

Date: 2026-06-15

Goal: determine whether `61_wam_contact_counterfactuals` can honestly be upgraded from `STRONG_REVISE` to an ICLR-main-target submission, or reaffirm a terminal non-ready decision with current evidence.

## Execution Gates

1. Reproducibility gate:
   - Compile `src/run_experiment.py`.
   - Re-run `scripts/analyze_mujoco_results.py` from existing CSV outputs to regenerate paired statistics and figures.
   - Confirm all CSV result values are finite and required columns are present.

2. Evidence gate:
   - Confirm the benchmark is a real MuJoCo contact-pushing task rather than synthetic tables.
   - Confirm multiple seeds, paired episodes, stress splits, uncertainty estimates, and ablations exist.
   - Confirm the method is compared against random, nominal MPC, ensemble mean MPC, robust worst-case MPC, and oracle hidden-parameter MPC.

3. ICLR-main claim gate:
   - Require the proposed branch MPC to clearly beat strong non-oracle baselines across stress splits.
   - Require ablations to isolate the proposed branch-reweighting/counterfactual mechanism.
   - Require hostile prior-work pressure, honest limitations, and reproducible release artifacts.

4. Artifact gate:
   - Rebuild the PDF with LaTeX.
   - Copy only the numbered PDF to `C:/Users/wangz/Downloads/61.pdf`.
   - Confirm no numbered Paper 61 PDF exists on the visible Desktop.
   - Confirm the GitHub repository is public and pushed.

## Decision Rule

Upgrade to ICLR-main-ready only if every ICLR-main claim gate is supported by current evidence. If the method still ties or loses to ensemble/robust MPC, or if ablations do not identify the claimed mechanism, keep the terminal state as `STRONG_REVISE` and document the blockers precisely.
