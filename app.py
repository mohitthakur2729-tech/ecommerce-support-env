import gradio as gr
from inference import run_env

def run_agent(difficulty):
    run_env(difficulty)
    return f" SUCCESS\n\n✔ {difficulty.upper()} task completed\n✔ Agent executed correctly\n✔ Check logs for step-by-step actions"

def clear_output():
    return ""

#  Custom CSS for premium look
custom_css = """
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

.gradio-container {
    max-width: 1000px !important;
    margin: auto;
}

h1, h3 {
    text-align: center;
}

.card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.3);
}

button {
    border-radius: 10px !important;
    font-weight: bold !important;
}

#run-btn {
    background: linear-gradient(90deg, #ff7a18, #ffb347) !important;
    color: black !important;
}

#clear-btn {
    background: #334155 !important;
    color: white !important;
}
"""

with gr.Blocks() as demo:

    # Header
    gr.Markdown("""
    #  Ecommerce Support RL Agent
    ### AI-Powered Customer Support Automation
    """)

    with gr.Row():

        # LEFT PANEL
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### Controls")

                difficulty = gr.Dropdown(
                    ["easy", "medium", "hard"],
                    value="easy",
                    label="Select Difficulty"
                )

                run_btn = gr.Button(" Run Agent", elem_id="run-btn")
                clear_btn = gr.Button(" Clear", elem_id="clear-btn")

        # RIGHT PANEL
        with gr.Column(scale=2):
            with gr.Group():
                gr.Markdown("###  Execution Output")

                output = gr.Textbox(lines=10,placeholder="Agent execution results will appear here...")

    #  Actions
    run_btn.click(
        fn=run_agent,
        inputs=difficulty,
        outputs=output,
        show_progress=True
    )

    clear_btn.click(
        fn=clear_output,
        outputs=output
    )

    #  Footer
    gr.Markdown("""
    ---
     **Features**
    - Reinforcement Learning environment  
    - LLM + fallback hybrid agent  
    - Multi-step task execution  

     Built for real-world ecommerce automation
    """)

demo.launch(css=custom_css)