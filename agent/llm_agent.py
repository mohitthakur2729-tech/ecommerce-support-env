import os
from openai import OpenAI
from env.models import Action
from agent.simple_agent import simple_agent

from dotenv import load_dotenv
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = None
if API_BASE_URL and MODEL_NAME and HF_TOKEN:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )
    
def llm_agent(obs):
    if client is None:
        print("No API config found, using fallback")
    return simple_agent(obs)

    try:
        prompt = f"""You are an ecommerce support AI.

Current user query: {obs.query}
Current progress: {obs.progress}
Difficulty: {getattr(obs, 'difficulty', 'unknown')}

Task: Select the logical NEXT action. Avoid repeats.

Available actions:
- respond_user
- ask_order_id
- verify_order
- process_refund
- handle_missing_item
- identify_multiple_issues

Respond with ONLY the action name:"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        action_text = response.choices[0].message.content.strip()
        action_text = action_text.lower().replace("-", "_").split()[0]

    except Exception as e:
        print("LLM failed, switching to fallback (no retry)")
        print(f"Error: {e}")

        progress = getattr(obs, "progress", []) or []
        difficulty = getattr(obs, "difficulty", "unknown")

        if difficulty == "easy":
            action_text = "respond_user"

        elif difficulty == "medium":
            steps = ["ask_order_id", "verify_order", "process_refund"]
            remaining = [step for step in steps if step not in progress]
            action_text = remaining[0] if remaining else "respond_user"

        elif difficulty == "hard":
            steps = ["identify_multiple_issues", "process_refund", "handle_missing_item"]
            remaining = [step for step in steps if step not in progress]
            action_text = remaining[0] if remaining else "respond_user"

        else:
            action_text = "respond_user"

    return Action(action_type=action_text, content="")