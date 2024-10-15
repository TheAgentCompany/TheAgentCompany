import os
import litellm

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
