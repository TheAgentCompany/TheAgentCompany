import logging
import requests
import sys

#Check if the repository has been deleted.
def check_repository_deleted():
    """Check if the repository has been deleted."""
    url = "http://ogma.lti.cs.cmu.edu:8929/api/v4/projects/root/raft"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 404:
            return True
        else:
            logging.warning(f"Repository still exists or encountered an unexpected status code: {response.status_code}")
            return False
    except Exception as e:
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
        (check_repository_deleted, "Repository 'root/raft' has been deleted"),
    ]

    total_points = 0
    for check_func, description in checkpoints:
        points = grade_checkpoint(check_func, description)
        total_points += points

    print(f"\nFinal score for repository deletion task: {total_points}/1")