"""Post-process Paper 61 MuJoCo results into paired statistics and figures."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PROPOSED = "branch_counterfactual_mpc"
BASELINES = [
    "random_push",
    "nominal_single_branch_mpc",
    "ensemble_mean_mpc",
    "robust_worst_case_mpc",
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
            out.append(
                {
                    "split": split,
                    "baseline": baseline,
                    "paired_episodes": len(paired),
                    "success_delta_mean": f"{mean(success_delta):.4f}",
                    "success_delta_ci95": f"{ci95(success_delta):.4f}",
                    "distance_improvement_mean": f"{mean(distance_delta):.4f}",
                    "distance_improvement_ci95": f"{ci95(distance_delta):.4f}",
                    "progress_delta_mean": f"{mean(progress_delta):.4f}",
                    "progress_delta_ci95": f"{ci95(progress_delta):.4f}",
                    "branch_wins_distance": sum(1 for v in distance_delta if v > 0),
                    "branch_losses_distance": sum(1 for v in distance_delta if v < 0),
                }
            )
    return out


def plot_main(metrics: list[dict]) -> None:
    methods = [
        "nominal_single_branch_mpc",
        "ensemble_mean_mpc",
        "robust_worst_case_mpc",
        PROPOSED,
        "oracle_hidden_params",
    ]
    labels = ["Nominal", "Ensemble", "Robust", "Branch", "Oracle"]
    splits = sorted({row["split"] for row in metrics})
    x = list(range(len(splits)))
    width = 0.15

    plt.figure(figsize=(12, 4.8))
    for idx, method in enumerate(methods):
        vals = [
            float(next(row["success_rate"] for row in metrics if row["split"] == split and row["method"] == method))
            for split in splits
        ]
        plt.bar([v + (idx - 2) * width for v in x], vals, width=width, label=labels[idx])
    plt.xticks(x, splits, rotation=20, ha="right")
    plt.ylabel("Success rate")
    plt.ylim(0, 1.02)
    plt.title("MuJoCo contact-pushing success by stress split")
    plt.legend(ncol=5, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "mujoco_success_by_split.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 4.8))
    for idx, method in enumerate(methods):
        vals = [
            float(next(row["final_distance_mean"] for row in metrics if row["split"] == split and row["method"] == method))
            for split in splits
        ]
        plt.bar([v + (idx - 2) * width for v in x], vals, width=width, label=labels[idx])
    plt.xticks(x, splits, rotation=20, ha="right")
    plt.ylabel("Final distance to target (m)")
    plt.title("MuJoCo contact-pushing final error by stress split")
    plt.legend(ncol=5, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "mujoco_final_distance_by_split.png", dpi=180)
    plt.close()


def plot_ablation(ablation: list[dict]) -> None:
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
    ablation = read_csv(RESULTS / "mujoco_contact_ablation.csv")
    write_csv(RESULTS / "mujoco_contact_pairwise.csv", paired_stats(raw))
    write_csv(RESULTS / "pairwise_stats.csv", paired_stats(raw))
    plot_main(metrics)
    plot_ablation(ablation)
    print("wrote paired stats and figures")


if __name__ == "__main__":
    main()
