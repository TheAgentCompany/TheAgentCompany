import os

from PIL import Image
import numpy as np

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
GITLAB_PORT = os.getenv("GITLAB_PORT")
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"


def check_url(browser_logs):
    return (
        f"{GITLAB_URL}/root/janusgraph"
        and f"{GITLAB_URL}/root/janusgraph/-/blob/main/LICENSE?ref_type=heads"
        and f"{GITLAB_URL}/root/sotopia"
        and f"{GITLAB_URL}/root/sotopia/-/blob/main/LICENSE?ref_type=heads"
        in browser_logs
    )


def check_code_clone():
    # check path exists
    if os.path.exists("/workspace/janusgraph"):
        with open("/workspace/janusgraph/README.MD") as f:
            code_content = f.read()
            if (
                "JanusGraph is a highly scalable [graph database](https://en.wikipedia.org/wiki/Graph_database)",
                "optimized for storing and querying large graphs with billions of vertices and edges distributed",
                "across a multi-machine cluster. JanusGraph is a transactional database that can support thousands",
                "of concurrent users, complex traversals, and analytic graph queries.",
            ) in code_content:
                return True
    return False

def check_code_clone_2():
    # check path exists
    if os.path.exists("/workspace/sotopia"):
        with open("/workspace/sotopia/README.MD") as f:
            code_content = f.read()
            if (
                "Sotopia is an open-ended social learning environment that allows agents to interact with each other and the environment. The environment is designed to be a platform for evaluating and faciliating social intelligence in language agents. The environment is designed to be open-ended, meaning that the environment can be easily extended to include new environments and new agents. The environment is also designed to be scalable, meaning that the environment can be easily scaled to include a large number of agents and environments.",
            ) in code_content:
                return True
    return False



def check_license_update():
    # check path exists
    if os.path.exists("/workspace/janusgraph"):
        with open("/workspace/janusgraph/LICENSE") as f:
            code_content = f.read()
            if (
                "Apache-2.0"
                in code_content and "CC-BY-4.0" not in code_content
            ):
                return True
    return False


def check_license_update_2():
    # check path exists
    if os.path.exists("/workspace/sotopia"):
        with open("/workspace/sotopia/LICENSE") as f:
            code_content = f.read()
            if (
                "Apache-2.0"
                in code_content and "CC-BY-4.0" in code_content and "MIT" not in code_content
            ):
                return True
    return False


if __name__ == "__main__":
    print(
        check_url(
            [
                f"ACTION: goto('{GITLAB_URL}/root/janusgraph')",
                 f"{GITLAB_URL}/root/janusgraph/-/blob/main/LICENSE?ref_type=heads",
                f"ACTION: goto('{GITLAB_URL}/root/sotopia')",
                 f"{GITLAB_URL}/root/sotopia/-/blob/main/LICENSE?ref_type=heads"          
            ]
        )
    )
    print(check_code_clone())
    print(check_license_update())
    print(check_code_clone_2())
    print(check_license_update_2())
    score = check_url(
            [
                f"ACTION: goto('{GITLAB_URL}/root/janusgraph')",
                 f"{GITLAB_URL}/root/janusgraph/-/blob/main/LICENSE?ref_type=heads",
                f"ACTION: goto('{GITLAB_URL}/root/sotopia')",
                 f"{GITLAB_URL}/root/sotopia/-/blob/main/LICENSE?ref_type=heads"          
            ]
        ) + check_code_clone() + check_license_update() + check_code_clone_2() + check_license_update_2()
