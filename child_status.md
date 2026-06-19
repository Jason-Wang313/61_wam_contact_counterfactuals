# Child Status 61

Current stage: expanded v5 submission-grade rebuild terminal
Last update: 2026-06-19 18:41:51 +08:00
PDF: C:/Users/wangz/Downloads/61.pdf
GitHub: https://github.com/Jason-Wang313/61_wam_contact_counterfactuals
Submission-hardening version: v5 expanded frozen protocol
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence: v5 frozen evaluation completed with 17,600 main rows and 1,440 ablation rows, a 25-page ICLR-style PDF, VLA-v4 green/red boxed clickable link styling, generated result tables, posterior diagnostics, paired bootstrap/sign-flip analysis, oracle regret, and Downloads-only artifact validation.

Reason: the expanded method improves the low-friction split over several collapsed-belief baselines, but it fails the hostile-review acceptance gate. Branch v5 has positive success deltas in only 18/55 strong-baseline paired comparisons, positive distance improvements in only 19/55, loses badly on high-friction and nominal robust-MPC comparisons, and the ablation gate fails because several removed-component variants outperform the full method. The honest terminal state is STRONG_REVISE, not ICLR-main-ready.

PDF SHA256: 13E9C60E063E2A6F2C18C61FC07E9E8B274077462D66D73EDABFF297DF6784EB
