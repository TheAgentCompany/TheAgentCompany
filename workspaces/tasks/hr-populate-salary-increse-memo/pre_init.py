import os
import subprocess
import requests
import logging
from rocketchat_API.rocketchat import RocketChat
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

############################# init variable ##################################### 
HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'

############################# util function #####################################  
# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

############################# Test function ##################################### 


if __name__ == "__main__":
    pass
