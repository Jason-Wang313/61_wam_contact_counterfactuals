# Experiment Rigor Checklist

## v5 Expanded Frozen-Protocol Rigor

- [x] High-fidelity MuJoCo contact benchmark.
- [x] Paired hidden-physics tasks across methods.
- [x] Multiple seeds: 8.
- [x] Episodes per split/method: 160.
- [x] Main rows: 17,600.
- [x] Ablation rows: 1,440.
- [x] Confidence intervals.
- [x] Bootstrap paired intervals.
- [x] Paired sign-flip tests.
- [x] Oracle regret.
- [x] Posterior diagnostics.
- [x] Implemented strong baselines.
- [x] Ablations.
- [x] Stress tests.
- [x] Negative cases and limitations.
- [x] Frozen protocol before final evaluation.
- [x] 25-page manuscript with substantive theory/results appendix.
- [x] Clickable bright-box citation links.
- [x] Downloads-only numbered PDF validation.

## ICLR Main Bar

- [ ] Clear statistical win over ensemble, adaptive-ID, robust worst-case, and robust-mean MPC.
- [ ] Ablations isolate the proposed diagnostic/posterior/fallback mechanism.
- [ ] Real-robot validation.
- [ ] External manipulation benchmark.
- [ ] Learned WAM or learned branch inference.
- [ ] Manual full-paper related-work synthesis beyond local pool artifacts.

Decision: STRONG_REVISE. The evidence is real and much stronger than v4, but the mechanism is not decisive enough for ICLR main.
