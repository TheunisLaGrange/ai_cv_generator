import uuid
from typing import List, Dict, Any

class AgentState:
    """The clean domain state required for database persistence."""
    def __init__(self, objective: str):
        self.session_id: str = str(uuid.uuid4())
        self.objective: str = objective
        self.plan: List[str] = []
        self.current_step_index: int = 0
        self.trace_history: List[Dict[str, Any]] = []  # Just raw data logs
        self.status: str = "INITIALIZED"
        self.wake_time: float = 0.0

    def save_checkpoint(self):
        print(f"--- [CHECKPOINT SAVED] Status: {self.status} | Step: {self.current_step_index}/{len(self.plan)} ---")
