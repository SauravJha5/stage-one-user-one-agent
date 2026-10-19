from datetime import datetime, timezone
from src.models import ViewerState, TriggerEvent
from src.agent.planner import GoalPlanner

def test_unmeasurable_goal_trap_is_ignored():
    planner = GoalPlanner()
    state = ViewerState(viewer_id="V-104", arm="agent")
    trigger = TriggerEvent(
        event_id="EVT_G1",
        event="app_open",
        viewer_id="V-104",
        occurred_at=datetime.now(timezone.utc),
        received_at=datetime.now(timezone.utc)
    )

    goal, reason, conf = planner.select_goal(state, trigger)
    assert goal is not None
    # Must not pick unmeasurable trap
    assert goal.get("id") != "unmeasurable_goal_trap"
    assert goal.get("success_event") is not None
