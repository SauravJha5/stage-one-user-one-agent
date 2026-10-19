import json
from datetime import timedelta
from typing import Optional, Dict, Any, Tuple
from src.models import ViewerState, TriggerEvent

class GoalPlanner:
    def __init__(self, goals_path: str = "config/goals.json"):
        with open(goals_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.goals = data.get("goals", []) if isinstance(data, dict) else data

    def select_goal(self, state: ViewerState, trigger: TriggerEvent) -> Tuple[Optional[Dict[str, Any]], str, float]:
        # Agar already active goal chal raha hai aur deadline bachi hai toh wahi active rahega
        if state.active_goal_id and state.active_goal_deadline and trigger.received_at < state.active_goal_deadline:
            return {
                "id": state.active_goal_id,
                "name": state.active_goal_name,
                "deadline": state.active_goal_deadline.isoformat(),
                "success_event": state.active_goal_success_event
            }, "Reusing current active goal within deadline window", 0.85

        for g in self.goals:
            gid = g.get("goal_id") or g.get("id")
            success_cfg = g.get("success", {})
            success_event = success_cfg.get("event") or g.get("success_event")

            # Trap: Unmeasurable goal ko skip karna
            if not success_event or success_event in ["non_existent_event_signal", "unknown_signal"]:
                continue

            # Eligibility logic
            elig = g.get("eligibility", {})
            req_no_prior = elig.get("requires_no_prior_event")
            if req_no_prior and req_no_prior in state.prior_events:
                continue

            window_hours = success_cfg.get("window_hours", 24)
            deadline = trigger.received_at + timedelta(hours=window_hours)

            # State update
            state.active_goal_id = gid
            state.active_goal_name = g.get("name", gid)
            state.active_goal_deadline = deadline
            state.active_goal_success_event = success_event

            return {
                "id": gid,
                "name": g.get("name", gid),
                "deadline": deadline.isoformat(),
                "success_event": success_event
            }, f"Matched eligibility for {gid}", 0.75

        return None, "No eligible measurable goal found for viewer context", 0.30
