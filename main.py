import sys
import time
from src.replay.harness import ReplayHarness
from src.evaluation.impact_reporter import ImpactReporter

def main():
    print("="*60)
    print("🚀 STAGE: ONE USER, ONE AGENT LIFECYCLE PLATFORM")
    print("="*60)
    
    t0 = time.time()
    
    # 1. Execute Live Replay Harness
    print("\n[1/2] Executing Event Replay & Decision Engine...")
    harness = ReplayHarness(
        arms_path="replay/arms.csv",
        goals_path="config/goals.json",
        catalogue_path="data/catalogue.csv",
        output_dir="sample_run"
    )
    # Defaulting to 1500 replay events for comprehensive sample run
    harness.run(triggers_path="replay/triggers.jsonl", max_events=1500)
    
    # 2. Generate Causal Impact Report (ITT vs Naive Selection Bias)
    print("\n[2/2] Generating Causal Impact Report & Selection Bias Audit...")
    ImpactReporter.generate_report(
        decisions_path="sample_run/decisions.jsonl",
        arms_path="replay/arms.csv",
        output_md="sample_run/impact_report.md"
    )
    
    elapsed = round(time.time() - t0, 2)
    print("\n" + "="*60)
    print(f"✨ SUCCESS: Pipeline completed in {elapsed}s.")
    print("Artifacts generated in sample_run/:")
    print("  - sample_run/decisions.jsonl")
    print("  - sample_run/actions.jsonl")
    print("  - sample_run/latency_report.json")
    print("  - sample_run/impact_report.md")
    print("="*60)

if __name__ == "__main__":
    main()
