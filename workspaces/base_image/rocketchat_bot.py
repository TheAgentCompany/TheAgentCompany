from pprint import pprint
from random import choice
from time import sleep
import os

from rocketchat_API.rocketchat import RocketChat

agent_username = os.getenv('AGENT_USERNAME') or 'jobbench'

class RocketChatBot(object):
    def __init__(self, botname, passwd, server, command_character=None):
        self.botname = botname
        self.api = RocketChat(user=botname, password=passwd, server_url=server)
        self.lastts = {}
        self.command_character = command_character
        self.last_channel_id = "GENERAL"
        self.username = self.api.me().json()['username']
        self.default_latestts = "2024-10-01T00:00:00.000Z"

    def get_status(self, auser):
        return self.api.users_get_presence(username=auser)

    def send_message(self, msg):
        self.api.chat_post_message(channel=self.last_channel_id, text=msg)

    def handle_messages(self, messages, channel_id):
        self.last_channel_id = channel_id
        for message in messages['messages']:
            if message['u']['username'] != self.botname:
                pprint(message)
                # filter out the message not from jobbench
                if message['u']['username'] != agent_username:
                    continue
                return message['msg']
        return None

    def load_ts(self, channel_id, messages):
        if len(messages) > 0:
            self.lastts[channel_id] = messages[0]['ts']
        else:
            self.lastts[channel_id] = ''

    def load_channel_ts(self, channel_id):
        self.load_ts(channel_id, self.api.channels_history(channel_id).json()['messages'])

    def load_group_ts(self, channel_id):
        self.load_ts(channel_id, self.api.groups_history(channel_id).json()['messages'])

    def load_im_ts(self, channel_id):
        response = self.api.im_history(channel_id).json()
        if response.get('success'):
            self.load_ts(channel_id, self.api.im_history(channel_id).json()['messages'])

    def process_messages(self, messages, channel_id):
        try:
            if "success" in messages:
                if messages['success'] == False:
                    return None
                    # raise RuntimeError(messages['error'])
            if len(messages['messages']) > 0:
                self.lastts[channel_id] = messages['messages'][0]['ts']
            return self.handle_messages(messages, channel_id)
        except Exception as e:
            pprint(e)
            return None

    def process_channel(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''
        if not self.lastts[channel_id]:
            self.lastts[channel_id] = self.default_latestts
        return self.process_messages(self.api.channels_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def process_group(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''
        if not self.lastts[channel_id]:
            self.lastts[channel_id] = self.default_latestts
        return self.process_messages(self.api.groups_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def process_im(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''
        if not self.lastts[channel_id]:
            self.lastts[channel_id] = self.default_latestts
        return self.process_messages(self.api.im_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def run(self):
        for channel in self.api.channels_list_joined().json().get('channels', []):
            self.load_channel_ts(channel.get('_id'))

        for group in self.api.groups_list().json().get('groups', []):
            self.load_group_ts(group.get('_id'))

        for im in self.api.im_list().json().get('ims', []):
            self.load_im_ts(im.get('_id'))

        message = ""
        while 1:
            # Add error handler None 
            for channel in self.api.channels_list_joined().json().get('channels', []):
                message = self.process_channel(channel.get('_id'))
                if message is not None:
                    return message

            for group in self.api.groups_list().json().get('groups', []):
                message = self.process_group(group.get('_id'))
                if message is not None:
                    return message

            for im in self.api.im_list().json().get('ims', []):
                message = self.process_im(im.get('_id'))
                if message is not None:
                    return message
            print("No message received, waiting...")
            sleep(1)

"""
message format
{
  "_id": "rZnsWiF9YywGi4itM",
  "rid": "qgyxXGaG3uzLq7gDtrocket.cat",
  "msg": "hi",
  "ts": "2024-09-07T09:07:13.769Z",
  "u": {
    "_id": "qgyxXGaG3uzLq7gDt",
    "username": "jobbench",
    "name": "jobbench"
  },
  "_updatedAt": "2024-09-07T09:07:13.817Z",
  "urls": [],
  "mentions": [],
  "channels": [],
  "md": [
    {
      "type": "PARAGRAPH",
      "value": [
        {
          "type": "PLAIN_TEXT",
          "value": "hi"
        }
      ]
    }
  ]
}

"""

"""
# Useage

import os
botname = os.getenv('BOTNAME') or "rocket.cat"
botpassword = os.getenv('BOTPASSWORD') or "jobbench"
server_url = os.getenv('BOT_URL') or 'http://localhost:3000'
# server_url = 'ogma.lti.cs.cmu.edu:3000'
bot = RocketChatBot(botname, botpassword, server_url)
bot.run()
"""