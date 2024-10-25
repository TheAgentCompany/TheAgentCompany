from common import llm_evaluate, get_nextcloud_url_in_file, download_nextcloud_content

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

    messages = [{"content": f"Is the content in the markdown file \"\"{final_content}\"\" a successful combination of the markdown template \"\"{template_content}\"\" and the requirement file \"\"{requirement_content}\"\"? Pay special consideration to all of the numerical details. Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]
    # Check result
    llm_resonse = llm_evaluate(messages)
    print(llm_resonse)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        print(f"New Grad software engineer job description is expected")
        return True
    else:
        print(f"New Grad software engineer job description's content is not expected")
        return False

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
