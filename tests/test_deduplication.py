from datetime import datetime, timezone
from src.ingestion.event_parser import EventParser

def test_duplicate_events_are_dropped():
    parser = EventParser()
    raw_event = {
        "event_id": "EVT_TEST_001",
        "event": "app_open",
        "viewer_id": "V-101",
        "occurred_at": "2026-09-12T10:00:00Z",
        "received_at": "2026-09-12T10:00:05Z",
        "app_dialect": "d3"
    }

    # First event must be accepted
    first = parser.parse_event(raw_event)
    assert first is not None
    assert first.event_id == "EVT_TEST_001"
    assert first.event_age_s == 5.0

    # Same event_id must be idempotently dropped
    second = parser.parse_event(raw_event)
    assert second is None, "Duplicate event_id was not dropped!"
