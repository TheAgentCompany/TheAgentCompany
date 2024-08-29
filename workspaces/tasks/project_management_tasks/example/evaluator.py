import requests
import os

def check_url_1(browser_logs):
    return "http://ogma.lti.cs.cmu.edu:3000/directory/channels" in browser_logs

def check_url_2(browser_logs):
    return "http://ogma.lti.cs.cmu.edu:3000/channel/general" in browser_logs


def check_message_sent():
    # This function checks if the message "Hi" was sent to the #general channel.
    # Call Rocket.Chat's API to check recent messages
    # in the #general channel and confirm if "Hi" was sent by the agent.
    
    rocketchat_url = "http://ogma.lti.cs.cmu.edu:3000/api/v1/channels.history"
    channel_name = "general"
    token = os.getenv('ROCKETCHAT_AUTH_TOKEN') or 'vn_Tadey_p7fHnMExAIpgwxFKjpsW4j4-kCpdmB3epq'
    user_id = os.getenv('ROCKETCHAT_USER_ID') or 'qgyxXGaG3uzLq7gDt'
    
    headers = {
        'X-Auth-Token': token,
        'X-User-Id': user_id,
        'Content-type': 'application/json',
    }
    
    response = requests.get(f"{rocketchat_url}?roomName={channel_name}", headers=headers)
    
    if response.status_code == 200:
        messages = response.json().get('messages', [])
        for message in messages:
            if message.get('msg') == 'Hi':
                return True
    return False


if __name__ == "__main__":
    print(check_url_1("ACTION: goto('http://ogma.lti.cs.cmu.edu:3000/directory/channels')"))
    print(check_url_2("ACTION: goto('http://ogma.lti.cs.cmu.edu:3000/channel/general')"))
    print(check_message_sent())
