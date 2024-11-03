import logging
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, get_rocketchat_channel_history

# Initialize RocketChat client
rocket = create_rocketchat_client()

# Define the expected URL and metrics
PLANE_ANALYTICS_URL = "http://the-agent-company.com:8091/tac/analytics"
ROCKETCHAT_CHANNEL = "general"
EXPECTED_METRICS = {
    "open tasks": 28,
    "backlog tasks": 7,
    "unstarted tasks": 9,
    "started tasks": 12,
    "unassigned issues": 4,
    "pending issues": 24
}

def grade_checkpoint1(trajectory: str) -> bool:
    """Check if the agent accessed the Plane Analytics section."""
    return PLANE_ANALYTICS_URL in trajectory

def grade_checkpoint2() -> bool:
    """
    Check if any message was sent to the #kudos channel on Rocket.Chat.
    """
    messages = get_rocketchat_channel_history(rocket, "kudos")
    return bool(messages)  # True if there is at least one message, False otherwise

def grade_checkpoint3() -> int:
    """
    Check if the summary message in Rocket.Chat contains the specific metrics.
    Award points based on the number of metrics present in the message.
    """
    messages = get_rocketchat_channel_history(rocket, "kudos")
    if not messages:
        return 0  # No points if no messages are found

    # Define the expected metrics as text for easier comparison
    expected_metrics_text = [
        f"{metric}: {count}" for metric, count in EXPECTED_METRICS.items()
    ]
    
    # Check each message to see how many of the expected metrics it contains
    for message in messages:
        message_text = message.get("msg", "").lower() 
        
        # Count the number of metrics found in the message
        metrics_found = sum(
            1 for expected_text in expected_metrics_text if expected_text.lower() in message_text
        )

        # Assign points based on the number of metrics found
        if metrics_found == len(expected_metrics_text):
            return 3  # Full points if all metrics are present
        elif metrics_found >= 4:
            return 2  # Partial points if most metrics are present
        elif metrics_found >= 2:
            return 1  # Minimum points if some metrics are present
    
    return 0  # No points if fewer than 2 metrics are present



def grade_checkpoints(trajectory: str) -> Result:
    checkpoints = []
    
    # Checkpoint 1: Accessed Plane Analytics
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))
    
    # Checkpoint 2: Collected and reported required metrics correctly
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))
    
    # Checkpoint 3: Confirmed summary report message in RocketChat
    points_for_checkpoint3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(3, points_for_checkpoint3))
    
    return Result(checkpoints, bonus_for_completing_final)
