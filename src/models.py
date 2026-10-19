from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TriggerEvent(BaseModel):
    event_id: str
    event: str
    viewer_id: str
    occurred_at: datetime
    received_at: datetime
    event_age_s: float = 0.0
    app_dialect: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)

class ViewerFact(BaseModel):
    value: Any
    source: str          # "app_setting", "events", "profile_snapshot"
    received_at: datetime

class ViewerState(BaseModel):
    viewer_id: str
    arm: str = "agent"   # "agent" or "holdout"
    dialect: Optional[ViewerFact] = None
    subscription_status: Optional[ViewerFact] = None
    signup_date: Optional[ViewerFact] = None
    notifications_opt_in: bool = True
    whatsapp_opt_in: bool = False
    last_message_date_ist: Optional[str] = None  # YYYY-MM-DD
    active_goal_id: Optional[str] = None
    active_goal_name: Optional[str] = None
    active_goal_deadline: Optional[datetime] = None
    active_goal_success_event: Optional[str] = None
    completed_goals: List[str] = Field(default_factory=list)
    watched_titles: List[str] = Field(default_factory=list)
    finished_episodes: List[str] = Field(default_factory=list)
    prior_events: List[str] = Field(default_factory=list)

class DecisionOutput(BaseModel):
    decision_id: str
    viewer_id: str
    trigger: Dict[str, Any]
    goal: Optional[Dict[str, Any]] = None
    action: str          # HOME_PAGE, PUSH, WHATSAPP, IN_APP, NO_ACTION
    dialect: Dict[str, Any]
    content: List[str] = Field(default_factory=list)
    confidence: float
    confidence_reason: str
    evidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    checks: Dict[str, List[str]] = Field(default_factory=lambda: {"passed": [], "failed": []})
    decided_in_ms: float
    status: str          # PUBLISHED, ABSTAINED, BLOCKED
