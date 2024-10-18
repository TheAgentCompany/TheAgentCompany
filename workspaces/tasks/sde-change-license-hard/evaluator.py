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
        and f"{GITLAB_URL}/root/colly"
        and f"{GITLAB_URL}/root/colly/-/blob/main/LICENSE?ref_type=heads"
        and f"{GITLAB_URL}/root/streamlit"
        and f"{GITLAB_URL}/root/streamlit/-/blob/main/LICENSE?ref_type=heads"
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
    if os.path.exists("/workspace/colly"):
        with open("/workspace/colly/README.MD") as f:
            code_content = f.read()
            if (
                "Scrapfly is an enterprise-grade solution providing Web Scraping API that aims to simplify the scraping process by managing everything: real browser rendering, rotating proxies, and fingerprints (TLS, HTTP, browser) to bypass all major anti-bots. Scrapfly also unlocks the observability by providing an analytical dashboard and measuring the success rate/block rate in detail.",
            ) in code_content:
                return True
    return False

def check_code_clone_3():
    # check path exists
    if os.path.exists("/workspace/streamlit"):
        with open("/workspace/streamlit/README.MD") as f:
            code_content = f.read()
            if (
                "Streamlit lets you transform Python scripts into interactive web apps in minutes, instead of weeks. Build dashboards, generate reports, or create chat apps. Once you’ve created an app, you can use our Community Cloud platform to deploy, manage, and share your app.",
            ) in code_content:
                return True
    return False



def check_license_update():
    # check path exists
    if os.path.exists("/workspace/janusgraph"):
        with open("/workspace/janusgraph/LICENSE") as f:
            code_content = f.read()
            if (
                "MIT"
                in code_content
            ):
                return True
    return False


def check_license_update_2():
    # check path exists
    if os.path.exists("/workspace/colly"):
        with open("/workspace/colly/LICENSE") as f:
            code_content = f.read()
            if (
                "MIT"
                in code_content
            ):
                return True
    return False


def check_license_update_3():
    # check path exists
    if os.path.exists("/workspace/streamlit"):
        with open("/workspace/streamlit/LICENSE") as f:
            code_content = f.read()
            if (
                "MIT"
                in code_content
            ):
                return True
    return False


if __name__ == "__main__":
    print(
        check_url(
            [
                f"ACTION: goto('{GITLAB_URL}/root/janusgraph')",
                 f"{GITLAB_URL}/root/janusgraph/-/blob/main/LICENSE?ref_type=heads",
                f"ACTION: goto('{GITLAB_URL}/root/colly')",
                 f"{GITLAB_URL}/root/colly/-/blob/main/LICENSE?ref_type=heads",
                f"ACTION: goto('{GITLAB_URL}/root/streamlit')",
                 f"{GITLAB_URL}/root/streamlit/-/blob/main/LICENSE?ref_type=heads"              
            ]
        )
    )
    print(check_code_clone())
    print(check_license_update())
    print(check_code_clone_2())
    print(check_license_update_2())
    print(check_code_clone_3())
    print(check_license_update_3())
    score = check_url(
            [
                f"ACTION: goto('{GITLAB_URL}/root/janusgraph')",
                 f"{GITLAB_URL}/root/janusgraph/-/blob/main/LICENSE?ref_type=heads",
                f"ACTION: goto('{GITLAB_URL}/root/sotopia')",
                 f"{GITLAB_URL}/root/sotopia/-/blob/main/LICENSE?ref_type=heads"          
            ]
        ) + check_code_clone() + check_license_update() + check_code_clone_2() + check_license_update_2() + check_code_clone_3() + check_license_update_3()
