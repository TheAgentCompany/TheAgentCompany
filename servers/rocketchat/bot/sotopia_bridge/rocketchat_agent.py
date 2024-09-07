import asyncio
import logging
from uuid import uuid4

import aiohttp
import pydantic
import requests

from sotopia.agents import BaseAgent
from sotopia.database import AgentProfile, MessageTransaction
from sotopia.messages import AgentAction, Observation

from pydantic import Field
from datetime import datetime

from typing import Any
from datetime import datetime
import os
from .rocket_chat_bot import RocketChatBot

botname = os.getenv('BOTNAME') or "rocket.cat"
botpassword = os.getenv('BOTPASSWORD') or "jobbench"
server_url = os.getenv('BOT_URL') or 'http://localhost:3000'

def parse_obj(obj: dict[str, Any]) -> "RocketChatMessageTransaction":
    if obj:
        return RocketChatMessageTransaction(
            timestamp_str=obj["timestamp"],
            sender=obj["username"],
            message=obj["text"],
        )
    else:
        print("obj is None")
        return RocketChatMessageTransaction(
            timestamp_str="2023-04-28T16:22:49.581778164-04:00",
            sender="",
            message="",
        )


class RocketChatMessageTransaction(MessageTransaction):
    def to_tuple(self) -> tuple[float, str, str]:
        timestamp = datetime.fromisoformat(self.timestamp_str)
        return (
            timestamp.timestamp(),
            self.sender,
            self.message,
        )


class RocketChatAgent(BaseAgent[Observation, AgentAction]):
    """An agent use rocket chat as a message broker."""

    def __init__(
        self,
        agent_name: str | None = None,
        uuid_str: str | None = None,
        session_id: str | None = None,
        agent_profile: AgentProfile | None = None,
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            uuid_str=uuid_str,
            agent_profile=agent_profile,
        )
        # super().__init__(agent_name=agent_name, uuid_str=uuid_str)
        self.session_id = session_id or str(uuid4())
        self.sender_id = str(uuid4())
        print("step 1: connect to the server")
        self.bot = RocketChatBot(botname, botpassword, server_url)
        self.send_init_message()
        logging.info(f"Session ID: {self.session_id}")

    def act(
        self,
        obs: Observation,
    ) -> AgentAction:
        raise NotImplementedError

    async def aact(
        self,
        obs: Observation,
    ) -> AgentAction:
        self.recv_message("Environment", obs)
        print("Enter function")
        if len(obs.available_actions) == 1 and "none" in obs.available_actions:
            print("No available actions.")
            if obs.turn_number == 0:
                await self.send_message(obs)
            return AgentAction(action_type="none", argument="")
        last_timestamp = await self.send_message(obs)
        return await self.get_action_from_message(last_timestamp)

    def send_init_message(self):
        login_info = self.bot.api.me().json()
        if 'error' in login_info:
            raise RuntimeError(f"Login failed: {login_info['error']}")
        
        print(f"Login successful! User info: {login_info}")
        self.bot.send_message("RocketChat Agent Listening")
        return

    async def send_message(self,obs: Observation):
        # 1. post observation to the message list
        print("step 2: post observation to the message list:",obs.last_turn)
        last_timestamp = current_timestamp = datetime.now()
        self.bot.send_message(obs.last_turn)
        return last_timestamp
    
    async def get_action_from_message(self,last_timestamp):
        # Get meesage from client
        # if not success:
        #     self.reset("Someone has left or the conversation is too long.")
        #     return AgentAction(action_type="leave", argument="")
        return self.constrct_speak_action(self.bot.run())

    def constrct_speak_action(self,message):
        action_string = message
        action_string_formatted = f'{{"action_type": "speak", "argument": "{action_string}"}}'
        try:
            action = AgentAction.parse_raw(action_string_formatted)
            return action
        except pydantic.error_wrappers.ValidationError:
            logging.warn(
                "Failed to parse action string {}. Fall back to speak".format(
                    action_string
                )
            )
            return AgentAction(
                action_type="speak", argument=message
            )

    def reset(
        self,
        reset_reason: str = "",
    ) -> None:
        super().reset()
        try:
            if reset_reason != "":
                self.bot.send_message(reset_reason)
        except Exception as e:
            logging.error(f"Failed to reset RedisAgent {self.sender_id}: {e}")