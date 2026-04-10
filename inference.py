import time
from agent.simple_agent import simple_agent
from dotenv import load_dotenv
load_dotenv()

from env.enviroment import EcommerceSupportEnv
from env.models import Action
from agent.llm_agent import llm_agent
from graders.easy_grader import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader import grade as hard_grade

import os
from openai import OpenAI

# ------------------------------
# ENV VARIABLES
# ------------------------------
API_BASE_URL = os.environ.get("API_BASE_URL", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "")

client = None
try:
    client = OpenAI(
        api_key=os.environ.get("API_KEY"),
        base_url=os.environ.get("API_BASE_URL")
    )
except:
    client = None

# ------------------------------
# RUN ENV
# ------------------------------
def run_env(difficulty="medium"):
    env = EcommerceSupportEnv(difficulty=difficulty)
    obs = env.reset()

    total_reward = 0.0
    done = False
    step_num = 0

    print("[START]")
    print(f"Initial Query: {obs.query}")

    final_progress = []

    while not done and step_num < 15:
        step_num += 1

        try:
            action = llm_agent(obs)
        except:
            action = simple_agent(obs)

        result = env.step(action)

        total_reward += result.reward

        print(f"[STEP {step_num}] {action.action_type} | Reward: {result.reward} | Progress: {result.info['progress']}")

        obs = result.observation
        done = result.done

        # ✅ FIX: Extract string action types from progress
        raw_progress = result.info["progress"]
        if isinstance(raw_progress, list):
            final_progress = []
            for p in raw_progress:
                if isinstance(p, str):
                    final_progress.append(p)
                elif hasattr(p, 'action_type'):
                    final_progress.append(p.action_type)
                else:
                    final_progress.append(str(p))
        else:
            final_progress = []

    print("DONE")
    print("[END]")

    # ------------------------------
    # GRADING
    # ------------------------------
    if difficulty == "easy":
        score = easy_grade(final_progress)
    elif difficulty == "medium":
        score = medium_grade(final_progress)
    else:
        score = hard_grade(final_progress)

    # ✅ FIX: Guarantee strict (0, 1) range — never 0.0 or 1.0
    score = max(0.01, min(0.99, float(score)))
    total_reward = max(0.01, min(0.99, float(total_reward)))

    print(f"Total Reward: {total_reward}")
    print(f"Score: {score}")

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    print("Running once...\n")

    run_env("easy")
    run_env("medium")
    run_env("hard")

    print("Finished execution.")