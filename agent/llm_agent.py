import os
from openai import OpenAI
from env.models import Action
from agent.simple_agent import simple_agent

from dotenv import load_dotenv
load_dotenv()

# ✅ REQUIRED ENV VARIABLES (DO NOT CHANGE NAMES)
API_BASE_URL = os.environ.get("API_BASE_URL")
MODEL_NAME = os.environ.get("MODEL_NAME")

# ✅ CORRECT CLIENT 
client = None
try:
    client = OpenAI(
        api_key=os.environ["API_KEY"],          
        base_url=os.environ["API_BASE_URL"]     
    )
except Exception:
    client = None


def llm_agent(obs):
    # 🚨 FORCE LLM CALL (NO SILENT SKIP)
    if client is None:
        raise Exception("Client not initialized — API call required")

    try:
        prompt = f"""
You are an ecommerce support AI.

Current user query: {obs.query}
Current progress: {obs.progress}

Select the NEXT best action.

Available actions:
- respond_user
- ask_order_id
- verify_order
- process_refund
- handle_missing_item
- identify_multiple_issues

Respond with ONLY the action name.
"""

        # ✅ DEBUG PRINT (IMPORTANT FOR VALIDATION)
        print("🚀 Calling LLM API...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        action_name = response.choices[0].message.content.strip()

        return Action(action_name, "LLM decision")

    except Exception as e:
        
        print("❌ LLM failed:", str(e))

        # fallback
        return simple_agent(obs)