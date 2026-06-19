# Final Audit

Date: 2026-06-19 12:50:18 +08:00

1. Chosen thesis: WAM Contact Counterfactuals tests whether branch-structured planning for latent contact dynamics improves closed-loop contact pushing by preserving unobserved physical alternatives until contact observations update a posterior.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v5 expanded frozen protocol.
4. Evidence: real MuJoCo contact-pushing benchmark with 17,600 main rows and 1,440 ablation rows.
5. Main result: Branch v5 improves low-friction behavior relative to several collapsed baselines, but fails the hostile strong-baseline gate: only 18/55 positive strong-baseline success deltas and 19/55 positive distance improvements.
6. Ablation result: failed mechanism isolation. Branch v5 wins/ties only 1/8 ablations on success and distance; several removed-component variants outperform the full method.
7. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, and `docs/hostile_reviewer_response.md`.
8. Reproducibility: code, CSVs, paired stats, bootstrap/sign-flip analysis, oracle regret, posterior diagnostics, generated LaTeX tables, and PDF reproduce locally.
9. Claim-validity status: not ICLR-main ready; strong empirical scaffold retained with honest negative evidence.
10. Exact Downloads PDF path: `C:/Users/wangz/Downloads/61.pdf`
11. PDF pages: 25.
12. PDF SHA256: `D9E85F35B6ABA1705C47A36944E59E6A195BD5830385869ECACC37ABC5FA4886`
13. GitHub URL: https://github.com/Jason-Wang313/61_wam_contact_counterfactuals
14. Confirmation: no visible Desktop copy was requested or made.

## 2026-06-19 Expanded Rebuild Audit

Executed `docs/paper61_expanded_submission_plan_20260619.md` and froze the final protocol in `docs/paper61_protocol_freeze_20260619.md`.

Additional verification:

- Python compile passed for `src/run_experiment.py`, `scripts/analyze_mujoco_results.py`, `scripts/render_latex_tables.py`, `scripts/summarize_final_decision.py`, and `scripts/validate_submission_artifacts.py`.
- Frozen final run completed with expected row counts.
- `scripts/analyze_mujoco_results.py` regenerated paired statistics, oracle regret, posterior diagnostics, and figures from final MuJoCo CSV outputs.
- `scripts/summarize_final_decision.py` assigned STRONG_REVISE from predefined gates.
- `scripts/build_submission_pdf.ps1` rebuilt the PDF and copied only `C:/Users/wangz/Downloads/61.pdf`.
- `scripts/validate_submission_artifacts.py` passed row-count, page-count, Downloads-match, and Desktop-absence gates.
- Bright boxed clickable citations are enabled through `hyperref` boxed border settings in `paper/main.tex`.

Decision remains `STRONG_REVISE`, not ICLR-main-ready. See `docs/paper61_final_v5_evidence_summary.md`.
