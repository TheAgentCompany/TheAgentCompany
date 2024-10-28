import os

from PIL import Image
import numpy as np

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
GITLAB_PORT = os.getenv("GITLAB_PORT")
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"


def check_url(browser_logs):
    return (
        f"{GITLAB_URL}/root/openhands"
        and f"{GITLAB_URL}/root/openhands/-/blob/main/pyproject.toml?ref_type=heads"
        and f"{GITLAB_URL}/root/openhands/-/blob/main/poetry.lock?ref_type=heads"
        in browser_logs
    )


def check_code_clone():
    # check path exists
    if os.path.exists("workspace/openhands"):
        with open("workspace/openhands/README.MD") as f:
            code_content = f.read()
            if (
                "Welcome to OpenHands (formerly OpenDevin), a platform for software development agents powered by AI."
            ) in code_content:
                return True
    return False

def check_poetry_update():
    # check path exists
    if os.path.exists("workspace/openhands"):
        with open("workspace/openhands/poetry.lock") as f:
            code_content = f.read()
            if (
                'uvicorn-0.31.1-py3-none-any.whl'
                and 'uvicorn-0.31.1.tar.gz' 
                in code_content
            ):
                return True
    return False

def check_pyproject_update():
    # check path exists
    if os.path.exists("workspace/openhands"):
        with open("workspace/openhands/pyproject.toml") as f:
            code_content = f.read()
            if (
                'uvicorn = "0.31.1"'
                in code_content 
            ):
                return True
    return False


if __name__ == "__main__":
    print(
        check_url(
            [
        f"{GITLAB_URL}/root/openhands",
        f"{GITLAB_URL}/root/openhands/-/blob/main/pyproject.toml?ref_type=heads",
        f"{GITLAB_URL}/root/openhands/-/blob/main/poetry.lock?ref_type=heads"        
            ]
        )
    )
    print(check_code_clone())
    print(check_poetry_update())
    print(check_pyproject_update())
    score =         check_url(
            [
        f"{GITLAB_URL}/root/openhands",
        f"{GITLAB_URL}/root/openhands/-/blob/main/pyproject.toml?ref_type=heads",
        f"{GITLAB_URL}/root/openhands/-/blob/main/poetry.lock?ref_type=heads"             
            ]
        ) + check_code_clone() + check_poetry_update() + check_pyproject_update()
    print(score)