# Submission Readiness Decision

Decision: STRONG_REVISE.

ICLR main-conference readiness: NO.

Submission-hardening version: v4 real MuJoCo rebuild.

Reason: the paper now has real high-fidelity MuJoCo evidence, implemented baselines, ablations, stress tests, and uncertainty summaries. However, the proposed adaptive branch MPC does not clearly outperform ensemble mean MPC or robust worst-case MPC, and the combined-shift ablations do not isolate the proposed mechanism strongly enough. Low-friction performance also remains far below the oracle hidden-parameter planner.

Honest terminal action: do not submit to ICLR main in this form. Keep as a strong-revise empirical scaffold.

Revival condition: add learned branch inference, external robotics benchmarks or hardware, stronger tactile/contact baselines, and statistically significant gains over ensemble and robust MPC.
