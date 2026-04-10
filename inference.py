import time
from agent.simple_agent import simple_agent
from dotenv import load_dotenv
load_dotenv()
from env.enviroment import EcommerceSupportEnv
from env.models import Action
from agent.llm_agent import llm_agent
from agent.simple_agent import simple_agent
from graders.easy_grader import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader import grade as hard_grade
from openai import OpenAI
import os

# ✅ Required environment variables (DO NOT CHANGE NAMES)
API_BASE_URL = os.environ.get("API_BASE_URL", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "")


#  Correct OpenAI client 
client = None
try:
    client = OpenAI(
        api_key=os.environ["API_KEY"],          
        base_url=os.environ["API_BASE_URL"]     
    )
except Exception:
    client = None
        



# -------------------------------
# RUN ENVIRONMENT
# -------------------------------
def run_env(difficulty="medium"):
    env = EcommerceSupportEnv(difficulty=difficulty)
    obs = env.reset()

    total_reward = 0
    done = False
    step_num = 0

    print("[START]")
    print(f"Initial Query: {obs.query}")

    while not done and step_num < 15:   
        step_num += 1

        try:
            action = llm_agent(obs)
        except:
            action = simple_agent(obs)  # backup

        result = env.step(action)

        total_reward += result.reward

        print(f"[STEP {step_num}] {action.action_type} | Reward: {result.reward} | Progress: {result.info['progress']}")

        obs = result.observation
        done = result.done

    print("DONE ✅")

    print("[END]")
    total_reward = min(total_reward, 1.0)
    
   # grading
    if difficulty == "easy":
        score = easy_grade(result.info["progress"])
    elif difficulty == "medium":
        score = medium_grade(result.info["progress"])
    else:
        score = hard_grade(result.info["progress"])

# ✅ VERY IMPORTANT FIX
    if score >= 1.0:
        score = 0.99
    elif score <= 0.0:
        score = 0.01

    print(f"[END]")
    print(f"Total Reward: {total_reward}")
    print(f"Score: {score}")


# -------------------------------
# MAIN ENTRY
# -------------------------------
if __name__ == "__main__":
    print("Running once...")

    run_env("easy")
    run_env("medium")
    run_env("hard")

    print("Finished execution.") 