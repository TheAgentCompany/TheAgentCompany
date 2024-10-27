import json
import logging
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import *

GITLAB_ISSUE_URL = "http://the-agent-company.com:8929/root/bustub/-/issues/759"

# Check if gitlab issue was accessed
def checkpoint1(trajectory):
    return GITLAB_ISSUE_URL in trajectory

# Check if shared page exists
def checkpoint2():
    return get_nextcloud_url_in_file('/workspace/sharelink.txt')

# Check if content in nextcloud has the same keyword as the original one
def checkpoint3():
    try:
        url_content = get_nextcloud_url_in_file('/workspace/sharelink.txt')
        if not url_content:
            logging.warning("Could not get valid Nextcloud URL")
            return False
        
        if not download_nextcloud_content(url_content, "/workspace/downloaded.md"):
            logging.warning("Failed to download content")
            return False
            
        with open("/workspace/downloaded.md", "r") as f:
            downloaded_content = f.read()
            
        with open("/utils/instructions.md", "r") as f:
            origin_content = f.read()

        predicate = f'the same project instruction as the origin content \"\"{origin_content}\"\"'
        additional_prompt = 'You must strictly compare the two texts. Return "yes" only if they are nearly identical in content and length. Even small missing sections or modifications should result in a "no".'
        
        return evaluate_with_llm(downloaded_content, predicate, additional_prompt)
            
    except Exception as e:
        logging.warning(f"Unexpected error in checkpoint3: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, checkpoint2()))
    checkpoints.append(Checkpoint(1, checkpoint3()))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
