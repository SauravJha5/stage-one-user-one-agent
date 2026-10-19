# STAGE: One User, One Agent — Autonomous Viewer Lifecycle Engine

[![Tests: Passing](https://img.shields.io/badge/Tests-5%2F5%20Passed-brightgreen)](tests/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.14-blue)](https://www.python.org/)
[![Latency: Sub--Second](https://img.shields.io/badge/P95%20Latency-19.13ms-success)](sample_run/latency_report.json)
[![Safety: Holdout Protected](https://img.shields.io/badge/Holdout%20Isolation-100%25-green)](sample_run/impact_report.md)

An autonomous, deterministic agentic lifecycle system built for STAGE's regional dialect OTT platform (spanning dialects d1–d6). 

Departing from conventional, superficial title recommendation loops, this platform allocates a **dedicated, long-lived autonomous agent to each individual viewer**. Each agent diagnoses real-time viewer state, selects single measurable lifecycle goals, executes policy-compliant interventions under a 60-second SLA, and proves causal uplift through randomized holdout arms.

---

## 🧭 System Architecture & Decision Flow

The system runs on an immutable, auditable **Sense → Resolve → Plan → Verify → Act → Measure** loop:

```text
[ Ingest & Deduplicate ] ─── Clock Skew Defense (Server received_at priority)
         │
         ▼
[ Fact Resolution Engine ] ── Hierarchy: Live App Setting > Billing Events > Profiles Snapshot
         │
         ▼
[ Goal Planner ] ────────── Selects Single Measurable Goal (Drops Unmeasurable Traps)
         │
         ▼
[ Intervention Planner ] ── Dialect Filtering, Catalogue Matching & Prompt-Injection Neutralization
         │
         ▼
[ Independent Verifier ] ── Hard-Veto Gatekeeper (Holdout Arm, Quiet Hours 22:00-08:00 IST, Caps)
         │
         ├─── If Cleared ────► [ Published Action ] ──► sample_run/actions.jsonl
         └─── If Blocked ────► [ Abstain / Block ]  ──► sample_run/decisions.jsonl

---

## 📊 Performance & Reliability Benchmark

Benchmark metrics recorded on sample replay runs (`sample_run/latency_report.json`):

| Evaluation Metric | Observed Result | System SLA Target | Verdict |
| :--- | :--- | :--- | :--- |
| **Mean Processing Latency** | `~1.92 ms` | `< 60,000 ms` | **Exceeded by >99%** |
| **P95 Latency** | `19.13 ms` | `< 60,000 ms` | **Deterministic Real-Time** |
| **Holdout Arm Leakage** | `0.00%` | `0.00%` | **100% Policy Compliant** |
| **Quiet Hours Violations** | `0` | `0` | **Fully Protected** |
| **Test Suite Coverage** | `5 / 5 Passed` | `100%` | **Verified** |

---

## 📁 Repository Structure & Deliverables

```text
├── config/                     # Core business configurations
│   ├── goals.json              # Lifecycle goal definitions & eligibility
│   ├── interventions.json      # Approved intervention templates
│   └── messaging_policy.md     # Quiet hours & frequency constraints
├── data/                       # Input catalogs & profile snapshots
│   ├── catalogue.csv           # Regional title metadata & availability
│   └── profiles_snapshot.csv   # Historical user snapshot records
├── replay/                     # Evaluation traces & arms
│   ├── arms.csv                # Randomized Treatment vs. Holdout allocations
│   └── triggers.jsonl          # Stream of real-time viewer events
├── sample_run/                 # Generated Execution Deliverables
│   ├── decisions.jsonl         # Detailed JSON decision trace per event
│   ├── actions.jsonl           # Verified, published intervention stream
│   ├── latency_report.json     # P50, P95, and average execution latencies
│   ├── impact_report.md        # Causal ITT evaluation & bias analysis
│   ├── final_report.md         # Comprehensive executive audit report
│   └── viewer_state/           # Durable JSON stores per viewer agent
├── src/                        # Core Engine Modules
│   ├── agent/                  # Goal Planner, Intervention, Mock Layer
│   ├── evaluation/             # Attributable Outcome Judge & Impact Reporter
│   ├── guardrails/             # Independent Verification Gatekeeper
│   ├── ingestion/              # Deduplication parser & Fact Resolver
│   ├── store/                  # Durable viewer state persistence
│   └── models.py               # Pydantic data contracts
├── tests/                      # Automated Verification Tests
│   ├── test_deduplication.py   # Idempotent event deduplication
│   ├── test_goal_rules.py      # Goal eligibility & trap filtering
│   ├── test_guardrails.py      # Holdout isolation & quiet hours checks
│   └── test_precedence.py      # Dialect conflict resolution rules
├── ARCHITECTURE.md             # System boundaries, state stores, and invariants
├── AI_COLLABORATION.md         # Documented LLM suggestions, tests, and rejections
├── KNOWN_LIMITATIONS.md        # Production scaling roadmap (Redis, SQS, Bandits)
├── main.py                     # One-command orchestration script
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview & reproduction guide
## 🔍 Provenance & Decision Output Schema

Every decision generated by an agent is fully traceable, auditable, and stored in `sample_run/decisions.jsonl`:

```json
{
  "decision_id": "D-00042",
  "viewer_id": "U-00124",
  "trigger": {
    "event": "app_open",
    "received_at": "2026-09-12T14:30:00+00:00",
    "event_age_s": 0.12
  },
  "goal": {
    "id": "G01",
    "name": "first_play_24h",
    "deadline": "2026-09-13T14:30:00+00:00",
    "success_event": "play_started"
  },
  "action": "HOME_PAGE",
  "dialect": {
    "used": "d3",
    "source": "app_setting",
    "conflicts": ["profile:d1"]
  },
  "content": ["title:T042", "title:T109", "title:T215"],
  "confidence": 0.85,
  "confidence_reason": "High affinity based on viewing stage and fresh dialect setting",
  "evidence": ["event:EVT_0984", "catalogue_dialect:d3"],
  "assumptions": ["arm_assignment:agent", "active_subscriber_state_assumed_valid"],
  "checks": {
    "passed": ["holdout_cleared", "content_validity"],
    "failed": []
  },
  "decided_in_ms": 1.45,
  "status": "PUBLISHED"
}
```
