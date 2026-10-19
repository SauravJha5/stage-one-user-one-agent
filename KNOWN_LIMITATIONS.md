# Known Limitations & Production Roadmap

This repository prioritizes a reliable, safe decide-act-measure loop within the 10–12 hour time boundary. The following deliberate trade-offs are documented for production scaling:

---

## 1. State Persistence Architecture
- **Current Implementation:** Durable per-user JSON flat files stored in \sample_run/viewer_state/\ with an in-memory LRU read cache.
- **Production Roadmap:** Migration to a distributed low-latency key-value store (e.g., Redis or DynamoDB) with optimistic locking to support concurrent triggers across distributed worker nodes.

---

## 2. Catalogue Indexing at Scale
- **Current Implementation:** In-memory filtered iteration over \data/catalogue.csv\.
- **Production Roadmap:** Inverted indexing by dialect and release timestamp backed by Elasticsearch or OpenSearch to support tens of thousands of titles across 40+ regional dialects without memory bloat.

---

## 3. Asynchronous Notification Queue
- **Current Implementation:** Outbound interventions evaluate quiet hours and immediately drop or approve messages.
- **Production Roadmap:** Integration with an asynchronous task scheduler (e.g., Celery/SQS) that pauses messages during quiet hours and schedules them for dispatch precisely when the quiet window terminates at 08:00 IST.

---

## 4. Multi-Armed Bandit Allocation
- **Current Implementation:** Deterministic priority-ordered goal selection matching the first eligible condition.
- **Production Roadmap:** Contextual Thompson Sampling or Upper Confidence Bound (UCB) bandits to balance exploration and exploitation across multiple eligible lifecycle goals.
