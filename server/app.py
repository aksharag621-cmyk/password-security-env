
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random, uuid, subprocess, sys

app = FastAPI()

state = {}

TASKS = [
    {"name": "weak_password_check", "password": "123456", "difficulty": "easy"},
    {"name": "medium_password_check", "password": "Password1", "difficulty": "medium"},
    {"name": "strong_password_check", "password": "T#9kL!mX2@pQ", "difficulty": "hard"},
]

def grade_password(password):
    score = 0.0
    if len(password) >= 8: score += 0.2
    if len(password) >= 12: score += 0.2
    if any(c.isupper() for c in password): score += 0.2
    if any(c.isdigit() for c in password): score += 0.2
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 0.2
    return round(min(score, 1.0), 2)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return {"tasks": [t["name"] for t in TASKS]}

@app.get("/grader")
def grader():
    results = []
    for t in TASKS:
        score = grade_password(t["password"])
        results.append({"task": t["name"], "difficulty": t["difficulty"], "score": score})
    return {"results": results}

@app.post("/baseline")
def baseline():
    result = subprocess.run(
        [sys.executable, "inference.py"],
        capture_output=True, text=True, timeout=300
    )
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}

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

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
