
from typing import Optional, List
from openenv.core.env_server import Action, Observation, State

class PasswordAction(Action):
    password: str
    task_type: str  # "classify", "improve", "analyze"

class PasswordObservation(Observation):
    task: str
    password: str
    feedback: str
    score: float
    attempts_remaining: int

class PasswordState(State):
    current_task: str = ""
    total_score: float = 0.0
    max_attempts: int = 3
