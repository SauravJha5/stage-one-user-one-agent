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
