import os
import sys

from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN", "dummy-key")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

TASKS = [
    {"name": "weak_password_check", "password": "123456", "difficulty": "easy"},
    {"name": "medium_password_check", "password": "Password1", "difficulty": "medium"},
    {"name": "strong_password_check", "password": "T#9kL!mX2@pQ", "difficulty": "hard"},
]

def grade_password(password):
    score = 0.0
    if len(password) >= 8:
        score += 0.2
    if len(password) >= 12:
        score += 0.2
    if any(c.isupper() for c in password):
        score += 0.2
    if any(c.isdigit() for c in password):
        score += 0.2
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 0.2
    return round(min(score, 1.0), 2)

def run_task(task):
    name = task["name"]
    password = task["password"]
    prompt = f"Evaluate the security of this password and suggest improvements: {password}"
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        agent_response = response.choices[0].message.content
    except Exception as e:
        agent_response = f"Error: {str(e)}"

    steps = 3
    rewards = []

    print(f"[START] task={name}", flush=True)

    # Step 1: analyse password
    reward1 = grade_password(password) * 0.4
    rewards.append(reward1)
    print(f"[STEP] step=1 reward={round(reward1,2)}", flush=True)

    # Step 2: agent response quality
    reward2 = 0.3 if len(agent_response) > 30 else 0.1
    rewards.append(reward2)
    print(f"[STEP] step=2 reward={round(reward2,2)}", flush=True)

    # Step 3: final grading
    reward3 = grade_password(password) * 0.3
    rewards.append(reward3)
    print(f"[STEP] step=3 reward={round(reward3,2)}", flush=True)

    total_score = round(sum(rewards), 2)
    print(f"[END] task={name} score={total_score} steps={steps}", flush=True)

    return total_score

def main():
    scores = []
    for task in TASKS:
        score = run_task(task)
        scores.append(score)

    avg = round(sum(scores) / len(scores), 2)
    print(f"Average score: {avg}", flush=True)

if __name__ == "__main__":
    main()
