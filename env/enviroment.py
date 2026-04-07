from env.models import Observation, Action, StepResult
from env.tasks import get_task

class EcommerceSupportEnv:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.current_task = None
        self.state_data = None
        self.done = False

    def reset(self):
        self.current_task = get_task(self.difficulty)

        self.state_data = {
            "query": self.current_task["query"],
            "difficulty": self.difficulty,
            "history": [],
            "order_status": self.current_task.get("order_status", "unknown"),
            "step_count": 0,
            "progress": []
        }

        self.done = False

        return Observation(**self.state_data)

    def state(self):
        return Observation(**self.state_data)

    def step(self, action: Action):
        if self.done:
            return StepResult(self.state(), 0, True, {})

        reward = 0
        self.state_data["step_count"] += 1
        self.state_data["history"].append(action.action_type)

        expected = self.current_task.get("expected_steps", [])

        # Unified progress tracking and rewards
        if action.action_type in expected:
            if action.action_type not in self.state_data["progress"]:
                self.state_data["progress"].append(action.action_type)
                reward = 0.3  # step progress
        
        # Completion check (all difficulties)
        if set(self.state_data["progress"]) == set(expected):
            reward = 1.0
            self.done = True
        elif action.action_type in expected:
            reward = 0.3
        else:
            reward = -0.1  # invalid/repeat penalty

        # Safety limits
        if self.state_data["step_count"] >= 15:
            self.done = True
            if reward != 1.0:
                reward = -0.5  # failure

        return StepResult(
            observation=self.state(),
            reward=reward,
            done=self.done,
            info={"progress": self.state_data["progress"]}
        )
