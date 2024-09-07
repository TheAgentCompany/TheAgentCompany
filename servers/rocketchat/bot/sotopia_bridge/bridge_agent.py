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


def parse_obj(obj: dict[str, Any]) -> "BridgeMessageTransaction":
    if obj:
        return BridgeMessageTransaction(
            timestamp_str=obj["timestamp"],
            sender=obj["username"],
            message=obj["text"],
        )
    else:
        print("obj is None")
        return BridgeMessageTransaction(
            timestamp_str="2023-04-28T16:22:49.581778164-04:00",
            sender="",
            message="",
        )


class BridgeMessageTransaction(MessageTransaction):
    def to_tuple(self) -> tuple[float, str, str]:
        timestamp = datetime.fromisoformat(self.timestamp_str)
        return (
            timestamp.timestamp(),
            self.sender,
            self.message,
        )


class MatterbridgeAgent(BaseAgent[Observation, AgentAction]):
    """An agent use matterbridge as a message broker."""

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
        self.headers = {"Content-Type": "application/json"}
        print("step 1: connect to the server")
        self._URL = "http://localhost:4242"
        self.send_init_message()
        logging.info(f"Session ID: {self.session_id}")
        # logging.info(f"Sender ID: {self.sender_id}")

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
        response = requests.request(
            "GET",
            f"{self._URL}/api/health",
        )
        assert (
            response.status_code == 200 and response.text == "OK"
        ), "Failed to connect to the server"
        data = {
            "text": "Sotopia bridge agent is connected to the server.",
            "username": "sotopia",
            "gateway": "gateway1",
        }
        requests.request(
            "POST",
            f"{self._URL}/api/message",
            headers=self.headers,
            json=data,
        )
        return

    def reset(
        self,
        reset_reason: str = "",
    ) -> None:
        super().reset()
        try:
            if reset_reason != "":
                response = requests.request(
                    "POST",
                    f"{self._URL}/api/message",
                    json=reset_reason,
                )
                assert response.status_code == 200

        except Exception as e:
            logging.error(f"Failed to reset RedisAgent {self.sender_id}: {e}")

    async def send_message(self,obs: Observation):
        # 1. post observation to the message list
        print("step 2: post observation to the message list:",obs.to_natural_language)
        async with aiohttp.ClientSession() as session:
            data = {
                "text": obs.to_natural_language(),
                "username": "sotopia",
                "gateway": "gateway1",
            }
            response = await session.request(
                "POST",
                f"{self._URL}/api/message",
                json=data,
                headers=self.headers,
            )
            assert response.status == 200, response
            sorted_message_list: list[tuple[float, str, str]] = list(
                map(
                    lambda x: parse_obj(x).to_tuple(),
                    [await response.json()],
                )
            )
            last_timestamp = sorted_message_list[-1][0]
        return last_timestamp
    
    async def get_action_from_message(self,last_timestamp):
        # Get meesage from client
        async with aiohttp.ClientSession() as session:
            message, success = await self.get_message_from_client(session, last_timestamp)
            if not success:
                self.reset("Someone has left or the conversation is too long.")
                return AgentAction(action_type="leave", argument="")
        return self.constrct_speak_action(message[2])
    

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
    
    async def get_message_from_client(self, session,last_timestamp):
        print("step 3: wait for the client to post their message")
        # 3. wait for the client to post their message
        for i in range(10000):
            response = await session.request(
                "GET",
                f"{self._URL}/api/messages",
            )
            assert response.status == 200, response
            sorted_message_list = list(
                map(
                    lambda x: parse_obj(x).to_tuple(),
                    await response.json(),
                )
            )
            if (
                sorted_message_list
                and sorted_message_list[-1][0] > last_timestamp  # we have to deal with the ordered here
                and sorted_message_list[-1][1] != "sotopia"
            ):
                # 3.a if the client has posted their message, break
                break
            else:
                # 3.b if the client has not posted their message, wait for 0.1 second and retry
                await asyncio.sleep(1)
        else:
            return "", False
        return sorted_message_list[-1], True