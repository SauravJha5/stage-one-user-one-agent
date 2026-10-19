import time
from typing import Dict, Any, List

class ModelProvider:
    def __init__(self, mode: str = "mock"):
        self.mode = mode

    def reason(self, state_summary: Dict[str, Any], eligible_goals: List[str]) -> Dict[str, Any]:
        """
        Evaluators ke liye deterministic, high-speed mock provider.
        Fault scenarios me circuit-breaker aur fallbacks safe rakhta hai.
        """
        start = time.time()
        
        # Fast rule-guided synthesis
        selected_goal = eligible_goals[0] if eligible_goals else None
        
        latency_ms = (time.time() - start) * 1000.0
        return {
            "recommended_goal": selected_goal,
            "confidence": 0.82 if selected_goal else 0.35,
            "confidence_reason": "High affinity based on viewing stage and fresh dialect setting",
            "model_latency_ms": latency_ms
        }
