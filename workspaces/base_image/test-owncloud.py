import logging
from common import (
    get_owncloud_url_in_file,
    download_owncloud_content,
    check_file_in_owncloud_directory,
    get_binary_file_content_owncloud
)

from config import *


filename = "job_description.md"
dir_name = "Documents/"
fileLink = "link.txt"
# Configure logging
logging.basicConfig(level=logging.INFO)

def test_get_owncloud_url_in_file():
    result = get_owncloud_url_in_file(fileLink)
    print(f"URL in file: {result}")

def test_download_owncloud_content():
    link = get_owncloud_url_in_file(fileLink)
    output_file_path = 'downloaded_content.txt'
    result = download_owncloud_content(link, output_file_path)
    print(f"Download result: {result}")

def test_check_file_in_owncloud_directory():
    result = check_file_in_owncloud_directory(filename, dir_name)
    print(f"File exists: {result}")

def test_get_binary_file_content_owncloud():
  
    content = get_binary_file_content_owncloud(filename, dir_name)
    if content:
        print(f"File content: {content[:100]}...")  # Print first 100 bytes
    else:
        print("Failed to retrieve file content")

if __name__ == "__main__":
    test_get_owncloud_url_in_file()
    test_download_owncloud_content()
    #test_check_file_in_owncloud_directory()
    #test_get_binary_file_content_owncloud()