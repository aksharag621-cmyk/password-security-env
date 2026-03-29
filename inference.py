
import os
import sys
sys.path.insert(0, '/content/password_security_env')

from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN or "dummy-key")

def run_task(task_type, password):
    prompt = f"Task: {task_type} this password: {password}"
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content
    except:
        return password

def main():
    tasks = [
        ("classify", "123456"),
        ("improve", "password"),
        ("analyze", "P@ssw0rd!")
    ]
    scores = []
    for task_type, pwd in tasks:
        result = run_task(task_type, pwd)
        score = len(result) / 100.0
        score = min(1.0, score)
        scores.append(score)
        print(f"Task: {task_type} | Password: {pwd} | Score: {score:.2f}")
    print(f"Average score: {sum(scores)/len(scores):.2f}")

if __name__ == "__main__":
    main()
