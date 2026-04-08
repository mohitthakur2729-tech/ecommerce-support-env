from fastapi import FastAPI
from inference import run_env

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server running"}

@app.post("/reset")
def reset():
    return {"status": "reset ok"}

@app.post("/step")
def step():
    return {"status": "step ok"}

@app.get("/state")
def state():
    return {"status": "state ok"}