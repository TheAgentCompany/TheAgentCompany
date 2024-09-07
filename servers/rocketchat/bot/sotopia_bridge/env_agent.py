from sotopia.agents.base_agent import BaseAgent
from sotopia.messages import AgentAction, Message, Observation
from sotopia.database import AgentProfile, EnvironmentProfile

class EmailServerAgent(BaseAgent[Observation, AgentAction]):
    """An agent use matterbridge as a message broker."""

    def __init__(
        self,
        agent_name: str | None = None,
        uuid_str: str | None = None,
        model_name: str | None = None,
        session_id: str | None = None,
        agent_profile: AgentProfile | None = None,
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            uuid_str=uuid_str,
            agent_profile=agent_profile,
        )
        
    async def aact(
        self,
        obs: Observation,
    ) -> AgentAction:
        if "fetch_employee_emails" in obs.last_turn:
            return AgentAction(
                action_type="action", argument="Here's the list of employees emails: [('Alice Smith', 'alice1@x.com'), ('Bob Johnson', 'bob.johnson@x.com'), ('Carol Martinez', 'carol.m@x.com'), ('David Lee', 'd.lee@x.com'), ('Eva Green', 'eva.green@x.com'), ('Frank Brown', 'frankb@x.com'), ('Grace Clark', 'grace.clark@x.com'), ('Henry Davis', 'henryd@x.com'), ('Irene White', 'irene.w@x.com'), ('Jack Wilson', 'jack.wilson@x.com'), (Alice Lee', 'alice2@x.com'), ('All Employees', 'all@x.com')]"
            )
        elif "fetch_customer_emails" in obs.last_turn:
            return AgentAction(
                action_type="action", argument="[('Alice Smith', 'alice1@gmail.com'), ('Bob Johnson', 'bob.johnson@gmail.com'), ('Carol Martinez', 'carol.m@gmail.com'), ('David Lee', 'd.lee@gmail.com'), ('Eva Green', 'eva.green@gmail.com'), ('Frank Brown', 'frankb@gmail.com'), ('Grace Clark', 'grace.clark@gmail.com'), ('Henry Davis', 'henryd@gmail.com'), ('Irene White', 'irene.w@gmail.com'), ('Jack Wilson', 'jack.wilson@gmail.com'), ('Alice Lee', 'alice2@gmail.com')]"
            )
        elif "send_email" in obs.last_turn:
            return AgentAction(
                action_type="action", argument="The email has been sent."
            )
        else:
            return AgentAction(action_type="none", argument="")

    def reset(
        self,
        reset_reason: str = "",
    ) -> None:
        super().reset()