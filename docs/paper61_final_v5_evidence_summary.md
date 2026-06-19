# Paper 61 Final v5 Evidence Summary

Decision: STRONG_REVISE

## Row Gates

- Main rows: 17600 / 17600
- Ablation rows: 1440 / 1440
- Row gate passed: True

## Strong-Baseline Gate

- Strong paired comparisons: 55
- Positive success deltas: 18
- Positive distance improvements: 19
- Mean proposed success across splits: 0.4097
- Strong-baseline gate passed: False

## Ablation Gate

- Ablations compared: 8
- Proposed wins or ties on success and distance: 1
- Ablation gate passed: False

## Strong Paired Rows

| Split | Baseline | Success delta | Distance improvement | p(distance) |
|---|---:|---:|---:|---:|
| actuation_noise | ensemble mean mpc | -0.0125 | -0.0027 | 0.6313 |
| actuation_noise | domain randomized mpc | 0.0125 | 0.0017 | 0.7498 |
| actuation_noise | adaptive id mpc | 0.0125 | -0.0009 | 0.8618 |
| actuation_noise | robust worst case mpc | -0.0563 | 0.0066 | 0.3342 |
| actuation_noise | robust mean hybrid mpc | 0.0187 | 0.0023 | 0.6543 |
| adversarial_low_friction_heavy | ensemble mean mpc | 0.0000 | -0.0026 | 0.2894 |
| adversarial_low_friction_heavy | domain randomized mpc | 0.0000 | -0.0043 | 0.1002 |
| adversarial_low_friction_heavy | adaptive id mpc | -0.0187 | 0.0000 | 0.9858 |
| adversarial_low_friction_heavy | robust worst case mpc | -0.0375 | -0.0051 | 0.0617 |
| adversarial_low_friction_heavy | robust mean hybrid mpc | -0.0063 | -0.0015 | 0.5736 |
| combined_shift | ensemble mean mpc | -0.0437 | -0.0065 | 0.1032 |
| combined_shift | domain randomized mpc | -0.0375 | -0.0054 | 0.2277 |
| combined_shift | adaptive id mpc | -0.0625 | -0.0075 | 0.0665 |
| combined_shift | robust worst case mpc | -0.0125 | -0.0011 | 0.8003 |
| combined_shift | robust mean hybrid mpc | -0.0750 | -0.0107 | 0.0072 |
| contact_offset | ensemble mean mpc | 0.0187 | 0.0046 | 0.5161 |
| contact_offset | domain randomized mpc | -0.0375 | -0.0083 | 0.1990 |
| contact_offset | adaptive id mpc | 0.0375 | 0.0091 | 0.1985 |
| contact_offset | robust worst case mpc | -0.0063 | -0.0010 | 0.8908 |
| contact_offset | robust mean hybrid mpc | -0.0375 | 0.0002 | 0.9760 |
| heavy_object | ensemble mean mpc | 0.0187 | 0.0009 | 0.6578 |
| heavy_object | domain randomized mpc | 0.0250 | 0.0000 | 0.9873 |
| heavy_object | adaptive id mpc | 0.0563 | 0.0027 | 0.2057 |
| heavy_object | robust worst case mpc | -0.0375 | -0.0008 | 0.8013 |
| heavy_object | robust mean hybrid mpc | 0.0125 | 0.0015 | 0.4031 |
| high_friction | ensemble mean mpc | -0.1250 | -0.0098 | 0.0002 |
| high_friction | domain randomized mpc | -0.0875 | -0.0074 | 0.0010 |
| high_friction | adaptive id mpc | -0.1187 | -0.0103 | 0.0002 |
| high_friction | robust worst case mpc | -0.1750 | -0.0186 | 0.0002 |
| high_friction | robust mean hybrid mpc | -0.1437 | -0.0133 | 0.0002 |
| light_object | ensemble mean mpc | -0.0125 | -0.0021 | 0.4109 |
| light_object | domain randomized mpc | 0.0063 | 0.0008 | 0.6923 |
| light_object | adaptive id mpc | -0.0125 | -0.0023 | 0.4049 |
| light_object | robust worst case mpc | -0.0500 | -0.0029 | 0.4081 |
| light_object | robust mean hybrid mpc | 0.0000 | -0.0006 | 0.8218 |
| low_friction | ensemble mean mpc | 0.1437 | 0.0062 | 0.0055 |
| low_friction | domain randomized mpc | 0.1125 | 0.0045 | 0.0147 |
| low_friction | adaptive id mpc | 0.1437 | 0.0059 | 0.0070 |
| low_friction | robust worst case mpc | -0.0625 | -0.0008 | 0.8268 |
| low_friction | robust mean hybrid mpc | 0.1437 | 0.0073 | 0.0020 |
| nominal | ensemble mean mpc | -0.0375 | -0.0032 | 0.2074 |
| nominal | domain randomized mpc | -0.0375 | -0.0024 | 0.3269 |
| nominal | adaptive id mpc | -0.0187 | -0.0024 | 0.3107 |
| nominal | robust worst case mpc | -0.1437 | -0.0087 | 0.0105 |
| nominal | robust mean hybrid mpc | -0.0187 | -0.0003 | 0.9045 |
| observation_noise | ensemble mean mpc | 0.0063 | 0.0044 | 0.2379 |
| observation_noise | domain randomized mpc | 0.0063 | -0.0005 | 0.8845 |
| observation_noise | adaptive id mpc | 0.0813 | 0.0046 | 0.1687 |
| observation_noise | robust worst case mpc | -0.0125 | 0.0019 | 0.6403 |
| observation_noise | robust mean hybrid mpc | 0.0000 | 0.0017 | 0.6441 |
| target_shift | ensemble mean mpc | -0.0125 | -0.0018 | 0.1735 |
| target_shift | domain randomized mpc | -0.0187 | -0.0017 | 0.2067 |
| target_shift | adaptive id mpc | 0.0125 | -0.0000 | 0.9848 |
| target_shift | robust worst case mpc | -0.1000 | -0.0092 | 0.0015 |
| target_shift | robust mean hybrid mpc | -0.0187 | 0.0016 | 0.2904 |

