import os
# In test mode, we use mock servers and mock LLM responses
TEST_MODE = os.environ.get('TAC_TEST_MODE', False)

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'

# LLM Config
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY")
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "https://api.openai.com/v1")
LITELLM_MODEL = os.environ.get("LITELLM_MODEL", "gpt-4o")

# OwnCloud Config
OWNCLOUD_PORT = os.getenv('OWNCLOUD_PORT') or '8092'
OWNCLOUD_URL = f"http://{SERVER_HOSTNAME}:{OWNCLOUD_PORT}"
OWNCLOUD_USERNAME = "theagentcompany"
OWNCLOUD_PASSWORD = "theagentcompany"

# Rocketchat Config
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Gitlab Config
GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_BASEURL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}"
GITLAB_ACCESS_TOKEN = "root-token"
GITLAB_HEADERS = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}
GITLAB_USER = "root"

# Plane Config
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{SERVER_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
PLANE_API_KEY = os.environ.get("PLANE_API_KEY") or "plane_api_83f868352c6f490aba59b869ffdae1cf"
PLANE_HEADERS = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}
