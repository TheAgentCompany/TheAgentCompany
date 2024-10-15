import logging

from sotopia.agents import LLMAgent
from sotopia.database import AgentProfile
from sotopia.generation_utils.langchain_callback_handler import LoggingCallbackHandler
from sotopia.messages import Observation, AgentAction, ActionType
from sotopia.generation_utils.generate import agenerate
from langchain.output_parsers import PydanticOutputParser

async def agenerate_action_human(
    model_name: str,
    history: str,
    turn_number: int,
    action_types: list[ActionType],
    agent: str,
    goal: str,
    temperature: float = 0.7,
    script_like: bool = False,
) -> AgentAction:
    """
    Generate the action for the agent, only should be used for generating human-like actions
    """
    try:
        if script_like:
            # model as playwright
            raise NotImplementedError(
                "Not implemented yet for script_like mode in agenerate_action_x"
            )
        else:
            # Normal case, model as agent
            template = """
                Imagine you are {agent}, your task is to act/speak as {agent} would, keeping in mind {agent}'s social goal.
                You can find {agent}'s goal (or background) in the 'Here is the context of the interaction' field.
                Note that {agent}'s goal is only visible to you.
                You should try your best to achieve {agent}'s goal in a way that align with their character traits. Please be aware that the tools available to AI agents are not accessible to you, so don't follow their arguments of using tools.
                Additionally, maintaining the conversation's naturalness and realism is essential (e.g., do not repeat what other people has already said before).
                IMPORTANT: You are communicating with other agents only through rocketchat, so any information you want to share with others should be outputted through rocketchat with the `speak` action. Don't say something like 'I have sent the information to your inbox'.
                {history}.
                You are at Turn #{turn_number}. Your available action types are
                {action_list}.
                Note: You can "leave" this conversation if 1. you have achieved your social goals, 2. this conversation makes you uncomfortable, 3. you find it uninteresting/you lose your patience, 4. or for other reasons you want to leave.

                Please only generate a JSON string including the action type and the argument.
                Your action should follow the given format:
                {format_instructions}
            """
        return await agenerate(
            model_name=model_name,
            template=template,
            input_values=dict(
                agent=agent,
                turn_number=str(turn_number),
                history=history,
                action_list=" ".join(action_types),
            ),
            output_parser=PydanticOutputParser(pydantic_object=AgentAction),
            temperature=temperature,
        )
    except Exception:
        return AgentAction(action_type="none", argument="")

class HumanUserAgent(LLMAgent):
    """
    This agent should only be used for simulating human characters in the environment.
    """

    def __init__(
        self,
        agent_name: str | None = None,
        uuid_str: str | None = None,
        agent_profile: AgentProfile | None = None,
        model_name: str = "gpt-3.5-turbo",
        script_like: bool = False,
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            uuid_str=uuid_str,
            agent_profile=agent_profile,
            model_name=model_name,
            script_like=script_like,
        )

    async def aact(self, obs: Observation) -> AgentAction:
        self.recv_message("Environment", obs)

        if len(obs.available_actions) == 1 and "none" in obs.available_actions:
            return AgentAction(action_type="none", argument="")
        else:
            action = await agenerate_action_human(
                self.model_name,
                history="\n".join(f"{y.to_natural_language()}" for x, y in self.inbox),
                turn_number=obs.turn_number,
                action_types=obs.available_actions,
                agent=self.agent_name,
                goal=self.goal,
                script_like=self.script_like,
            )
            # Temporary fix for mixtral-moe model for incorrect generation format
            if "Mixtral-8x7B-Instruct-v0.1" in self.model_name:
                current_agent = self.agent_name
                if f"{current_agent}:" in action.argument:
                    print("Fixing Mixtral's generation format")
                    action.argument = action.argument.replace(f"{current_agent}: ", "")
                elif f"{current_agent} said:" in action.argument:
                    print("Fixing Mixtral's generation format")
                    action.argument = action.argument.replace(
                        f"{current_agent} said: ", ""
                    )
            return action