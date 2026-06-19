# Paper 61 Expanded Submission Plan

Date: 2026-06-19

Paper: `61_wam_contact_counterfactuals`

Target: rebuild Paper 61 from a compact v4 `STRONG_REVISE` MuJoCo audit into a genuine 25+ page ICLR-main-target submission package if, and only if, the evidence honestly supports that bar. If the expanded evidence still does not support the central claim, keep the terminal decision as `STRONG_REVISE` or downgrade to `KILL_ARCHIVE` with precise evidence.

This plan must be completed before experiment edits, final evaluation runs, or manuscript expansion beyond planning notes.

## Starting Evidence

- Current manuscript: `paper/main.pdf`, 4 pages.
- Current numbered artifact: `C:/Users/wangz/Downloads/61.pdf`, 4 pages.
- Current terminal state: `STRONG_REVISE`.
- Current benchmark: real direct-MuJoCo contact pushing with hidden puck mass/friction, paired tasks, stress splits, baselines, ablations, and uncertainty summaries.
- Current main limitation: branch counterfactual MPC improves over random/nominal MPC but mostly ties ensemble mean MPC and does not consistently beat robust worst-case MPC.
- Current ablation limitation: no-branch-reweighting and reduced-branch-library variants are competitive with the proposed method on combined shift, so the mechanism is not isolated.
- Current low-friction limitation: large gap to oracle hidden-parameter MPC, suggesting poor identifiability or inadequate branch coverage.

## Non-Negotiable Standards

- No filler. A 25+ page PDF is required, but every added page must contain theory, implementation detail, real results, diagnostics, failure analysis, prior-work positioning, reproducibility detail, or honest limitations.
- CPU-only. Keep RAM light with single-threaded numeric libraries, small process pools, chunked result writes, and incremental analysis.
- Do not optimize for pretty results. Optimize for a result that survives hostile review.
- Use strong baselines and stress tests to expose weaknesses, improve the method during development, then freeze the final protocol and report all predefined results honestly.
- Final claims must follow the evidence. If the method fails strong baselines or ablations do not isolate the mechanism, the paper must not be labeled ICLR-main-ready.
- Numbered PDFs must live in Downloads only. Do not copy numbered PDFs to the visible Desktop.

## Development Phase

Use this phase to improve the method and analysis before the protocol is frozen. Development results may guide method design but must not be mixed with the final frozen evaluation table.

### Method Work

1. Add explicit branch-posterior diagnostics:
   - posterior entropy after each push;
   - posterior mass assigned to near-true physical branches;
   - diagnostic displacement disagreement across branch predictions;
   - realized branch prediction error.

2. Add an information-gain diagnostic planner:
   - score first-push candidates by expected posterior entropy reduction plus safe progress;
   - keep diagnostic actions inside a bounded regret/safety set relative to best progress action;
   - expose coefficients through named constants or CLI arguments.

3. Add a conservative adaptive fallback:
   - if posterior entropy remains high or low-friction ambiguity is unresolved, fall back to robust or robust-mean hybrid planning;
   - record which fallback was activated and how often;
   - treat fallback usage as evidence, not a hidden implementation detail.

4. Expand branch coverage without heavy compute:
   - include light/medium/heavy mass and very-low/low/nominal/high friction branches;
   - keep the library small enough for CPU-only runs;
   - include a reduced-library ablation to test whether coverage matters.

5. Preserve current strong baselines and add at least two stronger controls if feasible:
   - domain-randomized MPC with unweighted branch rollouts;
   - adaptive system-identification MPC that picks the maximum-likelihood branch after each observation;
   - robust-mean hybrid MPC as a risk interpolation baseline.

### Development Tests

- Use a small development suite only:
  - seeds: existing 0-4;
  - episodes: small enough to iterate quickly;
  - splits: low friction, combined shift, nominal.
- Development may change method constants, branch library, and diagnostics.
- Record every material method change in `docs/paper61_development_log.md`.
- Do not use development results as final ICLR evidence.

## Protocol Freeze

Before final evaluation, create `docs/paper61_protocol_freeze_20260619.md` containing:

- exact methods;
- exact baselines;
- exact ablations;
- exact stress splits;
- exact seeds and episodes;
- exact metrics;
- exact statistical tests;
- exact success criteria;
- exact compute/RAM constraints;
- exact manuscript decision rule.

After this freeze, do not tune methods, branch libraries, thresholds, coefficients, or metrics based on final results. Bug fixes are allowed only if documented with a before/after note and rerun from scratch.

## Frozen Evaluation Suite

The final suite should be larger than v4 while remaining CPU/RAM-light.

### Main Splits

Evaluate at least these splits:

- nominal;
- low friction;
- high friction;
- heavy object;
- light object;
- observation noise;
- actuation noise;
- target shift;
- contact offset;
- combined shift;
- adversarial low-friction/heavy-object shift.

### Main Methods

Evaluate at least:

