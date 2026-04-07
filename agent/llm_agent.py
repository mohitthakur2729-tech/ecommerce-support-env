import os
from openai import OpenAI
from env.models import Action
from agent.simple_agent import simple_agent

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
def llm_agent(obs):
    if client is None:
        print("No API key found, using fallback")
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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        action_text = response.choices[0].message.content.strip()
        action_text = action_text.lower().replace("-", "_").split()[0]

    except Exception as e:
        print("LLM failed, switching to fallback (no retry)")
        print(f"Error: {e}")

        progress = getattr(obs, "progress", [])
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