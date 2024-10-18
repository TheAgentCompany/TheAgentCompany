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


if __name__ == "__main__":
    print(
        check_url(
            [
                f"ACTION: goto('{GITLAB_URL}/root/janusgraph')",
                 f"{GITLAB_URL}/root/janusgraph/-/blob/main/LICENSE?ref_type=heads"           
            ]
        )
    )
    print(check_code_clone())
    print(check_license_update())
    score = check_code_clone() + check_license_update()
