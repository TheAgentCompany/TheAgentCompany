from common import create_rocketchat_client
from common import get_chat_history
from common import evaluate_chat_history_with_llm

# Initialize RocketChat client
rocket = create_rocketchat_client()

def evaluate_task():
    points = 0

    npcs = ["Mike Chen", "Li Ming", "Zhang Wei"]
    performance_evaluatee = "Liu Qiang"

    for npc in npcs:
        if get_chat_history(npc):
            points += 1

    if evaluate_chat_history_with_llm(rocket, performance_evaluatee, "the person receiving the feedback had an average job performance"):
        points += 2

    # Final result
    print(f"Evaluation completed. Final score: {points}/5")
    return points

if __name__ == "__main__":
    evaluate_task()
