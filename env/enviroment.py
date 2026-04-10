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
            return StepResult(self.state(), 0.01, True, {})

        reward = 0.01
        self.state_data["step_count"] += 1
        self.state_data["history"].append(action.action_type)

        expected = self.current_task.get("expected_steps", [])

        if action.action_type in expected:
            if action.action_type not in self.state_data["progress"]:
                self.state_data["progress"].append(action.action_type)
                reward = 0.3

        if set(self.state_data["progress"]) == set(expected):
            reward = 0.99   # ✅ completion — never 1.0
            self.done = True
        elif action.action_type in expected:
            reward = 0.3
        else:
            reward = 0.01   # ✅ invalid — never negative, never 0.0

        if self.state_data["step_count"] >= 15:
            self.done = True
            if reward != 0.99:
                reward = 0.01

        # Nuclear clamp — absolute guarantee
        reward = max(0.01, min(0.99, float(reward)))

        return StepResult(
            observation=self.state(),
            reward=reward,
            done=self.done,
            info={"progress": self.state_data["progress"]}
        )