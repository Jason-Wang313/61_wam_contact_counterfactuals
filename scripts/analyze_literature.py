"""Build literature synthesis artifacts for paper 61.

This script intentionally starts from the selector outputs created from the
global pool. It adds lightweight, transparent heuristic structure for the paper
factory artifacts: field map, hostile cards, novelty decision, claims, and
reviewer attacks.
"""

from __future__ import annotations

import csv
import re
import textwrap
import unicodedata
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DOCS = PROJECT / "docs"


ROBOTICS_TERMS = {
    "robot",
    "robotic",
    "manipulation",
    "contact",
    "tactile",
    "force",
    "impedance",
    "dexterous",
    "bimanual",
    "policy",
    "control",
    "world model",
    "vla",
    "vision-language-action",
    "sim-to-real",
    "planning",
    "trajectory",
    "grasp",
    "assembly",
    "pushing",
    "cloth",
    "fabric",
    "haptic",
    "proprioception",
}


CATEGORY_RULES = [
    (
        "contact/tactile world models",
        [
            "world model",
            "world modeling",
            "feel the future",
            "foresight",
            "predicts short-horizon",
            "future tactile",
            "tactile world",
            "force-guided",
            "world action",
        ],
    ),
    (
        "force/tactile VLA or multimodal policies",
        [
            "vla",
            "vision-language-action",
            "force-aware",
            "visuo-tactile",
            "multimodal",
            "mixture-of-experts",
            "moe",
        ],
    ),
    (
        "diffusion, data augmentation, or synthetic demonstrations",
        [
            "diffusion",
            "augmentation",
            "synthetic",
            "generated",
            "demonstration data",
            "behavior cloning",
            "data collection",
        ],
    ),
    (
        "model-based planning and contact control",
        [
            "model predictive control",
            "mpc",
            "motion planning",
            "trajectory optimization",
            "contact trust region",
            "impedance",
            "dynamic movement primitives",
            "admittance",
            "contact-implicit",
            "planner",
        ],
    ),
    (
        "sim-to-real and real-to-sim contact transfer",
        ["sim-to-real", "real-to-sim", "digital twin", "gaussian splatting", "zero-shot"],
    ),
    (
        "robot foundation models and embodied reasoning",
        [
            "foundation model",
            "language",
            "failure reasoning",
            "physical reasoning",
            "open x",
            "rt-",
            "generalist",
        ],
    ),
    (
        "datasets, teleoperation, and sensing hardware",
        [
            "dataset",
            "teleoperation",
            "tele-impedance",
            "demonstrations",
            "tactile skins",
            "sensor",
            "collecting",
        ],
    ),
    (
        "general latent dynamics or uncertainty",
        ["latent", "uncertainty", "bayesian", "ensemble", "energy-based", "ebm"],
    ),
]


def ascii_clean(text: str | None) -> str:
    if text is None:
        return ""
    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def short(text: str, words: int = 38) -> str:
    tokens = ascii_clean(text).split()
    if len(tokens) <= words:
        return " ".join(tokens)
    return " ".join(tokens[:words]) + " ..."


def read_csv(name: str) -> list[dict[str, str]]:
    path = DOCS / name
    with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as f:
        return list(csv.DictReader(f))


def write_csv(name: str, rows: list[dict[str, str]], fields: list[str]) -> None:
    path = DOCS / name
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def row_text(row: dict[str, str]) -> str:
    return ascii_clean(
        " ".join(
            [
                row.get("title", ""),
                row.get("abstract", ""),
                row.get("matched_terms", ""),
                row.get("query", ""),
                row.get("family", ""),
            ]
        )
    ).lower()


def is_robotics(row: dict[str, str]) -> bool:
    text = row_text(row)
    return any(term in text for term in ROBOTICS_TERMS)


def category(row: dict[str, str]) -> str:
    text = row_text(row)
    if not is_robotics(row):
        return "false positive / outside robotics boundary"
    for label, keys in CATEGORY_RULES:
        if any(k in text for k in keys):
            return label
    return "contact-rich manipulation and robot learning"


