import os
import logging
import sqlite3
import requests
import time
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Post-Init Test")

def test_server_running():
    """Test if the Flask server is running and accessible."""
    # Start the server if not already running
    try:
        subprocess.Popen(["python3", "events-viewer/app.py"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        # Give it a moment to start
        time.sleep(2)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        return False

    # Test server access
    try:
        response = requests.get('http://localhost:5000/events')
        if response.status_code != 200:
            logger.error(f"Server returned status code {response.status_code}")
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to connect to server: {e}")
        return False

if __name__ == "__main__":
    if not test_server_running():
        raise Exception("Failed to verify server setup")
