# ICLR Main Gate

Paper: 61 wam_contact_counterfactuals

Previous v3 decision: KILL_ARCHIVE.

v4 gate verdict: STRONG_REVISE.

ICLR main ready: no.

Evidence digest: real MuJoCo contact-pushing benchmark with 5 seeds, 5 stress splits, 6 main methods, paired tasks, ablations, confidence intervals, and figures.

Remaining blockers:
- Proposed branch MPC does not clearly dominate ensemble mean MPC.
- Proposed branch MPC does not consistently beat robust worst-case MPC.
- Low-friction split exposes a large oracle gap.
- Combined-shift ablations do not isolate branch reweighting as the decisive mechanism.
- No real robot, external benchmark, learned WAM checkpoint, or manual full-paper related-work synthesis.

The only honest main-conference-safe decision is STRONG_REVISE, not submission ready.
