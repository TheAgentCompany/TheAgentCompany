import base64
import os
import logging
import urllib
import subprocess
import functools
import re
import requests

import litellm
from rocketchat_API.rocketchat import RocketChat
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from config import *

logging.basicConfig(level=logging.INFO)

IMAGE_JPEG = 'image/jpeg'
IMAGE_PNG = 'image/png'


class MockRocketChatClient:

    class JsonResponse:
        def json(self):
            return {'users': [], 'messages': []}

    def __getattr__(self, name):
        def method(*args, **kwargs):
            return self.JsonResponse()
        return method


def grader(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return False
    return wrapper
    

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


def get_rocketchat_personal_chat_history(rocket_client, username: str, content_only: bool = True):
    """
    Get chat history from RocketChat server, between:
    1) param username,
    2) and the account used to create rocket client instance

    If content_only is True, only return the content of the messages, otherwise return all attributes,
    including but not limited to message content, timestamp, etc.

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
    if content_only:
        reversed_history = [] if msgs is None else [msg['msg'] for msg in msgs]
    else:
        reversed_history = [] if msgs is None else msgs
    history = reversed_history[::-1]
    logging.info(f'Chat history with {username} is: {history}')
    return history

def num_rocketchat_users_contacted(rocket_client, users):
    """
    returns the number of users contacted in the users list

    Args:
        rocket_client: RocketChat client instance
        users: List of usernames to check

    Returns:
        int: Number of users contacted
    """
    contacted_users = 0
    user_list = rocket_client.users_list().json()
    for item in user_list['users']:
        if item.get('username') in users:
            id = item["_id"]
            msgs = rocket_client.im_history(room_id=id).json()['messages']
            contacted_users += msgs is not None and len(msgs) > 0
    return contacted_users

def get_rocketchat_channel_history(rocket_client, channel):
    """
    Retrieve the message history of a specific public channel from the RocketChat server.

    Parameters:
        rocket_client: The RocketChat client instance, authenticated and connected to the server.
        channel (str): The name of the channel to retrieve messages from.

    Returns:
        list: A list of messages from the specified channel. If no messages are found, returns empty list.
              If an error occurs in retrieving the channel info or message history, also returns empty list.

    Example:
        >>> messages = get_rocketchat_channel_history(rocket_client, "general")
        >>> for message in messages:
        >>>     print(message["msg"])
    """
    response = rocket_client.channels_info(channel=channel).json()
    if not response.get('success'):
        logging.warning(f"Failed to retrieve {channel} channel info.")
        return []

    room_id = response['channel']['_id']

    response = rocket_client.channels_history(room_id=room_id).json()
    if not response.get('success'):
        logging.warning("Failed to retrieve message history.")
        return []

    messages = response.get('messages', [])

    if not messages:
        logging.warning("No messages found.")
        return []

    return messages

def get_rocketchat_channel_room_id(rocket_client, channel_name):
    """Get the room_id for a specific channel."""
    response = rocket_client.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_rocketchat_message_posted(rocket_client, channel_name, keywords):
    """
    Check if a message containing specific keywords was posted in the specified channel.

    Args:
        channel_name (str): Name of the Rocket.Chat channel.
        keywords (list): List of keywords to check in the message content.

    Returns:
        bool: True if a message containing all keywords is found, False otherwise.
    """
    room_id = get_rocketchat_channel_room_id(rocket_client, channel_name)
    if not room_id:
        return False
    
    messages = rocket_client.channels_history(room_id=room_id, count=10).json().get('messages', [])
    for message in messages:
        message_text = message.get("msg", "").lower()
        # Check if all keywords are present in the message text
        if all(keyword.lower() in message_text for keyword in keywords):
            return True
    return False

def download_image_from_url(image_url, output_file_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(output_file_path, "wb") as file:
                file.write(response.content)
            logging.info(f"Image downloaded from {image_url} to {output_file_path}")
            return output_file_path
        else:
            logging.error(f"Failed to download image from {image_url}: {response}")
            return None
    except Exception as e:
        logging.error(f"Failed to download image from {image_url}: {e}")
        return None

def evaluate_with_llm(content: str, predicate: str, additional_prompt: str = '', image_path: str = None, image_type: str = IMAGE_JPEG):
    """
    Evaluates if a predicate can be inferred from the content/image, judged by LLM
    """
    if image_path is not None and image_type not in [IMAGE_JPEG, IMAGE_PNG]:
        logging.warning(f"Invalid image type: {image_type}")
        return False
    if not content and not image_path:
        logging.warning(f"Both content and image are empty, cannot evaluate")
        return False
    elif content and image_path:
        query = f'Does the content """{content}""" and following picture indicate {predicate}?'
    elif content:
        query = f'Does the content """{content}""" indicate {predicate}?'
    else:
        query = f'Does the following picture indicate {predicate}?'

    query += f' Please answer "yes" if it does, or "no" if it does not. {additional_prompt}'
    content = [
        {
            "type": "text",
            "text": query
        }
    ]
    if image_path:
        try:
            with open(image_path, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            logging.error(f"Failed to read image from {image_path}: {e}")
            return False
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{image_type};base64,{base64_image}"
            }
        })

    try:
        # Construct LLM query
        llm_messages = [{
            "role": "user",
            "content": content
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
        messages = get_rocketchat_personal_chat_history(rocket_client, username)
        if not messages:
            logging.warning(f"No chat history found for user: {username}")
            return False
        
        return evaluate_with_llm(str(messages), predicate)

    except Exception as e:
        logging.error(f"Failed to evaluate chat history for user {username}: {str(e)}", exc_info=True)
        return False

def make_gitlab_request(project_identifier: str = None, additional_path: str = None, method: str = 'GET', params: dict = None):
    url = f"{GITLAB_BASEURL}/api/v4"

    if project_identifier:
        if '/' in project_identifier:
            project_identifier = urllib.parse.quote(project_identifier, safe='')
        url = f"{url}/projects/{project_identifier}"
    
    if additional_path:
        url = f"{url}/{additional_path}"
    
    try:
        response = requests.request(method, url, headers=GITLAB_HEADERS, params=params)
        return response
    except Exception as e:
        logging.error(f"GitLab API request failed: {e}")
        return None

def get_gitlab_project_id(project_name:str):
    """
    Get project ID for gitlab project

    Args:
        project_name: The name of the project

    Returns:
        str: The ID of the project

    """
    projects = make_gitlab_request(None,"projects")
    if not projects:
        logging.warning(f"No gitlab projects found")
        return None
    else:
        projects = projects.json()
    target_projects = [project['id'] for project in projects if project['name']==project_name]
    if len(target_projects) == 0:
        logging.warning(f"No gitlab projects found for project name {project_name}")
        return None
    else:
        return str(target_projects[0])

def get_gitlab_merge_request_by_title(project_id:str, merge_request_title:str):
    """
    Get merge request by title

    Args:
        project_id: The ID of the project
        merge_request_title: The title of the merge request

    Returns:
        dict: The merge request object
    """
    merge_requests = make_gitlab_request(project_id,"merge_requests")
    if not merge_requests:
        logging.warning(f"No gitlab merge requests found")
        return None
    else:
        merge_requests = merge_requests.json()
    target_merge_requests = [merge_request for merge_request in merge_requests if merge_request['title'].strip().lower()==merge_request_title.strip().lower()]
    if len(target_merge_requests) == 0:
        logging.warning(f"No gitlab merge requests found for title {merge_request_title}")
        return None
    else:
        return target_merge_requests[0]

def get_gitlab_file_in_mr(mr: dict, file_path: str) -> str:
    """
    Get the content of a file in a merge request.

    Args:
        mr: The merge request object
        file_path: The path to the file 

    Returns:
        str: The content of the file
    """
    mr_sha = mr['sha']
    file_path_in_url = urllib.parse.quote(file_path, safe='')
    path = f"repository/files/{file_path_in_url}/raw?ref={mr_sha}"
    resp = make_gitlab_request(str(mr['project_id']), path)
    if not resp:
        return None
    return resp.text


def get_owncloud_url_in_file(filename: str):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            if f"{OWNCLOUD_URL}" in content:
                return content
            return False
    except FileNotFoundError:
        logging.error(f"Error: The file '{filename}' was not found.")
        return False
    except IOError as e:
        logging.error(f"Error: An I/O error occurred. Details: {e}")
        return False

def download_owncloud_content(link: str, output_file_path: str):
    """
    link: Share link generated by ownCloud
    output_file_path: path to file where the downloaded content is stored
    """
    if not link:
        return False

    if "download" not in link:
        command = ["curl", "--output", "/tmp/.tmp_download_link", link.rstrip("\n")]
        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
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


def check_and_download_file(file_name, dir_name, output_file_path):
    """
    Check if a file exists in an ownCloud directory using WebDAV and download it if found.

    Parameters:
        file_name (str): The name of the file to check and download.
        dir_name (str): The directory path on NextCloud.
        output_file_path (str): Path to save the downloaded file locally.

    Returns:
        bool: True if the file was found and downloaded successfully, False otherwise.
    """
    # Construct WebDAV URL for the directory
    WEBDAV_BASE_URL = f"{OWNCLOUD_URL}/remote.php/webdav/"
    server_url = f"{WEBDAV_BASE_URL}{dir_name.strip('/')}/"
    headers = {'Depth': '1'}  # Request depth for PROPFIND

    try:
        # Check if the file exists in the directory
        response = requests.request(
            method="PROPFIND",
            url=server_url,
            headers=headers,
            auth=HTTPBasicAuth(OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD)
        )

        if response.status_code == 207:
            # Parse the XML response to find the file
            root = ET.fromstring(response.text)
            for response_element in root.findall(".//{DAV:}response"):
                href = response_element.find("{DAV:}href").text
                if file_name in href:
                    logging.info(f"File '{file_name}' found. Proceeding to download.")
                    
                    # Construct full file URL
                    file_url = server_url + file_name

                    # Download the file
                    download_response = requests.get(
                        file_url,
                        auth=HTTPBasicAuth(OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD),
                        stream=True
                    )

                    if download_response.status_code == 200:
                        with open(output_file_path, "wb") as file:
                            for chunk in download_response.iter_content(chunk_size=8192):
                                file.write(chunk)
                        logging.info(f"File '{file_name}' downloaded successfully to '{output_file_path}'.")
                        return True
                    else:
                        logging.error(f"Failed to download file '{file_name}'. HTTP Status: {download_response.status_code}")
                        return False

            # File not found in the directory
            logging.warning(f"File '{file_name}' not found in directory '{dir_name}'.")
            return False

        else:
            # Log unexpected HTTP status codes
            logging.error(f"Error checking directory. HTTP Status: {response.status_code}, Response: {response.text}")
            return False

    except requests.RequestException as e:
        logging.warning(f"Failed to check or download file in ownCloud directory: {e}")
        return False


def check_file_in_owncloud_directory(file_name, dir_name):
    """
    Check if a file exists in an ownCloud directory using WebDAV
    """
    server_url = f"{OWNCLOUD_URL}/remote.php/webdav/{dir_name}"
    headers = {
        'Depth': '1',
    }

    try:
        response = requests.request(
            method="PROPFIND",
        url=server_url,
        headers=headers,
        auth=HTTPBasicAuth(OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD)
        )
    except requests.RequestException as e:
        logging.warning(f"Failed to check file in owncloud directory: {e}")
        return False

    if response.status_code == 207:
        root = ET.fromstring(response.text)
        for response_element in root.findall(".//{DAV:}response"):
            href = response_element.find("{DAV:}href").text
            if file_name in href:
                logging.info(f"File '{file_name}' found.")
                return True
        logging.warning(f"File '{file_name}' not found.")
        return False
    else:
        logging.error(f"Error: {response.status_code}, {response.text}")
        return None

def get_binary_file_content_owncloud(file_name, dir_name):
    server_url = f"{OWNCLOUD_URL}/remote.php/webdav/{dir_name}/{file_name}"

    try:
        response = requests.get(
            server_url, 
        auth=HTTPBasicAuth(OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD)
        )
    except requests.RequestException as e:
        logging.warning(f"Failed to get binary file content from owncloud: {e}")
        return None

    if response.status_code == 200:
        return response.content
    else:
        return None
    

# Use the unique file name to check if the repository is cloned correctly.
PROJECT_FILES = {
    'openhands': '.openhands_instructions',
    'janusgraph': '.backportrc.json',
    'colly': 'xmlelement_test.go',
    'streamlit': '.ruff.toml',
    'risingwave': 'risedev.yml',
    'bustub': 'CMakeLists.txt'
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
    
def get_plane_cycle_details(project_id, cycle_name):
    """Get details of a specific cycle in a project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        cycles = response.json().get('results', [])
        for cycle in cycles:
            if cycle.get('name') == cycle_name:
                return cycle
        logging.info(f"Cycle with name '{cycle_name}' not found.")
    except requests.RequestException as e:
        logging.warning(f"Get cycle detail failed: {e}")
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

def create_plane_issue(project_id, issue_name):
    """ Create an issue in a project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.post(url, headers=PLANE_HEADERS, json={"name": issue_name})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.warning(f"Create issue failed: {e}")
        return None
    
def add_plane_issue_to_cycle(project_id, cycle_id, issue_id):
    """ Add an issue to a cycle."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/"
    try:
        response = requests.post(url, headers=PLANE_HEADERS, json={"issues": [issue_id]})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.warning(f"Add issue to cycle failed: {e}")
        return None


def get_all_texts_from_slide(slide):
    """Obtain all text content from the slide."""
    if slide is None:
        return ""

    texts = []

    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text
            texts.append(text.lower())

    return ' '.join(texts)
