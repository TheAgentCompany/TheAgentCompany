import asyncio
from server import run_server

asyncio.run(
    run_server(
        model_dict={
            "env": "gpt-4-turbo",
            "agent1": "gpt-4-turbo",
            "agent2": "rocketchat",
        },
        agents_roles={
            "agent1": "human",
            "agent2": "ai",
        },
    )
)
