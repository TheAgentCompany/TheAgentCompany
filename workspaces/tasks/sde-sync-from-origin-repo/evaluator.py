import requests
import logging
import urllib
from common import *

project_path = "root/janusgraph"
file_path = "janusgraph-dist/pom.xml"
target_keyword = "<docker.build.skip>"

def get_file_content():
    encoded_file_path = urllib.parse.quote(file_path, safe='')
    try:
        response = make_gitlab_request(project_path, f"repository/files/{encoded_file_path}/raw")
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        logging.error(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response content'}")
        return ""
    except Exception as e:
        logging.error(f"Failed to fetch file content: {e}")
        return ""

# Check if the docker.build.skip keyword exists in the pom.xml file.
def grade_checkpoint1():
    try:
        content = get_file_content()
        if not content:
            logging.error("Failed to get file content")
            return False
        has_keyword = target_keyword in content
        return has_keyword
    except Exception as e:
        logging.error(f"Checkpoint evaluation failed: {e}")
        return False

def grade_checkpoints():
    checkpoints = [
        (grade_checkpoint1, "Check docker.build.skip exists")
    ]

    points = 0
    for grade_func, description in checkpoints:
        try:
            passed = grade_func()
            points += int(passed)
            print(f"{'✓' if passed else '✗'} {description}")
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")
            break

    return points

if __name__ == "__main__":
    # Test the evaluator
    total_points = grade_checkpoints()
    print(f"\nTotal points earned: {total_points}/1")