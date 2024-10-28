import requests
import os
from rocketchat_API.rocketchat import RocketChat
import ipdb

# Rocket.Chat server URL and admin credentials
SERVER_HOSTNAME = 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'theagentcompany'
ADMIN_PASS = 'theagentcompany'
print(ROCKETCHAT_URL)
# Initialize the RocketChat client with username and password
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

def check_url_1(browser_logs):
    return f"{ROCKETCHAT_URL}/home" in browser_logs

def check_url_2(browser_logs):
    return f"{ROCKETCHAT_URL}/channel/literaturereview" in browser_logs

def check_url_3(browser_logs):
    return f"{ROCKETCHAT_URL}/channel/benchmarking" in browser_logs

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_channel_exists(channel_name):
    channels = rocket.channels_list().json()
    channel_names = channels.get("channels")
    return any(current_channel['name'] == channel_name for current_channel in channel_names)

def check_user_added(channel_name, username):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members")
    return any(user['username'] == username for user in users_list)


def check_message_sent(channel_name, message, username):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False

    # Fetch message history for the channel using room_id (channel_id)
    response = rocket.channels_history(room_id=room_id).json()

    if response.get('success'):
        messages = response.get('messages', [])
        # Check if the message 'Hi' is in the most recent messages from a specific user
        for msg in messages:
            if msg.get('msg') == message and msg.get('u', {}).get('username') == username:
                return True
    return False


if __name__ == "__main__":
    test_url_1 = f"{ROCKETCHAT_URL}/home"
    result1 = check_url_1(f"ACTION: goto('{test_url_1}')")
    result2 = check_channel_exists("literaturereview")
    test_url_2 = f"{ROCKETCHAT_URL}/channel/literaturereview"
    result3 = check_url_2(f"ACTION: goto('{test_url_2}')")
    result4 = check_channel_exists("benchmarking")
    test_url_3 = f"{ROCKETCHAT_URL}/channel/benchmarking"
    result5 = check_url_2(f"ACTION: goto('{test_url_3}')")
    result6 = check_user_added("literaturereview", "emma_lewis")
    result7 = check_user_added("literaturereview", "wang_fang")
    result8 = check_message_sent("literaturereview", 'Welcome to the literature review channel!', "theagentcompany")
    result9 = check_user_added("benchmarking", "emma_lewis")
    result10 = check_user_added("benchmarking", "alex_turner")
    result11 = check_user_added("benchmarking", "david_wong")
    result12 = check_message_sent("benchmarking", 'This will be for all our benchmarking projects.', "theagentcompany")

    # Summing all results to create a score
    score = (result1 + result2 + result3 + result4 + result5 + 
             result6 + result7 + result8 + result9 + result10 + 
             result11 + result12)
    
    print("Total score:", score)