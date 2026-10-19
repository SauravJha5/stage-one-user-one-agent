import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

class OutcomeJudge:
    def __init__(self, decisions_path: str = "sample_run/decisions.jsonl"):
        self.decisions_path = decisions_path

    @staticmethod
    def parse_iso(ts_str: str) -> datetime:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def evaluate(self, outcomes_file: str = "sample_run/outcomes.jsonl") -> List[Dict[str, Any]]:
        # Decision goals load karein
        viewer_goals = {}
        if os.path.exists(self.decisions_path):
            with open(self.decisions_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line)
                    vid = d.get("viewer_id")
                    goal = d.get("goal")
                    if vid and goal:
                        viewer_goals[vid] = {
                            "goal_id": goal.get("id"),
                            "deadline": self.parse_iso(goal.get("deadline")),
                            "success_event": goal.get("success_event"),
                            "status": "failed"
                        }

        # Agar outcomes file maujood hai toh correlate karein
        judged = []
        if os.path.exists(outcomes_file):
            with open(outcomes_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    ev = json.loads(line)
                    vid = ev.get("viewer_id") or ev.get("user_id")
                    ev_name = ev.get("event")
                    received_at = self.parse_iso(ev.get("received_at", ev.get("occurred_at", "2026-10-01T00:00:00Z")))

                    if vid in viewer_goals:
                        g = viewer_goals[vid]
                        # Window aur event match check
                        if ev_name == g["success_event"] and received_at <= g["deadline"]:
                            g["status"] = "succeeded"

        for vid, data in viewer_goals.items():
            judged.append({
                "viewer_id": vid,
                "goal_id": data["goal_id"],
                "outcome": data["status"]
            })
        return judged
