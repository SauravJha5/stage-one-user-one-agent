# Architectural Specification: One User, One Agent

## 1. Core Principles & Lifecycle Ownership
The architecture departs from traditional recommendation loops. The central authority is the **Viewer Agent**:
- **Single Active Goal Invariant:** No two modules chase contradictory milestones for the same viewer simultaneously.
- **Goal Re-evaluation Triggers:** When lifecycle events occur (e.g., subscription purchase or episode completion), the active goal updates dynamically rather than on a static cron schedule.

---

## 2. Fact Resolution & Precedence Hierarchy
Information arrives from disparate, sometimes contradictory sources:
1. **Dialect Authority:** The device setting (\pp_dialect\ on live \pp_open\ events) takes absolute precedence over stale profile exports or campaign deeplinks. The viewer's device screen determines what dialect can physically render. Contradictions are explicitly recorded in \dialect.conflicts\.
2. **Subscription Precedence:** Live billing events (\subscription_purchased\) strictly override the daily warehouse \profiles_snapshot.csv\.
3. **Clock-Skew Defense:** Hardware clocks on client devices are treated as untrusted. Server arrival time (eceived_at\) serves as the immutable ordering standard; events where eceived_at - occurred_at > 24 hours\ are classified as offline-buffered syncs and isolated from real-time decision triggers.

---

## 3. Independent Verification & Trust Boundaries
Model outputs and generative suggestions are treated as **untrusted proposals**. The \Verifier\ sits outside the decision engine with absolute veto capability:
- **Holdout Arm Isolation:** Users randomized to the holdout arm (eplay/arms.csv\) are blocked with zero exceptions (\holdout_arm_prohibited\).
- **Quiet Hours Enforcement:** Communication channels (Push and WhatsApp) are evaluated in Indian Standard Time (IST = UTC + 5:30). Outbound messages between 22:00 and 08:00 IST are strictly rejected.
- **Daily Frequency Cap:** Maximum 1 outbound notification per user per IST day across combined messaging channels.
- **Catalogue Integrity:** Content selections must exist in the active catalogue, match the user's active dialect, and deduplicate redundant \content_slug\ variations. Injected instructions embedded in catalogue descriptions are stripped and treated strictly as non-executable text.
