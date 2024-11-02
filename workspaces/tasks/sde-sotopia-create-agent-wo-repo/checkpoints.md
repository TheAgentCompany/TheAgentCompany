# Checkpoints

This task has 6 points in total.

## Checkpoint 1 (1pt)
Clone the sotopia repo from gitlab. (i.e., `git clone http://the-agent-company.com:8929/root/sotopia.git`)

## Checkpoint 2 (1pt)

Create a new branch called `feature/actionAgent` in the local sotopia repo following the contribution guidelines in the docs.

## Checkpoint 3 (2pt)

Write python code to create a new agent called `ActionAgent` that can only issue action commands in the `sotopia/agents/llm_agent.py` file.
(Ensure that the new agent class `ActionAgent` inherits from `LLMAgent` and includes the keyword "ActionAgent". We will only perform a basic sanity test to verify this.)

## Checkpoint 4 (1pt)

Make sure the new branch pass the mypy check.

## Checkpoint 5 (1pt)

Push the change to the gitlab and make a pull request