import os
import requests
from common import llm_evaluate

import logging
import urllib


############################# Init Variables #####################################
# Rocket.Chat variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'

ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

base_url = "http://the-agent-company.com:8929/api/v4"
project_path = "root/new-storage-project"
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}

readme_path = "README.md"

from common import create_rocketchat_client

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


def check_with_llm(msgs, pattern):
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg']

    if len(content)==0:
        return False

    messages = [
        {
            "content": f"Does the text \"{content}\" include some tasks to start a new data storage related project? Answer 'yes' if it does, or 'no' if it doesn't. Don't answer anything else.",
            "role": "user"}
    ]
    llm_resonse = llm_evaluate(messages)
    logging.info(llm_resonse)

    if pattern in llm_resonse['choices'][0]['message']['content'].lower():
        return True
    else:
        return False

def check_repo_exist():

    encoded_path = urllib.parse.quote(project_path, safe='')
    url = f"{base_url}/projects/{encoded_path}"

    try:
        response = requests.get(url, headers=headers)
 
        if response.status_code == 200:
            logging.info(f"New repository '{project_path}' created successfully.")
            return True
        else:
            logging.info(f"Repository '{project_path}' not found.")
            return False
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False

def check_readme_content():

    encoded_path = urllib.parse.quote(project_path, safe='')
    readme_encoded_path = urllib.parse.quote(readme_path, safe='')
    url = f"{base_url}/projects/{encoded_path}/repository/files/{readme_encoded_path}/raw?ref=main"

    try:
        readme = requests.get(url, headers=headers).text
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking readme file: {e}")
        return False

    messages = [{"content": f"Does the readme \"\"{readme}\"\" provide some details about a new storage system project? Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]
    
    # # Check result
    llm_resonse = llm_evaluate(messages)
    print(llm_resonse)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        print(f"README does include information about a new storage project")
        return True
    else:
        print(f"README does not include information about a new storage project")
        return False


def check_conversation_with_leader():
    msgs = get_history(username="zhang_wei")
    return check_with_llm(msgs, pattern='yes')

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