## Posterior Diagnostics

| Split | Method | Entropy | Near-true mass | Prediction error | Fallbacks |
|---|---:|---:|---:|---:|---:|
| actuation_noise | adaptive id mpc | 0.8217 | 0.3627 | 0.0544 | 0.0000 |
| actuation_noise | branch counterfactual mpc | 0.8215 | 0.3592 | 0.0530 | 0.0000 |
| actuation_noise | branch counterfactual mpc v5 | 0.8188 | 0.3621 | 0.0585 | 1.7875 |
| adversarial_low_friction_heavy | adaptive id mpc | 0.5636 | 0.3157 | 0.0791 | 0.0000 |
| adversarial_low_friction_heavy | branch counterfactual mpc | 0.5505 | 0.3190 | 0.0781 | 0.0000 |
| adversarial_low_friction_heavy | branch counterfactual mpc v5 | 0.5596 | 0.3176 | 0.0798 | 0.5437 |
| combined_shift | adaptive id mpc | 0.7245 | 0.2695 | 0.0636 | 0.0000 |
| combined_shift | branch counterfactual mpc | 0.7211 | 0.2635 | 0.0636 | 0.0000 |
| combined_shift | branch counterfactual mpc v5 | 0.7128 | 0.2617 | 0.0662 | 1.1812 |
| contact_offset | adaptive id mpc | 0.6723 | 0.3343 | 0.1503 | 0.0000 |
| contact_offset | branch counterfactual mpc | 0.6828 | 0.3166 | 0.1487 | 0.0000 |
| contact_offset | branch counterfactual mpc v5 | 0.6824 | 0.3262 | 0.1486 | 0.6625 |
| heavy_object | adaptive id mpc | 0.8499 | 0.2367 | 0.0363 | 0.0000 |
| heavy_object | branch counterfactual mpc | 0.8497 | 0.2386 | 0.0364 | 0.0000 |
| heavy_object | branch counterfactual mpc v5 | 0.8348 | 0.2462 | 0.0387 | 1.9187 |
| high_friction | adaptive id mpc | 0.8522 | 0.3592 | 0.0392 | 0.0000 |
| high_friction | branch counterfactual mpc | 0.8511 | 0.3598 | 0.0391 | 0.0000 |
| high_friction | branch counterfactual mpc v5 | 0.8414 | 0.3634 | 0.0429 | 1.9625 |
| light_object | adaptive id mpc | 0.8550 | 0.3218 | 0.0356 | 0.0000 |
| light_object | branch counterfactual mpc | 0.8559 | 0.3218 | 0.0356 | 0.0000 |
| light_object | branch counterfactual mpc v5 | 0.8478 | 0.3198 | 0.0390 | 1.9812 |
| low_friction | adaptive id mpc | 0.7800 | 0.4382 | 0.0410 | 0.0000 |
| low_friction | branch counterfactual mpc | 0.7796 | 0.4380 | 0.0410 | 0.0000 |
| low_friction | branch counterfactual mpc v5 | 0.7559 | 0.4483 | 0.0440 | 1.4375 |
| nominal | adaptive id mpc | 0.8563 | 0.3693 | 0.0352 | 0.0000 |
| nominal | branch counterfactual mpc | 0.8564 | 0.3693 | 0.0354 | 0.0000 |
| nominal | branch counterfactual mpc v5 | 0.8493 | 0.3730 | 0.0387 | 1.9688 |
| observation_noise | adaptive id mpc | 0.8510 | 0.3622 | 0.0438 | 0.0000 |
| observation_noise | branch counterfactual mpc | 0.8462 | 0.3699 | 0.0441 | 0.0000 |
| observation_noise | branch counterfactual mpc v5 | 0.8453 | 0.3658 | 0.0459 | 1.9750 |
| target_shift | adaptive id mpc | 0.8391 | 0.3771 | 0.0404 | 0.0000 |
| target_shift | branch counterfactual mpc | 0.8387 | 0.3772 | 0.0405 | 0.0000 |
| target_shift | branch counterfactual mpc v5 | 0.8352 | 0.3746 | 0.0414 | 1.8500 |
