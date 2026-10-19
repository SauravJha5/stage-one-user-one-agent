from datetime import datetime
from typing import Tuple, List, Optional
from src.models import ViewerState, ViewerFact, TriggerEvent

class FactResolver:
    @staticmethod
    def resolve_dialect(
        current_state: ViewerState, 
        trigger: TriggerEvent, 
        profile_dialect: Optional[str] = None, 
        campaign_dialect: Optional[str] = None
    ) -> Tuple[str, List[str]]:
        conflicts = []
        chosen_dialect = "d1"

        if trigger.app_dialect:
            chosen_dialect = trigger.app_dialect
            if profile_dialect and profile_dialect != chosen_dialect:
                conflicts.append(f"profile:{profile_dialect}")
            if campaign_dialect and campaign_dialect != chosen_dialect:
                conflicts.append(f"campaign:{campaign_dialect}")
        elif profile_dialect:
            chosen_dialect = profile_dialect
        elif current_state.dialect:
            chosen_dialect = current_state.dialect.value

        current_state.dialect = ViewerFact(
            value=chosen_dialect,
            source="app_setting" if trigger.app_dialect else "profile_snapshot",
            received_at=trigger.received_at
        )
        return chosen_dialect, conflicts

    @staticmethod
    def update_from_event(state: ViewerState, event: TriggerEvent):
        if event.event not in state.prior_events:
            state.prior_events.append(event.event)

        if event.event == "subscription_purchased":
            state.subscription_status = ViewerFact(
                value=event.properties.get("plan_type", "paid"),
                source="live_event",
                received_at=event.received_at
            )
        elif event.event == "notification_opt_out":
            state.notifications_opt_in = False
        elif event.event == "notification_opt_in":
            state.notifications_opt_in = True
        elif event.event == "whatsapp_opt_in":
            state.whatsapp_opt_in = True
        elif event.event == "whatsapp_opt_out":
            state.whatsapp_opt_in = False
        elif event.event == "play_started":
            title_id = event.properties.get("title_id")
            if title_id and title_id not in state.watched_titles:
                state.watched_titles.append(title_id)
        elif event.event == "episode_finished":
            title_id = event.properties.get("title_id")
            if title_id and title_id not in state.finished_episodes:
                state.finished_episodes.append(title_id)
