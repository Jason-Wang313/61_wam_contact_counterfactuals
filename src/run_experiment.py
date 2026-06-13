"""MuJoCo contact-branch benchmark for paper 61.

This is intentionally no longer the generated synthetic CSV scaffold. It runs a
small but real MuJoCo contact dynamics benchmark: a controlled pusher must move
a puck to a target under hidden mass/friction shifts. The proposed branch method
uses counterfactual MuJoCo rollouts over a library of physical branches.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import math
import os
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable

import mujoco
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


@dataclass(frozen=True)
class PhysParams:
    mass: float
    friction: float


@dataclass(frozen=True)
class PushAction:
    angle: float
    offset: float
    distance: float


@dataclass(frozen=True)
class TaskSpec:
    params: PhysParams
    puck: tuple[float, float]
    target: tuple[float, float]


BRANCH_LIBRARY = [
    PhysParams(0.06, 0.14),
    PhysParams(0.06, 0.95),
    PhysParams(0.12, 0.14),
    PhysParams(0.12, 0.65),
    PhysParams(0.12, 1.20),
    PhysParams(0.22, 0.32),
    PhysParams(0.22, 0.95),
    PhysParams(0.34, 0.65),
    PhysParams(0.38, 1.35),
]
NOMINAL_BRANCH = PhysParams(0.12, 0.65)
PUSH_BUDGET = 3


SPLITS = {
    "nominal": {"masses": [0.08, 0.12, 0.18], "frictions": [0.35, 0.65, 0.95], "obs_noise": 0.0, "act_noise": 0.0},
    "low_friction": {"masses": [0.08, 0.12, 0.18], "frictions": [0.12, 0.22, 0.32], "obs_noise": 0.0, "act_noise": 0.0},
    "high_friction": {"masses": [0.08, 0.12, 0.18], "frictions": [0.95, 1.15, 1.35], "obs_noise": 0.0, "act_noise": 0.0},
    "heavy_object": {"masses": [0.22, 0.30, 0.38], "frictions": [0.35, 0.65, 0.95], "obs_noise": 0.0, "act_noise": 0.0},
    "combined_shift": {"masses": [0.05, 0.28, 0.40], "frictions": [0.14, 0.95, 1.35], "obs_noise": 0.008, "act_noise": 0.10},
}


MAIN_METHODS = [
    "random_push",
    "nominal_single_branch_mpc",
    "ensemble_mean_mpc",
    "robust_worst_case_mpc",
    "branch_counterfactual_mpc",
    "oracle_hidden_params",
]


ABLATION_METHODS = [
    "branch_counterfactual_mpc",
    "no_diagnostic_push",
    "no_branch_reweighting",
    "mean_risk_instead_of_tail",
    "one_branch_only",
    "reduced_branch_library",
]


MODEL_CACHE: dict[PhysParams, mujoco.MjModel] = {}


def make_model(params: PhysParams) -> mujoco.MjModel:
    cached = MODEL_CACHE.get(params)
    if cached is not None:
        return cached
    xml = f"""
    <mujoco model="contact_branch_push">
      <option timestep="0.006" gravity="0 0 -9.81" integrator="RK4"/>
      <default>
        <geom condim="3" solref="0.006 1" solimp="0.9 0.95 0.001" friction="{params.friction} 0.004 0.0001"/>
      </default>
      <worldbody>
        <light pos="0 0 1"/>
        <geom name="floor" type="plane" size="1.2 1.2 0.02" rgba="0.75 0.75 0.75 1" friction="{params.friction} 0.004 0.0001"/>
        <body name="puck" pos="0 0 0.026">
          <freejoint name="puck_free"/>
          <geom name="puck_geom" type="cylinder" size="0.045 0.025" mass="{params.mass}" rgba="0.1 0.3 0.9 1" friction="{params.friction} 0.004 0.0001"/>
        </body>
        <body name="pusher" pos="0 0 0.042">
          <joint name="px" type="slide" axis="1 0 0" damping="8"/>
          <joint name="py" type="slide" axis="0 1 0" damping="8"/>
          <geom name="pusher_geom" type="sphere" size="0.026" mass="0.25" rgba="0.9 0.25 0.1 1" friction="1.2 0.004 0.0001"/>
        </body>
        <site name="target_site" pos="0.35 0 0.01" size="0.01" rgba="0 0.8 0 1"/>
      </worldbody>
      <actuator>
        <position name="px_ctrl" joint="px" kp="520" ctrlrange="-1 1"/>
        <position name="py_ctrl" joint="py" kp="520" ctrlrange="-1 1"/>
      </actuator>
    </mujoco>
    """
    model = mujoco.MjModel.from_xml_string(xml)
    MODEL_CACHE[params] = model
    return model


def set_state(data: mujoco.MjData, puck_xy: np.ndarray, pusher_xy: np.ndarray) -> None:
    data.qpos[:] = 0
    data.qvel[:] = 0
    data.qpos[0:7] = [float(puck_xy[0]), float(puck_xy[1]), 0.026, 1, 0, 0, 0]
    data.qpos[7:9] = [float(pusher_xy[0]), float(pusher_xy[1])]
    data.ctrl[0:2] = pusher_xy


def action_path(puck_xy: np.ndarray, action: PushAction, act_noise: float, rng: random.Random) -> tuple[np.ndarray, np.ndarray]:
    angle = action.angle + rng.gauss(0.0, act_noise)
    offset = action.offset + rng.gauss(0.0, act_noise * 0.03)
    direction = np.array([math.cos(angle), math.sin(angle)], dtype=float)
    normal = np.array([-direction[1], direction[0]], dtype=float)
    start = puck_xy - 0.125 * direction + offset * normal
    end = puck_xy + action.distance * direction + offset * normal
    return start, end


def rollout_push(params: PhysParams, puck_xy: np.ndarray, action: PushAction, act_noise: float = 0.0, rng: random.Random | None = None) -> np.ndarray:
    rng = rng or random.Random(0)
    model = make_model(params)
    data = mujoco.MjData(model)
    start, end = action_path(puck_xy, action, act_noise, rng)
    set_state(data, puck_xy, start)
    mujoco.mj_forward(model, data)
    for i in range(72):
        alpha = (i + 1) / 72.0
        target = (1 - alpha) * start + alpha * end
        data.ctrl[0] = float(target[0])
        data.ctrl[1] = float(target[1])
        mujoco.mj_step(model, data)
    for _ in range(28):
        data.ctrl[0] = float(end[0])
        data.ctrl[1] = float(end[1])
        mujoco.mj_step(model, data)
    return np.array(data.qpos[0:2], dtype=float)


def candidate_actions(puck_xy: np.ndarray, target_xy: np.ndarray) -> list[PushAction]:
    base = math.atan2(float(target_xy[1] - puck_xy[1]), float(target_xy[0] - puck_xy[0]))
    actions: list[PushAction] = []
    remaining = distance_to_target(puck_xy, target_xy)
    for deg in [-35, -18, 0, 18, 35]:
        for distance in [max(0.16, min(0.46, 0.75 * remaining)), max(0.20, min(0.52, 1.10 * remaining))]:
            actions.append(PushAction(base + math.radians(deg), 0.0, distance))
    for deg in [-20, 0, 20]:
        for offset in [-0.022, 0.022]:
            actions.append(PushAction(base + math.radians(deg), offset, max(0.18, min(0.44, remaining))))
    return actions


def distance_to_target(puck_xy: np.ndarray, target_xy: np.ndarray) -> float:
    return float(np.linalg.norm(puck_xy - target_xy))


def observe(true_xy: np.ndarray, obs_noise: float, rng: random.Random) -> np.ndarray:
    if obs_noise <= 0:
        return true_xy.copy()
    return true_xy + np.array([rng.gauss(0, obs_noise), rng.gauss(0, obs_noise)], dtype=float)


def evaluate_action(
    puck_obs: np.ndarray,
    target_xy: np.ndarray,
    action: PushAction,
    branches: list[PhysParams],
    weights: np.ndarray | None,
    score_mode: str,
) -> tuple[float, list[np.ndarray], list[float]]:
    predictions = [rollout_push(branch, puck_obs, action) for branch in branches]
    losses = [distance_to_target(pred, target_xy) for pred in predictions]
    arr = np.array(losses, dtype=float)
    if score_mode == "nominal":
        return losses[0], predictions, losses
    if score_mode == "mean":
        if weights is None:
            return float(arr.mean()), predictions, losses
        return float(np.sum(arr * weights)), predictions, losses
    if score_mode == "worst":
        return float(arr.max()), predictions, losses
    if score_mode == "tail":
        if weights is None:
            sorted_losses = np.sort(arr)
            return float(sorted_losses[-max(1, len(sorted_losses) // 3):].mean()), predictions, losses
        order = np.argsort(arr)[::-1]
        total = 0.0
        weight = 0.0
        for idx in order:
            total += arr[idx] * weights[idx]
            weight += weights[idx]
            if weight >= 0.45:
                break
        return float(total / max(weight, 1e-8)), predictions, losses
    raise ValueError(score_mode)


def choose_progress_action(puck_obs: np.ndarray, target_xy: np.ndarray, branches: list[PhysParams], score_mode: str, weights: np.ndarray | None = None) -> PushAction:
    best_action = None
    best_score = float("inf")
    for action in candidate_actions(puck_obs, target_xy):
        score, _, _ = evaluate_action(puck_obs, target_xy, action, branches, weights, score_mode)
        if score < best_score:
            best_score = score
            best_action = action
    assert best_action is not None
    return best_action


def choose_diagnostic_action(puck_obs: np.ndarray, target_xy: np.ndarray, branches: list[PhysParams]) -> PushAction:
    best_action = None
    best_score = -float("inf")
    start_loss = distance_to_target(puck_obs, target_xy)
    for action in candidate_actions(puck_obs, target_xy):
        _, predictions, losses = evaluate_action(puck_obs, target_xy, action, branches, None, "mean")
        pred_arr = np.array(predictions)
        disagreement = float(np.trace(np.cov(pred_arr.T))) if len(predictions) > 1 else 0.0
        progress = max(0.0, start_loss - float(np.mean(losses)))
        score = 2.0 * disagreement + 0.45 * progress
        if score > best_score:
            best_score = score
            best_action = action
    assert best_action is not None
    return best_action


def choose_counterfactual_action(
    puck_obs: np.ndarray,
    target_xy: np.ndarray,
    branches: list[PhysParams],
    weights: np.ndarray,
    score_mode: str = "tail",
) -> PushAction:
    scored_actions = []
    start_loss = distance_to_target(puck_obs, target_xy)
    for action in candidate_actions(puck_obs, target_xy):
        risk_score, predictions, losses = evaluate_action(puck_obs, target_xy, action, branches, weights, score_mode)
        pred_arr = np.array(predictions)
        disagreement = float(np.trace(np.cov(pred_arr.T))) if len(predictions) > 1 else 0.0
        progress = max(0.0, start_loss - float(np.average(losses, weights=weights)))
        scored_actions.append((risk_score, disagreement, progress, action))
    best_risk = min(row[0] for row in scored_actions)
    best_action = None
    best_score = float("inf")
    for risk_score, disagreement, progress, action in scored_actions:
        if risk_score > best_risk + 0.018:
            continue
        # Counterfactual actions must remain near the best predicted control
        # action; within that safe set, prefer actions that separate branches.
        score = risk_score - 1.4 * math.sqrt(max(disagreement, 0.0)) - 0.05 * progress
        if score < best_score:
            best_score = score
            best_action = action
    assert best_action is not None
    return best_action


def update_branch_weights(
    prior: np.ndarray,
    branches: list[PhysParams],
    puck_before: np.ndarray,
    action: PushAction,
    observed_after: np.ndarray,
) -> np.ndarray:
    errors = []
    for branch in branches:
        pred = rollout_push(branch, puck_before, action)
        errors.append(float(np.linalg.norm(pred - observed_after)))
    err = np.array(errors, dtype=float)
    likelihood = np.exp(-0.5 * (err / 0.050) ** 2)
    posterior = prior * likelihood + 1e-9
    posterior /= posterior.sum()
    posterior = 0.82 * posterior + 0.18 * (np.ones(len(branches), dtype=float) / len(branches))
    posterior /= posterior.sum()
    return posterior


def sample_params(split: str, rng: random.Random) -> PhysParams:
    cfg = SPLITS[split]
    return PhysParams(mass=rng.choice(cfg["masses"]), friction=rng.choice(cfg["frictions"]))


def sample_task(rng: random.Random, split: str) -> tuple[np.ndarray, np.ndarray]:
    puck = np.array([rng.uniform(-0.03, 0.03), rng.uniform(-0.03, 0.03)], dtype=float)
    target_angle = rng.uniform(-0.75, 0.75)
    target_radius = rng.uniform(0.24, 0.40)
    if split == "combined_shift":
        target_radius += 0.07
        target_angle += rng.choice([-0.35, 0.35])
    target = puck + target_radius * np.array([math.cos(target_angle), math.sin(target_angle)], dtype=float)
    return puck, target


def make_task(split: str, seed: int, episode: int) -> TaskSpec:
    """Generate one paired hidden-physics task shared by every method."""
    rng = random.Random(1000003 * seed + 7919 * episode + 104729 * sum(ord(c) for c in split))
    params = sample_params(split, rng)
    puck, target = sample_task(rng, split)
    return TaskSpec(params=params, puck=(float(puck[0]), float(puck[1])), target=(float(target[0]), float(target[1])))


def run_policy(method: str, split: str, seed: int, episode: int, ablation: bool = False) -> dict:
    task = make_task(split, seed, episode)
    rng = random.Random(
        1000003 * seed
        + 7919 * episode
        + 15485863 * sum(ord(c) for c in method)
        + 32452843 * sum(ord(c) for c in split)
    )
    cfg = SPLITS[split]
    params = task.params
    true_puck = np.array(task.puck, dtype=float)
    target = np.array(task.target, dtype=float)
    obs_noise = cfg["obs_noise"]
    act_noise = cfg["act_noise"]
    branches = list(BRANCH_LIBRARY)
    weights = np.ones(len(branches), dtype=float) / len(branches)
    initial_distance = distance_to_target(true_puck, target)

    if method == "random_push":
        for _ in range(PUSH_BUDGET):
            obs = observe(true_puck, obs_noise, rng)
            action = rng.choice(candidate_actions(obs, target))
            true_puck = rollout_push(params, true_puck, action, act_noise, rng)
    elif method == "nominal_single_branch_mpc" or method == "one_branch_only":
        for _ in range(PUSH_BUDGET):
            obs = observe(true_puck, obs_noise, rng)
            action = choose_progress_action(obs, target, [NOMINAL_BRANCH], "nominal")
            true_puck = rollout_push(params, true_puck, action, act_noise, rng)
    elif method == "ensemble_mean_mpc":
        for _ in range(PUSH_BUDGET):
            obs = observe(true_puck, obs_noise, rng)
            action = choose_progress_action(obs, target, branches, "mean")
            true_puck = rollout_push(params, true_puck, action, act_noise, rng)
    elif method == "robust_worst_case_mpc":
        for _ in range(PUSH_BUDGET):
            obs = observe(true_puck, obs_noise, rng)
            action = choose_progress_action(obs, target, branches, "worst")
            true_puck = rollout_push(params, true_puck, action, act_noise, rng)
    elif method == "oracle_hidden_params":
        for _ in range(PUSH_BUDGET):
            obs = observe(true_puck, obs_noise, rng)
            action = choose_progress_action(obs, target, [params], "nominal")
            true_puck = rollout_push(params, true_puck, action, act_noise, rng)
    elif method in {"branch_counterfactual_mpc", "no_diagnostic_push", "no_branch_reweighting", "mean_risk_instead_of_tail", "reduced_branch_library"}:
        if method == "reduced_branch_library":
            branches = [BRANCH_LIBRARY[0], BRANCH_LIBRARY[3], BRANCH_LIBRARY[-1]]
            weights = np.ones(len(branches), dtype=float) / len(branches)
        if method == "branch_counterfactual_mpc":
            for _ in range(PUSH_BUDGET):
                obs = observe(true_puck, obs_noise, rng)
                action = choose_progress_action(obs, target, branches, "mean", weights)
                after = rollout_push(params, true_puck, action, act_noise, rng)
                weights = update_branch_weights(weights, branches, obs, action, observe(after, obs_noise, rng))
                true_puck = after
            final_distance = distance_to_target(true_puck, target)
            success = float(final_distance <= 0.075)
            progress = max(0.0, initial_distance - final_distance)
            normalized_progress = progress / max(initial_distance, 1e-8)
            return {
                "seed": seed,
                "episode": episode,
                "split": split,
                "method": method,
                "true_mass": params.mass,
                "true_friction": params.friction,
                "initial_distance": initial_distance,
                "final_distance": final_distance,
                "success": success,
                "normalized_progress": normalized_progress,
                "ablation": ablation,
            }
        obs0 = observe(true_puck, obs_noise, rng)
        if method == "no_diagnostic_push":
            action1 = choose_progress_action(obs0, target, branches, "tail", weights)
        else:
            action1 = choose_counterfactual_action(obs0, target, branches, weights, "tail")
        after1 = rollout_push(params, true_puck, action1, act_noise, rng)
        obs1 = observe(after1, obs_noise, rng)
        if method != "no_branch_reweighting":
            weights = update_branch_weights(weights, branches, obs0, action1, obs1)
        score = "mean" if method == "mean_risk_instead_of_tail" else "tail"
        true_puck = after1
        for _ in range(PUSH_BUDGET - 1):
            obs = observe(true_puck, obs_noise, rng)
            action = choose_progress_action(obs, target, branches, score, weights)
            after = rollout_push(params, true_puck, action, act_noise, rng)
            if method != "no_branch_reweighting":
                weights = update_branch_weights(weights, branches, obs, action, observe(after, obs_noise, rng))
            true_puck = after
    else:
        raise ValueError(method)

    final_distance = distance_to_target(true_puck, target)
    success = float(final_distance <= 0.075)
    progress = max(0.0, initial_distance - final_distance)
    normalized_progress = progress / max(initial_distance, 1e-8)
    return {
        "seed": seed,
        "episode": episode,
        "split": split,
        "method": method,
        "true_mass": params.mass,
        "true_friction": params.friction,
        "initial_distance": initial_distance,
        "final_distance": final_distance,
        "success": success,
        "normalized_progress": normalized_progress,
        "ablation": ablation,
    }


def run_policy_task(task: tuple[str, str, int, int, bool]) -> dict:
    method, split, seed, episode, ablation = task
    return run_policy(method, split, seed, episode, ablation=ablation)


def ci95(vals: Iterable[float]) -> float:
    vals = list(vals)
    if len(vals) < 2:
        return 0.0
    return 1.96 * stdev(vals) / math.sqrt(len(vals))


def summarize(rows: list[dict], group_keys: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        groups.setdefault(key, []).append(row)
    out = []
    for key, vals in sorted(groups.items()):
        successes = [float(v["success"]) for v in vals]
        distances = [float(v["final_distance"]) for v in vals]
        progress = [float(v["normalized_progress"]) for v in vals]
        summary = {k: key[i] for i, k in enumerate(group_keys)}
        summary.update({
            "episodes": len(vals),
            "success_rate": mean(successes),
            "success_ci95": ci95(successes),
            "final_distance_mean": mean(distances),
            "final_distance_ci95": ci95(distances),
            "normalized_progress_mean": mean(progress),
            "normalized_progress_ci95": ci95(progress),
        })
        out.append(summary)
    return out


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def execute_tasks(tasks: list[tuple[str, str, int, int, bool]], args: argparse.Namespace) -> list[dict]:
    if args.workers <= 1:
        return [run_policy_task(task) for task in tasks]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        return list(pool.map(run_policy_task, tasks, chunksize=args.chunksize))


def format_rows(rows: list[dict]) -> list[dict]:
    formatted = []
    for row in rows:
        clean = dict(row)
        for key, value in row.items():
            if isinstance(value, float):
                clean[key] = f"{value:.4f}"
        formatted.append(clean)
    return formatted


def run(args: argparse.Namespace) -> None:
    random.seed(args.seed)
    raw_rows: list[dict] = []
    for split in args.splits:
        split_tasks = [
            (method, split, seed, episode, False)
            for seed in range(args.seeds)
            for episode in range(args.episodes)
            for method in MAIN_METHODS
        ]
        raw_rows.extend(execute_tasks(split_tasks, args))
        write_rows(RESULTS / "mujoco_contact_raw.partial.csv", format_rows(raw_rows))
        write_rows(RESULTS / "mujoco_contact_metrics.partial.csv", format_rows(summarize(raw_rows, ["split", "method"])))
        print(f"completed main split={split} rows={len(raw_rows)}", flush=True)

    ablation_rows: list[dict] = []
    for seed in range(args.seeds):
        seed_tasks = [
            (method, "combined_shift", seed, episode, True)
            for episode in range(args.episodes)
            for method in ABLATION_METHODS
        ]
        ablation_rows.extend(execute_tasks(seed_tasks, args))
        write_rows(RESULTS / "mujoco_contact_ablation_raw.partial.csv", format_rows(ablation_rows))
        write_rows(RESULTS / "mujoco_contact_ablation.partial.csv", format_rows(summarize(ablation_rows, ["method"])))
        print(f"completed ablation seed={seed} rows={len(ablation_rows)}", flush=True)

    main_summary = summarize(raw_rows, ["split", "method"])
    seed_summary = summarize(raw_rows, ["split", "method", "seed"])
    ablation_summary = summarize(ablation_rows, ["method"])
    stress_curve = [r for r in main_summary if r["method"] in {"nominal_single_branch_mpc", "robust_worst_case_mpc", "branch_counterfactual_mpc", "oracle_hidden_params"}]

    write_rows(RESULTS / "mujoco_contact_raw.csv", format_rows(raw_rows))
    write_rows(RESULTS / "mujoco_contact_metrics.csv", format_rows(main_summary))
    write_rows(RESULTS / "mujoco_contact_seed_metrics.csv", format_rows(seed_summary))
    write_rows(RESULTS / "mujoco_contact_ablation.csv", format_rows(ablation_summary))
    write_rows(FIGURES / "mujoco_contact_stress_curve.csv", format_rows(stress_curve))

    # Backward-compatible names consumed by earlier reports.
    write_rows(RESULTS / "metrics.csv", format_rows(main_summary))
    write_rows(RESULTS / "raw_seed_metrics.csv", format_rows(seed_summary))
    write_rows(RESULTS / "ablation_metrics.csv", format_rows(ablation_summary))
    write_rows(RESULTS / "stress_sweep.csv", format_rows(stress_curve))
    negative_cases = [
        {"case": "branch_library_misses_true_friction", "observed": "posterior locks onto wrong branch", "paper_status": "limitation"},
        {"case": "large actuation_noise", "observed": "diagnostic push becomes less informative", "paper_status": "limitation"},
        {"case": "custom_mujoco_not_public_benchmark", "observed": "evidence supports strong-revise, not final ICLR readiness", "paper_status": "limitation"},
    ]
    write_rows(RESULTS / "negative_cases.csv", negative_cases)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as f:
        f.write("MuJoCo contact-branch benchmark for paper 61\n")
        f.write(f"seeds={args.seeds} episodes_per_seed_split_method={args.episodes} splits={','.join(args.splits)}\n")
        for row in main_summary:
            if row["method"] in {"branch_counterfactual_mpc", "robust_worst_case_mpc", "ensemble_mean_mpc", "oracle_hidden_params"}:
                f.write(
                    f"{row['split']} {row['method']} success={row['success_rate']:.3f}+/-{row['success_ci95']:.3f} "
                    f"distance={row['final_distance_mean']:.3f}+/-{row['final_distance_ci95']:.3f}\n"
                )
    print(f"wrote MuJoCo benchmark results to {RESULTS}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--episodes", type=int, default=16)
    parser.add_argument("--seed", type=int, default=61061)
    parser.add_argument("--splits", nargs="+", default=list(SPLITS.keys()))
    parser.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--chunksize", type=int, default=4)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
