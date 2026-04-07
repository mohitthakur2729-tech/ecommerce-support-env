import time
from dotenv import load_dotenv
load_dotenv()
import os
from env.enviroment import EcommerceSupportEnv
from env.models import Action
from agent.llm_agent import llm_agent
from agent.simple_agent import simple_agent
from graders.easy_grader import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader import grade as hard_grade

# Required ENV variables (as per hackathon)
API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Keep simple_agent as backup
def simple_agent(observation):
    query = observation.query.lower()
    progress = observation.progress

    # 🟢 EASY TASK
    if "missing" in query and "damaged" in query:
        if "identify_multiple_issues" not in progress:
            return Action("identify_multiple_issues", "Detected multiple issues.")

        elif "process_refund" not in progress:
            return Action("process_refund", "Refunding damaged item.")

        elif "handle_missing_item" not in progress:
            return Action("handle_missing_item", "Handling missing item.")

        else:
            return Action("respond_user", "All issues resolved.")

    # 🟡 MEDIUM TASK
    if "ask_order_id" not in progress:
        return Action("ask_order_id", "Please provide your order ID.")

    elif "verify_order" not in progress:
        return Action("verify_order", "Verifying your order.")

    elif "process_refund" not in progress:
        return Action("process_refund", "Initiating refund.")

    else:
        return Action("respond_user", "Issue resolved.")


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

    print("Finished execution. Sleeping...")
    time.sleep(3600)  