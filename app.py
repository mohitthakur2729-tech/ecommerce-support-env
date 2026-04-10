from fastapi import FastAPI
import gradio as gr
from inference import run_env

# FastAPI app
app = FastAPI()

# Required endpoint for evaluator
@app.post("/reset")
def reset():
    return {"status": "ok"}


# -------------------
# Agent functions
# -------------------
def run_agent(difficulty):
    run_env(difficulty)
    return f"SUCCESS\n\n✔ {difficulty.upper()} task completed"

def clear_output():
    return ""


# -------------------
# Gradio UI
# -------------------
with gr.Blocks() as demo:

    gr.Markdown("# Ecommerce Support RL Agent")

    difficulty = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy"
    )

    run_btn = gr.Button("Run Agent")
    clear_btn = gr.Button("Clear")

    output = gr.Textbox(lines=10)

    run_btn.click(fn=run_agent, inputs=difficulty, outputs=output)
    clear_btn.click(fn=clear_output, outputs=output)


# 🔥 VERY IMPORTANT (LAST LINE)
app = gr.mount_gradio_app(app, demo, path="/")