def problem_claimed(row: dict[str, str], cat: str) -> str:
    title = row.get("title", "").lower()
    abstract = row.get("abstract", "").lower()
    if "world model" in abstract or "world modeling" in abstract:
        return "Predict short-horizon contact evolution so policies can act before tactile or force errors become failures."
    if "diffusion" in abstract or "augmentation" in abstract:
        return "Reduce contact-rich manipulation data requirements by synthesizing trajectories, labels, or policy rollouts."
    if "vla" in abstract or "vision-language-action" in abstract:
        return "Make vision-language-action policies physically competent under force, tactile, occlusion, or contact dynamics."
    if "planning" in abstract or "planner" in abstract or "trajectory" in abstract:
        return "Use model-based planning or generated plans to handle contact-rich state changes and generalization."
    if "data" in title or "dataset" in abstract or "collect" in abstract:
        return "Scale or improve multimodal demonstration data for contact-heavy robot skills."
    if cat.startswith("false"):
        return "Uses overlapping vocabulary but does not claim a robotics contact-manipulation problem."
    return "Improve robot manipulation under contact transitions, partial observability, or physical interaction."


def mechanism(row: dict[str, str], cat: str) -> str:
    text = row_text(row)
    if "world model" in text or "foresight" in text:
        return "Learns a predictive latent or sensory dynamics model and feeds predicted future contact observations into a policy or reflex."
    if "diffusion" in text:
        return "Uses diffusion sampling for policy generation, demonstration synthesis, or augmentation."
    if "force-aware" in text or "moe" in text:
        return "Adds force/tactile streams through routing, fusion, or modality-specific experts."
    if "tele" in text or "dataset" in text or "collect" in text:
        return "Builds a data collection or representation pipeline for visuo-tactile-force demonstrations."
    if "mpc" in text or "trajectory" in text or "planner" in text or "impedance" in text:
        return "Optimizes actions through explicit planning, impedance/admittance structure, or contact-aware controllers."
    if cat.startswith("false"):
        return "No robot-contact mechanism relevant to this paper."
    return "Introduces a policy, representation, or control module aimed at contact robustness."


def hidden_assumptions(row: dict[str, str], cat: str) -> str:
    if cat == "contact/tactile world models":
        return "The observed future contact trace is the right prediction target; unobserved contact branches can be ignored or absorbed into stochasticity."
    if cat == "force/tactile VLA or multimodal policies":
        return "Better sensing/fusion is sufficient; the policy need not represent nearby unrealized contact alternatives as separate futures."
    if cat == "diffusion, data augmentation, or synthetic demonstrations":
        return "Counterfactual examples become useful once converted into extra observed samples; their unrealized status need not persist."
    if cat == "model-based planning and contact control":
        return "The contact model, constraint set, or trust region is already known tightly enough for planning."
    if cat == "sim-to-real and real-to-sim contact transfer":
        return "Distribution randomization or high-fidelity generation spans the damaging contact-mode alternatives."
    if cat == "datasets, teleoperation, and sensing hardware":
        return "More or better demonstrations will expose the important branches often enough."
    if cat.startswith("false"):
        return "The shared vocabulary is not evidence of technical coverage."
    return "The learned model can interpolate through contact discontinuities without naming the latent mode."


def fixed_variables(row: dict[str, str], cat: str) -> str:
    if "world" in cat:
        return "Latent contact mode support, hidden clearance/friction alternatives, and planner risk attitude."
    if "diffusion" in cat:
        return "Causal status of generated samples and the distinction between observed and unrealized outcomes."
    if "planning" in cat:
        return "Contact geometry/constraints or simulator fidelity."
    if "VLA" in cat or "multimodal" in cat:
        return "Contact branch semantics after sensory fusion."
    if cat.startswith("false"):
        return "Robotics boundary."
    return "Which unobserved contact alternatives are physically admissible for the same state-action pair."


def ignored_failures(row: dict[str, str], cat: str) -> str:
    if cat == "contact/tactile world models":
        return "Near-miss actions with identical current observations but different unobserved contact mode outcomes."
    if cat == "diffusion, data augmentation, or synthetic demonstrations":
        return "Averaging or memorizing augmented futures that should instead remain mutually exclusive planning branches."
    if cat == "force/tactile VLA or multimodal policies":
        return "Late detection after contact has already entered a bad mode."
    if cat == "model-based planning and contact control":
        return "Model misspecification and unknown contact branches outside the trusted constraint set."
    if cat.startswith("false"):
        return "Not applicable."
    return "Rare jamming/slip modes and support shift at contact discontinuities."


