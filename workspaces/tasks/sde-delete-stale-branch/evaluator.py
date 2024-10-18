import logging
import requests
import sys

# Check if "permanently delete the branch" exists in the trajectory
def grade_checkpoint1(trajectory):
    target_context = "permanently delete the branch"
    
    try:
        return target_context in trajectory
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

# Check if http://ogma.lti.cs.cmu.edu:8929/root/opensearch/-/tree/feature/ssl returns 404
def grade_checkpoint2():
    url = "http://ogma.lti.cs.cmu.edu:8929/root/opensearch/-/tree/feature/ssl"
    
    try:
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 404:
            logging.info(f"URL '{url}' returns 404, indicating the branch is deleted.")
            return True
        else:
            logging.warning(f"URL '{url}' returned status code {response.status_code}, expected 404.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the URL: {e}")
        return False

def grade_checkpoints(trajectory):
    checkpoints = [
        (lambda t: grade_checkpoint1(t), "Check if 'permanently delete the branch' exists in the trajectory"),
        (grade_checkpoint2, "Check if http://ogma.lti.cs.cmu.edu:8929/root/opensearch/-/tree/feature/ssl returns 404")
    ]

    points = 0
    for grade_func, description in checkpoints:
        try:
            passed = grade_func(trajectory) if grade_func != grade_checkpoint2 else grade_func()
            points += int(passed)
            print(f"{'✓' if passed else '✗'} {description}")
            if not passed:
                break
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
    print(f"\nFinal points for branch deletion task: {points}/2")