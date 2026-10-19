import json
from datetime import datetime, timezone
from typing import Set, Generator, Optional
from src.models import TriggerEvent

class EventParser:
    def __init__(self, stale_threshold_s: float = 86400.0):
        self.seen_event_ids: Set[str] = set()
        self.stale_threshold_s = stale_threshold_s

    @staticmethod
    def parse_iso(ts_str: str) -> datetime:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def parse_event(self, raw_data: dict) -> Optional[TriggerEvent]:
        event_id = raw_data.get("event_id")
        if not event_id or event_id in self.seen_event_ids:
            return None
        self.seen_event_ids.add(event_id)

        received_at = self.parse_iso(raw_data["received_at"])
        occurred_raw = raw_data.get("occurred_at", raw_data["received_at"])
        occurred_at = self.parse_iso(occurred_raw)

        # Clock-skew check
        event_age_s = max(0.0, (received_at - occurred_at).total_seconds())
        viewer_id = raw_data.get("viewer_id") or raw_data.get("user_id")

        return TriggerEvent(
            event_id=event_id,
            event=raw_data["event"],
            viewer_id=viewer_id,
            occurred_at=occurred_at,
            received_at=received_at,
            event_age_s=event_age_s,
            app_dialect=raw_data.get("app_dialect"),
            properties=raw_data.get("properties", {})
        )

    def stream_events(self, file_path: str) -> Generator[TriggerEvent, None, None]:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                ev = self.parse_event(json.loads(line))
                if ev:
                    yield ev
