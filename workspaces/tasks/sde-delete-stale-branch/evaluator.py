import logging
import requests
import sys
import urllib.parse

# GitLab configuration
base_url = "http://ogma.lti.cs.cmu.edu:8929/api/v4"
project_path = "root/opensearch"
stale_branch = "feature/ssl"
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}

def check_repository_exists():
    encoded_path = urllib.parse.quote(project_path, safe='')
    url = f"{base_url}/projects/{encoded_path}"
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False

def check_branch_deleted():
    encoded_path = urllib.parse.quote(project_path, safe='')
    encoded_branch = urllib.parse.quote(stale_branch, safe='')
    url = f"{base_url}/projects/{encoded_path}/repository/branches/{encoded_branch}"
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 404
    except Exception as e:
        logging.error(f"Error occurred while checking the branch: {e}")
        return False

def grade_checkpoint1(trajectory):
    target_context = "permanently delete the branch"
    
    try:
        return target_context in trajectory
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

def grade_checkpoint2():
    repo_exists = check_repository_exists()
    branch_deleted = check_branch_deleted()
    
    if repo_exists and branch_deleted:
        logging.info("Repository exists and branch 'feature/ssl' is deleted.")
        return True
    else:
        logging.warning(f"Repository exists: {repo_exists}, Branch deleted: {branch_deleted}")
        return False

def grade_checkpoints(trajectory):
    checkpoints = [
        (lambda t: grade_checkpoint1(t), "Check if 'permanently delete the branch' exists in the trajectory"),
        (grade_checkpoint2, "Check if repository exists and branch 'feature/ssl' is deleted")
    ]

    points = 0
    checkpoint2_passed = False

    for i, (grade_func, description) in enumerate(checkpoints):
        try:
            passed = grade_func(trajectory) if grade_func != grade_checkpoint2 else grade_func()
            if i == 1 and passed:
                checkpoint2_passed = True
            points += int(passed)
            print(f"{'✓' if passed else '✗'} {description}")
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")

    # If checkpoint 2 passed, give full points
    if checkpoint2_passed:
        points = 2

    return points

def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, assuming empty trajectory")
        trajectory = ""
    else:
        trajectory = load_trajectory(sys.argv[1])

    points = grade_checkpoints(trajectory)
    print(f"\nFinal points for branch deletion task: {points}/2")