import asyncio
from server import run_server
import argparse

def main():
    # Use argparse to capture command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent_first_name', type=str, help="Input NPC first name")
    args = parser.parse_args()

    # Run the asyncio task
    asyncio.run(
        run_server(
            model_dict={
                "env": "gpt-4-turbo",
                "agent1": "rocketchat",
                "agent2": "gpt-4-turbo",
            },
            agents_roles={
                "agent1": "human",
                "agent2": "ai",
            },
            agent_first_name = args.agent_first_name
        )
    )

if __name__ == "__main__":
    main()