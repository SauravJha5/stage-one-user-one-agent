# STAGE: One User, One Agent Lifecycle System

A deterministic agentic lifecycle architecture designed for STAGE's regional dialect OTT platform. Rather than a superficial title recommender, this system functions as an autonomous lifecycle manager for each viewer—selecting measurable goals, executing policy-compliant interventions within a 60-second budget, enforcing strict safety guardrails, and estimating true causal uplift via randomized holdout arms.

---

## Quick Start (One-Command Reproduction)

### 1. Environment Setup
\\ash
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
\
### 2. Run Complete Pipeline (One Command)
\\ash
python main.py
\
### 3. Run Automated Safety & Reliability Tests
\\ash
python -m pytest -v
\
---

## Deliverables & Output Artifacts

All outputs are saved to \sample_run/\:
- \sample_run/decisions.jsonl\: Machine-readable decision logs containing trigger age, confidence justification, assumptions, evidence provenance, check audits, and latency in milliseconds.
- \sample_run/actions.jsonl\: Published interventions for eligible treatment users.
- \sample_run/latency_report.json\: Replay latency metrics (Average and P95 latency).
- \sample_run/impact_report.md\: Causal Intention-to-Treat (ITT) evaluation contrasting the naive observational bias present in previous pilot reports.
- \sample_run/final_report.md\: Executive report covering handled traps, safety compliance, and performance.
- \sample_run/viewer_state/\: Persistent per-user state files tracking active goals, watched episodes, and communication consent.
