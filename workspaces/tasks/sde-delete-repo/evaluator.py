import logging
import requests
import urllib.parse

# GitLab configuration
base_url = "http://ogma.lti.cs.cmu.edu:8929/api/v4"
project_path = "root/raft"
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}

# Check if the repository returns a 404 status via the API.
def check_repository_deleted():
    encoded_path = urllib.parse.quote(project_path, safe='')
    url = f"{base_url}/projects/{encoded_path}"
    
    try:
        response = requests.get(url, headers=headers)
 
        if response.status_code == 404:
            logging.info(f"Repository '{project_path}' not found (404), as expected.")
            return True
        else:
            logging.warning(f"Unexpected status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False

def grade_checkpoint(check_func, description):
    try:
        passed = check_func()
        print(f"{'✓' if passed else '✗'} {description}")
        return 1 if passed else 0
    except Exception as e:
        logging.error(f"Error while grading checkpoint '{description}': {e}")
        return 0

if __name__ == "__main__":
    checkpoints = [
        (check_repository_deleted, f"Repository '{project_path}' returns 404"),
    ]

    total_points = 0
    for check_func, description in checkpoints:
        points = grade_checkpoint(check_func, description)
        total_points += points

    print(f"\nFinal score for repository deletion check: {total_points}/{len(checkpoints)}")
