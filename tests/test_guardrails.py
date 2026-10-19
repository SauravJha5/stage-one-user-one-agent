from datetime import datetime, timezone
from src.models import ViewerState, TriggerEvent
from src.guardrails.verifier import Verifier

def test_holdout_arm_is_strictly_blocked():
    holdout_state = ViewerState(viewer_id="V-HOLDOUT", arm="holdout")
    trigger = TriggerEvent(
        event_id="EVT_H1",
        event="app_open",
        viewer_id="V-HOLDOUT",
        occurred_at=datetime.now(timezone.utc),
        received_at=datetime.now(timezone.utc)
    )

    is_valid, passed, failed = Verifier.verify(
        state=holdout_state,
        trigger=trigger,
        action="HOME_PAGE",
        content=["title:T001", "title:T002", "title:T003"]
    )

    assert is_valid is False
    assert "holdout_arm_prohibited" in failed

def test_quiet_hours_blocks_push_notification():
    state = ViewerState(viewer_id="V-103", arm="agent", notifications_opt_in=True)
    # 23:30 IST is 18:00 UTC (Night time / Quiet hours)
    night_time_utc = datetime(2026, 9, 12, 18, 0, 0, tzinfo=timezone.utc)
    trigger = TriggerEvent(
        event_id="EVT_Q1",
        event="app_open",
        viewer_id="V-103",
        occurred_at=night_time_utc,
        received_at=night_time_utc
    )

    is_valid, passed, failed = Verifier.verify(
        state=state,
        trigger=trigger,
        action="PUSH",
        content=["title:T001"]
    )

    assert is_valid is False
    assert "quiet_hours_violation" in failed
