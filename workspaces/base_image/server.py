import json
import os

from rocketchat_agent import RocketChatAgent
from typing import Literal, Type, cast, Any, Generator, TypeVar

from beartype import beartype
from tqdm.asyncio import tqdm_asyncio

from human_user_agent import HumanUserAgent
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

scenarios_file_path = os.getenv('SCENARIOS_FILE_PATH') or 'scenarios.json'

def get_scenarios(npc_first_name):
    # Attempt to get the user's scenarios based on the provided key
    with open(scenarios_file_path, 'r') as file:
        json_data = json.load(file)

    agent_scenario = json_data.get(npc_first_name)
    if not agent_scenario:
        raise RuntimeError("Didn't find the NPC scenarios in file")

    agent_goal = "You goal is to instruct the other agent to help with you something about work."
    if "extra_info" in agent_scenario:
        agent_goal += " <extra_info>" + agent_scenario["extra_info"] + "</extra_info>"
    if "strategy_hint" in agent_scenario:
        agent_goal += " <strategy_hint>" + agent_scenario["strategy_hint"] + "</strategy_hint>"
    if "clarification_hint" in agent_scenario:
        agent_goal += " <clarification_hint>" + agent_scenario["clarification_hint"] + "</clarification_hint>"

    # sotopia is an agent-agent interaction framework, but here we are using it between
    # agent (NPC) and examinee. The framework requires us to define a goal for both
    # counter-parties, even though sotopia doesn't really control examinee.
    examinee_goal = "You need to seek help from another agent to complete your work."
    return  {
        "codename": "working_space_1" + npc_first_name,
        "scenario": "Analyze information to determine, recommend, and plan installation of a new system or modification of an existing system.",
        "agent_goals": [
            examinee_goal,
            agent_goal
        ]
    }


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
        agent_first_name: str = "",
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
        env_profile = EnvironmentProfile.parse_obj(
            get_scenarios(agent_first_name)
        )
        env = ParallelSotopiaEnv(env_profile=env_profile, **env_params)
        agent_profiles = [
            # Only get the first result. If not item in list, should raise error
            # Please check the redis server, you should populate data before running
            AgentProfile.find(AgentProfile.first_name == 'X').execute()[0],
            AgentProfile.find(AgentProfile.first_name == agent_first_name).execute()[0],
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
async def run_server(
    model_dict: dict[str, LLM_Name],
    agents_roles: dict[str, str],
    sampler: BaseSampler[Observation, AgentAction] = BridgeSampler(),
    action_order: Literal["simutaneous", "round-robin", "random"] = "round-robin",
    env_agent_combo_list: list[EnvAgentCombo[Observation, AgentAction]] = [],
    tag: str | None = None,
    push_to_db: bool = False,
    using_async: bool = True,
    agent_first_name: str = "",
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
        else:
            return HumanUserAgent

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
                {"model_name": model_name} if model_name != "rocketchat"  else {"first_name": agent_first_name}
                for model_name in agents_model_dict.values()
            ],
            agent_first_name = agent_first_name,
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
