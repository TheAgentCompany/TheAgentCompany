import logging
from common import make_gitlab_request

# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Post-Init Test")

def test_gitlab_permissions():
    """Test if we have sufficient permissions to create issues and comments."""
    # Try to create a test issue
    response = make_gitlab_request("janusgraph/janusgraph", "issues", method='POST', params={
        'title': 'test-issue-please-ignore',
        'description': 'This is a test issue to verify permissions. Please ignore.'
    })
    if response is None or response.status_code != 201:
        logger.error("Cannot create issues in GitLab repository")
        return False
    
    # Get the issue ID
    issue_iid = response.json()['iid']
    
    # Try to create a comment
    response = make_gitlab_request("janusgraph/janusgraph", f"issues/{issue_iid}/notes", method='POST', params={
        'body': 'Test comment - please ignore'
    })
    if response is None or response.status_code != 201:
        logger.error("Cannot create comments on issues")
        return False
    
    # Clean up - close the test issue
    response = make_gitlab_request("janusgraph/janusgraph", f"issues/{issue_iid}", method='PUT', params={
        'state_event': 'close'
    })
    if response is None or response.status_code != 200:
        logger.warning("Could not close test issue")
    
    return True

if __name__ == "__main__":
    if not test_gitlab_permissions():
        raise Exception("Failed to verify GitLab permissions")
