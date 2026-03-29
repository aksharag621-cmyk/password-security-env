
import random
import uuid
from openenv.core.env_server import Environment
from models import PasswordAction, PasswordObservation, PasswordState

class PasswordSecurityEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS = True

    TASKS = ["classify", "improve", "analyze"]

    def __init__(self):
        self._state = PasswordState()
        self._task = "classify"
        self._attempts = 3

    def _get_password(self):
        passwords = [
            "123456", "password", "abc123",
            "P@ssw0rd!", "Xy#9mK2$pL", "hello"
        ]
        return random.choice(passwords)

    def _check_strength(self, pwd):
        score = 0
        if len(pwd) >= 8: score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        if any(c in "!@#$%^&*" for c in pwd): score += 1
        if score <= 1: return "weak", score/4
        if score <= 3: return "medium", score/4
        return "strong", 1.0

    def reset(self, seed=None, episode_id=None, **kwargs):
        self._task = random.choice(self.TASKS)
        self._attempts = 3
        self._password = self._get_password()
        self._state = PasswordState(
            episode_id=episode_id or str(uuid.uuid4()),
            step_count=0,
            current_task=self._task
        )
        return PasswordObservation(
            done=False,
            reward=None,
            task=self._task,
            password=self._password,
            feedback=f"Task: {self._task} this password",
            score=0.0,
            attempts_remaining=self._attempts
        )

    def step(self, action: PasswordAction, **kwargs):
        self._state.step_count += 1
        self._attempts -= 1
        strength, score = self._check_strength(action.password)
        done = self._attempts <= 0
        return PasswordObservation(
            done=done,
            reward=score,
            task=self._task,
            password=action.password,
            feedback=f"Strength: {strength}",
            score=score,
            attempts_remaining=self._attempts
        )

    @property
    def state(self):
        return self._state
