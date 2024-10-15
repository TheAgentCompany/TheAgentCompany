import requests
import logging

base_url = "http://ogma.lti.cs.cmu.edu:8929/api/v4"
project_id = "root%2Fopenhands" 
issue_iid = "3797"
target_comment = "Closing due to inactivity"
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}

def grade_checkpoint1():
    comments_url = f"{base_url}/projects/{project_id}/issues/{issue_iid}/notes"
    
    try:
        comments_response = requests.get(comments_url, headers=headers)
        comments_response.raise_for_status()
        comments_data = comments_response.json()
        has_target_comment = any(target_comment in comment['body'] for comment in comments_data)
        
        return has_target_comment
    except Exception as e:
        logging.error(f"Get comment failed: {e}")
        return False

def grade_checkpoint2():
    issue_url = f"{base_url}/projects/{project_id}/issues/{issue_iid}"

    try: 
        issue_response = requests.get(issue_url, headers=headers)
        issue_response.raise_for_status()
        issue_data = issue_response.json()
        return issue_data['state'] == 'closed'
    except Exception as e:
        logging.error(f"Error fetching issue status: {e}")
    return False

if __name__ == "__main__":
    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2()
    print(f"Final points for task: {passed1 + passed2}")
