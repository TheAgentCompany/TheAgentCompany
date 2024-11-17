import logging

from common import create_rocketchat_client, evaluate_with_llm, get_rocketchat_personal_chat_history, download_image_from_url, get_gitlab_project_id, make_gitlab_request, grader
from scoring import Result, Checkpoint, bonus_for_completing_final

PROJECT_NAME = "sotopia"
NPC_NAME = "Jessica Lee"

@grader
def grade_checkpoint1(rocket_client):
    """Check if the agent sent the picture to NPC"""
    history = get_rocketchat_personal_chat_history(rocket_client, NPC_NAME, content_only=False)
    for msg in history:
        if msg.get("attachments"):
            return True
    return False

@grader
def grade_checkpoint2():
    project_id = get_gitlab_project_id(PROJECT_NAME)
    if project_id is None:
        logging.error(f"Project {PROJECT_NAME} not found")
        return False

    project_resp = make_gitlab_request(project_id)
    if project_resp is None:
        logging.error(f"Failed to get project {PROJECT_NAME}")
        return False
    project = project_resp.json()

    avatar_url = project.get("avatar_url")
    if avatar_url is None:
        logging.error(f"Avatar should be set for the project {PROJECT_NAME}")
        return False

    image_path = download_image_from_url(avatar_url, "gitlab_project_logo.jpg")
    if not image_path:
        logging.error(f"Failed to download image from {avatar_url}")
        return False
    
    return evaluate_with_llm(
        content="",
        predicate="there is a letter 'S' in the middle of the picture",
        image_path=image_path
    )

def grade_checkpoints(trajectory=""):
    rocket_client = create_rocketchat_client()
    checkpoint1 = Checkpoint(1, 1*int(grade_checkpoint1(rocket_client)))
    checkpoint2 = Checkpoint(2, 2*int(grade_checkpoint2()))
    checkpoints = [checkpoint1, checkpoint2]
    return Result(checkpoints)

