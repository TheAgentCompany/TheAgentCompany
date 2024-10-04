import asyncio
import os
import base64
import time

from openhands.controller.state.state import State
from openhands.core.config import (
    AppConfig,
    SandboxConfig,
    LLMConfig,
    get_llm_config_arg,
    get_parser,
)
from openhands.core.logger import openhands_logger as logger
from openhands.core.main import create_runtime, run_controller
from openhands.events.action import CmdRunAction, BrowseInteractiveAction
from openhands.events.observation import CmdOutputObservation, BrowserOutputObservation, ErrorObservation
from openhands.runtime.runtime import Runtime
from openhands.runtime.browser.browser_env import BrowserEnv


def get_config(
    base_container_image: str,
    llm_config: LLMConfig
) -> AppConfig:
    config = AppConfig(
        run_as_openhands=False,
        max_budget_per_task=4,
        sandbox=SandboxConfig(
            base_container_image=base_container_image,
            enable_auto_lint=True,
            use_host_network=False,
            # large enough timeout, since some testcases take very long to run
            timeout=300,
            api_key=os.environ.get('ALLHANDS_API_KEY', None),
        ),
        # do not mount workspace
        workspace_base=None,
        workspace_mount_path=None,
    )
    config.set_llm_config(llm_config)
    return config


def pre_login(runtime: Runtime, save_screenshots=True, screenshots_dir='screenshots'):
    rocketchat_login_actions = [
        'goto("http://ogma.lti.cs.cmu.edu:3000/")',
        'noop(5000)',
        'fill("52", "jobbench")',
        'fill("57", "jobbench")',
        'click("60")',
        'goto("http://ogma.lti.cs.cmu.edu:3000/")',
    ]

    all_login_actions = [
        ('rocket_chat', rocketchat_login_actions)
    ]

    for (website_name, login_actions) in all_login_actions:
        if save_screenshots:
            directory = os.path.join(screenshots_dir, website_name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            image_id = 0
        for instruction in login_actions:
            action = BrowseInteractiveAction(
                browser_actions=instruction
            )
            action.timeout = 10000
            logger.info(action, extra={'msg_type': 'ACTION'})
            obs: BrowserOutputObservation = runtime.run_action(action)
            logger.info(obs, extra={'msg_type': 'OBSERVATION'})
            if save_screenshots:
                image_data = base64.b64decode(obs.screenshot)
                with open(os.path.join(directory, f'{image_id}.png'), 'wb') as file:
                    file.write(image_data)
                    image_id += 1


def init_task_env(runtime: Runtime):
    action = CmdRunAction(command="""bash ./utils/init.sh""")
    action.timeout = 600
    logger.info(action, extra={'msg_type': 'ACTION'})
    obs = runtime.run_action(action)
    logger.info(obs, extra={'msg_type': 'OBSERVATION'})
    assert obs.exit_code == 0


def run_solver(runtime: Runtime, config: AppConfig) -> State:
    instruction = "Complete the task in /instruction/task.md"

    # TODO: OpenHands should:
    # 1) optionally, save browser screenshots to a place
    # 2) optionally, return trajectory or save it to a given place
    state: State | None = asyncio.run(
        run_controller(
            config=config,
            task_str=instruction,
            runtime=runtime,
        )
    )
    logger.info(state)
    return state


def run_evaluator(runtime: Runtime):
    action = CmdRunAction(command="""python /utils/evaluator.py""")
    action.timeout = 600
    logger.info(action, extra={'msg_type': 'ACTION'})
    obs = runtime.run_action(action)
    logger.info(obs, extra={'msg_type': 'OBSERVATION'})
    assert obs.exit_code == 0


if __name__ == '__main__':
    parser = get_parser()
    parser.add_argument(
        '--task_image_name',
        type=str,
        default='example-exam-image',
        help='Task image name',
    )
    args, _ = parser.parse_known_args()

    llm_config = None
    if args.llm_config:
        llm_config = get_llm_config_arg(args.llm_config)

    if llm_config is None:
        raise ValueError(f'Could not find LLM config: --llm_config {args.llm_config}')

    logger.info(f"Task image name is {args.task_image_name}")
    config: AppConfig = get_config(args.task_image_name, llm_config)
    runtime: Runtime = create_runtime(config)

    pre_login(runtime)

    init_task_env(runtime)

    state = run_solver(runtime, config)

    run_evaluator(runtime)
    