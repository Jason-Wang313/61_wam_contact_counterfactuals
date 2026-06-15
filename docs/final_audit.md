# Final Audit

1. Chosen thesis: WAM Contact Counterfactuals explores branch-structured planning for contact-rich manipulation by keeping unobserved physical alternatives explicit until contact observations update them.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.
4. Evidence: real MuJoCo contact-pushing benchmark with 2,400 main rows and 480 ablation rows.
5. Main result: branch MPC beats random and generally improves over nominal single-branch MPC, but mostly ties ensemble MPC and does not consistently beat robust MPC.
6. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, and `docs/hostile_reviewer_response.md`.
7. Reproducibility: code, CSVs, paired stats, figures, and PDF reproduce locally.
8. Claim-validity status: not ICLR-main ready; strong empirical scaffold retained.
9. Exact Downloads PDF path: `C:/Users/wangz/Downloads/61.pdf`
10. GitHub URL: https://github.com/Jason-Wang313/61_wam_contact_counterfactuals
11. Confirmation: no visible Desktop copy was requested or made.

## 2026-06-15 Continuation Audit

Executed `docs/paper61_iclr_submission_execution_plan_20260615.md`.

Additional verification:
- Python compile passed for `src/run_experiment.py` and `scripts/analyze_mujoco_results.py`.
- `scripts/analyze_mujoco_results.py` regenerated paired statistics and figures from existing MuJoCo CSV outputs.
- CSV finite/schema audit passed for main, paired, ablation, seed, and negative-case result files.
- LaTeX/BibTeX/PDF rebuild completed and `C:/Users/wangz/Downloads/61.pdf` was refreshed.
- `C:/Users/wangz/Desktop/61.pdf` is absent.

Decision remains `STRONG_REVISE`, not ICLR-main-ready. See `docs/paper61_terminal_audit_20260615.md`.
