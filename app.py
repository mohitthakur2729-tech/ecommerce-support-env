import gradio as gr
from inference import run_env

def run_agent(difficulty):
    run_env(difficulty)
    return f"✅ Completed {difficulty} task. Check logs."

iface = gr.Interface(
    fn=run_agent,
    inputs=gr.Dropdown(["easy", "medium", "hard"], label="Select Difficulty"),
    outputs="text",
    title="🛒 Ecommerce Support RL Agent"
)

if __name__ == "__main__":
    iface.launch()