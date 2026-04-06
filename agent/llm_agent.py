import os
from openai import OpenAI
from env.models import Action

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_agent(obs):
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
        # Parse action (robust)
        action_text = action_text.lower().replace("-", "_").split()[0]

    except Exception as e:
        print("LLM failed, switching to fallback (no retry)")
        print(f"Error: {e}")

        # Deterministic fallback using difficulty
        progress = obs.progress
        try:
            difficulty = obs.difficulty
        except AttributeError:
            difficulty = "unknown"  # backward compat

        if difficulty == "easy":
            action_text = "respond_user"
        elif difficulty == "medium":
            medium_steps = ["ask_order_id", "verify_order", "process_refund"]
            remaining = [step for step in medium_steps if step not in progress]
            action_text = remaining[0] if remaining else "respond_user"
        elif difficulty == "hard":
            hard_steps = ["identify_multiple_issues", "process_refund", "handle_missing_item"]
            remaining = [step for step in hard_steps if step not in progress]
            action_text = remaining[0] if remaining else "respond_user"
        else:
            # Keyword fallback for unknown
            query_lower = obs.query.lower()
            if any(word in query_lower for word in ['status', 'delivery']):
                action_text = "respond_user"
            elif any(word in query_lower for word in ['payment', 'order']):
                medium_steps = ["ask_order_id", "verify_order", "process_refund"]
                remaining = [step for step in medium_steps if step not in progress]
                action_text = remaining[0] if remaining else "respond_user"
            else:
                action_text = "respond_user"

    return Action(action_type=action_text, content="")
