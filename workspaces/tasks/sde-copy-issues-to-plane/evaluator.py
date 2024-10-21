import os
import sys
import logging
import requests

logging.basicConfig(level=logging.INFO)

############################# init variable #####################################
HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
PLANE_PROJECT_ID = "2bc631a1-8515-4bca-858e-129337c83c8d"
API_KEY = os.getenv('PLANE_API')
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Check if the title are in the trajectory
def grade_checkpoint1(trajectory):
    return ("[FEAT]: Unify evaluation prompt and episode rendering for human readers" in trajectory
            and "Roadmap to Sotopia v0.1" in trajectory)

# Check if the required issues exist on the project page
def grade_checkpoint2():
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{PLANE_PROJECT_ID}/issues/"
    
    try:
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            resp = response.json()
            required_issues = [
                "[FEAT]: Unify evaluation prompt and episode rendering for human readers",
                "Roadmap to Sotopia v0.1"
            ]
            found_issues = set()
            for issue in resp.get("results", []):
                if issue.get('name') in required_issues:
                    found_issues.add(issue.get('name'))
            return len(found_issues) == len(required_issues)
        return False
    except Exception as e:
        logging.warning(f"Error getting issues: {e}")
        return False

def grade_checkpoints(trajectory):

    checkpoints = [
        (grade_checkpoint1, "[FEAT]: Unify evaluation prompt and episode rendering for human readers and Roadmap to Sotopia v0.1 appear in the trajectory"),
        (grade_checkpoint2, "[FEAT]: Unify evaluation prompt and episode rendering for human readers and Roadmap to Sotopia v0.1 appear on the issues webpage")
    ]
    
    points = 0
    for i, (grade_func, description) in enumerate(checkpoints):
        try:
            passed = grade_func(trajectory) if grade_func == grade_checkpoint1 else grade_func()
            if passed:
                if i == 1:
                    points = 2
                else:
                    points += 1
            print(f"{'✓' if passed else '✗'} {description}")
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")
            break
    
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
    print(f"\nFinal points: {points}/2")