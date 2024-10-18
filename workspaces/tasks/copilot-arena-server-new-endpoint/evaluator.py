import requests
import logging
import sys


def grade_checkpoint1():
    json_input = {
        "prefix": "test_prefix",
        "userId": "test_user",
        "privacy": "Private",
        "modelTags": [],
    }
    # Check if a POST request to mock_create_pair contains "completionItems"
    response = requests.post("http://localhost:5000/mock_create_pair", json=json_input)
    return response.status_code == 200


def grade_checkpoint2():
    json_input = {
        "prefix": "test_prefix",
        "userId": "test_user",
        "privacy": "Private",
        "modelTags": [],
    }
    # Check if a POST request to mock_create_pair contains "completionItems"
    response = requests.post("http://localhost:5000/mock_create_pair", json=json_input)
    response_json = response.json()
    if response.status_code != 200:
        return False
    # Check if the response contains "completionItems"
    if "completionItems" not in response_json:
        return False
    # Check if the "completionItems" is a list
    if not isinstance(response_json["completionItems"], list):
        return False

    # Check if "completion" in the first completion item is "test"
    if response_json["completionItems"][0]["completion"] != "test":
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning(
            "No trajectory file provided, partial credit might not be granted"
        )
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], "r") as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)

    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2(trajectory)
    points = 3 * int(passed1) + 4 * int(passed2)
    print(f"Final points for task Example: {points}")
