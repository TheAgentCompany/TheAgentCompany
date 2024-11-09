import os
import base64
import logging
import requests
from typing import List
from common import make_gitlab_request, evaluate_with_llm
from scoring import Result, Checkpoint, bonus_for_completing_final

TITLE = "agent workflow memory"
ABSTRACT = "Despite the potential of language model-based agents to solve real-world tasks such as web navigation, current methods still struggle with long-horizon tasks with complex action trajectories. In contrast, humans can flexibly solve complex tasks by learning reusable task workflows from past experiences and using them to guide future actions. To build agents that can similarly benefit from this process, we introduce Agent Workflow Memory (AWM), a method for inducing commonly reused routines, i.e., workflows, and selectively providing workflows to the agent to guide subsequent generations. AWM flexibly applies to both offline and online scenarios, where agents induce workflows from training examples beforehand or from test queries on the fly. We experiment on two major web navigation benchmarks — Mind2Web and WebArena — that collectively cover 1000+ tasks from 200+ domains across travel, shopping, and social media, among others. AWM substantially improves the baseline results by 24.6% and 51.1% relative success rate on Mind2Web and WebArena while reducing the number of steps taken to solve WebArena tasks successfully. Furthermore, online AWM robustly generalizes in cross-task, website, and domain evaluations, surpassing baselines from 8.9 to 14.0 absolute points as train-test task distribution gaps widen.".lower()


def grade_checkpoint1(trajectory):
    return "https://ogma.lti.cs.cmu.edu/apps/files/files/7095?dir=/Documents/Research&openfile=true" in trajectory


def grade_checkpoint2() -> int:
    """Check if agent correctly creates the teaser figure."""
    score = 0
    # 1. check if the file exists
    if not os.path.exists('/workspace/teaser.pdf'):
        return score
    score += 1
    
    # 2. check if figure shows agent improving
    # wait for image-supporting evaluation

    # 3. check if figure shows agent learn more complex skills over time
    # wait for image-supporting evaluation

    # 4. check if the figure shows baseline agent not improving
    # wait for image-supporting evaluation

    # 5. check if the figure does not have excessive whitespace
    # wait for image-supporting evaluation
    
    return score


def grade_checkpoint3() -> int:
    """Check if agent correctly creates the gitlab readme page."""
    score = 0
    
    # 1. check if the repo exists
    response = make_gitlab_request(additional_path="projects").json()
    for resp in response: 
        if resp["name"] == "agent-workflow-memory": print(resp)
    repo_names = [repo["name"] for repo in response]
    if "agent-workflow-memory" not in repo_names:
        return score
    score += 1
    
    # 2. check if the readme exists
    try:
        response = make_gitlab_request(
            project_identifier="root/agent-workflow-memory",
            additional_path="repository/files/README.md?ref=main",
        )
        if not response: return score
        response_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error occurred while extracting the README.md content: {e}")
        return score

    if response.status_code == 200:
        score += 1
        content = response_data.get("content", "")
        # decode the base64 encoded content
        content = base64.b64decode(content).decode("utf-8").lower()

        # 3. check if the README.md contains the title and abstract
        if TITLE in content and ABSTRACT in content:
            score += 1
        return score

    else:
        logging.warning(f"Unexpected status code: {response.status_code}")
        return score


def grade_checkpoint4() -> int:
    """Check if agent correctly creates a twitter thread."""
    score = 0
    
    # 1. if file exists
    if not os.path.exists('/workspace/thread.txt'):
        return score
    score += 1

    # 2. if each post have no more than 140 characters
    post_list = open('/workspace/thread.txt').read().split('\n\n\n')
    for post in post_list:
        if len(post.replace(' ', '')) > 140:
            return score
    score += 1

    # 3. if the posts are relevant to the project
    PROMPT = "The content do not need to express the same meaning as the predicate. As long as the two texts are topically relevant, a 'yes' answer is expected."
    for post in post_list:
        if not evaluate_with_llm(ABSTRACT, post, PROMPT):
            return score
    score += 1


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    scores2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(5, scores2))

    scores3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(3, scores3))

    scores4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(3, scores4))

    return result
