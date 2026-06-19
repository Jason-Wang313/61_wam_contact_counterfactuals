"""Summarize the frozen Paper 61 v5 results against the readiness gate."""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PROPOSED = "branch_counterfactual_mpc_v5"
STRONG_BASELINES = [
    "ensemble_mean_mpc",
    "domain_randomized_mpc",
    "adaptive_id_mpc",
    "robust_worst_case_mpc",
    "robust_mean_hybrid_mpc",
]
EXPECTED_MAIN_ROWS = 17600
EXPECTED_ABLATION_ROWS = 1440


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def f(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "nan"))
    except ValueError:
        return float("nan")


def method_label(method: str) -> str:
    return method.replace("_", " ")


def main() -> None:
    raw = read_csv(RESULTS / "mujoco_contact_raw.csv")
    ablation_raw = read_csv(RESULTS / "mujoco_contact_ablation_raw.csv")
    metrics = read_csv(RESULTS / "mujoco_contact_metrics.csv")
    pairwise = read_csv(RESULTS / "mujoco_contact_pairwise.csv")
    ablation = read_csv(RESULTS / "mujoco_contact_ablation.csv")
    posterior = read_csv(RESULTS / "posterior_diagnostics.csv")

    row_gate = len(raw) == EXPECTED_MAIN_ROWS and len(ablation_raw) == EXPECTED_ABLATION_ROWS

    strong_rows = [r for r in pairwise if r.get("baseline") in STRONG_BASELINES]
    strong_success = [f(r, "success_delta_mean") for r in strong_rows]
    strong_distance = [f(r, "distance_improvement_mean") for r in strong_rows]
    positive_success = sum(1 for v in strong_success if v > 0.0)
    positive_distance = sum(1 for v in strong_distance if v > 0.0)
    total_strong = len(strong_rows)

    ablation_by_method = {r["method"]: r for r in ablation}
    proposed_ablation = ablation_by_method.get(PROPOSED, {})
    proposed_success = f(proposed_ablation, "success_rate")
    proposed_distance = f(proposed_ablation, "final_distance_mean")
    ablation_wins = 0
    ablation_compared = 0
    for method, row in ablation_by_method.items():
        if method == PROPOSED:
            continue
        ablation_compared += 1
        if proposed_success >= f(row, "success_rate") and proposed_distance <= f(row, "final_distance_mean"):
            ablation_wins += 1

    split_metrics = [r for r in metrics if r.get("method") == PROPOSED]
    proposed_mean_success = mean([f(r, "success_rate") for r in split_metrics]) if split_metrics else float("nan")

    strict_pair_gate = total_strong > 0 and positive_success >= int(0.75 * total_strong) and positive_distance >= int(0.75 * total_strong)
    ablation_gate = ablation_compared > 0 and ablation_wins >= int(0.75 * ablation_compared)
    ready = row_gate and strict_pair_gate and ablation_gate

    decision = "ICLR_MAIN_TARGET_READY" if ready else "STRONG_REVISE"
    if row_gate and total_strong > 0 and positive_success == 0 and positive_distance == 0:
        decision = "KILL_ARCHIVE"

    lines = [
        "# Paper 61 Final v5 Evidence Summary",
        "",
        f"Decision: {decision}",
        "",
        "## Row Gates",
        "",
        f"- Main rows: {len(raw)} / {EXPECTED_MAIN_ROWS}",
        f"- Ablation rows: {len(ablation_raw)} / {EXPECTED_ABLATION_ROWS}",
        f"- Row gate passed: {row_gate}",
        "",
        "## Strong-Baseline Gate",
        "",
        f"- Strong paired comparisons: {total_strong}",
        f"- Positive success deltas: {positive_success}",
        f"- Positive distance improvements: {positive_distance}",
        f"- Mean proposed success across splits: {proposed_mean_success:.4f}",
        f"- Strong-baseline gate passed: {strict_pair_gate}",
        "",
        "## Ablation Gate",
        "",
        f"- Ablations compared: {ablation_compared}",
        f"- Proposed wins or ties on success and distance: {ablation_wins}",
        f"- Ablation gate passed: {ablation_gate}",
        "",
        "## Strong Paired Rows",
        "",
        "| Split | Baseline | Success delta | Distance improvement | p(distance) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in strong_rows:
        lines.append(
            f"| {row.get('split','')} | {method_label(row.get('baseline',''))} | "
            f"{row.get('success_delta_mean','')} | {row.get('distance_improvement_mean','')} | "
            f"{row.get('distance_improvement_signflip_p','')} |"
        )

    lines.extend([
        "",
        "## Posterior Diagnostics",
        "",
        "| Split | Method | Entropy | Near-true mass | Prediction error | Fallbacks |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for row in posterior:
        if row.get("method") in {PROPOSED, "adaptive_id_mpc", "branch_counterfactual_mpc"}:
            lines.append(
                f"| {row.get('split','')} | {method_label(row.get('method',''))} | "
                f"{row.get('posterior_entropy_final_mean','')} | "
                f"{row.get('near_true_branch_mass_final_mean','')} | "
                f"{row.get('branch_prediction_error_mean_mean','')} | "
                f"{row.get('fallback_activations_mean','')} |"
            )

    output = DOCS / "paper61_final_v5_evidence_summary.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"decision={decision}")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
