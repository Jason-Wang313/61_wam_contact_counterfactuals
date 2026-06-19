# Submission Readiness Decision

Decision: STRONG_REVISE.

ICLR main-conference readiness: NO.

Submission-hardening version: v5 expanded frozen-protocol rebuild.

Reason: the paper now has a 25-page ICLR-style manuscript, real MuJoCo evidence, expanded theory, frozen protocol, strong baselines, stress tests, ablations, posterior diagnostics, paired bootstrap/sign-flip statistics, oracle regret, and verified Downloads-only PDF artifacts. However, the proposed Branch v5 method does not survive the hostile strong-baseline gate. It has positive success deltas in only 18/55 strong-baseline comparisons and positive distance improvements in only 19/55. The ablation gate also fails because removed-component variants often outperform the full method.

Honest terminal action: do not submit to ICLR main in this form. Keep as a strong-revise empirical scaffold with useful negative evidence.

Revival condition: redesign the diagnostic/fallback mechanism so the full method beats robust and ensemble/adaptive controls under frozen paired stress tests, isolate the mechanism through ablations, and add external or hardware validation.
