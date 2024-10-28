import json
from typing import List

from scoring import Result, Checkpoint

from common import evaluate_with_llm, get_nextcloud_url_in_file, download_nextcloud_content

############################# Helper Functions #####################################

def check_job_description_content():

    with open("/workspace/job_description.md", "r") as f:
        final_content = f.read()
    
    with open("/workspace/template.md", "r") as f:
        template_content = f.read()
    
    with open("/workspace/requirement.txt", "r") as f:
        requirement_content = f.read()
    
    if "[Insert Information]" in final_content:
        print("some placeholder still present in the final job description.")
        return False

    predicate = f'a successful combination of the markdown template \"\"{template_content}\"\" and the requirement file \"\"{requirement_content}'
    additional_prompt = 'Pay special consideration to all of the numerical details. '
    return evaluate_with_llm(final_content, predicate, additional_prompt)

############################# Evaluator #####################################

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    link = get_nextcloud_url_in_file("/workspace/link.txt")
    pass_checkpoint1 = bool(link)
    checkpoints.append(Checkpoint(1, int(pass_checkpoint1)))

    pass_checkpoint2 = pass_checkpoint1 and download_nextcloud_content(link, "/workspace/job_description.md")
    checkpoints.append(Checkpoint(1, int(pass_checkpoint2)))

    pass_checkpoint3 = pass_checkpoint2 and check_job_description_content()
    checkpoints.append(Checkpoint(1, int(pass_checkpoint3)))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
