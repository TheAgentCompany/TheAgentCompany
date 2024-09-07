import json

from sotopia_bridge.env_agent import EmailServerAgent
from .rocketchat_agent import RocketChatAgent
from typing import Literal, Type, cast, Any, Generator, TypeVar

from beartype import beartype
from tqdm.asyncio import tqdm_asyncio

from sotopia.agents import LLMAgent
from sotopia.agents.base_agent import BaseAgent
from sotopia.envs.evaluators import (
    ReachGoalLLMEvaluator,
    RuleBasedTerminatedEvaluator,
)
from sotopia.generation_utils.generate import LLM_Name
from sotopia.messages import AgentAction, Message, Observation
from sotopia.database import AgentProfile, EnvironmentProfile
from sotopia.samplers import BaseSampler, EnvAgentCombo
from sotopia.server import arun_one_episode
from sotopia.envs.parallel import ParallelSotopiaEnv
from sotopia.envs.evaluators import EvaluationForTwoAgents

ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")


class BridgeSampler(BaseSampler[ObsType, ActType]):
    def sample(
        self,
        agent_classes: Type[BaseAgent[ObsType, ActType]]
        | list[Type[BaseAgent[ObsType, ActType]]],
        n_agent: int = 3,
        replacement: bool = True,
        size: int = 1,
        env_params: dict[str, Any] = {},
        agents_params: list[dict[str, Any]] = [{}, {}],
    ) -> Generator[EnvAgentCombo[ObsType, ActType], None, None]:
        # This is a simplified version of the original function
        # The original function is not provided in the snippet
        assert (
            not isinstance(agent_classes, list) or len(agent_classes) == n_agent
        ), f"agent_classes should be a list of length {n_agent} or a single agent class"

        if not isinstance(agent_classes, list):
            agent_classes = [agent_classes] * n_agent
        assert (
            len(agents_params) == n_agent
        ), f"agents_params should be a list of length {n_agent}"
        filename = './data/scenarios.json'
        with open(filename, 'r') as file:
            env_profiles_json = json.load(file)
        env_profile = EnvironmentProfile.parse_obj(
            env_profiles_json['work_space_1']
        )
        env = ParallelSotopiaEnv(env_profile=env_profile, **env_params)
        agent_profiles = [
            AgentProfile.parse_obj(
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "age": 30,
                    "occupation": "Software Engineer",
                }
            ),
            AgentProfile.parse_obj(
                {
                    "first_name": "X",
                    "last_name": "AI",
                    "occupation": "AI Assistant",
                }
            ),
            AgentProfile.parse_obj(
                {  
                    "first_name": "Email",
                    "last_name": "Server",
                }
            ),
        ]
        for _ in range(size):
            agents = [
                agent_class(agent_profile=agent_profile, **agent_params)
                for agent_class, agent_profile, agent_params in zip(
                    agent_classes, agent_profiles, agents_params
                )
            ]
            for agent, goal in zip(agents, env.profile.agent_goals):
                agent.goal = goal
            yield env, agents


@beartype
async def run_bridge_server(
    model_dict: dict[str, LLM_Name],
    agents_roles: dict[str, str],
    sampler: BaseSampler[Observation, AgentAction] = BridgeSampler(),
    action_order: Literal["simutaneous", "round-robin", "random"] = "round-robin",
    env_agent_combo_list: list[EnvAgentCombo[Observation, AgentAction]] = [],
    tag: str | None = None,
    push_to_db: bool = False,
    using_async: bool = True,
) -> list[list[tuple[str, str, Message]]]:
    """
    Doc incomplete

    Args:
        omniscient (bool): Whether the agent knows the goal of the other, default to False
        script_like (bool): Whether we generate the turn in script like manner, default to False
        json_in_script (bool): Whether we requires the script generator to return json (Only valid when script_like is True), default to False

    Note: env_agent_combo_list is optional. When it defaults to [], sampler is used
    else the sampler is not used. Please pass in BaseSampler or simply not specify it when using this option.
    """

    assert not (push_to_db and tag is None), "please provide a tag when push to db"

    # Create Environment and agents
    # This step will be moved to outside this function

    env_params = {
        "model_name": model_dict["env"],
        "action_order": action_order,
        "evaluators": [
            RuleBasedTerminatedEvaluator(max_turn_number=20, max_stale_turn=4),
        ],
        "terminal_evaluators": [
            ReachGoalLLMEvaluator(model_dict["env"], response_format_class=EvaluationForTwoAgents),
        ],

    }
    agents_model_dict = {
        "agent1": model_dict["agent1"],
        "agent2": model_dict["agent2"],
    }

    def get_agent_class(
        model_name: str,
        agent_role: str,
    ) -> Type[BaseAgent[Observation, AgentAction]]:
        if model_name == "rocketchat":
            return RocketChatAgent
        elif model_name == "email_server":
            return EmailServerAgent
        else:
            if agent_role == "human":
                return LLMAgent
            else:
                return LLMAgent

    if env_agent_combo_list:
        assert (
            type(sampler) is BaseSampler
        ), "No sampler should be used when `env_agent_combo_list` is not empty"
        env_agent_combo_iter = iter(env_agent_combo_list)
    else:
        env_agent_combo_iter = sampler.sample(
            agent_classes=[
                get_agent_class(model_name, agents_role) for model_name, agents_role in zip(agents_model_dict.values(), agents_roles.values())
            ],
            n_agent=len(agents_model_dict),
            env_params=env_params,
            agents_params=[
                {"model_name": model_name} if model_name != "rocketchat"  else {}
                for model_name in agents_model_dict.values()
            ],
        )
    episode_futures = [
        arun_one_episode(
            env=env_agent_combo[0],
            agent_list=env_agent_combo[1] ,
            tag=tag,
            push_to_db=push_to_db,
        )
        for env_agent_combo in env_agent_combo_iter
    ]

    batch_results = (
        await tqdm_asyncio.gather(*episode_futures, desc="Running one batch")
        if using_async
        else [await i for i in episode_futures]
    )

    return cast(list[list[tuple[str, str, Message]]], batch_results)
