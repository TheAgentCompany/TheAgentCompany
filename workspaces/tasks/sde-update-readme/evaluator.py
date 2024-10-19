import logging
import requests
import urllib.parse
import base64

# GitLab configuration
base_url = "http://ogma.lti.cs.cmu.edu:8929/api/v4"
project_path = "root/api-server"
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}
target_title = "## Contribute to this project"
target_content = "We welcome contributions to this project. Please follow the guidelines to contribute."


def grade_checkpoint(check_func, description):
    try:
        passed = check_func()
        print(f"{'✓' if passed else '✗'} {description}")
        return 1 if passed else 0
    except Exception as e:
        logging.error(f"Error while grading checkpoint '{description}': {e}")
        return 0


def extract_readme_content():
    encoded_path = urllib.parse.quote(project_path, safe="")
    readme_url = (
        f"{base_url}/projects/{encoded_path}/repository/files/README.md?ref=main"
    )
    print(readme_url)
    try:
        response = requests.get(readme_url, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            content = response_data.get("content", "")
            # decode the base64 encoded content
            content = base64.b64decode(content).decode("utf-8")
            return content
        else:
            logging.warning(f"Unexpected status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Error occurred while extracting the README.md content: {e}")
        return None


# check if the README.md contains the expected title
def check_readme_title():
    content = extract_readme_content()
    if content is None:
        return False

    if target_title in content:
        logging.info(f"README.md contains the title '{target_title}'")
        return True
    else:
        logging.warning(f"README.md does not contain the title '{target_title}'")
        return False


# check if the README.md contains the expected content
def check_readme_content():
    content = extract_readme_content()
    if content is None:
        return False
    content = content.split(target_title)
    if len(content) != 2:
        logging.warning(f"Expected 2 parts, got {len(content)}")
        return False

    content = content[1].strip().split("\n")[0]
    if content == target_content:
        logging.info(f"README.md contains the content '{target_content}'")
        return True


if __name__ == "__main__":
    checkpoints = [
        (check_readme_title, f"README.md contains the title '{target_title}'"),
        (check_readme_content, f"README.md contains the content '{target_content}'"),
    ]

    total_points = 0
    for check_func, description in checkpoints:
        points = grade_checkpoint(check_func, description)
        total_points += points

    print(f"\nFinal score for updating readme check: {total_points}/{len(checkpoints)}")
