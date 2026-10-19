# AI Collaboration & Verification Log

In compliance with the assignment brief, LLMs and coding assistants were utilized as productivity accelerators. All architecture decisions, data audits, safety constraints, and code implementations were directed, reviewed, and tested independently.

---

## 1. Where AI Assisted Effectively
- Generating Pydantic validation models matching STAGE's nested JSON decision output schema.
- Scaffolding unit test suites covering duplicate event deduplication, quiet hours time-zone math, and holdout protection.
- Drafting initial mathematical explanations contrasting Intention-to-Treat (ITT) evaluation against observational selection bias.

---

## 2. What Was Detected, Corrected, and Rejected
| Suggested AI Proposal | Why It Was Flawed | How It Was Corrected |
| :--- | :--- | :--- |
| **Monolithic LLM Prompt for Title Selection** | The assistant initially proposed sending the entire user history and catalog into an LLM prompt to select titles. | **Rejected:** Violates latency constraints, cost budgets, and exposes the system to prompt injection. Implemented a deterministic, indexed catalogue retrieval pipeline in \intervention.py\. |
| **Using Device Time (\occurred_at\) for Window Deadlines** | The assistant suggested computing goal deadlines using client device timestamps. | **Rejected:** Client device clocks suffer from severe clock skew and manipulation. Replaced with server-trusted eceived_at\. |
| **Comparing Served vs. Unserved Users for Uplift** | The assistant initially generated code computing uplift by measuring served users against unserved users. | **Rejected:** This perpetuates the exact selection bias trap present in the historical pilot report. Replaced with true Intention-to-Treat (ITT) comparing randomized treatment vs. holdout arms. |
| **Allowing Free-Form Generative Copy for WhatsApp** | The assistant attempted to let the model generate dynamic WhatsApp marketing text. | **Rejected:** Violates messaging policies and pricing rules. Restricted interventions to approved templates with deterministic variable slots. |
