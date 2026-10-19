import os

files_to_create = {
    # 1. main.py
    "main.py": '''import sys
import time
from src.replay.harness import ReplayHarness
from src.evaluation.impact_reporter import ImpactReporter

def main():
    print("=" * 60)
    print("STAGE: ONE USER, ONE AGENT LIFECYCLE PLATFORM")
    print("=" * 60)
    
    t0 = time.time()
    
    print("\\n[1/2] Executing Event Replay & Decision Engine...")
    harness = ReplayHarness(
        arms_path="replay/arms.csv",
        goals_path="config/goals.json",
        catalogue_path="data/catalogue.csv",
        output_dir="sample_run"
    )
    harness.run(triggers_path="replay/triggers.jsonl", max_events=1500)
    
    print("\\n[2/2] Generating Causal Impact Report & Selection Bias Audit...")
    ImpactReporter.generate_report(
        decisions_path="sample_run/decisions.jsonl",
        arms_path="replay/arms.csv",
        output_md="sample_run/impact_report.md"
    )
    
    elapsed = round(time.time() - t0, 2)
    print("\\n" + "=" * 60)
    print(f"SUCCESS: Pipeline completed in {elapsed}s.")
    print("Artifacts generated in sample_run/:")
    print("  - sample_run/decisions.jsonl")
    print("  - sample_run/actions.jsonl")
    print("  - sample_run/latency_report.json")
    print("  - sample_run/impact_report.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
''',

    # 2. README.md
    "README.md": '''# STAGE: One User, One Agent Lifecycle System

A deterministic agentic lifecycle architecture designed for STAGE's regional dialect OTT platform. Rather than a superficial title recommender, this system functions as an autonomous lifecycle manager for each viewer—selecting measurable goals, executing policy-compliant interventions within a 60-second budget, enforcing strict safety guardrails, and estimating true causal uplift via randomized holdout arms.

---

## Quick Start (One-Command Reproduction)

### 1. Environment Setup
```bash
python -m venv venv
# Windows:
.\\venv\\Scripts\\Activate.ps1
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt