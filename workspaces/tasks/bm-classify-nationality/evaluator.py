from typing import List
import pandas as pd
from common import get_rocketchat_personal_chat_history, create_rocketchat_client, download_owncloud_content, grader
from scoring import Result, Checkpoint, bonus_for_completing_any
import logging


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define constants
OWNCLOUD_FILE_URL = "http://the-agent-company.com:8092/apps/files/files/1749?dir=/Documents/Data%20Analysis&openfile=true"
DOWNLOADED_FILE = "/workspace/Customer_downloaded.xlsx"

# Define expected classifications
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

# Create RocketChat client
rocket = create_rocketchat_client()


def load_customer_data(file_path: str):
    """Load customer data from the Excel file."""
    try:
        df = pd.read_excel(file_path, skiprows=2, usecols=["Order ID", "Location", "Domestic or International"])
        return df
    except Exception as e:
        logging.warning(f"Failed to load Excel file: {e}")
        return None


def evaluate_classifications(df):
    """Evaluate the correctness of classifications."""
    if "Order ID" not in df.columns or "Domestic or International" not in df.columns:
        logging.warning("Required columns not found in the Excel sheet.")
        return 0

    correct = 0
    total = len(EXPECTED_CLASSIFICATIONS)

    for _, row in df.iterrows():
        order_id = str(row.get("Order ID"))
        actual = row.get("Domestic or International", "").strip() if isinstance(row.get("Domestic or International"), str) else ""
        expected = EXPECTED_CLASSIFICATIONS.get(order_id, "")

        if actual == expected:
            correct += 1

    accuracy = correct / total
    if accuracy == 1:
        return 2  # Full points
    elif accuracy >= 0.5:
        return 1  # Partial points
    return 0

@grader
def grade_checkpoint1(trajectory):
    """Check if the correct file was accessed on NextCloud."""
    return OWNCLOUD_FILE_URL in trajectory

@grader
def grade_checkpoint2():
    """Check the classification correctness."""
    if not download_owncloud_content(OWNCLOUD_FILE_URL, DOWNLOADED_FILE):
        return 0

    df = load_customer_data(DOWNLOADED_FILE)
    if df is None:
        return 0
    return evaluate_classifications(df)

@grader
def grade_checkpoint3():
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


@grader
def grade_final_checkpoint():
    """Check if the correct counts were sent to Sarah Johnson."""
    expected_domestic_count = 5
    expected_international_count = 12
    required_info = [f"domestic: {expected_domestic_count}", f"international: {expected_international_count}"]

    messages = get_rocketchat_personal_chat_history(rocket, "sarah_johnson")
    if not messages:
        return 0

    combined_text = "\n".join(message.lower() for message in messages)
    return 2 if all(info in combined_text for info in required_info) else 0


def grade_checkpoints(trajectory=""):
    """Evaluate all checkpoints."""
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(2, int(grade_final_checkpoint())))

    logging.info(f"Evaluation completed: {checkpoints}")
    return result
