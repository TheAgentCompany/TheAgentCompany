from common import llm_evaluate, create_rocketchat_client
import subprocess
import re
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

# Construct RocketChat URL
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Helper Functions #####################################

def get_history(username):
    id = ""
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        logger.info(f"{username}'s chat: {msg['msg']}")

    if len(msgs)>0:
        return True
    else:
        return False


def check_url_file_exist():
    filename = "/workspace/link.txt"
    try:
        with open(filename, 'r') as file:
            content = file.read()
            if f"https://ogma.lti.cs.cmu.edu" in content:
                return content
            return False
    except FileNotFoundError:
        logger.error(f"Error: The file '{filename}' was not found.")
        return False
    except IOError as e:
        logger.error(f"Error: An I/O error occurred. Details: {e}")
        return False

def verify_nextcloud_content_exists(link):

    if "download" not in link:
        command = ["curl", "--output", "/workspace/download_link", link.rstrip("\n")]
        try:
            subprocess.run(command)
        except Exception as e:
            logger.error(f"Unable to download from link: {link}")
            return False

        pattern = r'https?://[^\s]*\bdownload\b[^\s]*(?=")'

        download_link: str | None = None
        with open("/workspace/download_link", "r") as f:
            content = f.read()
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                download_link = matches[0]
        
        if download_link is None:
            logger.error(f"Did not find proper download link")
            return False
    else:
        download_link = link.rstrip("\n")

    try:
        logger.info(download_link)
        subprocess.run([f"curl {download_link} --output /workspace/job_description.md"], shell=True)
    except Exception as e:
        logger.error(f"Download from link: {download_link} not successful")
        return False

    logger.info(f"Successfully downloaded from link {download_link}")
    return True


def check_job_description_content():

    with open("/workspace/job_description.md", "r") as f:
        final_content = f.read()
    
    with open("/workspace/template.md", "r") as f:
        template_content = f.read()
    
    with open("/utils/requirement.txt", "r") as f:
        requirement_content = f.read()
    
    if "[Insert Information]" in final_content:
        logger.error("some placeholder still present in the final job description.")
        return False

    messages = [{"content": f"Is the content in the markdown file \"\"{final_content}\"\" a successful combination of the markdown template \"\"{template_content}\"\" and the requirement file \"\"{requirement_content}\"\"? Pay special consideration to all of the numerical details. Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]
    # Check result
    llm_resonse = llm_evaluate(messages)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        logger.info(f"New Grad software engineer job description is expected")
        return True
    else:
        logger.error(f"New Grad software engineer job description's content is not expected")
        return False

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    if get_history("zhang_wei"):
        points += 1

    link = check_url_file_exist()
    if link:
        points += 1
        if verify_nextcloud_content_exists(link):
            points += 1

        if check_job_description_content():
            logger.info("Job description succesfully created")
            points += 1

    # Final result
    logger.info(f"Evaluation completed. Final score: {points}/4")
    return points

if __name__ == "__main__":
    evaluate_task()
