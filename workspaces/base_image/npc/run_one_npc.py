import asyncio
from server import run_server
import argparse
import logging
import os
FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
logging.basicConfig(
    level=15,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        logging.StreamHandler(),
    ],
) 

os.environ['CUSTOM_API_KEY'] = os.getenv('LITELLM_API_KEY')
BASE_URL = os.getenv('LITELLM_BASE_URL')
MODEL_NAME = os.getenv('LITELLM_MODEL')

# HACK: sotopia is not compatible with LITELLM, so we have to remove
# "openai/" prefix, if any, from the model name.
if MODEL_NAME.startswith("openai/"):
    MODEL_NAME = MODEL_NAME[7:]  # Skip first 7 characters ("openai/")

def main():
    # Use argparse to capture command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent_name', type=str, help="Input NPC first name")
    args = parser.parse_args()

    # Run the asyncio task
    asyncio.run(
        run_server(
            # The agent1 is the examinee
            # The agent2 is the sotopia NPC
            # This should match the profile and goals order
            model_dict={
                "env": "gpt-4",
                "agent1": "rocketchat",
                "agent2": f"custom/{MODEL_NAME}@{BASE_URL}",
            },
            # Agent Roles are uesless here.
            agents_roles={
                "agent1": "",
                "agent2": "",
            },
            agent_name = args.agent_name
        )
    )

if __name__ == "__main__":
    main()