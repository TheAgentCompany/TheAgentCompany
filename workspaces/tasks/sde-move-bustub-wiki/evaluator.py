import requests
import logging


from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_any


def check_trajectory(trajectory):
    return f"bustub/-/issues/759" in trajectory

def test_wiki():
    try:
        response = requests.get(f"doc/-/wikis/HyperLogLog_project") 
    except requests.RequestException as e:
        logging.error(f"Error fetching wiki: {e}")
        return False

    if response.status_code != 200:
        print("wiki page not successfully created")
        return False
    print("wiki page successfully created")
    return True

def check_key_contents():
    key_words = ["HyperLogLog", "algorithm", "hash", "A great database is a great life", "MSB", "Task #1", "Task #2", "Instructions", "Important Information", "Setting Up Your Development Environment", "Testing"]
    key_image_links = ["https://15445.courses.cs.cmu.edu/fall2024/project0/img/cardinality.png", "https://15445.courses.cs.cmu.edu/fall2024/project0/img/hll-example.png"]
    key_links = ["https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf", "https://engineering.fb.com/2018/12/13/data-infrastructure/hyperloglog/", "https://www.youtube.com/watch?v=lJYufx0bfpw", "https://www.youtube.com/watch?v=2PlrMCiUN_s"]
    
    try:
        response = requests.get(f"doc/-/wikis/HyperLogLog_project").text
    except requests.RequestException as e:
        logging.error(f"Error fetching wiki: {e}")
        return False
    
    return all(item in response for item in key_words) and \
            all(item in response for item in key_image_links) and  \
            all(item in response for item in key_links)

def check_url_file_exist():
    filename = "/workspace/wiki_url.txt"
    try:
        with open(filename, 'r') as file:
            content = file.read()
            if f"doc/-/wikis/HyperLogLog_project" in content:
                return True
            return False
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return False
    except IOError as e:
        print(f"Error: An I/O error occurred. Details: {e}")
        return False


def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return ""

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    passed_checkpoint1 = check_trajectory(trajectory)
    checkpoints.append(Checkpoint(1, passed_checkpoint1))

    passed_checkpoint2 = test_wiki()
    checkpoints.append(Checkpoint(1, passed_checkpoint2))

    passed_checkpoint3 = check_key_contents()
    checkpoints.append(Checkpoint(1, passed_checkpoint3))

    passed_checkpoint4 = check_url_file_exist()
    checkpoints.append(Checkpoint(1, passed_checkpoint4))

    return result



