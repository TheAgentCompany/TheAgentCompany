import asyncio
from bridge_server import run_bridge_server

asyncio.run(
    run_bridge_server(
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
