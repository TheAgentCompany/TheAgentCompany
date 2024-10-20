import os
import logging
from rocketchat_API.rocketchat import RocketChat

# In test mode, we use mock servers
TEST_MODE = True

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
