"""
Evaluator for the task <Delete all Rocket.Chat channels>
"""

import json
import logging
from typing import List

from common import create_rocketchat_client
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

def grade_checkpoints(trajectory="") -> Result:
    all_channels, joined_channels = get_channel_lists()
    checkpoint1_score = 0
    if joined_channels is not None:
        checkpoint1_score = int(len(joined_channels) == 0)
    checkpoint1 = Checkpoint(1, checkpoint1_score)

    checkpoint2_score = 0
    if all_channels is not None:
        if len(all_channels) > 0:
            logging.info(f"found undeleted channels {str([c['name'] for c in all_channels])}")
        checkpoint2_score = int(len(all_channels) == 0)
    checkpoint2 = Checkpoint(1, checkpoint2_score)

    return Result([checkpoint1, checkpoint2], bonus_for_completing_final)
