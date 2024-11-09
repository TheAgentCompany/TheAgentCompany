from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Dict, List, Union
import re
import base64
import os
import requests
import json
import sys

from openhands.core.logger import openhands_logger as logger
from openhands.events.action import BrowseInteractiveAction
from openhands.events.observation import BrowserOutputObservation
from openhands.runtime.base import Runtime


class ActionType(Enum):
    GOTO = auto()
    FILL = auto()
    CLICK = auto()
    NOOP = auto()


@dataclass
class Selector:
    """
    Represents either a direct anchor ID or a descriptive selector
    """
    value: str
    is_anchor: bool = False
    
    def __str__(self) -> str:
        return f"{self.value}"

@dataclass
class BrowserAction:
    """Base class for all browser actions"""
    action_type: ActionType
    
    def to_instruction(self) -> str:
        """Convert the action to a browser instruction string"""
        raise NotImplementedError

@dataclass
class GotoAction(BrowserAction):
    url: str
    
    def __init__(self, url: str):
        super().__init__(ActionType.GOTO)
        self.url = url
    
    def to_instruction(self) -> str:
        return f'goto("{self.url}")'


@dataclass
class NoopAction(BrowserAction):
    milliseconds: int
    
    def __init__(self, milliseconds: int):
        super().__init__(ActionType.NOOP)
        self.milliseconds = milliseconds
    
    def to_instruction(self) -> str:
        return f'noop({self.milliseconds})'


@dataclass
class InputAction(BrowserAction):
    selector: Selector
    value: str
    
    def __init__(self, selector: Union[str, Selector], value: str):
        super().__init__(ActionType.FILL)
        self.selector = selector if isinstance(selector, Selector) else Selector(selector)
        self.value = value
    
    def to_instruction(self) -> str:
        return f'fill("{self.selector}", "{self.value}")'

@dataclass
class ClickAction(BrowserAction):
    selector: Selector
    
    def __init__(self, selector: Union[str, Selector]):
        super().__init__(ActionType.CLICK)
        self.selector = selector if isinstance(selector, Selector) else Selector(selector)
    
    def to_instruction(self) -> str:
        return f'click("{self.selector}")'

def parse_content_to_elements(content: str) -> Dict[str, str]:
    """Parse the observation content into a dictionary mapping anchors to their descriptions"""
    elements = {}
    current_anchor = None
    description_lines = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for anchor line
        anchor_match = re.match(r'\[(\d+)\](.*)', line)
        if anchor_match:
            # Save previous element if it exists
            if current_anchor and description_lines:
                elements[current_anchor] = ' '.join(description_lines)
            
            # Start new element
            current_anchor = anchor_match.group(1)
            description_lines = [anchor_match.group(2).strip()]
        else:
            # Add to current description if we have an anchor
            if current_anchor:
                description_lines.append(line)
    
    # Save last element
    if current_anchor and description_lines:
        elements[current_anchor] = ' '.join(description_lines)
        
    return elements

def find_matching_anchor(content: str, selector: str) -> Optional[str]:
    """Find the anchor ID that matches the given selector description"""
    elements = parse_content_to_elements(content)
    
    # Clean up selector and create a pattern
    selector = selector.lower().strip()
    
    for anchor, description in elements.items():
        description = description.lower().strip()
        if selector in description:
            return anchor

    return None

def resolve_action(action: BrowserAction, content: str) -> BrowserAction:
    """
    Resolve any descriptive selectors in the action to anchor IDs based on the content.
    Returns a new action with resolved selectors.
    """
    if isinstance(action, (InputAction, ClickAction)):
        if not action.selector.is_anchor:
            anchor = find_matching_anchor(content, action.selector.value)
            if anchor:
                new_selector = Selector(anchor, is_anchor=True)
                if isinstance(action, InputAction):
                    return InputAction(new_selector, action.value)
                else:
                    return ClickAction(new_selector)
            else:
                logger.error(f"NO MATCH FOUND FOR SELECTOR, {action.selector}")
                return None
    return action


