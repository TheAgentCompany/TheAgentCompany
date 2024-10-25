from common import evaluate_with_llm, create_rocketchat_client, get_chat_history, get_nextcloud_url_in_file, download_nextcloud_content
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Helper Functions #####################################

def check_job_description_content():

    with open("/workspace/job_description.md", "r") as f:
        final_content = f.read()
    
    with open("/instruction/template.md", "r") as f:
        template_content = f.read()
    
    with open("/utils/requirement.txt", "r") as f:
        requirement_content = f.read()
    
    if "[Insert Information]" in final_content:
        logger.error("some placeholder still present in the final job description.")
        return False

    predicate = f'a successful combination of the markdown template \"\"{template_content}\"\" and the requirement file \"\"{requirement_content}'
    additional_prompt = 'Pay special consideration to all of the numerical details. '
    return evaluate_with_llm(final_content, predicate, additional_prompt)

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    if get_chat_history(rocket, "zhang_wei"):
        points += 1

    link = get_nextcloud_url_in_file("/workspace/link.txt")
    if link:
        points += 1
        if download_nextcloud_content(link, "/workspace/job_description.md"):
            points += 1

        if check_job_description_content():
            logger.info("Job description succesfully created")
            points += 1

    # Final result
    logger.info(f"Evaluation completed. Final score: {points}/4")
    return points

if __name__ == "__main__":
    evaluate_task()
