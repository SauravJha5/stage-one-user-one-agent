from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple
from src.models import ViewerState, TriggerEvent

class Verifier:
    @staticmethod
    def to_ist(utc_dt: datetime) -> datetime:
        return utc_dt.astimezone(timezone(timedelta(hours=5, minutes=30)))

    @classmethod
    def verify(
        cls, 
        state: ViewerState, 
        trigger: TriggerEvent, 
        action: str, 
        content: List[str]
    ) -> Tuple[bool, List[str], List[str]]:
        passed = []
        failed = []

        # 1. HOLDOUT PROTECTION CHECK
        if state.arm == "holdout":
            failed.append("holdout_arm_prohibited")
            return False, passed, failed
        passed.append("holdout_cleared")

        if action == "NO_ACTION":
            passed.append("no_action_allowed")
            return True, passed, failed

        # 2. CONTENT INTEGRITY CHECK
        if action == "HOME_PAGE" and len(content) < 3:
            failed.append("insufficient_titles_for_row")
            return False, passed, failed
        passed.append("content_validity")

        # 3. QUIET HOURS & FREQUENCY CAPS (For Push / WhatsApp)
        if action in ["PUSH", "WHATSAPP"]:
            ist_time = cls.to_ist(trigger.received_at)
            hour = ist_time.hour
            # Quiet hours: 22:00 to 08:00 IST
            if hour >= 22 or hour < 8:
                failed.append("quiet_hours_violation")
                return False, passed, failed
            passed.append("quiet_hours_cleared")

            # Frequency cap: max 1 per IST day
            current_ist_date = ist_time.strftime("%Y-%m-%d")
            if state.last_message_date_ist == current_ist_date:
                failed.append("frequency_cap_exceeded")
                return False, passed, failed
            passed.append("frequency_cap_cleared")

            # Consent checks
            if action == "PUSH" and not state.notifications_opt_in:
                failed.append("push_consent_missing")
                return False, passed, failed
            if action == "WHATSAPP" and not state.whatsapp_opt_in:
                failed.append("whatsapp_consent_missing")
                return False, passed, failed
            passed.append("consent_verified")

        return True, passed, failed