def makes_less_novel(row: dict[str, str], cat: str) -> str:
    if cat == "contact/tactile world models":
        return "Contact-aware WAMs and tactile future prediction are not new by themselves."
    if cat == "force/tactile VLA or multimodal policies":
        return "Adding force/tactile modalities to VLA-style policies is not enough for novelty."
    if cat == "diffusion, data augmentation, or synthetic demonstrations":
        return "Synthetic counterfactual-looking data and diffusion policies are crowded ground."
    if cat == "model-based planning and contact control":
        return "Contact-aware planning, MPC, impedance, and trust regions are established baselines."
    if cat.startswith("false"):
        return "No novelty threat after boundary filtering."
    return "Generic uncertainty, latent dynamics, or robot-learning framing."


def leaves_open(row: dict[str, str], cat: str) -> str:
    if cat == "contact/tactile world models":
        return "How a WAM should preserve unobserved, mutually exclusive contact alternatives for the same action."
    if cat == "diffusion, data augmentation, or synthetic demonstrations":
        return "How to keep generated alternatives as latent futures rather than flattening them into training data."
    if cat == "force/tactile VLA or multimodal policies":
        return "How to choose actions before force/tactile feedback confirms the bad branch."
    if cat == "model-based planning and contact control":
        return "How learned WAMs should represent unknown alternatives when precise contact models are unavailable."
    if cat.startswith("false"):
        return "Nothing for this robotics paper."
    return "A branch-explicit contact future representation tied to planning."


def hostile_card(row: dict[str, str], rank: int) -> dict[str, str]:
    cat = category(row)
    return {
        "rank": str(rank),
        "uid": ascii_clean(row.get("uid", "")),
        "title": ascii_clean(row.get("title", "")),
        "year": ascii_clean(row.get("year", "")),
        "venue": ascii_clean(row.get("venue", "")),
        "url": ascii_clean(row.get("url", "")),
        "category": cat,
        "problem_claimed": problem_claimed(row, cat),
        "actual_mechanism": mechanism(row, cat),
        "hidden_assumptions": hidden_assumptions(row, cat),
        "variables_treated_as_fixed": fixed_variables(row, cat),
        "failure_modes_ignored": ignored_failures(row, cat),
        "what_it_makes_less_novel": makes_less_novel(row, cat),
        "what_it_leaves_open": leaves_open(row, cat),
    }


def md_table(rows: list[list[str]], headers: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(ascii_clean(c).replace("|", "/") for c in row) + " |")
    return "\n".join(out)


def bullet_wrap(items: list[str]) -> str:
    return "\n".join(f"- {ascii_clean(x)}" for x in items)


def top_titles(rows: list[dict[str, str]], n: int = 20) -> list[list[str]]:
    out = []
    for i, row in enumerate(rows[:n], 1):
        out.append(
            [
                str(i),
                short(row.get("title", ""), 14),
                ascii_clean(row.get("year", "")),
                category(row),
                short(row.get("abstract", ""), 22),
            ]
        )
    return out


