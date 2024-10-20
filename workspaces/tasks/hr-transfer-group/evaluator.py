from llm_evaluator import *
from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()
############################# Helper Functions #####################################

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_if_user_in_channel(channel_name: str, username: str):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return None
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members")
    return any(user['name'] == username for user in users_list)


def check_job_description(username: str):

    user_info = rocket.users_info(username=username).json().get('user', {})
    job_description = user_info.get('bio', '')
    print(f"{username}''s Job Description: {job_description}")

    messages = [{"content": f"Does the phrase \"\"{job_description}\"\" indicate the person does not work in database team and now works in the AI team? Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]
    # Check result
    llm_resonse = llm_evaluator(messages).json()
    print(llm_resonse)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        print(f"{username}'s job description is updated correctly")
        return True
    else:
        print(f"{username}'s job description is not updated correctly")
        return False

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    employee = "Li Ming"
    user_name = "li_ming"

    res =  check_if_user_in_channel("project-graphdb", employee)
    if res is not None and not res:
        print("succesfully removed from #project-graphdb channel")
        points += 1
    
    res = check_if_user_in_channel("project-ai", employee)
    if res:
        print("succesfully added to #project-ai channel")
        points += 1

    if check_job_description(user_name):
        print("Job description succesfully updated")
        points += 1

    # Final result
    print(f"Evaluation completed. Final score: {points}/3")
    return points

if __name__ == "__main__":
    evaluate_task()
