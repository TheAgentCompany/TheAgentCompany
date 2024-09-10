from openhands.controller.state.state import State
from openhands.core.config import (
    AppConfig,
    SandboxConfig,
    get_llm_config_arg,
    get_parser,
)
from openhands.core.logger import openhands_logger as logger
from openhands.core.main import create_runtime, run_controller
from openhands.events.action import CmdRunAction
from openhands.events.observation import CmdOutputObservation, ErrorObservation
from openhands.runtime.runtime import Runtime


if __name__ == '__main__':
    parser = get_parser()
    parser.add_argument(
        '--task',
        type=str,
        default='example',
        help='Task to evaluate on',
    )
    args, _ = parser.parse_known_args()