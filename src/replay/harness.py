import os
import csv
import json
import time
from datetime import datetime
from typing import Dict

from src.models import DecisionOutput, TriggerEvent
from src.ingestion.event_parser import EventParser
from src.ingestion.fact_resolver import FactResolver
from src.store.state_store import StateStore
from src.agent.planner import GoalPlanner
from src.agent.intervention import InterventionPlanner
from src.guardrails.verifier import Verifier
from src.agent.model_provider import ModelProvider

class ReplayHarness:
    def __init__(
        self,
        arms_path: str = "replay/arms.csv",
        goals_path: str = "config/goals.json",
        catalogue_path: str = "data/catalogue.csv",
        output_dir: str = "sample_run"
    ):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "viewer_state"), exist_ok=True)

        self.arms: Dict[str, str] = {}
        if os.path.exists(arms_path):
            with open(arms_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uid = row.get("viewer_id") or row.get("user_id")
                    if uid:
                        self.arms[uid] = row.get("arm", "agent")

        self.parser = EventParser()
        self.store = StateStore(storage_dir=os.path.join(self.output_dir, "viewer_state"))
        self.planner = GoalPlanner(goals_path=goals_path)
        self.intervention = InterventionPlanner(catalogue_path=catalogue_path)
        self.model = ModelProvider(mode="mock")

    def run(self, triggers_path: str = "replay/triggers.jsonl", max_events: int = 1000):
        decisions_file = os.path.join(self.output_dir, "decisions.jsonl")
        actions_file = os.path.join(self.output_dir, "actions.jsonl")
        latency_file = os.path.join(self.output_dir, "latency_report.json")

        decision_count = 0
        latencies = []
        start_replay_time = time.time()

        with open(decisions_file, "w", encoding="utf-8") as d_out, \
             open(actions_file, "w", encoding="utf-8") as a_out:

            for trigger in self.parser.stream_events(triggers_path):
                t0 = time.time()
                decision_count += 1
                if decision_count > max_events:
                    break

                arm = self.arms.get(trigger.viewer_id, "agent")
                state = self.store.get_or_create(trigger.viewer_id, arm=arm)

                # 1. Fact Resolution & Dialect Selection
                chosen_dialect, dialect_conflicts = FactResolver.resolve_dialect(state, trigger)
                FactResolver.update_from_event(state, trigger)

                # 2. Goal Planning
                goal_obj, goal_reason, confidence = self.planner.select_goal(state, trigger)

                # 3. Intervention Planning
                plan = self.intervention.plan_action(state, chosen_dialect)
                action = plan["action"]
                content = plan["content"]

                # 4. Independent Verification
                is_valid, passed_checks, failed_checks = Verifier.verify(
                    state, trigger, action, content
                )

                if not is_valid:
                    status = "BLOCKED" if "holdout_arm_prohibited" in failed_checks else "ABSTAINED"
                    published_action = "NO_ACTION"
                    published_content = []
                else:
                    status = "PUBLISHED" if action != "NO_ACTION" else "ABSTAINED"
                    published_action = action
                    published_content = content

                t1 = time.time()
                elapsed_ms = round((t1 - t0) * 1000.0, 2)
                latencies.append(elapsed_ms)

                # 5. Form Decision Object (Exact STAGE Format)
                decision = DecisionOutput(
                    decision_id=f"D-{decision_count:05d}",
                    viewer_id=trigger.viewer_id,
                    trigger={
                        "event": trigger.event,
                        "received_at": trigger.received_at.isoformat(),
                        "event_age_s": round(trigger.event_age_s, 2)
                    },
                    goal=goal_obj,
                    action=published_action,
                    dialect={
                        "used": chosen_dialect,
                        "source": state.dialect.source if state.dialect else "fallback",
                        "conflicts": dialect_conflicts
                    },
                    content=published_content,
                    confidence=confidence,
                    confidence_reason=goal_reason,
                    evidence=[
                        f"event:{trigger.event_id}",
                        f"catalogue_dialect:{chosen_dialect}"
                    ],
                    assumptions=[
                        f"arm_assignment:{state.arm}",
                        "active_subscriber_state_assumed_valid"
                    ],
                    checks={
                        "passed": passed_checks,
                        "failed": failed_checks
                    },
                    decided_in_ms=elapsed_ms,
                    status=status
                )

                d_out.write(decision.model_dump_json() + "\n")

                # Agar action publish hua hai toh actions.jsonl mein record karo
                if status == "PUBLISHED":
                    action_payload = {
                        "decision_id": decision.decision_id,
                        "viewer_id": decision.viewer_id,
                        "action": published_action,
                        "dialect": chosen_dialect,
                        "content": published_content,
                        "published_at": trigger.received_at.isoformat()
                    }
                    a_out.write(json.dumps(action_payload) + "\n")

                # Per-user state save karo
                self.store.save(state)

        # 6. Latency Report
        p95 = sorted(latencies)[int(0.95 * len(latencies))] if latencies else 0.0
        avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
        lat_report = {
            "total_decisions": decision_count,
            "average_ms": round(avg_lat, 2),
            "p95_ms": round(p95, 2),
            "sla_breaches_above_60s": sum(1 for x in latencies if x > 60000),
            "total_run_time_s": round(time.time() - start_replay_time, 2)
        }
        with open(latency_file, "w", encoding="utf-8") as f:
            json.dump(lat_report, f, indent=2)

        print(f"Replay Complete: {decision_count} events processed.")
        print(f"Avg Latency: {lat_report['average_ms']} ms | P95: {lat_report['p95_ms']} ms")
