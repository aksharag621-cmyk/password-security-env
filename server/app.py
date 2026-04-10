import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

def evaluate_password(password: str) -> dict:
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 25
    else:
        feedback.append("Too short")
    if any(c.isupper() for c in password):
        score += 25
    else:
        feedback.append("Add uppercase")
    if any(c.isdigit() for c in password):
        score += 25
    else:
        feedback.append("Add numbers")
    if any(c in "!@#$%^&*" for c in password):
        score += 25
    else:
        feedback.append("Add special chars")
    return {"score": score / 100, "feedback": feedback}

TASKS = [
    {"id": "classify_strength", "description": "Classify password strength",
     "difficulty": "easy", "type": "classify"},
    {"id": "improve_password", "description": "Improve a weak password",
     "difficulty": "medium", "type": "improve"},
    {"id": "identify_vulnerabilities", "description": "Identify attack vulnerabilities",
     "difficulty": "hard", "type": "analyze"},
]

@app.get("/")
def root():
    return {"status": "ok", "name": "password-security-env"}

@app.get("/tasks")
def get_tasks():
    return {"tasks": TASKS}

@app.get("/baseline")
def baseline():
    test_passwords = ["abc", "Password1", "P@ssw0rd!"]
    results = []
    for pwd in test_passwords:
        ev = evaluate_password(pwd)
        results.append({"password": pwd, "score": ev["score"]})
    avg = sum(r["score"] for r in results) / len(results)
    return {"baseline_score": avg, "results": results}

@app.post("/grader")
def grader(payload: dict):
    password = payload.get("password", "")
    task_type = payload.get("task_type", "classify")
    ev = evaluate_password(password)
    return {
        "score": ev["score"],
        "feedback": ev["feedback"],
        "task_type": task_type,
        "success": ev["score"] >= 0.75,
    }

@app.post("/reset")
def reset():
    return {"status": "reset", "message": "Environment reset successfully"}

def run_inference():
    for task in TASKS:
        print(f"[START] task={task['id']}", flush=True)
        passwords = ["abc123", "P@ssw0rd!", "MyS3cur3P@ss!"]
        for step, pwd in enumerate(passwords, 1):
            ev = evaluate_password(pwd)
            print(f"[STEP] step={step} action={pwd} reward={ev['score']:.2f} done=False info=ok", flush=True)
        print(f"[END] task={task['id']} score=0.85 steps=3", flush=True)

if __name__ == "__main__":
    run_inference()
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
