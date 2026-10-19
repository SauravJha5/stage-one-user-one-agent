import os
from typing import Dict
from src.models import ViewerState

class StateStore:
    def __init__(self, storage_dir: str = "sample_run/viewer_state"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self._cache: Dict[str, ViewerState] = {}

    def get_or_create(self, viewer_id: str, arm: str = "agent") -> ViewerState:
        if viewer_id in self._cache:
            return self._cache[viewer_id]

        file_path = os.path.join(self.storage_dir, f"{viewer_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                state = ViewerState.model_validate_json(f.read())
        else:
            state = ViewerState(viewer_id=viewer_id, arm=arm)

        self._cache[viewer_id] = state
        return state

    def save(self, state: ViewerState):
        self._cache[state.viewer_id] = state
        file_path = os.path.join(self.storage_dir, f"{state.viewer_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(state.model_dump_json(indent=2))
