from fastapi import FastAPI
from pydantic import BaseModel
from inference import run_env

app = FastAPI()

# -------- REQUEST MODELS --------
class StepRequest(BaseModel):
    action: str

# -------- GLOBAL STATE --------
current_task = None


# -------- RESET ENDPOINT --------
@app.post("/reset")
def reset():
    global current_task
    current_task = "easy"
    return {
        "status": "reset successful",
        "task": current_task
    }


# -------- STEP ENDPOINT --------
@app.post("/step")
def step(req: StepRequest):
    return {
        "status": "step executed",
        "action": req.action
    }


# -------- STATE ENDPOINT --------
@app.get("/state")
def state():
    return {
        "state": "running",
        "task": current_task
    }