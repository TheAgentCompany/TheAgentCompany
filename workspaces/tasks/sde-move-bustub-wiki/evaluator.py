import requests
import logging
import os
import sys

import os
import requests
import logging


############################# init variable ##################################### 

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"


def check_trajectory(trajectory):
    return f"{GITLAB_URL}/bustub/-/issues/759" in trajectory

def test_wiki():
    response = requests.get(f"{GITLAB_URL}/doc/-/wikis/HyperLogLog_project") 
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
        response = requests.get(f"{GITLAB_URL}/doc/-/wikis/HyperLogLog_project").text
    except Exception as e:
        print("Unable to access the new wiki page due to exception ", e)
    
    return all(item in response for item in key_words) and \
            all(item in response for item in key_image_links) and  \
            all(item in response for item in key_links)

def check_url_file_exist():
    filename = "/workspace/wiki_url.txt"
    try:
        with open(filename, 'r') as file:
            content = file.read()
            if f"{GITLAB_URL}/doc/-/wikis/HyperLogLog_project" in content:
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

def evaluate(trajectory):
    points = 0

    if check_trajectory(trajectory):
        print("bathtub issue accessed")
        points += 1
    else:
        print("bathtub issue not accessed")

    if test_wiki():
        points += 1

    if check_key_contents():
        print("Important information are preserved in copied wiki")
        points += 1
    else:
        print("Missing important information in copied wiki")

    if check_url_file_exist():
        points += 1
        print("new wiki URL returned successfully")
    else:
        print("new wiki URL not returned successfully")
    
    print(f"Evaluation completed. Final score: {points}/4")
    return points

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, assuming empty trajectory")
        trajectory = ""
    else:
        trajectory = load_trajectory(sys.argv[1])

    evaluate(trajectory)