- random push;
- nominal single-branch MPC;
- ensemble mean MPC;
- domain-randomized MPC;
- adaptive system-identification MPC;
- robust worst-case MPC;
- robust-mean hybrid MPC;
- branch counterfactual MPC v5;
- oracle hidden-parameter MPC.

### Ablations

Evaluate at least:

- full branch counterfactual MPC v5;
- no diagnostic push;
- no branch reweighting;
- mean-risk instead of tail/robust risk;
- no information-gain diagnostic term;
- no conservative fallback;
- reduced branch library;
- one branch only.

### Metrics

Report:

- success rate;
- final distance;
- normalized progress;
- oracle regret;
- success regret against oracle;
- paired success delta against each baseline;
- paired distance improvement against each baseline;
- posterior entropy after each push;
- near-true branch posterior mass;
- branch prediction error;
- fallback activation rate;
- wall-clock runtime per method/split.

### Statistics

Report:

- paired tables by split and baseline;
- 95% confidence intervals;
- bootstrap confidence intervals for paired deltas;
- paired permutation sign tests for success deltas;
- per-seed tables;
- negative-case tables for splits where branch MPC fails or ties strong baselines.

### Minimum Final Run

Target:

- at least 8 seeds if runtime is acceptable;
- at least 20 episodes per seed/split/method if runtime is acceptable;
- workers capped at 1-2 unless memory measurements show safe headroom.

If runtime is too high, preserve breadth first: keep all methods/splits and reduce episodes only enough to complete CPU-only final evaluation. Document the final choice in the freeze file.

## Theory Expansion

Add a real theoretical section, not decoration.

Required components:

1. Formal latent-contact problem setup:
   - hidden physical parameter or contact-mode variable;
   - action sequence;
   - observation model;
   - finite-horizon loss;
   - branch posterior.

2. Branch-value decomposition:
   - mean-risk planning;
   - tail-risk/worst-case planning;
   - posterior-weighted branch value;
   - oracle and nominal special cases.

3. Diagnostic-action analysis:
   - define branch-separation value;
   - show how diagnostic actions trade immediate progress for posterior concentration;
   - state conditions under which a diagnostic action can improve the second-stage plan.

4. Negative/identifiability result:
   - formalize when branch MPC cannot outperform ensemble or robust MPC because observations do not distinguish latent branches before the action budget is exhausted;
   - connect this directly to low-friction and combined-shift failures.

5. Acceptance-gate theorem or proposition:
   - state that branch structure is only a contribution when posterior concentration produces statistically detectable gains over ensemble/robust controls;
   - use this to justify honest `STRONG_REVISE` if final evidence remains mixed.

## Manuscript Expansion

The final manuscript must be at least 25 pages and should use ICLR style.

Required structure:

- Abstract;
- Introduction;
- Contributions and evidence gate;
- Related work with hostile positioning;
- Formal problem setup;
- Branch-structured contact planning method;
- Theory and identifiability analysis;
- MuJoCo benchmark;
- Development protocol and frozen final protocol;
- Main results;
- Paired statistical analysis;
- Ablations;
- Stress tests;
- Posterior/diagnostic analysis;
- Failure cases and negative results;
- Runtime and compute analysis;
- Limitations;
- Reproducibility checklist;
- Appendix with derivations, implementation details, full tables, branch library, and additional plots.

## Citation and PDF Requirements

- In-text citations must be clickable and route to the bibliography.
- Citation links must be visually obvious bright boxes, similar to arXiv sample papers.
- Use LaTeX `hyperref` settings with boxed citation borders rather than hidden links.
- Verify no unresolved citations, no unresolved references, and no LaTeX fatal errors.
- Final `paper/main.pdf` must be 25+ pages.
- Final `C:/Users/wangz/Downloads/61.pdf` must match `paper/main.pdf`.
- No `61.pdf` may be copied to `C:/Users/wangz/Desktop`.

## Repository and Status Requirements

Update:

- `child_status.md`;
- `README.md`;
- `docs/final_audit.md`;
- `docs/submission_readiness_decision.md`;
- `docs/experiment_rigor_checklist.md`;
- root `GLOBAL_POOL_STATUS.md`;
- root `BATCH_STATUS.md`;
- root `MASTER_REPORT.md`.

Commit and push to the public repository:

- `https://github.com/Jason-Wang313/61_wam_contact_counterfactuals`

## Terminal Decision Rule

Set `ICLR_MAIN_TARGET_READY` only if all are true:

- the final frozen suite is reproducible;
- the method clearly beats ensemble, domain-randomized, adaptive-ID, and robust baselines on the predefined primary splits or has a sharply justified narrower claim;
- ablations isolate the diagnostic/posterior mechanism;
- low-friction or combined-shift failures are either fixed or honestly bounded by theory and reported as limitations;
- manuscript is 25+ pages of substantive content;
- bright boxed clickable citations are verified;
- Downloads-only numbered PDF is verified;
- GitHub and status ledgers are current.

Otherwise:

- use `STRONG_REVISE` if the work is scientifically useful but not ICLR-main-ready;
- use `KILL_ARCHIVE` if the central mechanism fails and the paper cannot support a defensible contribution.
