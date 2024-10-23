# In test mode, we use mock servers and mock LLM responses
TEST_MODE = os.environ.get('TAC_TEST_MODE', False)

LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY")
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "https://api.openai.com/v1")
LITELLM_MODEL = os.environ.get("LITELLM_MODEL", "gpt-4o")

PLANE_API_KEY = os.environ.get("PLANE_API_KEY") or "plane_api_569b8e604e0c46d0b65ef56bb9e76f03"
