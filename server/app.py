from fastapi import FastAPI
import uvicorn

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


# ✅ REQUIRED FOR OPENENV
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()