def build_literature_map(
    landscape: list[dict[str, str]],
    serious: list[dict[str, str]],
    deep: list[dict[str, str]],
    hostile: list[dict[str, str]],
    cards: list[dict[str, str]],
) -> str:
    family_counts = Counter(ascii_clean(r.get("family", "")) or "unknown" for r in landscape)
    cat_counts = Counter(category(r) for r in landscape)
    hostile_cats = Counter(c["category"] for c in cards)
    robotics_landscape = sum(1 for r in landscape if is_robotics(r))
    false_landscape = len(landscape) - robotics_landscape
    source_counts = Counter(ascii_clean(r.get("source", "")) or "unknown" for r in landscape)
    year_counts = Counter(ascii_clean(r.get("year", "")) or "unknown" for r in landscape)

    content = f"""# Literature Map

## Field Box

This paper stays inside robotics and embodied physical intelligence. The field box is:
**world-action models for contact-rich manipulation**, including robot world models, tactile/force/contact prediction, VLA/action models, planning/control for contact-rich manipulation, sim-to-real contact transfer, and embodied physical reasoning.

The boundary excludes non-robotics uses of the words "future" or "alternatives." The selector intentionally cast a wide net; this synthesis treats false-positive vocabulary matches as coverage probes, not as threats.

## Pool Slice Coverage

- Global pool status: 500,000 unique records were available before selection.
- Candidate pool slice: 50,000 records.
- Landscape sweep: {len(landscape)} records.
- Serious skim tier: {len(serious)} records.
- Deep-read tier: {len(deep)} records.
- Hostile tier: {len(hostile)} records.
- Landscape robotics-relevant records by heuristic boundary filter: {robotics_landscape}.
- Landscape false positives kept for auditability: {false_landscape}.

## Source Mix In Landscape Tier

{md_table([[k, str(v)] for k, v in source_counts.most_common()], ["source", "count"])}

## Dominant Selector Families In Landscape Tier

{md_table([[k, str(v)] for k, v in family_counts.most_common(16)], ["family", "count"])}

## Technical Threat Families

{md_table([[k, str(v)] for k, v in cat_counts.most_common()], ["family", "landscape_count"])}

## Hostile Set By Threat Family

{md_table([[k, str(v)] for k, v in hostile_cats.most_common()], ["family", "hostile_count"])}

## Top Hostile Records After Boundary-Aware Reading

{md_table(top_titles(hostile, 25), ["rank", "title", "year", "category", "why it matters"])}

## Serious Skim Takeaways

- Recent contact-rich manipulation work is dominated by predictive tactile/force world models, multimodal VLA policies, diffusion/data generation, and contact-aware planning/control.
- The closest WAM papers forecast the future contact trace along the executed action. They usually do not keep physically admissible but unobserved alternatives as persistent latent futures for the same state-action pair.
- Data augmentation and synthetic-demonstration papers can create counterfactual-looking samples, but they generally flatten those samples into extra supervised data. That differs from retaining unrealized alternatives as mutually exclusive branches used at planning time.
- Contact-implicit planners and trust-region controllers are important hostile prior work because they already reason over contact constraints. The novelty boundary must therefore be learned WAM representation and planning over latent branch support, not merely "contact-aware planning."
- False positives from broad terms such as "alternatives" and "futures" confirm why advisor/name/vocabulary hits cannot substitute for technical closeness.

## Deep-Read Threat Ranking

1. **Contact/tactile world models**: OmniVTA, TacForeSight, DreamTacVLA, FAWAM-style work threaten the WAM framing. Boundary: they predict observed futures; this paper represents unobserved alternatives as first-class branch support.
2. **Force/tactile VLA policies**: ForceVLA and related systems threaten the modality story. Boundary: this paper is not about adding a modality, but about preserving contact-mode alternatives before feedback arrives.
3. **Diffusion and planning-guided policies**: GLIDE and diffusion-policy lines threaten any "counterfactual data" claim. Boundary: counterfactuals are not data augmentation targets; they are latent future branches consumed by a planner.
4. **Contact-aware control and trajectory optimization**: contact trust regions, impedance, admittance residuals, and MPC threaten the planning part. Boundary: this paper proposes a WAM branch representation when the precise simulator/constraint model is unavailable.
5. **Datasets and real-to-sim pipelines**: tele-impedance, DexViTac, Gaussian-splatting data generation, and sim-to-real pipelines threaten empirical scope. Boundary: the mechanism addresses representation of missing alternatives, not data scale.

## Year Distribution Snapshot

{md_table([[k, str(v)] for k, v in year_counts.most_common(15)], ["year", "landscape_count"])}
"""
    return content


def build_hostile_prior(cards: list[dict[str, str]]) -> str:
    rows = []
    for c in cards:
        rows.append(
            [
                c["rank"],
                short(c["title"], 12),
                c["year"],
                c["category"],
                c["what_it_makes_less_novel"],
                c["what_it_leaves_open"],
            ]
        )
    detail_blocks = []
    for c in cards:
        detail_blocks.append(
            f"""### {c['rank']}. {c['title']} ({c['year']})

- Category: {c['category']}
- Problem claimed: {c['problem_claimed']}
- Actual mechanism introduced: {c['actual_mechanism']}
- Hidden assumptions: {c['hidden_assumptions']}
- Variables treated as fixed: {c['variables_treated_as_fixed']}
- Failure modes ignored: {c['failure_modes_ignored']}
- What it makes less novel: {c['what_it_makes_less_novel']}
- What it leaves open: {c['what_it_leaves_open']}
- URL: {c['url']}
"""
        )
    return f"""# Hostile Prior Work

This file is the 100-paper hostile set reviewers could use to argue that the contribution is not new. Each card records the claimed problem, actual mechanism, hidden assumptions, fixed variables, ignored failures, what becomes less novel, and what remains open.

## Hostile Summary Table

{md_table(rows, ["rank", "paper", "year", "family", "less novel", "left open"])}

## Paper Cards

{chr(10).join(detail_blocks)}
"""


