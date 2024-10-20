import os
import logging

import litellm

from rocketchat_API.rocketchat import RocketChat

# In test mode, we use mock servers
TEST_MODE = True

LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY")
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL")
LITELLM_MODEL = os.environ.get("LITELLM_MODEL")

# messages: a list of message.
# example [{ "content": "Hello, how are you?","role": "user"}]
def llm_evaluator(messages):
    response = litellm.completion(
        api_key=LITELLM_API_KEY,
        base_url=LITELLM_BASE_URL,
        model=LITELLM_MODEL,
        messages=messages
    )
    return response


class MockRocketChatClient:

    class JsonResponse:
        def json(self):
            return {'users': [], 'messages': []}

    def __getattr__(self, name):
        def method(*args, **kwargs):
            return self.JsonResponse()
        return method


def create_rocketchat_client():
    SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
    ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
    
    # Construct RocketChat URL
    ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
    
    # Set admin credentials
    ADMIN_USERNAME = 'jobbench'
    ADMIN_PASSWORD = 'jobbench'

    try:
        return RocketChat(ADMIN_USERNAME, ADMIN_PASSWORD, server_url=ROCKETCHAT_URL)
    except Exception as e:
        logging.warning("Fail to connect to rocketchat", e)
        if TEST_MODE:
            return MockRocketChatClient()
        else:
            raise
