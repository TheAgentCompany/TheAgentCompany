"""
Evaluator for the task <Delete all Rocket.Chat channels>
"""

import json
import logging
from typing import List

from common import create_rocketchat_client, checkpoint
from scoring import Result, Checkpoint, bonus_for_completing_final

def get_channel_lists():
    all_channels, joined_channels = None, None
    try:
        rocket_client = create_rocketchat_client()
        all_channels = rocket_client.channels_list().json().get('channels', [])
        joined_channels = rocket_client.channels_list_joined().json().get('channels', [])
    except Exception as e:
        logging.error(f"Failed to get channel lists: {str(e)}")

    return all_channels, joined_channels


@checkpoint
def grade_checkpoint1(joined_channels):
    if joined_channels is not None:
        return len(joined_channels) == 0
    return False

@checkpoint
def grade_checkpoint2(all_channels):
    if all_channels is not None:
        if len(all_channels) > 0:
            logging.info(f"found undeleted channels {str([c['name'] for c in all_channels])}")
        return len(all_channels) == 0
    return False

def grade_checkpoints(trajectory="") -> Result:
    all_channels, joined_channels = get_channel_lists()
    checkpoint1 = Checkpoint(1, int(grade_checkpoint1(joined_channels)))

    checkpoint2 = Checkpoint(1, int(grade_checkpoint2(all_channels)))

    return Result([checkpoint1, checkpoint2], bonus_for_completing_final)
