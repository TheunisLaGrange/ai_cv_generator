import time
from typing import Dict, Any, Optional

class StepTrace:
    """A completely generic tracer that knows nothing about your specific business logic."""
    def __init__(self, step_name: str, step_index: int):
        self.step_name: str = step_name
        self.step_index: int = step_index
        self.timestamp: float = time.time()
        self.status: str = "PENDING"
        self.payload: Dict[str, Any] = {}
        self.error_code: Optional[str] = None
        self.diagnostic_msg: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