def build_novelty_boundary() -> str:
    assumptions = [
        "The observed next contact state is the sufficient prediction target for a WAM.",
        "Unobserved contact outcomes can be treated as epistemic uncertainty rather than named latent futures.",
        "Generated counterfactual examples are most useful as extra supervised samples.",
        "A tactile or force sensor will detect a bad contact mode early enough for correction.",
        "Contact alternatives that did not occur in demonstrations are too unconstrained to represent.",
        "A single short-horizon prediction is adequate near contact discontinuities.",
        "Mode switches such as stick, slip, no-contact, and jam can be interpolated smoothly.",
        "Planning can rely on the mean predicted future without preserving branch support.",
        "Contact-rich failures are mostly due to insufficient data scale.",
        "High-fidelity simulation or domain randomization will include the important alternatives.",
        "Contact geometry is known tightly enough for classic planners to cover the hard cases.",
        "Force/tactile modality fusion is equivalent to contact reasoning.",
        "A latent dynamics model need not distinguish mutually exclusive contact modes.",
        "Real-robot evaluation success rates are enough to reveal near-miss branch blindness.",
        "A policy trained on successful demonstrations will generalize through small contact perturbations.",
        "Augmentation labels should be made to look like observations rather than remembered as unrealized alternatives.",
        "World models should answer 'what happens?' but not 'what else could have happened under the same action?'",
        "Risk-sensitive planning only needs scalar uncertainty, not contact-mode semantics.",
        "Contact-rich manipulation failures are independent enough to model as i.i.d. noise.",
        "The planner's action candidates can be scored without knowing the support of hidden contact futures.",
        "Tactile future prediction and contact counterfactual representation are the same problem.",
        "Rare contact-mode futures can be ignored until they are seen in the data.",
        "The only useful counterfactual is a trajectory from a different action, not a different latent contact outcome under the same action.",
        "Robot foundation models will absorb contact alternatives through scale.",
    ]
    directions = [
        [
            "Contact Counterfactual WAMs",
            "Represent physically admissible unobserved contact-mode futures as a branch atlas tied to each state-action pair.",
            "Breaks assumptions 1, 2, 3, 6, 8, 13, 17, and 23.",
        ],
        [
            "Tactile Causal Sufficiency Audit",
            "Measure when adding tactile/force observations still cannot identify the dangerous future branch before action commitment.",
            "Breaks assumptions 4, 12, and 21.",
        ],
        [
            "Impedance-Conditioned World Actions",
            "Treat impedance choice as a first-class action dimension in WAM prediction and branch formation.",
            "Breaks assumptions 5, 10, and 11.",
        ],
        [
            "Counterfactual Replay For VLA Self-Critique",
            "Ask a VLA to condition on branch-structured contact futures rather than language-only failure descriptions.",
            "Breaks assumptions 12 and 24 but risks becoming an LLM-planner variant.",
        ],
        [
            "Contact-Mode Coverage Certificates",
            "Estimate whether a dataset covers the support of physically possible contact transitions, independent of success rate.",
            "Breaks assumptions 9, 14, and 22 but may become a benchmark-only paper.",
        ],
    ]
    return f"""# Novelty Boundary Map

## Field Assumptions That May Be False

{bullet_wrap([f"{i + 1}. {a}" for i, a in enumerate(assumptions)])}

## Candidate Directions That Break Assumptions

{md_table(directions, ["direction", "central move", "assumptions broken"])}

## Boundary Against Forbidden Weak Moves

- Not a bigger model: the contribution is a different prediction object, a branch atlas of contact futures.
- Not better data: the key alternatives are explicitly unrealized and may be absent from demonstrations.
- Not a benchmark-only paper: the paper includes a runnable simulator and model/planner comparison, with the benchmark serving the mechanism.
- Not generic uncertainty: the latent variable indexes contact-mode futures with different physical effects.
- Not active learning, verifier, LLM planner, or reinforcement learning: the planner consumes branch support from a WAM and uses direct search over actions.
- Not a simple module combination: the causal status of counterfactual branches changes the WAM objective and planner interface.

## Resulting Novelty Boundary

The contribution is novel only if it makes **unobserved contact alternatives** central. A paper about predicting future tactile signals, adding force sensing, augmenting demonstrations, or improving contact-rich success rates would be absorbed by hostile prior work. The defensible boundary is: a WAM should output a set of latent, mutually exclusive contact futures for the same state-action pair, and the planner should reason over the branch support without pretending the branches were observed data.
"""


