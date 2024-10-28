import time
import requests
import os

url = "http://localhost:3000"

def wait_for_rocketchat(retries=300, delay=3):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Web service is up!")
                break
            else:
                print(f"Web service returned status code {response.status_code}. Waiting...")
        except requests.ConnectionError:
            print("Web service is not available yet. Retrying...")
        time.sleep(delay)


wait_for_rocketchat()

os.system("make reset-rocketchat")