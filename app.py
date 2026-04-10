from fastapi import FastAPI
import gradio as gr
from inference import run_env

app = FastAPI()

@app.post("/reset")
def reset():
    return {"status": "ok"}

def run_agent(difficulty):
    run_env(difficulty)
    return f"{difficulty.upper()} task completed"

def clear_output():
    return ""

with gr.Blocks() as demo:
    gr.Markdown("# Ecommerce Support RL Agent")

    difficulty = gr.Dropdown(["easy", "medium", "hard"], value="easy")
    run_btn = gr.Button("Run Agent")
    clear_btn = gr.Button("Clear")
    output = gr.Textbox(lines=10)

    run_btn.click(run_agent, inputs=difficulty, outputs=output)
    clear_btn.click(clear_output, outputs=output)

# ✅ ONLY THIS (NO launch)
app = gr.mount_gradio_app(app, demo, path="/")