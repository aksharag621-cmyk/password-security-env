from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random, uuid

app = FastAPI()

state = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    passwords = ["123456", "password", "P@ssw0rd!", "abc123"]
    pwd = random.choice(passwords)
    task = random.choice(["classify", "improve", "analyze"])
    state["password"] = pwd
    state["task"] = task
    state["episode_id"] = str(uuid.uuid4())
    state["step_count"] = 0
    return {"observation": {"task": task, "password": pwd, "feedback": "Start!", "score": 0.0, "attempts_remaining": 3}, "reward": None, "done": False, "episode_id": state["episode_id"]}

@app.post("/step")
def step(req: dict):
    state["step_count"] = state.get("step_count", 0) + 1
    pwd = req.get("password", "")
    score = min(1.0, len([c for c in pwd if c.isupper() or c.isdigit() or c in "!@#$%"]) / 4)
    done = state["step_count"] >= 3
    return {"observation": {"task": state.get("task","classify"), "password": pwd, "feedback": "Checked!", "score": score, "attempts_remaining": 3 - state["step_count"]}, "reward": score, "done": done, "episode_id": state.get("episode_id","")}

@app.get("/state")
def get_state():
    return {"episode_id": state.get("episode_id",""), "step_count": state.get("step_count",0), "current_task": state.get("task",""), "max_attempts": 3}
