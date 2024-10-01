import asyncio
import os
import base64

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
    runtime = create_runtime(config)

    # pre-login to websites
    rocketchat_login_actions = [
        'goto("http://ogma.lti.cs.cmu.edu:3000/")',
        'noop(5000)',
        'fill("89", "jobbench")',
        'fill("94", "jobbench")',
        'click("97")'
    ]

    image_id = 0
    for instruction in rocketchat_login_actions:
        action = BrowseInteractiveAction(
            browser_actions=instruction
        )
        action.timeout = 10000
        logger.info(action, extra={'msg_type': 'ACTION'})
        obs: BrowserOutputObservation = runtime.run_action(action)
        logger.info(obs, extra={'msg_type': 'OBSERVATION'})
        image_data = base64.b64decode(obs.screenshot)
        with open("screenshots/" + str(image_id) + ".png", 'wb') as file:
            file.write(image_data)
            image_id += 1

    # run agent to solve the task
    instruction = "Complete the task in /instruction/task.md"

    state: State | None = asyncio.run(
        run_controller(
            config=config,
            task_str=instruction,
            runtime=runtime,
        )
    )

    # TODO: run evaluator