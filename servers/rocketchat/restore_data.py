import time
import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.logging_config import logger

url = "http://localhost:3000"

def wait_for_rocketchat(retries=300, delay=3):
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Web service is up!")
                return True
            else:
                logger.warning(f"Web service returned status code {response.status_code}. Waiting...")
        except requests.ConnectionError:
            logger.warning("Web service is not available yet. Retrying...")
        time.sleep(delay)
    return False


if __name__ == "__main__":
    if wait_for_rocketchat():
        logger.info("Starting RocketChat data restoration...")
        os.system("make reset-rocketchat")
    else:
        logger.error("Failed to connect to RocketChat after maximum retries")

