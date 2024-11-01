import logging
from common import make_gitlab_request

# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

def test_gitlab_access():
    """Test if we can access the JanusGraph GitLab repository."""
    response = make_gitlab_request("janusgraph/janusgraph")
    if response is None or response.status_code != 200:
        logger.error("Cannot access JanusGraph GitLab repository")
        return False
    return True

if __name__ == "__main__":
    if not test_gitlab_access():
        raise Exception("Failed to access GitLab repository")
    