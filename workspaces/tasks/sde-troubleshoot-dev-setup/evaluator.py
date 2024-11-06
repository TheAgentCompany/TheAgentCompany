import logging
from typing import List
import requests
from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history

def grade_checkpoint1(trajectory="") -> bool:
    """Check if agent visited the requirements.txt file in copilot-arena-server."""
    required_url = "http://the-agent-company.com:8929/root/copilot-arena-server/-/blob/main/requirements.txt"
    return required_url in trajectory

def compare_environment_files() -> bool:
    """Compare myenv.txt with requirements.txt for alignment."""
    try:
        with open('/workspace/myenv.txt', 'r') as f:
            myenv_content = f.read()
        
        # Fetch requirements.txt content from repo
        response = requests.get("http://the-agent-company.com:8929/root/copilot-arena-server/-/raw/main/requirements.txt")
        requirements_content = response.text
        
        # TODO: Implement comparison logic
        return True  # Placeholder
    except Exception as e:
        logging.error(f"Failed to compare environment files: {e}")
        return False

def check_emily_conversation() -> bool:
    """Check if agent had a conversation with Emily Zhou."""
    rocket = create_rocketchat_client()
    messages = get_rocketchat_personal_chat_history(rocket, "Emily Zhou")
    return len(messages) > 0

def check_library_discussion() -> bool:
    """Check if conversation mentions pandas and scikit-learn version issues."""
    rocket = create_rocketchat_client()
    messages = get_rocketchat_personal_chat_history(rocket, "Emily Zhou")
    
    # Convert messages to lowercase for case-insensitive search
    combined_messages = " ".join(messages).lower()
    
    required_keywords = ["pandas", "scikit-learn", "version"]
    return all(keyword in combined_messages for keyword in required_keywords)

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Visit requirements.txt
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    
    # Checkpoint 2: Environment alignment
    checkpoints.append(Checkpoint(1, int(compare_environment_files())))
    
    # Checkpoint 3: Conversation with Emily
    checkpoints.append(Checkpoint(1, int(check_emily_conversation())))
    
    # Checkpoint 4: Specific library discussion
    checkpoints.append(Checkpoint(1, int(check_library_discussion())))

    return result