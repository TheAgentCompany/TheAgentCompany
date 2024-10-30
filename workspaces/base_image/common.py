import os
import logging
import urllib
import subprocess
import re
import requests

import litellm
from rocketchat_API.rocketchat import RocketChat

from config import *

logging.basicConfig(level=logging.INFO)


class MockRocketChatClient:

    class JsonResponse:
        def json(self):
            return {'users': [], 'messages': []}

    def __getattr__(self, name):
        def method(*args, **kwargs):
            return self.JsonResponse()
        return method
    

# messages: a list of message.
# example [{ "content": "Hello, how are you?","role": "user"}]
def llm_complete(messages):
    if TEST_MODE:
        return {'choices': [{'message': {"content": "Hello, how are you?","role": "user"}}]}

    return litellm.completion(
        api_key=LITELLM_API_KEY,
        base_url=LITELLM_BASE_URL,
        model=LITELLM_MODEL,
        messages=messages
    ).json()


def create_rocketchat_client(username='theagentcompany', password='theagentcompany'):
    SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
    ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
    
    # Construct RocketChat URL
    ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
    
    try:
        return RocketChat(username, password, server_url=ROCKETCHAT_URL)
    except:
        logging.warning("Fail to connect to rocketchat")
        if TEST_MODE:
            logging.info("TEST_MODE, use mock rocketchat client")
            return MockRocketChatClient()
        else:
            raise


def get_chat_history(rocket_client, username: str):
    """
    Get chat history from RocketChat server, between:
    1) param username,
    2) and the account used to create rocket client instance

    Returns the messages as a list. If no history, returns an empty list.
    """
    id = None
    for item in rocket_client.users_list().json()['users']:
        if item.get('nameInsensitive', '').lower() == username.lower() or item.get('username', '').lower() == username.lower():
            id = item["_id"]
            break

    if id is None:
        logging.error(f'Cannot fetch chat history for {username}')
        return []

    msgs = rocket_client.im_history(room_id=id).json()['messages']
    reversed_history = [] if msgs is None else [msg['msg'] for msg in msgs]
    history = reversed_history[::-1]
    logging.info(f'Chat history with {username} is: {history}')
    return history



def get_channel_room_id(rocket_client, channel_name):
    """Get the room_id for a specific channel."""
    response = rocket_client.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_message_posted(rocket_client, channel_name, keywords):
    """
    Check if a message containing specific keywords was posted in the specified channel.

    Args:
        channel_name (str): Name of the Rocket.Chat channel.
        keywords (list): List of keywords to check in the message content.

    Returns:
        bool: True if a message containing all keywords is found, False otherwise.
    """
    room_id = get_channel_room_id(rocket_client, channel_name)
    if not room_id:
        return False
    
    messages = rocket_client.channels_history(room_id=room_id, count=10).json().get('messages', [])
    for message in messages:
        message_text = message.get("msg", "").lower()
        # Check if all keywords are present in the message text
        if all(keyword.lower() in message_text for keyword in keywords):
            return True
    return False

def evaluate_with_llm(content: str, predicate: str, additional_prompt: str = ''):
    """
    Evaluates if a predicate can be inferred from the content, judged by LLM
    """
    if not content:
        logging.warning(f"Content is empty, cannot evaluate")
        return False

    try:
        # Construct LLM query
        llm_messages = [{
            "role": "user",
            "content": f'Does the content """{content}""" indicate {predicate}?'
                      f'Please answer "yes" if it does, or "no" if it does not. {additional_prompt}'
        }]

        # Call LLM for evaluation
        llm_response = llm_complete(llm_messages)
        logging.info("LLM evaluation completed", extra={"response": llm_response})

        # Extract and process response
        content = llm_response["choices"][0]["message"]["content"].lower().strip()

        # Evaluate result
        result = "yes" in content
        if result:
            logging.info(f'Predicate "{predicate}" evaluated to "{result}"')
        else:
            logging.warning(f'Predicate "{predicate}" evaluated to "{result}"')

        return result

    except KeyError as e:
        logging.error("Invalid LLM response structure", exc_info=True)
        return False

    except Exception as e:
        logging.error(f"Failed to evaluate message: {str(e)}", exc_info=True)
        return False


