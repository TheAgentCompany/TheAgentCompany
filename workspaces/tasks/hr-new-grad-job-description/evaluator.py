from common import evaluate_with_llm, get_nextcloud_url_in_file, download_nextcloud_content

############################# Helper Functions #####################################

def check_job_description_content():

    with open("/workspace/job_description.md", "r") as f:
        final_content = f.read()
    
    with open("/workspace/template.md", "r") as f:
        template_content = f.read()
    
    with open("/workspace/requirement.txt", "r") as f:
        requirement_content = f.read()
    
    if "[Insert Information]" in final_content:
        print("some placeholder still present in the final job description.")
        return False

    predicate = f'a successful combination of the markdown template \"\"{template_content}\"\" and the requirement file \"\"{requirement_content}'
    additional_prompt = 'Pay special consideration to all of the numerical details. '
    return evaluate_with_llm(final_content, predicate, additional_prompt)

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    link = get_nextcloud_url_in_file("/workspace/link.txt")
    if link:
        points += 1
        if download_nextcloud_content(link, "/workspace/job_description.md"):
            points += 1

        if check_job_description_content():
            print("Job description succesfully created")
            points += 1

    # Final result
    print(f"Evaluation completed. Final score: {points}/3")
    return points

if __name__ == "__main__":
    evaluate_task()
