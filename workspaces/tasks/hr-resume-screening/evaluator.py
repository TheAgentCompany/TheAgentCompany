import logging

from common import create_rocketchat_client
from common import evaluate_chat_history_with_llm
from common import get_chat_history

# Initialize RocketChat client
rocket = create_rocketchat_client()

def run_checkpoint_1():
    messages = get_chat_history(rocket, 'Chen Xinyi')
    if not messages:
        logging.warning(f"No chat history found for Chen Xinyi")
        return False

    messages_cleaned = str(messages).lower()
    return 'green card' in messages_cleaned or 'citizen' in messages_cleaned


def run_checkpoint_2():
    return evaluate_chat_history_with_llm(
        rocket,
        'Li Ming',
        'Jane Lee cannot be hired because she fails to meet visa/green card/citizenship requirement'
        )


if __name__ == "__main__":
    points = run_checkpoint_1() + 2 * run_checkpoint_2()
    print(f"Evaluation completed. Final score: {points}/3")
