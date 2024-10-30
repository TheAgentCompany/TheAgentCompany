import requests
import logging
import sys
import os

from typing import List

from scoring import Result, Checkpoint


def grade_checkpoint1():
    try:
        response = requests.get("http://localhost:5000/list_models")
        if response.status_code != 200:
            logging.warning(
                "Checkpoint 1 failed: Unexpected status code %d", response.status_code
            )
            return False
        return True
    except Exception as e:
        logging.warning(
            "Checkpoint 1 failed: Local server is not launched correctly. Error: %s",
            str(e),
        )
        return False


def grade_checkpoint2():
    try:
        json_input = {
            "prefix": "test_prefix",
            "userId": "test_user",
            "privacy": "Private",
            "modelTags": [],
        }
        response = requests.post(
            "http://localhost:5000/mock_create_pair", json=json_input
        )
        if response.status_code != 200:
            logging.warning(
                "Checkpoint 2 failed: Unexpected status code %d", response.status_code
            )
            return False
        return True
    except Exception as e:
        logging.warning(
            "Checkpoint 2 failed: Local server is not launched correctly. Error: %s",
            str(e),
        )
        return False


def grade_checkpoint3():
    try:
        json_input = {
            "prefix": "test_prefix",
            "userId": "test_user",
            "privacy": "Private",
            "modelTags": [],
        }
        response = requests.post(
            "http://localhost:5000/mock_create_pair", json=json_input
        )
        response_json = response.json()
        if response.status_code != 200:
            logging.warning(
                "Checkpoint 3 failed: Unexpected status code %d", response.status_code
            )
            return False
        if "completionItems" not in response_json:
            logging.warning("Checkpoint 3 failed: 'completionItems' not in response")
            return False
        if not isinstance(response_json["completionItems"], list):
            logging.warning("Checkpoint 3 failed: 'completionItems' is not a list")
            return False
        if response_json["completionItems"][0]["completion"] != "test":
            logging.warning("Checkpoint 3 failed: First completion item is not 'test'")
            return False
        return True
    except Exception as e:
        logging.warning(
            "Checkpoint 3 failed: Local server is not launched correctly. Error: %s",
            str(e),
        )
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(2, 2 * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(3, 3 * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(4, 4 * int(passed3)))

    return result



