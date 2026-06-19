"""Post-process Paper 61 MuJoCo results into paired statistics and figures."""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PROPOSED = "branch_counterfactual_mpc_v5"
BASELINES = [
    "random_push",
    "nominal_single_branch_mpc",
    "ensemble_mean_mpc",
    "domain_randomized_mpc",
    "adaptive_id_mpc",
    "robust_worst_case_mpc",
    "robust_mean_hybrid_mpc",
    "branch_counterfactual_mpc",
    "oracle_hidden_params",
]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def ci95(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    return 1.96 * stdev(vals) / math.sqrt(len(vals))


def finite(vals: list[float]) -> list[float]:
    return [v for v in vals if math.isfinite(v)]


def bootstrap_ci(vals: list[float], samples: int = 2000) -> tuple[float, float]:
    vals = finite(vals)
    if len(vals) < 2:
        center = vals[0] if vals else float("nan")
        return center, center
    rng = random.Random(61061 + len(vals))
    means = []
    for _ in range(samples):
        draw = [vals[rng.randrange(len(vals))] for _ in vals]
        means.append(mean(draw))
    means.sort()
    return means[int(0.025 * samples)], means[int(0.975 * samples)]


def sign_flip_pvalue(vals: list[float], samples: int = 4000) -> float:
    vals = [v for v in finite(vals) if abs(v) > 1e-12]
    if not vals:
        return 1.0
    observed = abs(mean(vals))
    rng = random.Random(12061 + len(vals))
    extreme = 0
    for _ in range(samples):
        flipped = [v if rng.random() < 0.5 else -v for v in vals]
        if abs(mean(flipped)) >= observed:
            extreme += 1
    return (extreme + 1) / (samples + 1)


def paired_stats(raw: list[dict]) -> list[dict]:
    by_key = {}
    for row in raw:
        key = (row["split"], row["seed"], row["episode"])
        by_key.setdefault(key, {})[row["method"]] = row

    out = []
    for split in sorted({row["split"] for row in raw}):
        split_cases = [(key, methods) for key, methods in by_key.items() if key[0] == split and PROPOSED in methods]
        for baseline in BASELINES:
            paired = [(methods[PROPOSED], methods[baseline]) for _, methods in split_cases if baseline in methods]
            if not paired:
                continue
            success_delta = [float(p["success"]) - float(b["success"]) for p, b in paired]
            distance_delta = [float(b["final_distance"]) - float(p["final_distance"]) for p, b in paired]
            progress_delta = [float(p["normalized_progress"]) - float(b["normalized_progress"]) for p, b in paired]
            success_low, success_high = bootstrap_ci(success_delta)
            distance_low, distance_high = bootstrap_ci(distance_delta)
            out.append(
                {
                    "split": split,
                    "baseline": baseline,
                    "paired_episodes": len(paired),
                    "success_delta_mean": f"{mean(success_delta):.4f}",
                    "success_delta_ci95": f"{ci95(success_delta):.4f}",
                    "success_delta_bootstrap_low": f"{success_low:.4f}",
                    "success_delta_bootstrap_high": f"{success_high:.4f}",
                    "success_delta_signflip_p": f"{sign_flip_pvalue(success_delta):.4f}",
                    "distance_improvement_mean": f"{mean(distance_delta):.4f}",
                    "distance_improvement_ci95": f"{ci95(distance_delta):.4f}",
                    "distance_improvement_bootstrap_low": f"{distance_low:.4f}",
                    "distance_improvement_bootstrap_high": f"{distance_high:.4f}",
                    "distance_improvement_signflip_p": f"{sign_flip_pvalue(distance_delta):.4f}",
                    "progress_delta_mean": f"{mean(progress_delta):.4f}",
                    "progress_delta_ci95": f"{ci95(progress_delta):.4f}",
                    "branch_wins_distance": sum(1 for v in distance_delta if v > 0),
                    "branch_losses_distance": sum(1 for v in distance_delta if v < 0),
                }
            )
    return out


def oracle_regret(raw: list[dict]) -> list[dict]:
    by_key = {}
    for row in raw:
        key = (row["split"], row["seed"], row["episode"])
        by_key.setdefault(key, {})[row["method"]] = row
    out = []
    for split in sorted({row["split"] for row in raw}):
        split_cases = [(key, methods) for key, methods in by_key.items() if key[0] == split and "oracle_hidden_params" in methods]
        methods = sorted({row["method"] for row in raw if row["split"] == split and row["method"] != "oracle_hidden_params"})
        for method in methods:
            paired = [(methods_by_name[method], methods_by_name["oracle_hidden_params"]) for _, methods_by_name in split_cases if method in methods_by_name]
            if not paired:
                continue
            distance_regret = [float(m["final_distance"]) - float(o["final_distance"]) for m, o in paired]
            success_regret = [float(o["success"]) - float(m["success"]) for m, o in paired]
            out.append(
                {
                    "split": split,
                    "method": method,
                    "paired_episodes": len(paired),
                    "distance_regret_mean": f"{mean(distance_regret):.4f}",
                    "distance_regret_ci95": f"{ci95(distance_regret):.4f}",
                    "success_regret_mean": f"{mean(success_regret):.4f}",
                    "success_regret_ci95": f"{ci95(success_regret):.4f}",
                }
            )
    return out


def posterior_diagnostics(raw: list[dict]) -> list[dict]:
    metrics = [
        "posterior_entropy_final",
        "posterior_entropy_mean",
        "near_true_branch_mass_final",
        "near_true_branch_mass_mean",
        "branch_prediction_error_mean",
        "fallback_activations",
    ]
    groups = {}
    for row in raw:
        groups.setdefault((row["split"], row["method"]), []).append(row)
    out = []
    for (split, method), rows in sorted(groups.items()):
        summary = {"split": split, "method": method, "episodes": len(rows)}
        emitted = False
        for metric in metrics:
            vals = []
            for row in rows:
                try:
                    value = float(row.get(metric, "nan"))
                except ValueError:
                    continue
                if math.isfinite(value):
                    vals.append(value)
            if vals:
                summary[f"{metric}_mean"] = f"{mean(vals):.4f}"
                summary[f"{metric}_ci95"] = f"{ci95(vals):.4f}"
                emitted = True
        if emitted:
            out.append(summary)
    return out


def plot_main(metrics: list[dict]) -> None:
    methods = [
        "nominal_single_branch_mpc",
        "ensemble_mean_mpc",
        "adaptive_id_mpc",
        "robust_worst_case_mpc",
        "robust_mean_hybrid_mpc",
        PROPOSED,
        "oracle_hidden_params",
    ]
    labels_by_method = {
        "nominal_single_branch_mpc": "Nominal",
        "ensemble_mean_mpc": "Ensemble",
        "adaptive_id_mpc": "Adaptive-ID",
        "robust_worst_case_mpc": "Robust",
        "robust_mean_hybrid_mpc": "Hybrid",
        PROPOSED: "Branch v5",
        "oracle_hidden_params": "Oracle",
    }
    methods = [method for method in methods if any(row["method"] == method for row in metrics)]
    if not methods:
        return
    splits = sorted({row["split"] for row in metrics})
    x = list(range(len(splits)))
    width = min(0.12, 0.78 / max(1, len(methods)))

    plt.figure(figsize=(12, 4.8))
    for idx, method in enumerate(methods):
        vals = [
            float(next(row["success_rate"] for row in metrics if row["split"] == split and row["method"] == method))
            for split in splits
        ]
        offset = idx - (len(methods) - 1) / 2
        plt.bar([v + offset * width for v in x], vals, width=width, label=labels_by_method[method])
    plt.xticks(x, splits, rotation=20, ha="right")
    plt.ylabel("Success rate")
    plt.ylim(0, 1.02)
    plt.title("MuJoCo contact-pushing success by stress split")
    plt.legend(ncol=min(5, len(methods)), fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "mujoco_success_by_split.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 4.8))
    for idx, method in enumerate(methods):
        vals = [
            float(next(row["final_distance_mean"] for row in metrics if row["split"] == split and row["method"] == method))
            for split in splits
        ]
        offset = idx - (len(methods) - 1) / 2
        plt.bar([v + offset * width for v in x], vals, width=width, label=labels_by_method[method])
    plt.xticks(x, splits, rotation=20, ha="right")
    plt.ylabel("Final distance to target (m)")
    plt.title("MuJoCo contact-pushing final error by stress split")
    plt.legend(ncol=min(5, len(methods)), fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "mujoco_final_distance_by_split.png", dpi=180)
    plt.close()


def plot_ablation(ablation: list[dict]) -> None:
    if not ablation:
        return
    order = sorted(ablation, key=lambda row: float(row["final_distance_mean"]))
    plt.figure(figsize=(9, 4.8))
    plt.barh([row["method"] for row in order], [float(row["final_distance_mean"]) for row in order])
    plt.xlabel("Final distance to target (m)")
    plt.title("Combined-shift ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "mujoco_ablation_distance.png", dpi=180)
    plt.close()


def main() -> None:
    raw = read_csv(RESULTS / "mujoco_contact_raw.csv")
    metrics = read_csv(RESULTS / "mujoco_contact_metrics.csv")
    ablation_path = RESULTS / "mujoco_contact_ablation.csv"
    ablation = read_csv(ablation_path) if ablation_path.exists() else []
    paired = paired_stats(raw)
    write_csv(RESULTS / "mujoco_contact_pairwise.csv", paired)
    write_csv(RESULTS / "pairwise_stats.csv", paired)
    write_csv(RESULTS / "oracle_regret.csv", oracle_regret(raw))
    write_csv(RESULTS / "posterior_diagnostics.csv", posterior_diagnostics(raw))
    plot_main(metrics)
    plot_ablation(ablation)
    print("wrote paired stats and figures")


if __name__ == "__main__":
    main()
