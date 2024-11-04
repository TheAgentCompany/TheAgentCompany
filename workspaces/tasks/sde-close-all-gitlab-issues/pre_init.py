import logging

from common import make_gitlab_request

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

def find_an_issue():
    page_index = 1
    while True:
        resp = make_gitlab_request(additional_path=f"projects?page={page_index}&per_page=100")
        if resp is None:
            raise Exception("Failed to retrieve projects")
        projects = resp.json()
        for project in projects:
            project_detail_resp = make_gitlab_request(str(project['id']))
            if project_detail_resp is None:
                raise Exception("Failed to retrieve project details")
            open_issues_count = project_detail_resp.json().get('open_issues_count', 0)
            if open_issues_count > 0:
                return
        if len(projects) < 100:
            break
        page_index += 1
    raise Exception("No issue found")


if __name__ == "__main__":
    find_an_issue()
