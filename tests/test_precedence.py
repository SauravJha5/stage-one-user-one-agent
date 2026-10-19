from datetime import datetime, timezone
from src.models import ViewerState, TriggerEvent
from src.ingestion.fact_resolver import FactResolver

def test_app_setting_overrides_stale_profile():
    state = ViewerState(viewer_id="V-102")
    trigger = TriggerEvent(
        event_id="EVT_TEST_002",
        event="app_open",
        viewer_id="V-102",
        occurred_at=datetime.now(timezone.utc),
        received_at=datetime.now(timezone.utc),
        app_dialect="d3"
    )

    chosen_dialect, conflicts = FactResolver.resolve_dialect(
        current_state=state,
        trigger=trigger,
        profile_dialect="d1",
        campaign_dialect="d2"
    )

    # App setting wins
    assert chosen_dialect == "d3"
    # Conflicts are captured explicitly
    assert "profile:d1" in conflicts
    assert "campaign:d2" in conflicts
    assert state.dialect.value == "d3"
