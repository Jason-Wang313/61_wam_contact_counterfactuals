"""Render Paper 61 CSV results into LaTeX tables.

The manuscript imports paper/results_tables.tex. This script intentionally
renders broad appendix tables because the expanded submission standard requires
the paper to expose the full frozen protocol, not just attractive aggregates.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"


METHOD_LABELS = {
    "random_push": "Random",
    "nominal_single_branch_mpc": "Nominal",
    "ensemble_mean_mpc": "Ensemble",
    "domain_randomized_mpc": "Domain rand.",
    "adaptive_id_mpc": "Adaptive ID",
    "robust_worst_case_mpc": "Robust",
    "robust_mean_hybrid_mpc": "Robust-mean",
    "branch_counterfactual_mpc": "Branch v4",
    "branch_counterfactual_mpc_v5": "Branch v5",
    "oracle_hidden_params": "Oracle",
    "no_diagnostic_push": "No diagnostic",
    "no_branch_reweighting": "No reweighting",
    "mean_risk_instead_of_tail": "Mean risk",
    "no_information_gain_term": "No info gain",
    "no_conservative_fallback": "No fallback",
    "one_branch_only": "One branch",
    "reduced_branch_library": "Reduced library",
}

SPLIT_LABELS = {
    "nominal": "nominal",
    "low_friction": "low friction",
    "high_friction": "high friction",
    "heavy_object": "heavy object",
    "light_object": "light object",
    "observation_noise": "obs. noise",
    "actuation_noise": "act. noise",
    "target_shift": "target shift",
    "contact_offset": "contact offset",
    "combined_shift": "combined shift",
    "adversarial_low_friction_heavy": "adv. low-fric heavy",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def esc(text: object) -> str:
    s = str(text)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s


def fmt(value: str, digits: int = 3) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "--"


def label(method: str) -> str:
    return METHOD_LABELS.get(method, method.replace("_", " "))


def split_label(split: str) -> str:
    return SPLIT_LABELS.get(split, split.replace("_", " "))


def table_header(caption: str, label_name: str, columns: str, header: str) -> list[str]:
    return [
        r"\begingroup\small",
        r"\begin{longtable}{" + columns + "}",
        r"\caption{" + caption + r"}\label{" + label_name + r"}\\",
        r"\toprule",
        header + r"\\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        header + r"\\",
        r"\midrule",
        r"\endhead",
    ]


def end_table() -> list[str]:
    return [r"\bottomrule", r"\end{longtable}", r"\endgroup", ""]


def render_main_compact(metrics: list[dict[str, str]]) -> list[str]:
    wanted = [
        "ensemble_mean_mpc",
        "adaptive_id_mpc",
        "robust_worst_case_mpc",
        "robust_mean_hybrid_mpc",
        "branch_counterfactual_mpc_v5",
        "oracle_hidden_params",
    ]
    rows = [r for r in metrics if r.get("method") in wanted]
    out = table_header(
        "Frozen main-suite success and distance for the proposed method and strongest comparators. Entries are mean $\\pm$ 95\\% CI over paired episodes.",
        "tab:main-compact",
        "llcc",
        "Split & Method & Success & Final dist.",
    )
    for row in rows:
        success = f"{fmt(row.get('success_rate', ''))} $\\pm$ {fmt(row.get('success_ci95', ''))}"
        dist = f"{fmt(row.get('final_distance_mean', ''))} $\\pm$ {fmt(row.get('final_distance_ci95', ''))}"
        out.append(f"{esc(split_label(row.get('split', '')))} & {esc(label(row.get('method', '')))} & {success} & {dist}\\\\")
    out.extend(end_table())
    return out


def render_full_metrics(metrics: list[dict[str, str]]) -> list[str]:
    out = table_header(
        "Full frozen main-suite aggregate metrics for every split and method.",
        "tab:full-main",
        "llcccc",
        "Split & Method & Episodes & Success & Final dist. & Progress",
    )
    for row in metrics:
        success = f"{fmt(row.get('success_rate', ''))} $\\pm$ {fmt(row.get('success_ci95', ''))}"
        dist = f"{fmt(row.get('final_distance_mean', ''))} $\\pm$ {fmt(row.get('final_distance_ci95', ''))}"
        progress = f"{fmt(row.get('normalized_progress_mean', ''))} $\\pm$ {fmt(row.get('normalized_progress_ci95', ''))}"
        out.append(
            f"{esc(split_label(row.get('split', '')))} & {esc(label(row.get('method', '')))} & "
            f"{esc(row.get('episodes', ''))} & {success} & {dist} & {progress}\\\\"
        )
    out.extend(end_table())
    return out


def render_pairwise(pairwise: list[dict[str, str]]) -> list[str]:
    out = table_header(
        "Paired comparison of Branch v5 against each baseline on identical hidden-physics tasks.",
        "tab:paired",
        "llcccc",
        "Split & Baseline & Pairs & $\\Delta$ success & $\\Delta$ dist. & p(dist.)",
    )
    for row in pairwise:
        out.append(
            f"{esc(split_label(row.get('split', '')))} & {esc(label(row.get('baseline', '')))} & "
            f"{esc(row.get('paired_episodes', ''))} & {fmt(row.get('success_delta_mean', ''))} & "
            f"{fmt(row.get('distance_improvement_mean', ''))} & {fmt(row.get('distance_improvement_signflip_p', ''))}\\\\"
        )
    out.extend(end_table())
    return out


def render_ablation(ablation: list[dict[str, str]]) -> list[str]:
    out = table_header(
        "Frozen combined-shift ablation results.",
        "tab:ablation",
        "lcccc",
        "Method & Episodes & Success & Final dist. & Progress",
    )
    for row in ablation:
        success = f"{fmt(row.get('success_rate', ''))} $\\pm$ {fmt(row.get('success_ci95', ''))}"
        dist = f"{fmt(row.get('final_distance_mean', ''))} $\\pm$ {fmt(row.get('final_distance_ci95', ''))}"
        progress = f"{fmt(row.get('normalized_progress_mean', ''))} $\\pm$ {fmt(row.get('normalized_progress_ci95', ''))}"
        out.append(f"{esc(label(row.get('method', '')))} & {esc(row.get('episodes', ''))} & {success} & {dist} & {progress}\\\\")
    out.extend(end_table())
    return out


def render_posterior(diag: list[dict[str, str]]) -> list[str]:
    rows = [r for r in diag if r.get("method") in {"branch_counterfactual_mpc_v5", "adaptive_id_mpc", "branch_counterfactual_mpc"}]
    out = table_header(
        "Posterior and model-diagnostic summaries for adaptive methods.",
        "tab:posterior",
        "llcccc",
        "Split & Method & Entropy & Near-true mass & Pred. err. & Fallbacks",
    )
    for row in rows:
        out.append(
            f"{esc(split_label(row.get('split', '')))} & {esc(label(row.get('method', '')))} & "
            f"{fmt(row.get('posterior_entropy_final_mean', ''))} & "
            f"{fmt(row.get('near_true_branch_mass_final_mean', ''))} & "
            f"{fmt(row.get('branch_prediction_error_mean_mean', ''))} & "
            f"{fmt(row.get('fallback_activations_mean', ''))}\\\\"
        )
    out.extend(end_table())
    return out


def render_oracle_regret(regret: list[dict[str, str]]) -> list[str]:
    rows = [r for r in regret if r.get("method") in {"branch_counterfactual_mpc_v5", "adaptive_id_mpc", "robust_worst_case_mpc", "robust_mean_hybrid_mpc", "ensemble_mean_mpc"}]
    out = table_header(
        "Oracle regret for primary non-oracle methods.",
        "tab:oracle-regret",
        "llccc",
        "Split & Method & Pairs & Dist. regret & Success regret",
    )
    for row in rows:
        out.append(
            f"{esc(split_label(row.get('split', '')))} & {esc(label(row.get('method', '')))} & "
            f"{esc(row.get('paired_episodes', ''))} & {fmt(row.get('distance_regret_mean', ''))} & "
            f"{fmt(row.get('success_regret_mean', ''))}\\\\"
        )
    out.extend(end_table())
    return out


def render_seed(seed_metrics: list[dict[str, str]]) -> list[str]:
    rows = [r for r in seed_metrics if r.get("method") in {"branch_counterfactual_mpc_v5", "adaptive_id_mpc", "robust_worst_case_mpc", "robust_mean_hybrid_mpc", "ensemble_mean_mpc", "oracle_hidden_params"}]
    out = table_header(
        "Per-seed frozen metrics for primary methods.",
        "tab:per-seed",
        "lllccc",
        "Split & Method & Seed & Success & Final dist. & Progress",
    )
    for row in rows:
        out.append(
            f"{esc(split_label(row.get('split', '')))} & {esc(label(row.get('method', '')))} & {esc(row.get('seed', ''))} & "
            f"{fmt(row.get('success_rate', ''))} & {fmt(row.get('final_distance_mean', ''))} & "
            f"{fmt(row.get('normalized_progress_mean', ''))}\\\\"
        )
    out.extend(end_table())
    return out


def main() -> None:
    metrics = read_csv(RESULTS / "mujoco_contact_metrics.csv")
    pairwise = read_csv(RESULTS / "mujoco_contact_pairwise.csv")
    ablation = read_csv(RESULTS / "mujoco_contact_ablation.csv")
    posterior = read_csv(RESULTS / "posterior_diagnostics.csv")
    oracle = read_csv(RESULTS / "oracle_regret.csv")
    seed_metrics = read_csv(RESULTS / "mujoco_contact_seed_metrics.csv")

    lines = [
        "% Auto-generated by scripts/render_latex_tables.py. Do not edit by hand.",
        r"\section{Frozen Quantitative Results}",
        r"\label{app:frozen-results}",
        "",
        r"These tables are generated directly from the frozen CSV outputs. Empty entries indicate diagnostics that do not apply to a non-adaptive method.",
        "",
    ]
    if metrics:
        lines.extend(render_main_compact(metrics))
        lines.extend(render_full_metrics(metrics))
    if pairwise:
        lines.extend(render_pairwise(pairwise))
    if ablation:
        lines.extend(render_ablation(ablation))
    if posterior:
        lines.extend(render_posterior(posterior))
    if oracle:
        lines.extend(render_oracle_regret(oracle))
    if seed_metrics:
        lines.extend(render_seed(seed_metrics))
    if not metrics:
        lines.append(r"\paragraph{Pending final run.} The frozen result tables have not yet been generated.")

    (PAPER / "results_tables.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {PAPER / 'results_tables.tex'}")


if __name__ == "__main__":
    main()
