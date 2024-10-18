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
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/README.MD") as f:
            code_content = f.read()
            if (
                "Welcome to OpenHands (formerly OpenDevin), a platform for software development agents powered by AI.",
            ) in code_content:
                return True
    return False

def check_poetry_update1():
    # check path exists
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/poetry.lock") as f:
            code_content = f.read()
            if (
                'fastapi-0.116.0'
                in code_content and 'fastapi-0.115.0' not in code_content
            ):
                return True
    return False

def check_pyproject_update1():
    # check path exists
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/pyproject.toml") as f:
            code_content = f.read()
            if (
                'fastapi = "0.116.0"'
                in code_content 
            ):
                return True
    return False

def check_poetry_update2():
    # check path exists
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/poetry.lock") as f:
            code_content = f.read()
            if (
                'seaborn-0.13.3'
                in code_content and 'seaborn-0.13.2' not in code_content
            ):
                return True
    return False

def check_pyproject_update2():
    # check path exists
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/pyproject.toml") as f:
            code_content = f.read()
            if (
                'seaborn = "0.13.3"'
                in code_content 
            ):
                return True
    return False

def check_poetry_update3():
    # check path exists
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/poetry.lock") as f:
            code_content = f.read()
            if (
                'litellm-1.48.8'
                in code_content and 'litellm-1.48.9' not in code_content
            ):
                return True
    return False

def check_pyproject_update3():
    # check path exists
    if os.path.exists("/workspace/openhands"):
        with open("/workspace/openhands/pyproject.toml") as f:
            code_content = f.read()
            if (
                'litellm = "1.48.8"'
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
    print(check_poetry_update1())
    print(check_poetry_update2())
    print(check_pyproject_update2())
    score =         check_url(
            [
        f"{GITLAB_URL}/root/openhands",
        f"{GITLAB_URL}/root/openhands/-/blob/main/pyproject.toml?ref_type=heads",
        f"{GITLAB_URL}/root/openhands/-/blob/main/poetry.lock?ref_type=heads"           
            ]
        ) + check_code_clone() + check_poetry_update1() + check_pyproject_update1() + check_poetry_update2() + check_pyproject_update2() + check_poetry_update3() + check_pyproject_update3()
