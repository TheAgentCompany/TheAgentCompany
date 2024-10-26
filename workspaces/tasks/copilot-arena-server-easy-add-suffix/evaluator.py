import requests
import logging
import sys
import os


def grade_checkpoint1():
    return os.path.exists("/workspace/copilot-arena-server")


def grade_checkpoint2():
    try:
        response = requests.get("http://localhost:5000/list_models")
        return response.status_code == 200
    except Exception:
        logging.warning("Local server is not launched correctly")
        return False


def grade_final_checkpoint():
    try:
        json_input = {
            "prefix": "test_prefix",
            "userId": "test_user",
            "privacy": "Private",
            "modelTags": [],
        }
        response = requests.post("http://localhost:5000/create_pair", json=json_input)
        return response.status_code == 400  # This should now fail
    except Exception:
        logging.warning("Local server is not launched correctly")
        return False


if __name__ == "__main__":
    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2()
    passed3 = grade_final_checkpoint()
    points = 4 if passed3 else int(passed1) + int(passed2)
    print(f"Final points for task Example: {points}")
