from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Observation:
    query: str
    difficulty: str
    history: List[str]
    order_status: str
    step_count: int
    progress: List[str]

@dataclass
class Action:
    action_type: str
    content: str = ""

@dataclass
class StepResult:
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]
