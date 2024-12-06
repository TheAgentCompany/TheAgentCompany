from typing import List
import pandas as pd
from common import get_rocketchat_personal_chat_history, create_rocketchat_client, grader
from scoring import Result, Checkpoint, bonus_for_completing_final
import logging


# Updated expected classifications based on the provided table
EXPECTED_CLASSIFICATIONS = {
    "1010": "Domestic",
    "1011": "Domestic",
    "1012": "International",
    "1013": "International",
    "1014": "International",
    "1015": "International",
    "1016": "Domestic",
    "1017": "Domestic",
    "1018": "International",
    "1019": "International",
    "1020": "International",
    "1021": "International",
    "1022": "International",
    "1023": "International",
    "1024": "International",
    "1025": "International",
    "1026": "",
    "1027": "Domestic"
}

# Create RocketChat instance
rocket = create_rocketchat_client()


@grader
def grade_checkpoint1():
    """Check if the agent has a conversation with Sarah Johnson on Rocket.Chat about customer orders."""
    # Required keywords that should all be present in a message
    required_keywords = ["domestic", "international"]

    # Retrieve chat history with Sarah Johnson
    messages = get_rocketchat_personal_chat_history(rocket, "sarah_johnson")
    if not messages:
        return False


    # Join all messages into a single text to allow for distributed keyword search
    combined_message_text = "\n".join(message.lower() for message in messages)

    # Check if all required keywords are present in the combined text
    return all(keyword in combined_message_text for keyword in required_keywords)



def grade_final_checkpoint():
    """Check if the correct domestic and international order numbers were delivered to Sarah Johnson."""
    # Expected counts for domestic and international orders
    expected_domestic_count = 5
    expected_international_count = 12

    # Keywords to look for in the message
    required_info = [f"domestic: {expected_domestic_count}", f"international: {expected_international_count}"]

    # Retrieve chat history with Sarah Johnson
    messages = get_rocketchat_personal_chat_history(rocket, "sarah_johnson")
    if not messages:
        return 0

    # Join all messages into a single text to allow for distributed information search
    combined_message_text = "\n".join(message.lower() for message in messages)

    # Check if all required information is present in the combined text
    if all(info in combined_message_text for info in required_info):
        return 2  # Full points for a complete report

    return 0

    
def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    
    # Checkpoint 1: Conversation with Sarah Johnson
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, result=int(passed1)))

    # Final Checkpoint: Delivered correct order numbers to Sarah Johnson
    passed_final = grade_final_checkpoint()
    checkpoints.append(Checkpoint(total=2, result=passed_final))

    return result