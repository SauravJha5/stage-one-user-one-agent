# Impact Measurement & Uplift Report

## 1. Executive Summary & Causal Validity
In previous pilot reports, uplift was computed by comparing **Served Viewers vs. Unserved Viewers**. This is an observational fallacy driven by **Selection Bias**: users who are served are systematically more active, meaning their organic baseline conversion was already higher.

In this evaluation, we enforce a strict **Intention-to-Treat (ITT)** framework across the randomized holdout arms:
- **Treatment Arm (Agent Group):** All users eligible to receive agent decisions (including intentional abstentions).
- **Control Arm (Holdout Group):** Complete zero-intervention group.

---

## 2. Cohort Statistics
- **Total Viewers in Randomized Arms:** 5000
- **Agent Arm Viewers:** 2513
- **Holdout Arm Viewers (Zero Touch):** 2487
- **Total Decisions Evaluated:** 1500
- **Successfully Served (Interventions Published):** 533
- **Agent Arm Abstention / No-Action Decisions:** 967

---

## 3. Naive vs. True Causal Comparison
| Metric Strategy | Comparison Group | Methodological Flaw | Validity Verdict |
| :--- | :--- | :--- | :--- |
| **Naive Report** | Served vs. Non-Served | Selection Bias (Confounding) | **Invalid** (Artificially Inflated) |
| **True Uplift (ITT)** | Agent Arm vs. Holdout Arm | Randomized Intent-to-Treat | **Valid Causal Ground Truth** |

---

## 4. Policy & Safety Compliance
- **Holdout Leakage:** 0% (All holdout arm users received zero interventions).
- **Quiet Hours Violations (22:00–08:00 IST):** 0
- **Daily Frequency Cap Overages (>1 msg/day):** 0
