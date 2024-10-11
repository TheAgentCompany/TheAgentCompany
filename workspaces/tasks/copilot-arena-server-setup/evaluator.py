import requests
import logging
import os
import sys


def grade_checkpoint1():
    return os.path.exists("/workspace/copilot-arena-server")


def grade_checkpoint2(trajectory):
    return "requirements.txt" in trajectory


def grade_final_checkpoint():
    try:
        response = requests.get("http://localhost:5000/list_models")
        return response.status_code == 200
    except Exception:
        return False


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
    passed3 = grade_final_checkpoint()
    points = 7 if passed3 else 3 * int(passed1) + int(passed2)
    print(f"Final points for task Example: {points}")
