import requests
import os

HOSTNAME = os.getenv("HOSTNAME") or "ogma.lti.cs.cmu.edu"
GITLAB_PORT = os.getenv("GITLAB_PORT") or "8929"
GITLAB_URL = f"http://{HOSTNAME}:{GITLAB_PORT}"
API_SERVER_PATH = "root/api-server"


def check_url(trajectory):
    return f"{GITLAB_URL}/{API_SERVER_PATH}" in trajectory


def check_code_clone():
    # check path exists
    if os.path.exists("/workspace/api-server"):
        with open("/workspace/api-server/server.py") as f:
            code_content = f.read()
            if "# Route 1: Welcome message" in code_content:
                return True
    return False


def check_api():
    response = requests.get("http://localhost:5000/welcome")
    return response.status_code == 200 and response.json() == {
        "message": "Welcome to the Flask API!"
    }


def check_locust_installed():
    try:
        import locust

        return True
    except Exception as e:
        return False


def check_load_test_result(browser_logs):
    expected_keywords = [
        "GET",
        "Type",
        "Name",
        "Request Count",
        "Failure Count",
        "Median Response Time",
        "Average Response Time",
        "Min Response Time",
        "Max Response Time",
        "Requests/s",
        "Failures/s",
        "50%",
        "90%",
        "95%",
        "99%",
    ]
    load_test_filepath = "/workspace/load_test_results.csv"
    if os.path.exists(load_test_filepath):
        with open(load_test_filepath, "r") as f:
            load_test_results = f.read()
            for keyword in expected_keywords:
                if keyword not in load_test_results:
                    return False

            return True

    return False


if __name__ == "__main__":
    print(check_url(f"ACTION: goto('{GITLAB_URL}/{API_SERVER_PATH}')"))
    print(check_code_clone())
    print(check_api())
    print(check_locust_installed())
    print(check_load_test_result())
