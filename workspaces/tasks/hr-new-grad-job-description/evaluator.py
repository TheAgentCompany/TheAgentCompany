from common import evaluate_with_llm
import subprocess
import re

############################# Helper Functions #####################################

def check_url_file_exist():
    filename = "/workspace/link.txt"
    try:
        with open(filename, 'r') as file:
            content = file.read()
            if f"https://ogma.lti.cs.cmu.edu" in content:
                return content
            return False
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return False
    except IOError as e:
        print(f"Error: An I/O error occurred. Details: {e}")
        return False

def verify_nextcloud_content_exists(link):

    if "download" not in link:
        command = ["curl", "--output", "/workspace/download_link", link.rstrip("\n")]
        try:
            subprocess.run(command)
        except Exception as e:
            print(f"Unable to download from link: {link}")
            return False

        pattern = r'https?://[^\s]*\bdownload\b[^\s]*(?=")'

        download_link: str | None = None
        with open("/workspace/download_link", "r") as f:
            content = f.read()
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                download_link = matches[0]
        
        if download_link is None:
            print(f"Did not find proper download link")
            return False
    else:
        download_link = link.rstrip("\n")

    try:
        print(download_link)
        subprocess.run([f"curl {download_link} --output /workspace/job_description.md"], shell=True)
    except Exception as e:
        print(f"Download from link: {download_link} not successful")
        return False

    print(f"Successfully downloaded from link {download_link}")
    return True


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

    link = check_url_file_exist()
    if link:
        points += 1
        if verify_nextcloud_content_exists(link):
            points += 1

        if check_job_description_content():
            print("Job description succesfully created")
            points += 1

    # Final result
    print(f"Evaluation completed. Final score: {points}/3")
    return points

if __name__ == "__main__":
    evaluate_task()