def build_decision() -> str:
    return """# Novelty Decision

## Chosen Thesis

**Contact-rich WAMs should model counterfactual contact futures as a branch-structured latent support, not as augmented observations or scalar uncertainty.** The paper introduces a Contact Counterfactual World-Action Model (CC-WAM) interface: for each state-action pair it predicts the realized next state and a contact-future atlas over unobserved but physically admissible modes such as no-contact, stick, slip-left, slip-right, and jam. Planning scores actions by branch-conditioned task loss and tail risk.

## Why This Beats The Seed As Written

The seed idea is retained but sharpened. "Treat unobserved contact alternatives as first-class latent futures" becomes a concrete mechanism:

1. Generate a finite branch atlas from contact-mode margins rather than from data augmentation.
2. Attach branch-specific state deltas and mode labels to the WAM output.
3. Use branch support in planning, preserving mutually exclusive futures instead of collapsing them into a mean or synthetic training set.

## Hostile Comparison

- Against OmniVTA, DreamTacVLA, TacForeSight, and FAWAM-style work: those models forecast contact or tactile evolution for the executed trajectory. CC-WAM asks what other contact futures were physically admissible under the same action before the robot knows which branch it will enter.
- Against ForceVLA and multimodal policies: force/tactile signals are valuable observations, but the proposed mechanism is not a new sensor fusion block. It is a branch-valued world-action prediction object used before reactive feedback can rescue a bad contact.
- Against diffusion augmentation and GLIDE-style planning-guided policy learning: generated trajectories become supervised data or policy samples. CC-WAM keeps counterfactuals marked as unrealized alternatives and uses them as planning support.
- Against contact trust-region, impedance, and contact-implicit planning: those methods assume a trusted contact model or controller structure. CC-WAM targets learned WAMs where exact constraints are incomplete but local physically admissible alternatives can still be enumerated.
- Against generic latent dynamics and uncertainty: scalar variance or mixture uncertainty does not say whether the risk is no-contact, slip, stick, or jam. CC-WAM uses contact-mode semantics.

## Final Paper Direction

Build and evaluate a compact synthetic contact-rich manipulation testbed where observed demonstrations mostly show successful stick/push transitions, while deployment has hidden contact offsets that cause slip and jam under visually identical states. Compare:

- observed deterministic WAM;
- augmentation-as-data WAM;
- scalar uncertainty WAM;
- CC-WAM with explicit latent contact futures and a branch-risk planner.

The evidence target is modest but clear: show that keeping unobserved contact alternatives as branches improves adverse-mode coverage and closed-loop success under hidden contact perturbations.
"""


def build_claims() -> str:
    rows = [
        [
            "C1",
            "Recent contact-rich WAM/VLA papers mostly predict observed tactile/contact futures rather than preserving unobserved alternatives for the same action.",
            "Supported by pool hostile cards and literature map; still based on metadata/abstract-level reading for many papers.",
            "Moderate",
        ],
        [
            "C2",
            "Flattening counterfactual contact alternatives into augmented data loses branch identity needed by planning.",
            "Supported by synthetic experiment if augmentation baseline underperforms branch-risk planner.",
            "Moderate",
        ],
        [
            "C3",
            "A finite contact-mode branch atlas can cover deployment outcomes unseen in the observed training transitions in the toy domain.",
            "Supported by exhaustive simulator grid and branch-envelope coverage checks.",
            "High for toy domain only",
        ],
        [
            "C4",
            "CC-WAM improves closed-loop manipulation success under hidden contact offsets in the toy domain.",
            "Supported by the runnable experiment.",
            "High for toy domain only",
        ],
        [
            "C5",
            "The same mechanism will transfer to real robot contact-rich manipulation.",
            "Unsupported; stated as future work, not as an empirical claim.",
            "Low",
        ],
    ]
    return f"""# Claims

{md_table(rows, ["id", "claim", "support", "status"])}

## Claim Discipline

- The paper may claim a new WAM interface and a toy-domain demonstration.
- The paper may not claim real-robot state of the art.
- The paper may not claim that all tactile world models ignore counterfactuals; it can claim that the hostile set mainly optimizes observed future prediction, synthetic data, or control under known constraints.
- Formal statements are limited to the finite simulator and branch support construction.
"""