def get_nextcloud_password():
    """
    Retrieves NEXTCLOUD_PASSWORD from the API endpoint

    TODO: this is a temporary solution. Once #169 is solved,
    we should be able to use a hard-coded password to avoid
    this extra API call.
    
    Returns:
        str: The NEXTCLOUD_PASSWORD value
    
    Raises:
        requests.RequestException: If API call fails
        KeyError: If NEXTCLOUD_PASSWORD is not in response
        json.JSONDecodeError: If response is not valid JSON
    """
    url = "http://the-agent-company.com:2999/api/nextcloud-config"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        data = response.json()
        return data["NEXTCLOUD_PASSWORD"]
        
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        raise
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error processing response: {e}")
        raise


def pre_login(runtime: Runtime, save_screenshots=True, screenshots_dir='screenshots'):
    """
    Logs in to all the websites that are needed for the evaluation.
    Once logged in, the sessions would be cached in the browser, so OpenHands
    agent doesn't need to log in to these websites again.

    TODO: right now we assume all login actions succeed. We need to add some sanity
    checks to ensure that login is successful.

    TODO: we only need login actions for dependencies of the task.
    """
    nextcloud_password = get_nextcloud_password()
    nextcloud_login_actions = [
        GotoAction("https://ogma.lti.cs.cmu.edu"),
        NoopAction(1000),
        InputAction(
            "textbox 'Login with username or email', clickable",
            "admin"
        ),
        NoopAction(1000),
        InputAction(
            "textbox 'Password', clickable",
            nextcloud_password
        ),
        NoopAction(1000),
        ClickAction("button 'Log in', clickable")
    ]

    rocketchat_login_actions = [
        GotoAction("http://the-agent-company.com:3000"),
        NoopAction(1000),
        InputAction(
            "textbox '', clickable, focused",
            "theagentcompany"
        ),
        NoopAction(1000),
        InputAction(
            "textbox '', clickable",
            "theagentcompany"
        ),
        NoopAction(1000),
        ClickAction("button 'Login', clickable"),
        NoopAction(1000),
        # TODO: after login, a popup asking to change hostname appears. We need to click on cancel button.
    ]

    gitlab_login_actions = [
        GotoAction("http://the-agent-company.com:8929/users/sign_in"),
        NoopAction(1000),
        InputAction(
            "textbox 'Username or primary email'",
            "root"
        ),
        NoopAction(1000),
        InputAction(
            "textbox 'Password'",
            "theagentcompany"
        ),
        NoopAction(1000),
        ClickAction("button 'Sign in', clickable")
    ]

    # TODO: this sometimes fails, seems bid for plane login is not deterministic
    # TODO (yufansong): plane reset is not stable, and sometimes it fails to launch
    plane_login_actions = [
        GotoAction("http://the-agent-company.com:8091"),
        NoopAction(1000),
        InputAction(
            "textbox 'Email', clickable, focused",
            "agent@company.com",
        ),
        NoopAction(1000),
        ClickAction("button 'Continue'"),
        # 'fill("85", "theagentcompany")',
        # 'click("92")'
    ]

    all_login_actions = [
        ('nextcloud', nextcloud_login_actions),
        ('rocket_chat', rocketchat_login_actions),
        ('gitlab', gitlab_login_actions),
        ('plane', plane_login_actions),
    ]
    
    for (website_name, login_actions) in all_login_actions:
        if save_screenshots:
            directory = os.path.join(screenshots_dir, website_name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            image_id = 0
        obs: BrowserOutputObservation = None
        for action in login_actions:
            # Resolve any descriptive selectors to anchor IDs
            if obs:
                action = resolve_action(action, obs.get_agent_obs_text())

            if not action:
                logger.error(f"FAILED TO RESOLVE ACTION, {action}")
                sys.exit(1)

            # Convert the action to an instruction string
            instruction = action.to_instruction()
            
            browser_action = BrowseInteractiveAction(
                browser_actions=instruction
            )
            browser_action.timeout = 10000
            logger.info(browser_action, extra={'msg_type': 'ACTION'})
            obs: BrowserOutputObservation = runtime.run_action(browser_action)
            logger.info(obs, extra={'msg_type': 'OBSERVATION'})
            if save_screenshots:
                image_data = base64.b64decode(obs.screenshot)
                with open(os.path.join(directory, f'{image_id}.png'), 'wb') as file:
                    file.write(image_data)
                    image_id += 1