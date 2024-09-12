import json
import logging

from redis_om import Migrator
from sotopia.database import AgentProfile

Migrator().run()

with open('npc_definition.json', 'r') as file:
    agent_definitions = json.load(file)
    logging.info(f"NPC definitions loaded, number of NPCs = {len(agent_definitions)}")

def get_by_first_name(first_name):
    return AgentProfile.find(AgentProfile.first_name == first_name).execute()

for definition in agent_definitions:
    if get_by_first_name(definition["first_name"]):
        # TODO: shall we support modifications?
        logging.info(f'NPC ({definition["first_name"]}) already inserted, skip')
        continue
    agent_profile = AgentProfile.parse_obj(definition)
    agent_profile.save()
    logging.info(f'Inserted {definition["first_name"]} successfully')
