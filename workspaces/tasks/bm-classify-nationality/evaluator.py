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


def load_customer_data(EXCEL_FILE_PATH):
    """Load customer data from the Excel file with custom header."""
    try:
        # Skip the first two rows, which are not part of the data
        df = pd.read_excel(EXCEL_FILE_PATH, skiprows=2, usecols=["Order ID", "Location", "Domestic or International"])
        return df
    except Exception as e:
        logging.warning(f"Failed to load Excel file: {e}")
        return None

def evaluate_classifications(df):
    """
    Evaluate if the classifications in the 'Domestic or International' column of the DataFrame
    match the expected classifications in EXPECTED_CLASSIFICATIONS for the first 18 rows.
    """
    if "Order ID" not in df.columns or "Domestic or International" not in df.columns:
        logging.warning("Required columns 'Order ID' and 'Domestic or International' not found in the Excel sheet.")
        return 0
    
    correct_classifications = 0
    total_classifications = min(18, len(df))  # Limit to the first 18 rows

    # Iterate over each valid row in the DataFrame
    for _, row in df.iloc[:18].iterrows():
        order_id = str(row.get("Order ID"))
        actual_classification = row.get("Domestic or International")
        
        # Only call .strip() if actual_classification is a string, otherwise set it to an empty string
        if isinstance(actual_classification, str):
            actual_classification = actual_classification.strip()
        else:
            actual_classification = ""

        expected_classification = EXPECTED_CLASSIFICATIONS.get(order_id, "")

        # Compare actual classification with the expected classification
        if actual_classification == expected_classification:
            correct_classifications += 1

    # Calculate accuracy and award points based on it
    accuracy = correct_classifications / total_classifications
    if accuracy == 1:
        return 2  # Full points for perfect classification
    elif accuracy >= 0.5:
        return 1  # Partial points for more than half classified correctly
    return 0  # No points if accuracy is below 50%


@grader
def grade_checkpoint1(trajectory):
    """Check if the 'Customer.xlsx' file on Nextcloud was accessed."""
    required_url_part = "dir=/Documents/Data%20Analysis"
    return required_url_part in trajectory

@grader
def grade_checkpoint2():
    """Check if all orders are classified correctly as domestic or international."""
    df = load_customer_data('/utils/Customer.xlsx')

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
    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    return result
    
def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Access to Customer.xlsx file
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, result=int(passed1)))

    # Load customer data

    # Checkpoint 2: Order classification correctness
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(2, result=passed2))

    # Checkpoint 3: Conversation with Sarah Johnson
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, result=int(passed3)))

    # Final Checkpoint: Delivered correct order numbers to Sarah Johnson
    passed_final = grade_final_checkpoint()
    checkpoints.append(Checkpoint(total=2, result=passed_final))

    return result