def evaluate_chat_history_with_llm(rocket_client, username: str, predicate: str):
    """
    Evaluates chat history from RocketChat server against a given predicate using LLM.

    Args:
        rocket_client: RocketChat client instance
        username: The username whose chat history to evaluate
        predicate: The condition to evaluate against (e.g., "Liu Qiang had average job performance")

    Returns:
        bool: True if the chat history matches the predicate, False otherwise

    Example:
        >>> result = evaluate_chat_history_with_llm(
        ...     rocket_client,
        ...     "Liu Qiang",
        ...     "the person receiving the feedback had an average job performance"
        ... )
    """
    try:
        # Retrieve chat history
        messages = get_chat_history(rocket_client, username)
        if not messages:
            logging.warning(f"No chat history found for user: {username}")
            return False
        
        return evaluate_with_llm(str(messages), predicate)

    except Exception as e:
        logging.error(f"Failed to evaluate chat history for user {username}: {str(e)}", exc_info=True)
        return False

def make_gitlab_request(project_identifier: str = None, additional_path: str = None, method: str = 'GET'):
    url = f"{GITLAB_BASEURL}/api/v4"

    if project_identifier:
        if '/' in project_identifier:
            project_identifier = urllib.parse.quote(project_identifier, safe='')
        url = f"{url}/projects/{project_identifier}"
    
    if additional_path:
        url = f"{url}/{additional_path}"
    
    try:
        response = requests.request(method, url, headers=GITLAB_HEADERS)
        return response
    except Exception as e:
        logging.error(f"GitLab API request failed: {e}")
        return None


def get_nextcloud_url_in_file(filename: str):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            if f"https://ogma.lti.cs.cmu.edu" in content:
                return content
            return False
    except FileNotFoundError:
        logging.error(f"Error: The file '{filename}' was not found.")
        return False
    except IOError as e:
        logging.error(f"Error: An I/O error occurred. Details: {e}")
        return False


def download_nextcloud_content(link: str, output_file_path: str):
    """
    link: Share link generated by NextCloud
    output_file_path: path to file where the downloaded content is stored
    """
    if not link:
        return False

    if "download" not in link:
        command = ["curl", "--output", "/tmp/.tmp_download_link", link.rstrip("\n")]
        try:
            subprocess.run(command)
        except Exception as e:
            logging.warning(f"Unable to download from link: {link} due to {e}")
            return False

        pattern = r'https?://[^\s]*\bdownload\b[^\s]*(?=")'

        download_link: str | None = None
        with open("/tmp/.tmp_download_link", "r") as f:
            content = f.read()
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                download_link = matches[0]
        
        if download_link is None:
            logging.warning(f"Did not find proper download link")
            return False
    else:
        download_link = link.rstrip("\n")

    try:
        logging.info(download_link)
        subprocess.run([f"curl {download_link} --output {output_file_path}"], shell=True)
    except Exception as e:
        logging.warning(f"Download from link: {download_link} not successful")
        return False

    logging.info(f"Successfully downloaded from link {download_link}")
    return True


# Use the unique file name to check if the repository is cloned correctly.
PROJECT_FILES = {
    'openhands': '.openhands_instructions',
    'janusgraph': '.backportrc.json',
    'colly': 'xmlelement_test.go',
    'streamlit': '.ruff.toml'
}

def check_repo_exists(project_name: str):
    try:
        if project_name not in PROJECT_FILES:
            logging.warning(f"Unknown project: {project_name}")
            return False
            
        file_path = os.path.join('/workspace', project_name, PROJECT_FILES[project_name])
        return os.path.isfile(file_path)
    except Exception as e:
        logging.warning(f"Error checking file: {e}")
        return False
    
    
