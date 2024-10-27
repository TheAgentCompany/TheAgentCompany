import sys
import logging
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

def grade_checkpoints(trajectory):
    checkpoints = [
        (lambda: checkpoint1(trajectory), "GitLab issue page accessed"),
        (checkpoint2, "Shared page exists and is accessible"),
        (checkpoint3, "Content verification passed"),
    ]
    
    points = 0
    for i, (grade_func, description) in enumerate(checkpoints):
        try:
            passed = grade_func()
            if passed:
                if i == 2:  
                    points = 3 
                else:
                    points += 1
            print(f"{'✓' if passed else '✗'} {description}")
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")
            break
    
    return points

def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return ""
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, assuming empty trajectory")
        trajectory = []
    else:
        trajectory = load_trajectory(sys.argv[1])

    points = grade_checkpoints(trajectory)
    print(f"\nFinal points for moving page to nextcloud task: {points}/3")