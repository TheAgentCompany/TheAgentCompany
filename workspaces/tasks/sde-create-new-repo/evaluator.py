import requests
import logging
import urllib

from common import create_rocketchat_client
from common import make_gitlab_request
from common import evaluate_with_llm
from common import evaluate_chat_history_with_llm


############################# Init Variables #####################################
project_path = "root/new-storage-project"

readme_path = "README.md"

# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Helper Functions #####################################

def get_history(username):
    id = ""
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")
    return msgs


def check_repo_exist():
    try:
        response = make_gitlab_request(project_path)
 
        if response is not None and response.status_code == 200:
            logging.info(f"New repository '{project_path}' created successfully.")
            return True
        else:
            logging.info(f"Repository '{project_path}' not found.")
            return False
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False


def check_readme_content():
    readme_encoded_path = urllib.parse.quote(readme_path, safe='')
    try:
        readme = make_gitlab_request(project_path, f"repository/files/{readme_encoded_path}/raw?ref=main")
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking readme file: {e}")
        return False
    
    if not readme:
        logging.warning("Readme file doesn't exist or is empty")
        return False

    predicate = "some details about a new storage system project"
    return evaluate_with_llm(readme, predicate)


def check_conversation_with_leader():
    return evaluate_chat_history_with_llm(
        rocket,
        "zhang_wei",
        "there are some tasks to start a new data storage related project"
        )

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    if check_conversation_with_leader():
        print("successfully asked leader about the new storage project")
        points += 1

    if check_repo_exist():
        print("new repo successfully created")
        points += 1
    
    if check_readme_content():
        print("README successfully updated")
        points += 1

    # Final result
    print(f"Evaluation completed. Final score: {points}/3")
    return points

if __name__ == "__main__":
    evaluate_task()
