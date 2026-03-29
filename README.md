# Password Security Environment

A real-world OpenEnv environment where AI agents learn to evaluate and improve password security.

## Tasks
- Task 1 (Easy): Classify password strength
- Task 2 (Medium): Improve a weak password
- Task 3 (Hard): Identify attack vulnerabilities

## Action Space
- password: string
- task_type: string (classify, improve, analyze)

## Observation Space
- task, password, feedback, score, attempts_remaining

## Setup
pip install openenv-core