def get_all_plane_projects():
    """Get all projects in plane."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        logging.warning(f"Get all projects failed: {e}")
        return []
    

def get_plane_project_id(project_name):
    """Get the project_id for a specific project by its name."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        projects = response.json().get('results', [])
        for project in projects:
            if project.get('name') == project_name:
                return project.get('id')
        logging.info(f"Project with name '{project_name}' not found.")
    except Exception as e:
        logging.warning(f"Get project id failed: {e}")
        return None

def get_plane_project_all_issues(project_id):
    """Get the issues for a specific project"""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        issues = response.json().get('results', [])
        return issues
    except Exception as e:
        logging.warning(f"Get issues failed: {e}")
        return []

def get_plane_state_id_dict(project_id):
    """Get the relationship between state and id.

    Args:
        project_id: The ID of the project

    Returns:
        tuple: A tuple containing two dictionaries:
            - state_map (dict): Mapping of state names to state IDs
            - id_map (dict): Mapping of state IDs to state names

    Examples:
        >>> state_map
        {
            'Backlog': '9350e0ce-4d64-4ffc-8071-5918a3c3af4f',
            'Todo': 'a03edcc9-9934-4432-b93a-ab0a33b02964',
            'In Progress': '4873d638-bb79-48ef-8449-d1b75e0111a3',
            'Done': '190e69a1-5f7c-465d-a3ad-0fec204fd365',
            'Cancelled': 'c5ba193b-fab9-475f-bc4d-3161b2a52c70'
        }
        >>> id_map
        {
            '9350e0ce-4d64-4ffc-8071-5918a3c3af4f': 'Backlog',
            'a03edcc9-9934-4432-b93a-ab0a33b02964': 'Todo',
            '4873d638-bb79-48ef-8449-d1b75e0111a3': 'In Progress',
            '190e69a1-5f7c-465d-a3ad-0fec204fd365': 'Done',
            'c5ba193b-fab9-475f-bc4d-3161b2a52c70': 'Cancelled'
        }
    """
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/states/"
    id_map = {}
    state_map = {}
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        projects = response.json().get('results', [])
        for project in projects:
            state_map[project['name']]=project['id']
            id_map[project['id']]=project['name']
    except Exception as e:
        logging.warning(f"Get project id failed: {e}")
        return {}, {}
    return state_map, id_map

def get_plane_issue_details(project_id, issue_name):
    """Get details of a specific issue in a project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        issues = response.json().get('results', [])
        for issue in issues:
            if issue.get('name') == issue_name:
                return issue
        logging.info(f"Issue with name '{issue_name}' not found.")
    except requests.RequestException as e:
        logging.warning(f"Get issue detail failed: {e}")
        return None

def get_plane_issues_by_project_cycle(project_id: str, cycle_id:str):
    """
    Get issues for a specific cycle.

    Args:
        project_id: The ID of the project
        cycle_id: The ID of the cycle

    Returns:
        List: A list of issues in the cycle
    """
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        logging.error(f"Error: {e}")
    return []

def get_plane_state_details(project_id, state_id):
    """
    Get details for a state.
    
    Args:
        project_id: The ID of the project
        state_id: The ID of the state

    Returns:
        dict: A status configuration object with the following structure:
           {
               "id": str,                # ba9d7f8c-9faf-464e-941e-865cd55f37d9
               "created_at": str,        # 2024-10-05T20:37:51.143913Z  
               "updated_at": str,        # 2024-10-05T20:37:51.143929Z
               "name": str,              # In Progress
               "description": str,       # ""
               "color": str,             # #F59E0B
               "slug": str,              # ""
               "sequence": float,        # 35000.0
               "group": str,             # started
               "is_triage": bool,        # false
               "default": bool,          # false
               "external_source": str | None,  # null
               "external_id": str | None,      # null
               "created_by": str,        # 666d7509-469c-41ba-8ade-fd5e56bfafa6
               "updated_by": str | None, # null
               "project": str,           # ea796314-eeec-41aa-816d-58be13909bf2
               "workspace": str          # a56ce149-8ef9-4401-8de6-4dac6a21b4b1
           }
    """
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/states/{state_id}"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error: {e}")
    return dict()