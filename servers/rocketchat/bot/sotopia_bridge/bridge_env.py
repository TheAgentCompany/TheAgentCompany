from typing import Any
import requests
from sotopia.envs import ParallelSotopiaEnv
from sotopia.messages import MessengerMixin
from sotopia.messages.message_classes import Message, AgentAction

class BridgeMessenger(MessengerMixin):
    def __init__(self) -> None:
        super().__init__()
        self._URL = "http://localhost:4242"
    
    def parse_message(self, message: Message) -> str:
        if isinstance(message, AgentAction) and message.action_type == "speak":
            return message.argument
        elif isinstance(message, AgentAction) and message.action_type == "action":
            return f"`{message.argument}`"
        else:
            return message.to_natural_language()
        

    def recv_message(self, source: str, message: Message) -> None:
        super().recv_message(source, message)
        if (source != "Environment" and message.to_natural_language() != "did nothing") or len(self.inbox) == 1:
            self.headers = {"Content-Type": "application/json"}
            avatar_dict = {
                "Environment": "https://secure.gravatar.com/avatar/1234567890abcdef1234567890abcdef.jpg",
                "Xuhui Zhou": "https://xuhuiz.com/assets/img/xuhuizhou.jpg",
                "X AI": "https://cmu.box.com/shared/static/r5xkl977ktt0bke29iuqiafasn900y45.png",
                "Email Server": "https://media.wired.com/photos/5a1c63aaf50a476ea628e725/master/w_1920,c_limit/emailtracking-TA.jpg",
            }
            data = {
                "text": self.parse_message(message),
                "username": source,
                "avatar": avatar_dict[source],
                "gateway": "gateway1",
            }
            requests.request(
                "POST",
                f"{self._URL}/api/message",
                headers=self.headers,
                json=data,
            )

class BridgeEnv(ParallelSotopiaEnv, BridgeMessenger):
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs) # type: ignore