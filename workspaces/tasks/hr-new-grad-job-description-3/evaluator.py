import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm, create_rocketchat_client, get_chat_history, get_nextcloud_url_in_file, download_nextcloud_content


# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Helper Functions #####################################

def check_job_description_content():

    with open("/workspace/job_description.md", "r") as f:
        final_content = f.read()
    
    with open("/instruction/template.md", "r") as f:
        template_content = f.read()
    
    with open("/utils/requirement.txt", "r") as f:
        requirement_content = f.read()
    
    if "[Insert Information]" in final_content:
        logging.error("some placeholder still present in the final job description.")
        return False

    predicate = f'a successful combination of the markdown template \"\"{template_content}\"\" and the requirement file \"\"{requirement_content}'
    additional_prompt = 'Pay special consideration to all of the numerical details. '
    return evaluate_with_llm(final_content, predicate, additional_prompt)

############################# Evaluator #####################################


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    chat_history = get_chat_history(rocket, "zhang_wei")
    pass_checkpoint1 = chat_history is not None and len(chat_history) > 0
    checkpoints.append(Checkpoint(1, int(pass_checkpoint1)))

    chat_history = get_chat_history(rocket, "li_ming")
    pass_checkpoint2 = chat_history is not None and len(chat_history) > 0
    checkpoints.append(Checkpoint(1, int(pass_checkpoint2)))

    link = get_nextcloud_url_in_file("/workspace/link.txt")
    pass_checkpoint3 = bool(link)
    checkpoints.append(Checkpoint(1, int(pass_checkpoint3)))

    pass_checkpoint4 = pass_checkpoint3 and download_nextcloud_content(link, "/workspace/job_description.md")
    checkpoints.append(Checkpoint(1, int(pass_checkpoint4)))

    pass_checkpoint5 = pass_checkpoint4 and check_job_description_content()
    checkpoints.append(Checkpoint(1, int(pass_checkpoint5)))
    return result
