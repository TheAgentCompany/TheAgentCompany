import os
import logging

import litellm
import urllib

import subprocess
import re

import requests
from rocketchat_API.rocketchat import RocketChat

from config import *

logging.basicConfig(level=logging.INFO)

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


class MockRocketChatClient:

    class JsonResponse:
        def json(self):
            return {'users': [], 'messages': []}

    def __getattr__(self, name):
        def method(*args, **kwargs):
            return self.JsonResponse()
        return method


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


def evaluate_with_llm(content: str, predicate: str, additional_prompt: str = ''):
    """
    Evaluates if a predicate can be inferred from the content, judged by LLM
    """
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
    url = f"{BASE_URL}:{GITLAB_PORT}/api/v4"

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