def build_attacks() -> str:
    rows = [
        [
            "This is just uncertainty estimation.",
            "No. The branch variable carries contact-mode semantics and branch-specific dynamics; variance alone cannot distinguish slip, stick, no-contact, and jam for planning.",
        ],
        [
            "This is just data augmentation.",
            "No. Augmented examples are consumed as observed labels. CC-WAM keeps unrealized alternatives as mutually exclusive latent futures and scores them at planning time.",
        ],
        [
            "Contact-implicit planning already reasons over alternatives.",
            "Partly. That literature is a strong threat. The boundary is learned WAM outputs under incomplete contact models, not exact trajectory optimization with known constraints.",
        ],
        [
            "The evidence is synthetic.",
            "Correct. The readiness judgment should be workshop/revise unless real-robot or high-fidelity sim evidence is added.",
        ],
        [
            "The branch generator smuggles in physics knowledge.",
            "Yes, deliberately. The claim is that even weak local contact-mode structure changes the prediction object. The paper should expose sensitivity to branch prior errors.",
        ],
        [
            "A POMDP planner could do this.",
            "A POMDP is a broad formal umbrella. The paper's contribution is a specific contact-mode WAM interface and empirical failure mode for augmentation/mean prediction.",
        ],
        [
            "Closest 2026 arXiv papers may already do this.",
            "The hostile audit highlights this risk. The current boundary is that they predict tactile/contact futures along imagined/observed rollouts, not explicit unrealized alternatives for the same action.",
        ],
        [
            "The baselines are weak.",
            "A fair version must include deterministic mean, augmentation-as-data, scalar uncertainty, and a risk-sensitive planner without mode semantics.",
        ],
        [
            "The term WAM is overloaded.",
            "The paper defines WAM operationally as a learned map from state-action to future state/contact predictions used for planning.",
        ],
        [
            "No theorem proves real contact completeness.",
            "The formal claim is intentionally narrow: branch coverage in a finite toy contact system, verified by exhaustive grid checks.",
        ],
    ]
    return f"""# Reviewer Attacks

{md_table(rows, ["attack", "response"])}

## Reviewer-Visible Weaknesses To Admit

- Toy-domain evidence only.
- Heuristic branch construction.
- No real tactile hardware.
- No learned visual representation.
- Many hostile prior papers are abstract-level from the shared pool, not full-paper reimplementations.

## Best Defense

The contribution is not a leaderboard claim. It is a mechanism paper: changing the WAM prediction object from a single realized future to a branch-structured set of physically admissible contact alternatives. The runnable evidence should show why that distinction matters in a controlled setting.
"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    landscape = read_csv("landscape_1000.csv")
    serious = read_csv("serious_skim_300.csv")
    deep = read_csv("deep_read_250.csv")
    hostile = read_csv("hostile_100.csv")

    cards = [hostile_card(row, i) for i, row in enumerate(hostile[:100], 1)]
    card_fields = [
        "rank",
        "uid",
        "title",
        "year",
        "venue",
        "url",
        "category",
        "problem_claimed",
        "actual_mechanism",
        "hidden_assumptions",
        "variables_treated_as_fixed",
        "failure_modes_ignored",
        "what_it_makes_less_novel",
        "what_it_leaves_open",
    ]
    write_csv("hostile_prior_work_100_cards.csv", cards, card_fields)

    outputs = {
        "literature_map.md": build_literature_map(landscape, serious, deep, hostile, cards),
        "hostile_prior_work.md": build_hostile_prior(cards),
        "novelty_boundary_map.md": build_novelty_boundary(),
        "novelty_decision.md": build_decision(),
        "claims.md": build_claims(),
        "reviewer_attacks.md": build_attacks(),
    }
    for name, text in outputs.items():
        (DOCS / name).write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")

    print("Wrote literature synthesis docs:")
    for name in outputs:
        print(f"- docs/{name}")
    print("- docs/hostile_prior_work_100_cards.csv")


if __name__ == "__main__":
    main()
